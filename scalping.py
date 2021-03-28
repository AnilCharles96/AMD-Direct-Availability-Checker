# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 23:56:54 2021

@author: Anil
"""
import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime
from email.header import Header



"""
Note
----
If you are using gmail then I recommend using app passwords in gmail
1. Turn on 2 step in gmail
2. Turn on allow less secure apps
3. create new app password and paste it in the below variable EMAIL_PASS

"""

EMAIL_ADDRESS = "your email address"
EMAIL_PASS = "your email password"
SENDER_NAME = "name of the sender sending mail"

# you can add more than one using list eg: RECEIVER_EMAIL = ["a@gmail.com","b@gmail.com"]
RECEIVER_EMAIL = "receiver email"



def send_mail(title):
    msg = EmailMessage()
    msg['subject'] = title + " in stock"
    msg['From'] = str(Header(f"{SENDER_NAME} <{EMAIL_ADDRESS}>"))
    msg['to'] = RECEIVER_EMAIL
    msg.set_content(f"{title} available please buy ASAP")
    with smtplib.SMTP('smtp.gmail.com',"587") as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)  
        smtp.close()


def write_log(message):
    with open("log.txt","a") as f:
        f.write(message + "\n")
        f.close()
        

"""
keys list are what needs to be searched
need list are what you will be notified through mail

An email will be send when if items in need list is available


keys >= need ie. if what you need is not available in need list then it wont be checked

eg 1:
keys = ["6900 XT", "6800 XT"] need = ["6900 XT", "6800 XT"]
search for 6900xt and 6800xt. I need 6900xt and 6800xt

eg 2:
keys = ["6900 XT", "6800 XT", "5600X"] need = ["6900 XT", "6800 XT"]
search for 6900xt, 6800xt and 5600x. I need only 6900xt and 6800xt
"""
def scalping(response, keys, need):
    soup = BeautifulSoup(response)
    for body in soup.find_all("div", {"class":"direct-buy"}):   
        for key in keys:
            title = body.find("div", {"class":"shop-title"}).text.strip()
            if key in title:
                avail = body.find("div", {"class":"shop-links"}).text.strip()
                if "Out of Stock" in avail:
                    message = title + " ---- " + avail
                else:
                    button = body.find("button", {"class":"btn-shopping-cart"}).text.strip()
                    if "Add to cart" in button:  
                        message = title + " ---- " + "Add to cart"
                        for each_need in need:
                            if each_need in title:
                                send_mail(title)                         
                    else:
                        message = None
                        raise Exception()
                write_log(message)
                print(str(datetime.now().strftime('%Y:%m:%d %H:%M:%S')) + " ---- " + message + "\n")
                


"""
Access-Control-Request-Method and origin header is important if you are 
deploying the script to RDP/Cloud. If you dont use this then there wont be any response from the server
Its not necessary to use above header if you are running the script locally

User-Agent is also very important without it there wont be any response from the server

"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Accept-Language': 'en-US,en;q=0.5',
    "Access-Control-Request-Method": "GET",
    "Origin": "*",
}
keys = ["6900 XT", "6800 XT"]
need = ["6900 XT", "6800 XT"]

if __name__ == '__main__':
    while(True):
        res = requests.get("https://www.amd.com/de/direct-buy/de",headers=headers,timeout=10).content.decode('utf-8')
        scalping(res, keys, need)
        time.sleep(1)
        # sometimes command line gets stuck clearing will solve such issue
        os.system("cls")

