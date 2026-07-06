import requests, json, time, threading

TELEGRAM_TOKEN = "XXXXXXXXXXXXXXXXXXX"
URL_base  = "https://api.telegram.org/bot"+TELEGRAM_TOKEN+"/"

def telegram_get_updates(offset = 0):
    payload  = {"offset": offset}
    r = requests.post(URL_base+"getUpdates", data=payload)
    r.raise_for_status()
    return r.json()["result"]

def telegram_send_answer(chat_id, answer):
    payload = {"chat_id": chat_id, "text": answer}
    r = requests.post(URL_base+"sendMessage", data=payload)
    r.raise_for_status()
    
def talk_telegram():
    global active, all_msgs 
    print ("Esperando mensagens do telegram!!!")
    last_update = 0
    while active:
        updates = telegram_get_updates(last_update+1)
        for update in updates:
            update_id = update["update_id"]
            message = update.get("message", None)
            if message:
                all_msgs[update_id] = message
            last_update = update_id
        time.sleep(2)

def user_show_messages():
    for update_id in all_msgs:
        message = all_msgs[update_id]
        print (f'\tupdate_id: {update_id} - {message["chat"]["first_name"]} -> {message["text"]}')

def user_answer_message():
    update_id = int(input ("Qual o update a responder: "))
    message = all_msgs.get(update_id, None)
    if message:
        answer = input ("Resposta: ")
        telegram_send_answer(message["chat"]["id"], answer)
        del all_msgs[update_id]
    else:
        print ("Update não encontrado!")

def show_menu():
    try:
        print ("1. Mostra mensagens")
        print ("2. Responde mensagem")
        print ("3. Sai")
        return int(input("opcao: "))
    except ValueError:
        return 0

def talk_user():
    global active
    while True:
        option = show_menu()
        if option == 1:
            user_show_messages()
        elif option == 2:
            user_answer_message()
        elif option == 3:
            active = False
            return 
        else:
            print ("Opção inválida.")

def main():
    global active, all_msgs
    all_msgs = {}
    active = True

    ttelegram = threading.Thread(target=talk_telegram)
    tuser     = threading.Thread(target=talk_user)
    ttelegram.start()
    tuser.start()

    ttelegram.join()
    tuser.join()

main()