#!/bin/python

import json
import urllib
from time import sleep
LAST_PROCESSED_MESSAGE = 0
TOKEN = ''#
BOT_API_URL = 'https://api.telegram.org/bot'
# send message
def sendmessage(chat_id=0, text="", reply_to_message_id=None, disable_web_page_preview=True, token = TOKEN, botapiurl = BOT_API_URL):
    url = "%s%s/sendMessage" % (botapiurl, token)
    try:
        message = "%s?chat_id=%s&text=%s" % (url, chat_id, urllib.quote_plus(text.encode('utf-8', 'ignore')))
    except:
        message = "%s?chat_id=%s&text=%s" % (url, chat_id, urllib.quote_plus(text))
    if reply_to_message_id:
        message = message + "&reply_to_message_id=%s" % reply_to_message_id
    if disable_web_page_preview:
        message = message + "&disable_web_page_preview=1"
    print message
    return json.load(urllib.urlopen(message))
# get update messages
def getupdates(offset=0, limit=100, token = TOKEN, botapiurl = BOT_API_URL):
    url = "%s%s/getUpdates" % (botapiurl, token)
    message = "%s?" % url
    if offset != 0:
        message = message + "offset=%s&" % offset
    message = message + "limit=%s" % limit
    try:
        result = json.load(urllib.urlopen(message))['result']
    except:
        result = []
    for item in result:
        yield item
# trash all updates
def clearupdates(offset, token = TOKEN, botapiurl = BOT_API_URL):
    url = "%s%s/getUpdates" % (botapiurl, token)
    message = "%s?" % url
    message = message + "offset=%s&" % offset
    try:
        result = json.load(urllib.urlopen(message))
    except:
        result = None
    return result
# commands parser
def telegramcommands(texto, chat_id, token = TOKEN, botapiurl = BOT_API_URL):
    word = texto.split()[0]
    cmdText = None
    if word == '/help':
        cmdText = r"""
Help!!!
        """
    elif word == '/start' or word == '/stop':
        cmdText = r"""
It is not supported!
        """
        
    if cmdText:
        sendmessage(chat_id, cmdText)
    return
def process(sourceGroupID = -5407864, targetGroupID = -25645443):
    global LAST_PROCESSED_MESSAGE
    for message in getupdates(LAST_PROCESSED_MESSAGE):
        if LAST_PROCESSED_MESSAGE < message['update_id']:
            LAST_PROCESSED_MESSAGE = message['update_id']
        #else:
        #    print 'Ignoring %d, %s' % (message['update_id'], message['message']['text'].lower()),
        #    continue

            error = False
            print message

            try:
                texto = message['message']['text']
                #chat_id = message['message']['chat']['id']
                message_id = int(message['message']['message_id'])
                #date = int(float(message['message']['date']))
                #chat_name = message['message']['chat']['title']
                #who_gn = message['message']['from']['first_name']
                #who_id = message['message']['from']['id']
            except: 
                error = True

            try:
                who_ln = message['message']['from']['last_name']
            except:
                who_ln = None

            try:
                who_un = message['message']['from']['username']
            except:
                who_un = None

            if not error:
                telegramcommands(texto, message_id)
                print texto
                if texto.split()[0][0] != '/':
                    sendmessage(targetGroupID, texto)
        else:
            print 'No new messages'#, message[-1]

if __name__ == '__main__':
    LAST_PROCESSED_MESSAGE = 0
    counter = 0
    while True:
        process()
        sleep(5)
        print counter
        counter += 1

