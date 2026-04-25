from hydrogram.enums import ChatAction
from hydrogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

import httpx

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
        has_audio = bool(audio_items)
        send_caption = data.caption if not has_audio else None
        send_button = data.button if not has_audio else None

        if len(non_audio_items) == 1:
            item = non_audio_items[0]
            if item.type == "video":
                await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                try:
                    await m.reply_video(
                        item.url, caption=send_caption, reply_markup=send_button
                    )
                except Exception:
                    result = await convert_to_io(data.result)
                    new_media = result.links[0]
                    await m.reply_video(
                        new_media.url, caption=send_caption, reply_markup=send_button
                    )
            elif item.type == "image":
                await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                try:
                    await m.reply_photo(
                        item.url, caption=send_caption, reply_markup=send_button
                    )
                except Exception:
                    result = await convert_to_io(data.result)
                    new_media = result.links[0]
                    await m.reply_photo(
                        new_media.url, caption=send_caption, reply_markup=send_button
                    )
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

            # Send last non-audio item (with caption/button if no audio)
            last_non_audio = non_audio_items[-1]
            has_audio = bool(audio_items)
            send_caption = data.caption if not has_audio else None
            send_button = data.button if not has_audio else None

            if last_non_audio.type == "video":
                await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                try:
                    await m.reply_video(
                        last_non_audio.url, caption=send_caption, reply_markup=send_button
                    )
                except Exception:
                    result = await convert_to_io(data.result)
                    new_media = [item for item in result.links if item.type == "video"][-1]
                    await m.reply_video(
                        new_media.url, caption=send_caption, reply_markup=send_button
                    )
            elif last_non_audio.type == "image":
                await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                try:
                    await m.reply_photo(
                        last_non_audio.url, caption=send_caption, reply_markup=send_button
                    )
                except Exception:
                    result = await convert_to_io(data.result)
                    new_media = [item for item in result.links if item.type == "image"][-1]
                    await m.reply_photo(
                        new_media.url, caption=send_caption, reply_markup=send_button
                    )

    # Send audio last with caption and button
    if audio_items:
        # Convert to IO first for audio fallback
        audio_failed = False
        try:
            # Test if URL works
            async with httpx.AsyncClient().head(audio_items[0].url, timeout=5) as resp:
                if resp.status_code >= 400:
                    audio_failed = True
        except Exception:
            audio_failed = True

        if audio_failed:
            result = await convert_to_io(data.result)

        for i, audio in enumerate(audio_items):
            # Get audio from converted result if available
            send_audio = audio.url
            if audio_failed and result:
                audio_links = [item for item in result.links if item.type == "audio"]
                if i < len(audio_links):
                    send_audio = audio_links[i].url
            elif audio_failed and result:
                send_audio = audio.url

            # Last audio gets caption and button
            is_last = (i == len(audio_items) - 1)
            await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
            try:
                if is_last:
                    await m.reply_audio(
                        send_audio,
                        title="music",
                        performer="bytedance",
                        caption=data.caption,
                        reply_markup=data.button,
                    )
                else:
                    await m.reply_audio(send_audio, title="music", performer="music.mp3")
            except Exception:
                if result:
                    audio_links = [item for item in result.links if item.type == "audio"]
                    if i < len(audio_links):
                        send_audio = audio_links[i].url
                        if is_last:
                            await m.reply_audio(
                                send_audio,
                                title="music",
                                performer="music.mp3",
                                caption=data.caption,
                                reply_markup=data.button,
                            )
                        else:
                            await m.reply_audio(send_audio, title="music", performer="music.mp3")


async def reply_audio(m: Message, data: ResponseUtility) -> None:
    await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)

    # Get audio from result.links
    audio_links = [item for item in data.result.links if item.type == "audio"]
    if not audio_links:
        return

    audio = audio_links[0]

    try:
        await m.reply_audio(
            audio.url, caption=data.caption, reply_markup=data.button
        )
    except Exception:
        result = await convert_to_io(data.result)
        new_audio_links = [item for item in result.links if item.type == "audio"]
        if new_audio_links:
            await m.reply_audio(
                new_audio_links[0].url, caption=data.caption, reply_markup=data.button
            )
