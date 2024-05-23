from hydrogram.enums import ChatAction
from hydrogram import Client, filters


@Client.on_message(
    (
        ((filters.regex("http|https") & filters.regex("facebook.|fb.|instagram.")))
        | filters.command("facebook")
    )
    & filters.incoming
)
def facebook_download(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    m.reply(
        "Facebook API has no endpoint server to run. If you want to contribute, contact admin.\n\nHiện chúng tôi đã ngừng cung cấp dịch vụ tải nội dung từ những nền tảng này do thiếu máy chủ API. Nếu bạn có nhu cầu đóng góp, hãy liên hệ nhà sáng lập bot",
        quote=True,
    )
