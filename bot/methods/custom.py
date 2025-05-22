from hydrogram.enums import ChatAction
from hydrogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

from bot.schemas.bot import ResponseUtility
from bot.schemas.common_link import CommonLink, CommonLinks
from bot.utils.convert_tools import convert_to_io


def convert_input_media(
    media: list[CommonLink],
) -> list[InputMediaPhoto | InputMediaVideo]:
    return [
        InputMediaVideo(link.url) if link.type == "video" else InputMediaPhoto(link.url)
        for link in media
    ]


async def reply_media_group(m: Message, data: ResponseUtility) -> None:
    if data.result == CommonLinks and (media := data.result.links) == 1:
        if media[0].type == "video":
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(
                    media.url, reply_markup=data.button, caption=data.caption
                )
            except Exception:
                result = await convert_to_io(data.result)
                new_media = result.links[0]
                await m.reply_video(
                    new_media.url,
                    reply_markup=data.button,
                    caption=data.caption,
                )
        elif media[0].type == "image":
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                await m.reply_photo(
                    media.content.url, reply_markup=data.button, caption=data.caption
                )
            except Exception:
                result = await convert_to_io(data.result)
                new_media = result.links[0]
                await m.reply_photo(
                    new_media.url,
                    reply_markup=data.button,
                    caption=data.caption,
                )
    else:
        result: CommonLinks = data.result
        items = result.links
        last_item = items[-1]
        for i in range(0, len(items) - 1, 10):
            part_items = items[i : min(i + 10, len(items) - 1)]
            if any(link.type == "video" for link in part_items):
                await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            else:
                await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                media_group = convert_input_media(part_items)
                await m.reply_media_group(media_group)
            except Exception:
                if any(link.type == "video" for link in part_items):
                    await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                else:
                    await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                result = await convert_to_io(data.result)
                items = result.links
                last_item = items[-1]
                part_files = items[i : min(i + 10, len(items) - 1)]
                media_group = convert_input_media(part_files)
                await m.reply_media_group(media_group)

        if last_item.type == "video":
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(
                    last_item.url, caption=data.caption, reply_markup=data.button
                )
            except Exception:
                result = await convert_to_io(data.result)
                last_item = result.links[-1]
                await m.reply_video(
                    last_item.url, caption=data.caption, reply_markup=data.button
                )

        elif last_item.type == "image":
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await m.reply_photo(
                last_item.url, caption=data.caption, reply_markup=data.button
            )


async def reply_audio(m: Message, data: ResponseUtility) -> None:
    await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    try:
        await m.reply_audio(
            data.audio.url, caption=data.caption, reply_markup=data.button
        )
    except Exception:
        result = await convert_to_io(data.result)
        await m.reply_audio(
            result.audio.url, caption=data.caption, reply_markup=data.button
        )
