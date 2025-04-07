import mimetypes

from google.genai import types
from hydrogram import Client
from hydrogram.types import Message


def get_user(m: Message) -> tuple[str | None, str | None]:
    if m.from_user:
        name = (
            f"{m.from_user.first_name} {m.from_user.last_name}"
            if m.from_user.last_name
            else m.from_user.first_name
        )
        username = m.from_user.username
    else:
        name = m.sender_chat.title
        username = m.sender_chat.username
    return name, username


async def split_parts(client: Client, message: Message | list[Message]):
    parts = []
    fullname, username = get_user(message)
    parts.append(
        types.Part.from_text(
            text=f"<<<NAME: {fullname}, USERNAME: {username}>>>",
        )
    )
    if isinstance(message, Message):
        rtm = message.reply_to_message
        if message.text:
            part = types.Part.from_text(text=message.text)
            parts.append(part)
        if message.sticker:
            part = types.Part.from_text(
                text="<<<send a sticker, you are not suppported>>>"
            )
            parts.append(part)
        if (
            message.video
            or message.audio
            or message.document
            or message.animation
            or message.voice
            or message.video_note
            or message.photo
        ):
            media_data = await client.download_media(message, in_memory=True)
            if message.video:
                mime_type = message.video.mime_type
            elif message.audio:
                mime_type = message.audio.mime_type
            elif message.document:
                mime_type = message.document.mime_type
            elif message.animation:
                mime_type = message.animation.mime_type
            elif message.voice:
                mime_type = message.voice.mime_type
            elif message.video_note:
                mime_type = message.video_note.mime_type
            elif message.photo:
                mime_type = "image/jpeg"
            else:
                mime_type = mimetypes.guess_type(media_data)[0]
            part = types.Part.from_bytes(
                data=media_data.getvalue(),
                mime_type=mime_type,
            )
            parts.append(part)

        if rtm:
            if (
                rtm.video
                or rtm.audio
                or rtm.document
                or rtm.sticker
                or rtm.animation
                or rtm.voice
                or rtm.video_note
                or rtm.photo
            ):
                media_data = await client.download_media(rtm, in_memory=True)
                if rtm.video:
                    mime_type = rtm.video.mime_type
                elif rtm.audio:
                    mime_type = rtm.audio.mime_type
                elif rtm.document:
                    mime_type = rtm.document.mime_type

                elif rtm.animation:
                    mime_type = rtm.animation.mime_type
                elif rtm.voice:
                    mime_type = rtm.voice.mime_type
                elif rtm.video_note:
                    mime_type = rtm.video_note.mime_type
                elif rtm.photo:
                    mime_type = "image/jpeg"
                else:
                    mime_type = mimetypes.guess_type(media_data)[0]
                part = types.Part.from_bytes(
                    data=media_data.getvalue(),
                    mime_type=mime_type,
                )
                parts.append(part)
        if message.caption:
            part = types.Part.from_text(text=message.caption)
            parts.append(part)

        return parts
