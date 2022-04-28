from .__init__ import __versiondate__, __version__
from .reusing.datetime_functions import string2dtnaive
from argparse import ArgumentParser, RawTextHelpFormatter
from configparser import ConfigParser
from datetime import datetime, timedelta
from gettext import translation
from logging import info, ERROR, WARNING, INFO, DEBUG, CRITICAL, basicConfig
from os import path
from pkg_resources import resource_filename
from requests import post
from subprocess import run
from sys import exit
from time import sleep

from signal import signal,  SIGINT

try:
    t=translation('ssh_telegram_advice', resource_filename("ssh_telegram_advice","locale"))
    _=t.gettext
except:
    _=str
    
def signal_handler( signal, frame):
        print(_("You pressed 'Ctrl+C', exiting..."))
        exit(0)

## Function used in argparse_epilog
## @return String
def argparse_epilog():
    return _("Developed by Mariano Muñoz 2022-{}").format(__versiondate__.year)

## Sets debug sustem, needs
## @param args It's the result of a argparse     args=parser.parse_args()        
def addDebugSystem(level):
    logFormat = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s [%(module)s:%(lineno)d]"
    dateFormat='%F %I:%M:%S'

    if level=="DEBUG":#Show detailed information that can help with program diagnosis and troubleshooting. CODE MARKS
        basicConfig(level=DEBUG, format=logFormat, datefmt=dateFormat)
    elif level=="INFO":#Everything is running as expected without any problem. TIME BENCHMARCKS
        basicConfig(level=INFO, format=logFormat, datefmt=dateFormat)
    elif level=="WARNING":#The program continues running, but something unexpected happened, which may lead to some problem down the road. THINGS TO DO
        basicConfig(level=WARNING, format=logFormat, datefmt=dateFormat)
    elif level=="ERROR":#The program fails to perform a certain function due to a bug.  SOMETHING BAD LOGIC
        basicConfig(level=ERROR, format=logFormat, datefmt=dateFormat)
    elif level=="CRITICAL":#The program encounters a serious error and may stop running. ERRORS
        basicConfig(level=CRITICAL, format=logFormat, datefmt=dateFormat)
    info("Debug level set to {}".format(level))


def main():
    
    signal(SIGINT, signal_handler)
    parser=ArgumentParser(description=_('Enables a ssh monitor with login advices in telegram'), epilog=argparse_epilog(), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--debug', help=_("Debug program information"), choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], default="ERROR")
    args=parser.parse_args()
    
    config_filename="/etc/ssh_telegram_advice/ssh_telegram_advice"
    addDebugSystem(args.debug)
        
    lastlog=datetime.now()-timedelta(minutes=30)
    global config
    if not path.exists(config_filename):
        print(_("You must set and configure {0}").format(config_filename))
        print(_("You can find in source code in conf.d directory"))
        return
    
    config = ConfigParser()
    config.read(config_filename)    
    print(_("Starting to monitor logs from {0}").format(lastlog))
    
    while True:
        # Search for sshd logins
        cat = run("cat /var/log/messages| grep -i sshd", shell=True, capture_output=True)        
        lines=cat.stdout.decode("UTF-8").split('\n')
        send=[]
        for line in lines:
            if any(pattern in line for pattern in [
                'sshd:auth', 
                'sshd:session', 
                'Accepted keyboard-interactive/pam', 
                'onnect', 
                'Permission denied', 
            ]):
                dt=string2dtnaive( line[:-len(line)+15], '%b %d %H:%M:%S')
                if lastlog<=dt:
                    lastlog=dt
                    send.append(line)
        lastlog=lastlog+timedelta(microseconds=1)# To not repeat lastlogs
        
        # Sends 3 lines on message
        if len(send)>0:
            message=""
            for i, line in enumerate(send):
                message=message+line+"\n"
                if i==len(send)-1 or i % 3==2:
                    send_message_with_requests(message)
                    message=""
                    
        # Waits interval
        sleep(float(config["Logs"]["interval"]))
            
def send_message_with_requests(message):
    token= config["Telegram"]["token"]
    chat_id= config["Telegram"]["chat_id"]
    d={"chat_id": chat_id,  "text": message}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r=post(url, d)
    print("Message sent at", datetime.now(),  r, d)

    
