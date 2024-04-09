from hydrogram import Client, filters
from data import add_off, rm_off, check_listoff
from ext import owner, filter_right

@Client.on_message(filters.command("set_auto_download_off") & (owner|filter_right) & filters.group)
def set_auto_download_off(c, m):
    status = add_off(m.chat.id)
    if status:
        if m.from_user.language_code == "vi":
            m.reply("Tự động tải xuống đã được tắt cho nhóm chat này. Bạn vẫn có thể tải xuống bằng cách dùng lệnh /download")
        else:
            m.reply("Auto downloads for this group was disabled. You still can download by using command /download")
    else:
        if m.from_user and m.from_user.language_code == "vi":
            m.reply("Tự động tải xuống cho nhóm chat này là đang tắt. Không cần thiết phải thực hiện lại hành động này")
        else:
            m.reply("Auto downloads for this group is disabled. Rewrite this status is unnecessary")
    

@Client.on_message(filters.command("set_auto_download_on") & (owner|filter_right) & filters.group)
def set_auto_download_on(c, m):
    status = rm_off(m.chat.id)
    if status:
        if m.from_user.language_code ==  "vi":
            m.reply("Tự động tải xuống cho nhóm chat này đã được khôi phục")
        else:
            m.reply("Auto downloads for this group have been restored")
    else:
        if m.from_user.language_code == "vi":
            m.reply("Tự động tải xuống không bị tắt")
        else:
            m.reply("Auto downloads are not disabled")