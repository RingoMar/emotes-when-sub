#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import re
import socket
import sys
import traceback
import random
from datetime import datetime as dt
from threading import Thread
from time import sleep as sleep

import requests
from colorama import Back, Fore, Style, init
from requests import Session

init()

HOST = "irc.twitch.tv"
PORT = 6667
botname = "Your_Channel" #--Place The Bots Name Here
chan = "#" + "The_Channel" #--Place The channel you want to spam in here
sock = socket.socket()
OAuth = "oauth:njsda72mas78vh342bh38nasd9dasbn3" #--Place your Auth Key here
cid = 'snnhafdssefmklhnjscanldikczc' #--Place your Client Id here
intstart = True
lastping = ""
subgifts = 0
mgft = False
giftcount = 0

lastping = dt.now().strftime('%Y%m%d%H%M%S')


class sitinchat(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def connectsock(self):
        global intstart
        print("Trying to connect to... irc.twitch.tv:6667")
        sock.connect((HOST, PORT))
        sock.send(f"PASS {OAuth}\r\n".encode("utf-8"))
        sock.send(f"NICK {botname}\r\n".encode("utf-8"))
        sock.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))
        sock.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
        sock.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
        sock.send("JOIN {} \r\n".format(chan).encode("utf-8")) 
        print(f"Joined {chan}.")
        intstart = False
        return

    def readfuntion(self):
        global lastping
        global mgft
        global giftcount
        pringtime = ("{:{tfmt}}".format(dt.now(), tfmt="%c"))
        buffer = ""
        buffer += sock.recv(2048).decode('utf-8')
        temp = buffer.split("\r\n")
        buffer = temp.pop()
        for line in temp:
            _line = str(line.encode("utf-8").decode("utf-8"))
            if line == "PING :tmi.twitch.tv":
                lastping = dt.now().strftime('%Y%m%d%H%M%S')
                sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                # print(Fore.WHITE + Back.CYAN + f"[{pringtime}] " + Style.RESET_ALL + f"{_line}") #--Show the last ping here if you want
            if str("tmi.twitch.tv USERNOTICE ") in _line:
                sleep(1) #--Sleep can be what ever you want
                messagetype = re.search(r"msg-id=([a-zA-Z]+)", _line)
                submsgmsg = "Your_Emotes(s) " * int(random.randint(30, 38)) #-- Replace "Your_Emotes(s)" with the emote/s that you like
                gs = re.search(r"system-msg=[a-zA-Z0-9-_\w]+ (gifted)", _line.replace("\s", " "))
                try:
                #this finds the subs to send too
                    if str(messagetype.group(1)) == "resub":
                        print(f"[{pringtime}] - RESUB")
                        sock.send(("PRIVMSG {} :{}\r\n").format(chan, submsgmsg).encode("utf-8"))
                    elif str(messagetype.group(1)) == "sub":
                        print(f"[{pringtime}] - SUB")
                        sock.send(("PRIVMSG {} :{}\r\n").format(chan, submsgmsg).encode("utf-8"))
                    elif str(messagetype.group(1)) == "primepaidupgrade":
                        print(f"[{pringtime}] - PRIMEPAIDUPGRADE")
                        sock.send(("PRIVMSG {} :{}\r\n").format(chan, submsgmsg).encode("utf-8"))
                    elif str(messagetype.group(1)) == "giftpaidupgrade":
                        print(f"[{pringtime}] - GIFTPAIDUPGRADE")
                        sock.send(("PRIVMSG {} :{}\r\n").format(chan, submsgmsg).encode("utf-8"))
                    elif str(messagetype.group(1)) == "subgift" or gs:
                        print(f"[{pringtime}] - SUBGIFT")
                        if (giftcount) > 0:
                            giftcount -= 1
                            pass
                        elif mgft == True:
                            mgft = False
                            sock.send(("PRIVMSG {} :{}\r\n").format(chan, submsgmsg).encode("utf-8"))
                        else:
                            sock.send(("PRIVMSG {} :{}\r\n").format(chan, submsgmsg).encode("utf-8"))
                    elif str(messagetype.group(1)) == "submysterygift":
                        print(f"[{pringtime}] - SUBMYSTERYGIFT")
                        giftcounta=re.search(r"msg-param-mass-gift-count=([0-9]+)", _line)
                        deting = int(giftcounta.group(1))
                        fcount = (deting - 1)
                        if fcount > 0:
                            mgft = True
                        giftcount += int(fcount)
                except Exception as e:
                    pass #-- You can show errors if you want
            return

    def run(self):
        global intstart
        try:
            if intstart:
                sitinchat.connectsock(self)
        except Exception as e:
            pass

        while True:
            try:
                sitinchat.readfuntion(self)
            except Exception as e:
                pass
        return


class hearthbeat(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def has_internet(self, url='http://www.google.com/', timeout=5):
        try:
            req = requests.get(url, timeout=timeout)
            req.raise_for_status()
            return True
        except requests.HTTPError as e:
            print("Checking internet connection failed, status code {0}.".format(
            e.response.status_code))
        except requests.ConnectionError:
            print("No internet connection available.")
        return False

    def run(self):
        global lastping
        while True:
            sleep(60)
            try:
                sock.send(("ping\r\n").encode("utf-8"))
            except BrokenPipeError:
                if str(hearthbeat.has_internet(self)) == "True":
                    print (hearthbeat.has_internet(self))
                    os.execv(sys.executable, ['python3'] + sys.argv)
            except Exception as e:
                print (hearthbeat.has_internet(self))
                print (traceback.format_exc())
            tnow = str(dt.now().strftime('%Y%m%d%H%M%S'))
            format = '%Y%m%d%H%M%S'
            delta = dt.strptime(tnow, format) - dt.strptime(lastping, format)
            if int(delta.total_seconds()) > 600.0:
                if str(hearthbeat.has_internet(self)) == "True":
                    os.execv(sys.executable, ['python3'] + sys.argv)
        return

try:
    sitinchat()
    hearthbeat()
    while True:
        pass
except KeyboardInterrupt:
    sys.exit("Good bye :)")
