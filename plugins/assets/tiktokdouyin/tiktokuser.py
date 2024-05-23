import logging
from hydrogram.enums import ChatAction
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from plugins.util import get_media_links, send_photos, send_videos


def TikTokUser(m, url, caption, TDDL):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("TikTok User", url=url),
                InlineKeyboardButton("Group", url="https://t.me/contentdownload_group"),
                InlineKeyboardButton("Channel", url="https://t.me/contentdownload"),
            ]
        ]
    )
    media_links = get_media_links(url)
    list_video = []
    list_photo = []
    for media_link in media_links:
        media, music, is_video = TDDL(media_link)
        if is_video:
            m.reply_chat_action(ChatAction.RECORD_VIDEO)
            list_video.append(media[0])
        else:
            list_photo.extend(media[0])
    if list_photo:
        try:
            send_photos(m, list_photo, button, caption)
        except Exception as e:
            logging.critical(e)
    if list_video:
        try:
            send_videos(m, list_video, button, caption)
        except Exception as e:
            logging.critical(e)
