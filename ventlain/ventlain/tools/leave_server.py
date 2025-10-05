import asyncio
import aiohttp
import os
import random
import time
import re
from pystyle import Colors, Colorate, Center

class UltimateServerLeaver:
    def __init__(self):
        self.banner = r"""
 ▄█          ▄████████    ▄████████  ▄█    █▄     ▄████████    ▄████████ 
███         ███    ███   ███    ███ ███    ███   ███    ███   ███    ███ 
███         ███    █▀    ███    ███ ███    ███   ███    █▀    ███    ███ 
███        ▄███▄▄▄       ███    ███ ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███       ▀▀███▀▀▀     ▀███████████ ███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███         ███    █▄    ███    ███ ███    ███   ███    █▄  ▀███████████ 
███▌    ▄   ███    ███   ███    ███ ███    ███   ███    ███   ███    ███ 
█████▄▄██   ██████████   ███    █▀   ▀██████▀    ██████████   ███    ███ 
▀                                                             ███    ███ 
        """
        self.tokens = []
        self.valid_tokens = []
        self.delay = 0.5
        self.rate_limit = 3
        self.random_delay = (0.3, 1.5)
        self.session = None
        self.stats = {
            'left': 0,
            'failed': 0,
            'protected': 0
        }

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("Leaver by vantixt")))
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

    async def get_guilds(self, token):
        headers = {'Authorization': token}
        try:
            async with self.session.get(
                'https://discord.com/api/v9/users/@me/guilds',
                headers=headers
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                return []
        except:
            return []

    async def leave_guild(self, token, guild_id):
        headers = {'Authorization': token}

        # Random delay to avoid detection
        await asyncio.sleep(random.uniform(*self.random_delay))

        try:
            async with self.session.delete(
                f'https://discord.com/api/v9/users/@me/guilds/{guild_id}',
                headers=headers
            ) as resp:
                if resp.status == 204:
                    self.stats['left'] += 1
                    return True
                elif resp.status == 400:
                    data = await resp.json()
                    if data.get('message') == "You are the owner of this guild":
                        self.stats['protected'] += 1
                        return False
                self.stats['failed'] += 1
                return False
        except:
            self.stats['failed'] += 1
            return False

    async def process_token(self, token):
        guilds = await self.get_guilds(token)
        if not guilds:
            print(Colorate.Horizontal(Colors.blue_to_white,
                Center.XCenter(f"[*] No servers found for token: {token[:25]}... [*]")))
            return

        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"[*] Processing {len(guilds)} servers for token: {token[:25]}... [*]")))

        for guild in guilds:
            guild_id = guild['id']
            guild_name = guild.get('name', 'Unknown Server')

            result = await self.leave_guild(token, guild_id)
            if result:
                print(Colorate.Horizontal(Colors.green_to_white,
                    Center.XCenter(f"[+] Left server: {guild_name} [+]")))
            elif guild.get('owner', False):
                print(Colorate.Horizontal(Colors.yellow_to_white,
                    Center.XCenter(f"[!] Can't leave owned server: {guild_name} [!]")))
            else:
                print(Colorate.Horizontal(Colors.red_to_white,
                    Center.XCenter(f"[-] Failed to leave: {guild_name} [-]")))

            await asyncio.sleep(self.delay)

    async def run_leaver(self):
        if not self.load_tokens():
            return

        self.display_menu()
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"[*] Loaded {len(self.valid_tokens)} valid tokens [*]")))

        # Token selection options
        print("\n" + Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("1. Use all valid tokens")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("2. Select specific tokens")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("3. Use first N tokens")))

        choice = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nSelect option (1-3): "))).strip()

        tokens_to_use = []
        if choice == "1":
            tokens_to_use = self.valid_tokens
        elif choice == "2":
            self.display_menu()
            print(Colorate.Horizontal(Colors.blue_to_white,
                Center.XCenter("Available tokens:")))
            for i, token in enumerate(self.valid_tokens, 1):
                print(Colorate.Horizontal(Colors.blue_to_white,
                    Center.XCenter(f"{i}. {token[:25]}...")))
            selections = input(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\nEnter token numbers to use (e.g., 1,3,5 or 1-5): "))).strip()

            # Parse selections
            selected_indices = set()
            for part in selections.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    selected_indices.update(range(start, end + 1))
                else:
                    selected_indices.add(int(part))

            tokens_to_use = [self.valid_tokens[i-1] for i in selected_indices if 0 < i <= len(self.valid_tokens)]
        elif choice == "3":
            self.display_menu()
            n = input(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter(f"Enter number of tokens to use (1-{len(self.valid_tokens)}): "))).strip()
            n = min(int(n), len(self.valid_tokens)) if n.isdigit() else len(self.valid_tokens)
            tokens_to_use = self.valid_tokens[:n]
        else:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("[!] Invalid selection [!]")))
            return

        if not tokens_to_use:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("[!] No tokens selected [!]")))
            return

        self.display_menu()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(f"⚠️ WARNING: THIS WILL LEAVE ALL SERVERS ON {len(tokens_to_use)} SELECTED TOKENS! ⚠️")))
        time.sleep(2)

        confirm = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nStart Server Leaver? (y/n): "))).lower()

        if confirm != 'y':
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\n[!] OPERATION CANCELLED [!]\n")))
            return

        self.session = aiohttp.ClientSession()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\n[!] SERVER LEAVER ACTIVATED! [!]\n")))

        # Run with rate limiting
        semaphore = asyncio.Semaphore(self.rate_limit)
        async def limited_process(token):
            async with semaphore:
                return await self.process_token(token)

        await asyncio.gather(*[limited_process(token) for token in tokens_to_use])
        await self.session.close()

        print(Colorate.Horizontal(Colors.green_to_white,
            Center.XCenter(f"\n[+] SERVER LEAVER COMPLETE [+]")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"Left: {self.stats['left']} | Failed: {self.stats['failed']} | Protected: {self.stats['protected']}")))

if __name__ == "__main__":
    leaver = UltimateServerLeaver()
    asyncio.run(leaver.run_leaver())
    input(Colorate.Horizontal(Colors.red_to_white,
        Center.XCenter("\nPress ENTER to exit...")))