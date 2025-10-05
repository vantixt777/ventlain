import asyncio
import aiohttp
import os
import random
import re
import time
import json
from pystyle import Colors, Colorate, Center

class UltimateMessageSpammer:
    def __init__(self):
        self.banner = r"""
   ▄████████    ▄███████▄    ▄████████   ▄▄▄▄███▄▄▄▄     ▄▄▄▄███▄▄▄▄      ▄████████    ▄████████
  ███    ███   ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄ ▄██▀▀▀███▀▀▀██▄   ███    ███   ███    ███
  ███    █▀    ███    ███   ███    ███ ███   ███   ███ ███   ███   ███   ███    █▀    ███    ███
  ███          ███    ███   ███    ███ ███   ███   ███ ███   ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▀
▀███████████ ▀█████████▀  ▀███████████ ███   ███   ███ ███   ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀
         ███   ███          ███    ███ ███   ███   ███ ███   ███   ███   ███    █▄  ▀███████████
   ▄█    ███   ███          ███    ███ ███   ███   ███ ███   ███   ███   ███    ███   ███    ███
 ▄████████▀   ▄████▀        ███    █▀   ▀█   ███   █▀   ▀█   ███   █▀    ██████████   ███    ███

                                       by vantixt

                                                                                      

"""
        self.tokens = []
        self.valid_tokens = []
        self.session = None
        self.stats = {
            'sent': 0,
            'failed': 0,
            'rate_limited': 0
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
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] Token file '{token_file}' not found [!]")))
            return False
        with open(token_file, "r", encoding="utf-8") as f:
            raw_tokens = f.readlines()
        self.tokens = [self.clean_token(t) for t in raw_tokens if self.clean_token(t)]
        self.valid_tokens = [t for t in self.tokens if self.validate_token(t)]
        if not self.valid_tokens:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] No valid tokens found in tokens.txt [!]")))
            return False
        return True

    def validate_token(self, token):
        return len(token) >= 59 and "." in token

    def generate_random_suffix(self):
        suffixes = ["--xx", "--fz", "--dz", "--zz", "--yx", "--lk", "--op", "--mn", "--bv", "--qw"]
        return random.choice(suffixes)

    async def send_message(self, token, channel_id, message, delay):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        payload = {'content': f"{message}{self.generate_random_suffix()}"}

        try:
            async with self.session.post(
                f'https://discord.com/api/v9/channels/{channel_id}/messages',
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                response_text = await resp.text()
                if resp.status == 200:
                    self.stats['sent'] += 1
                    return True
                elif resp.status == 429:
                    retry_after = float((await resp.json()).get('retry_after', 1)) / 1000
                    self.stats['rate_limited'] += 1
                    print(f"Rate limited. Retry after {retry_after} seconds.")
                    await asyncio.sleep(retry_after)
                    return False
                else:
                    self.stats['failed'] += 1
                    print(f"Failed to send message. Status code: {resp.status}, Response: {response_text}")
                    return False
        except Exception as e:
            self.stats['failed'] += 1
            print(f"Exception occurred: {e}")
            return False
        finally:
            await asyncio.sleep(delay)

    async def mass_message(self, channel_id, message_base, delay, tokens):
        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"\n[!] MASS MESSAGE MODE ACTIVATED - {len(tokens)} TOKENS PARTICIPATING [!]\n")))
        messages = self.generate_variations(message_base, len(tokens) * 3)
        semaphore = asyncio.Semaphore(10)
        async def process_token(token, msg_queue):
            async with semaphore:
                while True:
                    msg = msg_queue.pop(0) if msg_queue else message_base
                    if await self.send_message(token, channel_id, msg, delay):
                        print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(f"[+] Message sent with token: {token[:25]}... [+]")))
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] Failed to send with token: {token[:25]}... [-]")))
                    await asyncio.sleep(delay * random.uniform(0.8, 1.2))
        message_queues = [messages[i::len(tokens)] for i in range(len(tokens))]
        await asyncio.gather(*[
            process_token(token, message_queues[i].copy())
            for i, token in enumerate(tokens)
        ])

    async def solo_mode(self, channel_id, message, delay):
        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter("\n[!] SOLO MODE ACTIVATED - SINGLE TOKEN SPAMMING [!]\n")))
        token = random.choice(self.valid_tokens)
        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"[*] Selected token: {token[:25]}... [*]")))
        messages = self.generate_variations(message, 20)
        msg_index = 0
        while True:
            current_msg = messages[msg_index % len(messages)]
            if await self.send_message(token, channel_id, current_msg, delay):
                print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(f"[+] Message sent: {current_msg[:50]}... [+]")))
            else:
                print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[-] Failed to send message [-]")))
            msg_index += 1
            await asyncio.sleep(delay * random.uniform(0.9, 1.1))

    def generate_variations(self, base_message, count):
        variations = set()
        while len(variations) < count:
            variation = base_message
            if random.random() < 0.3:
                variation += random.choice(["!", "?", "~", "...", "!!", "...?"])
            if random.random() < 0.2:
                variation = random.choice(["", "> ", "/ ", "*", "_"]) + variation + random.choice(["", "*", "_"])
            if random.random() < 0.15:
                variation = variation.upper() if random.choice([True, False]) else variation.lower()
            variations.add(variation.strip())
        return list(variations)

    async def run(self):
        if not self.load_tokens():
            return
        self.display_menu()
        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"[*] Loaded {len(self.valid_tokens)} valid tokens [*]")))
        print("\n" + Colorate.Horizontal(Colors.blue_to_white, Center.XCenter("1. MASS MESSAGE MODE (Multiple tokens spamming)")))
        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter("2. SOLO MODE (Single token spamming)")))
        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter("3. CUSTOM TOKEN MODE (Select specific tokens to spam)")))
        mode = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nSelect mode (1-3): "))).strip()
        if mode not in ["1", "2", "3"]:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\n[!] INVALID SELECTION [!]\n")))
            return
        self.display_menu()
        channel_id = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(" Channel ID to spam: "))).strip()
        message = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(" Base message to spam: "))).strip()
        delay = float(input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(" Delay between messages (seconds): ")) or "0.5"))
        tokens_to_use = []
        if mode == "3":
            self.display_menu()
            print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter("Available tokens:")))
            for i, token in enumerate(self.valid_tokens, 1):
                print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"{i}. {token[:25]}...")))
            selections = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nEnter token numbers to use (e.g., 1,3,5 or 1-5): "))).strip()
            selected_indices = set()
            for part in selections.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    selected_indices.update(range(start, end + 1))
                else:
                    selected_indices.add(int(part))
            tokens_to_use = [self.valid_tokens[i-1] for i in selected_indices if 0 < i <= len(self.valid_tokens)]
            if not tokens_to_use:
                print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] No tokens selected for custom mode [!]")))
                return
        elif mode == "1":
            tokens_to_use = self.valid_tokens
        elif mode == "2":
            tokens_to_use = [random.choice(self.valid_tokens)]
        self.display_menu()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(" WARNING: THIS WILL SEND MESSAGES REPEATEDLY ")))
        time.sleep(2)
        confirm = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nStart Spammer? (y/n): "))).lower()
        if confirm != 'y':
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\n[!] OPERATION CANCELLED [!]\n")))
            return
        self.session = aiohttp.ClientSession()
        try:
            if mode == "1":
                await self.mass_message(channel_id, message, delay, tokens_to_use)
            elif mode == "2":
                await self.solo_mode(channel_id, message, delay)
            elif mode == "3":
                await self.mass_message(channel_id, message, delay, tokens_to_use)
        except KeyboardInterrupt:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\n[!] SPAMMER STOPPED BY USER [!]\n")))
        finally:
            await self.session.close()

if __name__ == "__main__":
    spammer = UltimateMessageSpammer()
    asyncio.run(spammer.run())