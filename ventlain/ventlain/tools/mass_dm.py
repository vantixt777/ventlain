import asyncio
import aiohttp
import os
import json
import random
import time
import re 
from pystyle import Colors, Colorate, Center

class UltimateMassDM:
    def __init__(self):
        self.banner = r"""
   ▄▄▄▄███▄▄▄▄      ▄████████    ▄████████    ▄████████      ████████▄    ▄▄▄▄███▄▄▄▄   
 ▄██▀▀▀███▀▀▀██▄   ███    ███   ███    ███   ███    ███      ███   ▀███ ▄██▀▀▀███▀▀▀██▄ 
 ███   ███   ███   ███    ███   ███    █▀    ███    █▀       ███    ███ ███   ███   ███ 
 ███   ███   ███   ███    ███   ███          ███             ███    ███ ███   ███   ███ 
 ███   ███   ███ ▀███████████ ▀███████████ ▀███████████      ███    ███ ███   ███   ███ 
 ███   ███   ███   ███    ███          ███          ███      ███    ███ ███   ███   ███ 
 ███   ███   ███   ███    ███    ▄█    ███    ▄█    ███      ███   ▄███ ███   ███   ███ 
  ▀█   ███   █▀    ███    █▀   ▄████████▀   ▄████████▀       ████████▀   ▀█   ███   █▀  
                                                                                        
                                                                                                
        """
        self.tokens = []
        self.valid_tokens = []
        self.message = ""
        self.delay = 0.5
        self.rate_limit = 5
        self.max_retries = 3
        self.random_delay = (0.3, 1.2)
        self.session = None
        self.stats = {
            'sent': 0,
            'failed': 0,
            'retries': 0
        }

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("by vantixt")))
        print("\n")

    def clean_token(self, token):
        cleaned = re.sub(r'#.*$', '', token).strip()
        cleaned = re.sub(r'[^\x20-\x7E]', '', cleaned)
        return cleaned

    def load_tokens(self):
        token_file = "tokens.txt"
        if not os.path.exists(token_file):
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter(f"[!] Token file '{token_file}' not found [!]")))
            return False

        with open(token_file, "r", encoding="utf-8") as f:
            raw_tokens = f.readlines()

        self.tokens = [self.clean_token(t) for t in raw_tokens if self.clean_token(t)]
        self.valid_tokens = [t for t in self.tokens if self.validate_token(t)]

        if not self.valid_tokens:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("[!] No valid tokens found in tokens.txt [!]")))
            return False

        return True

    def validate_token(self, token):
        return len(token) >= 59 and "." in token

    async def get_user_channels(self, token):
        headers = {'Authorization': token}
        try:
            async with self.session.get(
                'https://discord.com/api/v9/users/@me/channels',
                headers=headers
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                return []
        except:
            return []

    async def get_user_friends(self, token):
        headers = {'Authorization': token}
        try:
            async with self.session.get(
                'https://discord.com/api/v9/users/@me/relationships',
                headers=headers
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return [friend['id'] for friend in data if friend['type'] == 1]
                return []
        except:
            return []

    async def create_dm_channel(self, token, user_id):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        payload = {'recipient_id': user_id}

        for attempt in range(self.max_retries):
            try:
                async with self.session.post(
                    'https://discord.com/api/v9/users/@me/channels',
                    headers=headers,
                    json=payload
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data['id']
                    elif resp.status == 429:
                        retry_after = (await resp.json()).get('retry_after', 1)
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        return None
            except:
                await asyncio.sleep(random.uniform(*self.random_delay))

        return None

    async def send_dm(self, token, channel_id):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        payload = {'content': self.message}

        for attempt in range(self.max_retries):
            try:
                async with self.session.post(
                    f'https://discord.com/api/v9/channels/{channel_id}/messages',
                    headers=headers,
                    json=payload
                ) as resp:
                    if resp.status == 200:
                        self.stats['sent'] += 1
                        return True
                    elif resp.status == 429:
                        retry_after = (await resp.json()).get('retry_after', 1)
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        self.stats['failed'] += 1
                        return False
            except:
                self.stats['retries'] += 1
                await asyncio.sleep(random.uniform(*self.random_delay))

        self.stats['failed'] += 1
        return False

    async def process_token(self, token):
        await asyncio.sleep(random.uniform(*self.random_delay))

        channels = await self.get_user_channels(token)
        for channel in channels:
            await self.send_dm(token, channel['id'])
            await asyncio.sleep(self.delay)

        friends = await self.get_user_friends(token)
        for friend_id in friends:
            channel_id = await self.create_dm_channel(token, friend_id)
            if channel_id:
                await self.send_dm(token, channel_id)
                await asyncio.sleep(self.delay)

    async def run_dm(self):
        if not self.load_tokens():
            return

        self.display_menu()
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"[*] Loaded {len(self.valid_tokens)} valid tokens [*]")))

        self.message = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\n Message to send: "))).strip()

        self.display_menu()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(f" WARNING: THIS WILL SEND TO ALL CONTACTS ON {len(self.valid_tokens)} TOKENS! ")))
        time.sleep(2)

        confirm = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nStart Mass DM? (y/n): "))).lower()

        if confirm != 'y':
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\n[!] OPERATION CANCELLED [!]\n")))
            return

        self.session = aiohttp.ClientSession()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\n[!] MASS DM ACTIVATED! [!]\n")))

        semaphore = asyncio.Semaphore(self.rate_limit)
        async def limited_process(token):
            async with semaphore:
                return await self.process_token(token)

        await asyncio.gather(*[limited_process(token) for token in self.valid_tokens])
        await self.session.close()

        print(Colorate.Horizontal(Colors.green_to_white,
            Center.XCenter(f"\n[+] MASS DM COMPLETE [+]")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"Sent: {self.stats['sent']} | Failed: {self.stats['failed']} | Retries: {self.stats['retries']}")))

if __name__ == "__main__":
    dm_tool = UltimateMassDM()
    asyncio.run(dm_tool.run_dm())
    input(Colorate.Horizontal(Colors.red_to_white,
        Center.XCenter("\nPress ENTER to exit...")))