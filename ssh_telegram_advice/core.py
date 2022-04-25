from configparser import ConfigParser
from datetime import datetime

from os import  makedirs
from subprocess import check_output
 
 
 ## To get channel_id  https://api.telegram.org/bot<YourBOTToken>/getUpdates
from telegram.ext import (Updater, CommandHandler)

#from pyinotify import WatchManager, ProcessEvent, ALL_EVENTS, Notifier

#class MyEventHandler(ProcessEvent):
#    lastlog=datetime.now()
#    fallidos=0
#    validos=0
#def process_IN_MODIFY(self, event):
#
#

def start(update, context):
    ''' START '''
    context.bot.send_message(update.message.chat_id, "Bienvenido")

def main():


    makedirs("/etc/ssh_telegram_advice", exist_ok=True)
    config = ConfigParser()
    config.read("/etc/ssh_telegram_advice/ssh_telegram_advice")
    api_id = config["Telegram"]["api_id"]
    api_hash = config["Telegram"]["api_hash"]
    token= config["Telegram"]["token"]
    phone= config["Telegram"]["phone"]
    username= config["Telegram"]["username"]
    print(api_id, api_hash, phone, username)
    
#    send_message("HOLA")
    
#    
#    
#    # event handler
#    eh = MyEventHandler()
#
#    # notifier
#    notifier = Notifier(wm, eh)
#    notifier.loop()


    updater=Updater(token, use_context=True)
    dp=updater.dispatcher

    # Eventos que activarán nuestro bot.
    dp.add_handler(CommandHandler('start',	start))

    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    import request

    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id=@telechanneltesting&text=message"
    requests.post(url)
    
    
    
    return
    lastlog=datetime.now()
    fallidos=0
    validos=0
    
    cat = check_output("cat /var/log/messages| grep -i sshd", shell=True)
    for line in cat.split(b'\n'):
        line=line.decode("UTF-8")
        print (line[:-1])
        d=str(datetime.now().year)+" " + line[:-len(line)+15]
        if line.find('pam_unix(sshd:auth): authentication failure')!=-1:
            try:
                nueva=datetime.strptime(d, '%Y %b %d %H:%M:%S')
            except:
                print("error parsing date")
            if lastlog<nueva:
                fallidos=fallidos+1
                send_message("espeak -v es 'Conexión remota fallida número {0}' >& /dev/null".format(fallidos))
            lastlog=nueva
        elif line.find('pam_unix(sshd:session): session opened for user ')!=-1:
            try:
                nueva=datetime.strptime(d, '%Y %b %d %H:%M:%S')
            except:
                print("error parsing date")
            if lastlog<nueva:
                validos=validos+1
                send_message("espeak -v es 'Conexión remota aceptada número {0}' >& /dev/null".format(validos))
            lastlog=nueva
    
def send_message_with_telethon(message):
    from telethon import TelegramClient
    config = ConfigParser()
    config.read("/etc/ssh_telegram_advice/ssh_telegram_advice")
    api_id = config["Telegram"]["api_id"]
    api_hash = config["Telegram"]["api_hash"]
    phone= config["Telegram"]["phone"]
    username= config["Telegram"]["username"]
    print(api_id, api_hash, phone, username)
    client = TelegramClient(username, api_id, api_hash)
  
    # connecting and building the session
    client.connect()
     
    # in case of script ran first time it will
    # ask either to input token or otp sent to
    # number or sent or your telegram id
    if not client.is_user_authorized():
      
        client.send_code_request(phone)
         
        # signing in the client
        client.sign_in(phone, input('Enter the code: '))
      
      
    try:
        # receiver user_id and access_hash, use
        # my user_id and access_hash for reference
#        receiver = InputPeerUser(
     
        # sending message using telegram client
        client.send_message(username, message, parse_mode='html')
    except Exception as e:
         
        # there may be many error coming in while like peer
        # error, wrong access_hash, flood_error, etc
        print(e);
     
    # disconnecting the telegram session
    client.disconnect()
    
