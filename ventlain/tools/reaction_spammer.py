import asyncio
import aiohttp
import os
import random
import re
import time
from pystyle import Colors, Colorate, Center

class UltimateReactionSpammer:
    def __init__(self):
        self.banner = r"""
   ▄████████    ▄████████    ▄████████  ▄████████     ███      ▄█   ▄██████▄  ███▄▄▄▄
  ███    ███   ███    ███   ███    ███ ███    ███ ▀█████████▄ ███  ███    ███ ███▀▀▀██▄
  ███    ███   ███    ███   ███    ███ ███    █▀     ▀███▀▀██ ███▌ ███    ███ ███   ███
 ▄███▄▄▄▄██▀  ▄███▄▄▄       ███    ███ ███            ███   ▀ ███▌ ███    ███ ███   ███
▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▀███████████ ███            ███     ███▌ ███    ███ ███   ███
▀███████████   ███    █▄    ███    ███ ███    █▄      ███     ███  ███    ███ ███   ███
  ███    ███   ███    ███   ███    ███ ███    ███     ███     ███  ███    ███ ███   ███
  ███    ███   ██████████   ███    █▀  ████████▀     ▄████▀   █▀    ▀██████▀   ▀█   █▀
  ███    ███
        """
        self.tokens = []
        self.valid_tokens = []
        self.session = None
        self.stats = {
            'added': 0,
            'failed': 0,
            'rate_limited': 0
        }
        self.emojis = ["😂", "🔥", "💯", "👍", "🤔", "🤣", "💀", "👌", "🎉", "🚀", "🌟", "💖", "😎", "👽", "🤖", "😈", "🍕", "🍔", "🍟", "🍦", "🍭"]

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

    async def add_reaction(self, token, channel_id, message_id, emoji, delay):
        headers = {
            'Authorization': token,
        }
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me'

        try:
            async with self.session.put(url, headers=headers) as resp:
                if resp.status == 204:
                    self.stats['added'] += 1
                    return True
                elif resp.status == 429:
                    retry_after = (await resp.json()).get('retry_after', 1)
                    self.stats['rate_limited'] += 1
                    await asyncio.sleep(retry_after)
                    return False
                else:
                    self.stats['failed'] += 1
                    return False
        except Exception as e:
            self.stats['failed'] += 1
            return False
        finally:
            await asyncio.sleep(delay)

    async def fetch_messages(self, token, channel_id, limit=100):
        headers = {
            'Authorization': token,
        }
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}'

        try:
            async with self.session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    messages = await resp.json()
                    return messages
                else:
                    return []
        except Exception as e:
            return []

    async def mass_reaction(self, channel_id, delay, tokens):
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"\n[!] MASS REACTION MODE ACTIVATED - {len(tokens)} TOKENS PARTICIPATING [!]\n")))

        semaphore = asyncio.Semaphore(20)  
        async def process_token(token):
            async with semaphore:
                messages = await self.fetch_messages(token, channel_id)
                for message in messages:
                    emoji = random.choice(self.emojis)  
                    if await self.add_reaction(token, channel_id, message['id'], emoji, delay):
                        print(Colorate.Horizontal(Colors.green_to_white,
                            Center.XCenter(f"[+] Reaction added with token: {token[:25]}... [+]")))
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white,
                            Center.XCenter(f"[-] Failed to add reaction with token: {token[:25]}... [-]")))
                    await asyncio.sleep(delay * random.uniform(0.5, 1.0))  

        await asyncio.gather(*[
            process_token(token)
            for token in tokens
        ])

    async def solo_reaction(self, channel_id, delay):
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("\n[!] SOLO REACTION MODE ACTIVATED - SINGLE TOKEN SPAMMING [!]\n")))

        token = random.choice(self.valid_tokens)
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"[*] Selected token: {token[:25]}... [*]")))

        messages = await self.fetch_messages(token, channel_id)
        for message in messages:
            emoji = random.choice(self.emojis)  
            if await self.add_reaction(token, channel_id, message['id'], emoji, delay):
                print(Colorate.Horizontal(Colors.green_to_white,
                    Center.XCenter(f"[+] Reaction added: {emoji} [+]")))
            else:
                print(Colorate.Horizontal(Colors.red_to_white,
                    Center.XCenter("[-] Failed to add reaction [-]")))
            await asyncio.sleep(delay * random.uniform(0.5, 1.0))  

    async def run(self):
        if not self.load_tokens():
            return

        self.display_menu()
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"[*] Loaded {len(self.valid_tokens)} valid tokens [*]")))

        print("\n" + Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("1. MASS REACTION MODE (Multiple tokens spamming)")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("2. SOLO REACTION MODE (Single token spamming)")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("3. CUSTOM TOKEN MODE (Select specific tokens to spam)")))

        mode = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nSelect mode (1-3): "))).strip()

        if mode not in ["1", "2", "3"]:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\n[!] INVALID SELECTION [!]\n")))
            return

        self.display_menu()
        channel_id = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Channel ID to spam: "))).strip()
        delay = float(input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Delay between reactions (seconds): ")) or "0.5"))

        tokens_to_use = []
        if mode == "3":
            self.display_menu()
            print(Colorate.Horizontal(Colors.blue_to_white,
                Center.XCenter("Available tokens:")))
            for i, token in enumerate(self.valid_tokens, 1):
                print(Colorate.Horizontal(Colors.blue_to_white,
                    Center.XCenter(f"{i}. {token[:25]}...")))
            selections = input(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\nEnter token numbers to use (e.g., 1,3,5 or 1-5): "))).strip()

            selected_indices = set()
            for part in selections.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    selected_indices.update(range(start, end + 1))
                else:
                    selected_indices.add(int(part))

            tokens_to_use = [self.valid_tokens[i-1] for i in selected_indices if 0 < i <= len(self.valid_tokens)]
            if not tokens_to_use:
                print(Colorate.Horizontal(Colors.red_to_white,
                    Center.XCenter("[!] No tokens selected for custom mode [!]")))
                return
        elif mode == "1":
            tokens_to_use = self.valid_tokens
        elif mode == "2":
            tokens_to_use = [random.choice(self.valid_tokens)]

        self.display_menu()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" THIS WILL ADD REACTIONS REPEATEDLY ")))
        time.sleep(2)

        confirm = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nStart Spammer? (y/n): "))).lower()

        if confirm != 'y':
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\n[!] OPERATION CANCELLED [!]\n")))
            return

        self.session = aiohttp.ClientSession()

        try:
            if mode == "1":
                await self.mass_reaction(channel_id, delay, tokens_to_use)
            elif mode == "2":
                await self.solo_reaction(channel_id, delay)
            elif mode == "3":
                await self.mass_reaction(channel_id, delay, tokens_to_use)
        except KeyboardInterrupt:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\n[!] SPAMMER STOPPED BY USER [!]\n")))
        finally:
            await self.session.close()

if __name__ == "__main__":
    spammer = UltimateReactionSpammer()
    asyncio.run(spammer.run())
