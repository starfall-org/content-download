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
    media = data.result.links
    
    # Separate audio from other media
    audio_items = [item for item in media if item.type == "audio"]
    non_audio_items = [item for item in media if item.type != "audio"]
    
    # Send non-audio media first (video/image)
    if non_audio_items:
        if len(non_audio_items) == 1:
            item = non_audio_items[0]
            if item.type == "video":
                await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                try:
                    await m.reply_video(item.url)
                except Exception:
                    result = await convert_to_io(data.result)
                    new_media = result.links[0]
                    await m.reply_video(new_media.url)
            elif item.type == "image":
                await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                try:
                    await m.reply_photo(item.url)
                except Exception:
                    result = await convert_to_io(data.result)
                    new_media = result.links[0]
                    await m.reply_photo(new_media.url)
        else:
            # Multiple non-audio items - send as media group
            for i in range(0, len(non_audio_items) - 1, 10):
                part_items = non_audio_items[i : min(i + 10, len(non_audio_items) - 1)]
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
                    part_files = [item for item in result.links if item.type != "audio"]
                    media_group = convert_input_media(
                        part_files[i : min(i + 10, len(part_files) - 1)]
                    )
                    await m.reply_media_group(media_group)

            # Send last non-audio item without caption (caption goes with audio)
            last_non_audio = non_audio_items[-1]
            if last_non_audio.type == "video":
                await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                try:
                    await m.reply_video(last_non_audio.url)
                except Exception:
                    result = await convert_to_io(data.result)
                    new_media = [item for item in result.links if item.type == "video"][-1]
                    await m.reply_video(new_media.url)
            elif last_non_audio.type == "image":
                await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                try:
                    await m.reply_photo(last_non_audio.url)
                except Exception:
                    result = await convert_to_io(data.result)
                    new_media = [item for item in result.links if item.type == "image"][-1]
                    await m.reply_photo(new_media.url)

    # Send audio last with caption and button
    if audio_items:
        for i, audio in enumerate(audio_items):
            # Last audio gets caption and button
            is_last = (i == len(audio_items) - 1)
            await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
            try:
                if is_last:
                    await m.reply_audio(
                        audio.url,
                        title="music",
                        performer="bytedance",
                        caption=data.caption,
                        reply_markup=data.button,
                    )
                else:
                    await m.reply_audio(audio.url, title="music", performer="music.mp3")
            except Exception:
                result = await convert_to_io(data.result)
                audio_links = [item for item in result.links if item.type == "audio"]
                if is_last:
                    await m.reply_audio(
                        audio_links[i].url,
                        title="music",
                        performer="music.mp3",
                        caption=data.caption,
                        reply_markup=data.button,
                    )
                else:
                    await m.reply_audio(audio_links[i].url, title="music", performer="music.mp3")


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
