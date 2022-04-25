from configparser import ConfigParser
from datetime import datetime, timedelta
from os import  makedirs
from subprocess import check_output
from time import sleep


def start(update, context):
    ''' START '''
    context.bot.send_message(update.message.chat_id, "Bienvenido")

def main():
    lastlog=datetime.now()-timedelta(days=1)
    
    while True:
        print(datetime.now())
        cat = check_output("cat /var/log/messages| grep -i sshd", shell=True).decode("UTF-8")
        
        send=False
        lines=cat.split('\n')
        for line in lines:
            d=str(datetime.now().year)+" " + line[:-len(line)+15]
            if line.find('pam_unix(sshd:auth): authentication failure')!=-1 or line.find('pam_unix(sshd:session): session opened')!=-1:
                try:
                    nueva=datetime.strptime(d, '%Y %b %d %H:%M:%S')
                except:
                    print("error parsing date") 
                if lastlog<nueva:
                    lastlog=nueva
                    send=True
        if send==True:
            send_message_with_requests(cat[-1000:])
        sleep(10)
            
def send_message_with_requests(message):
    import requests
    makedirs("/etc/ssh_telegram_advice", exist_ok=True)
    config = ConfigParser()
    config.read("/etc/ssh_telegram_advice/ssh_telegram_advice")
    token= config["Telegram"]["token"]
    chat_id= config["Telegram"]["chat_id"]
    d={"chat_id": chat_id,  "text": message[-00:]}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r=requests.post(url, d)
    sleep(0.5)
    print("Message sent",  url, r, d)

    
