
def add_off(chat_id):
    with open("listoff.txt", "r") as f:
        chat_ids = f.read().splitlines()
        if str(chat_id) not in chat_ids:
            with open("listoff.txt", "a") as w:
                w.write("\n" + str(chat_id))
                
def rm_off(chat_id):
    with open("listoff.txt", "r") as f:
        chat_ids = f.read().splitlines()
        if str(chat_id) in chat_ids:
            chat_ids.remove(str(chat_id)) 
            with open("listoff.txt", "w") as w:
                w.write("\n".join(chat_ids))
