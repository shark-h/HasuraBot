import json
import aiohttp
import logging
import random

logging.getLogger('asyncio').setLevel(logging.CRITICAL)

class Brain:
    def __init__(self, user, key, nick, loop):
        self.user = user
        self.key = key
        self.nick = nick
        self.body = {
                    'user': self.user,
                    'key': self.key,
                    'nick': self.nick
                }
        self.sess = aiohttp.ClientSession(loop=loop)

    async def create(self):
        async with self.sess.post('https://cleverbot.io/1.0/create', json=self.body) as resp:
            r = await resp.json()
        if resp.status == 200:
            if r["status"] != "success":
                self.nick += '-{}'.format(random.randint(1,1000))
                self.body['nick'] = self.nick
                async with self.sess.post('https://cleverbot.io/1.0/create', json=self.body) as resp:
                    r = await resp.json()
                if r["status"] == "success":
                    return "API is online. Using clever mode."
                else:
                    return "API is down. Will notify the users."    
            else:
                return "API is online. Using clever mode."
        else:
            return "API is down. Will notify the users."
            
        
    async def query(self, text):
        self.body['text'] = text
        try:
            async with self.sess.post('https://cleverbot.io/1.0/ask', json=self.body) as resp:
                r = await resp.json()

            if r['status'] == 'success':
                return r['response'], 200
        except:
            return "Looks like the CleverBot.IO api is down. Please try again later.", 500

