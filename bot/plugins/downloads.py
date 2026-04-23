from hydrogram import Client, filters
from hydrogram.types import Message

from bot.methods.custom import reply_media_group
from bot.services.downloads import DownloadTask, handle_download, handle_youtube_download


@Client.on_message(filters.regex("http|https") & filters.regex("youtube.|youtu.be"))
async def __youtube__(_: Client, m: Message):
    await handle_youtube_download(m)


@Client.on_message(filters.regex("http|https") & filters.regex("facebook.|fb."))
async def __facebook__(_: Client, m: Message):
    await handle_download(
        m,
        DownloadTask(
            endpoint="facebook",
            action_name="facebook",
            reply_handler=reply_media_group,
        ),
    )


@Client.on_message(filters.regex("http|https") & filters.regex("instagram."))
async def __instagram__(_: Client, m: Message):
    await handle_download(
        m,
        DownloadTask(
            endpoint="instagram",
            action_name="instagram",
            reply_handler=reply_media_group,
        ),
    )


@Client.on_message(
    filters.regex("http|https") & filters.regex("douyin.|iesdouyin.|tiktok.")
)
async def __douyin__(_: Client, m: Message):
    await handle_download(
        m,
        DownloadTask(
            endpoint="douyin",
            action_name="douyin",
            reply_handler=reply_media_group,
        ),
    )
