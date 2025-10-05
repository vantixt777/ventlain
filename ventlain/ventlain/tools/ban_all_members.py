import asyncio
import os
import time
from pystyle import Colors, Colorate, Center 
import discord
from discord.ext import commands
from colorama import Fore, Style, init 

init(autoreset=True) 

class UltimateBanHammer:
    def __init__(self):
        self.banner = r"""
▀█████████▄     ▄████████ ███▄▄▄▄   
  ███    ███   ███    ███ ███▀▀▀██▄ 
  ███    ███   ███    ███ ███   ███ 
 ▄███▄▄▄██▀    ███    ███ ███   ███ 
▀▀███▀▀▀██▄  ▀███████████ ███   ███ 
  ███    ██▄   ███    ███ ███   ███ 
  ███    ███   ███    ███ ███   ███ 
▄█████████▀    ███    █▀   ▀█   █▀  
                                    
        """
        self.token = ""
        self.target_guild_id = None 
        self.ban_reason = " by vantixt "
        self.delay_between_bans = 0.5 
        self.bot = None

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("kawaii modus")))
        print("\n")

    async def ban_members(self, guild_id, author_id):
        banned_count = 0
        failed_bans = 0

        guild = self.bot.get_guild(guild_id)
        if not guild:
            print(Fore.RED + f"[!] ERROR: Server with ID {guild_id} not found or the bot is not in it! [!]")
            return 0, 0

        print(Fore.YELLOW + f"\n[!] BAN WAVE STARTING ON SERVER: {guild.name} ({guild.id}) [!]")

        try:
            await guild.chunk_members()
        except discord.HTTPException as e:
            print(Fore.RED + f"[-] ERROR LOADING MEMBERS: {e} [!]")
            print(Fore.RED + "    Ensure that the 'SERVER MEMBERS INTENT' is enabled in the Discord Developer Portal!")
            return 0, 0

        for member in guild.members:
            if member.id == self.bot.user.id:
                print(Fore.BLUE + f"[*] SKIPPING: {member.name} (The bot itself)")
                continue
            if member.id == author_id:
                print(Fore.BLUE + f"[*] SKIPPING: {member.name} (The command issuer)")
                continue

            try:
                await member.ban(reason=self.ban_reason, delete_message_days=7)
                print(Fore.GREEN + f"[+] SUCCESSFULLY BANNED: {member.name} ({member.id})")
                banned_count += 1
                await asyncio.sleep(self.delay_between_bans) 
            except discord.Forbidden:
                print(Fore.RED + f"[-] FAILED (NO PERMISSION TO BAN USER): {member.name} ({member.id})")
                failed_bans += 1
            except discord.HTTPException as e:
                print(Fore.RED + f"[-] ERROR DURING BAN (HTTP EXCEPTION): {member.name} ({member.id}) - {e}")
                failed_bans += 1
            except Exception as e:
                print(Fore.RED + f"[-] UNEXPECTED ERROR DURING BAN: {member.name} ({member.id}) - {e}")
                failed_bans += 1

        print(Fore.YELLOW + f"\n[!] BAN WAVE COMPLETED! BANNED: {banned_count} | FAILED: {failed_bans} [!]")
        return banned_count, failed_bans

    def get_inputs(self):
        self.display_menu()
        self.token = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(" Bot Token: "))).strip()

        self.display_menu()
        while True:
            guild_id_input = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(" Server ID: "))).strip()
            if guild_id_input.isdigit():
                self.target_guild_id = int(guild_id_input)
                break
            else:
                print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Invalid Server ID. Please enter only numbers.")))
                time.sleep(1)
                self.display_menu() 

        self.display_menu()
        delay_input = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"Delay between bans (Default: {self.delay_between_bans} seconds): "))).strip()
        try:
            if delay_input:
                self.delay_between_bans = float(delay_input)
        except ValueError:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Invalid input for delay, using default value.")))
            self.delay_between_bans = 0.5

        self.display_menu()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(" WARNING: THIS WILL BAN EVERY MEMBER ON THE TARGET SERVER! ")))
        time.sleep(2)

        confirm = input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nStart Ban Wave? (y/n): "))).lower()

        if confirm == 'y':
            self.run_bot()
        else:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\n[!] OPERATION CANCELED [!]\n")))
            input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))

    def run_bot(self):
        intents = discord.Intents.default()
        intents.members = True 
        intents.message_content = True 

        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready():
            self.clear()
            self.display_menu()
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[+] BOT IS READY: {self.bot.user.name} ({self.bot.user.id}) [+]")))
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] TYPE `!banall` IN ANY TEXT CHANNEL TO START THE BAN WAVE.")))
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"    The bot will attempt to ban members on the server with ID: {self.target_guild_id}.")))
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("    Ensure the bot has Administrator permissions on this server!")))

        @self.bot.command(name='banall')
        async def banall(ctx):
            target_guild = self.bot.get_guild(self.target_guild_id)

            if not target_guild:
                await ctx.send(Fore.RED + f" Server with ID `{self.target_guild_id}` not found or the bot is not in it! Please check the ID and ensure the bot is on the server.")
                return

            if not ctx.author.guild_permissions.administrator:
                await ctx.send(Fore.RED + "YOU DO NOT HAVE PERMISSION FOR THIS COMMAND! Requires Administrator permission.")
                return

            me_in_target_guild = target_guild.get_member(self.bot.user.id)
            if not me_in_target_guild or not me_in_target_guild.guild_permissions.ban_members:
                await ctx.send(Fore.RED + f" The bot does not have the necessary permissions (`Ban Members`) on the target server (`{target_guild.name}` - ID: `{self.target_guild_id}`) to perform this action. Please grant the bot Administrator permissions on this server.")
                return

            await ctx.send(Fore.YELLOW + f" CONFIRMATION REQUIRED: This will ban ALL members on the server **`{target_guild.name}`** (ID: `{self.target_guild_id}`)! Type 'YES' in the next 10 seconds to proceed.")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() == 'YES'

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await ctx.send(Fore.RED + " Time expired. Ban wave canceled.")
                return
            else:
                await ctx.send(Fore.GREEN + " Confirmed! Starting ban wave...")

            banned_count, failed_bans = await self.ban_members(self.target_guild_id, ctx.author.id)

            await ctx.send(Fore.GREEN + f" **SERVER PURGE COMPLETED FOR {target_guild.name}!** {banned_count} members banned, {failed_bans} failed.")
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"\n[+] SERVER PURGE COMPLETED FOR SERVER: {target_guild.name} [+]")))
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))

        try:
            self.bot.run(self.token)
        except discord.LoginFailure:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\n[!] ERROR: Invalid Bot Token. Please check your token and try again. [!]\n")))
            input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))
        except discord.PrivilegedIntentsRequired as e:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"\n[!] ERROR: {e} [!]\n")))
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("    PLEASE ENABLE 'SERVER MEMBERS INTENT' AND 'MESSAGE CONTENT INTENT' IN THE DISCORD DEVELOPER PORTAL!")))
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("    Go to: https://discord.com/developers/applications/ -> Your Application -> Bot -> 'Privileged Gateway Intents'")))
            input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"\n[!] AN UNEXPECTED ERROR OCCURRED: {e} [!]\n")))
            input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("\nPress ENTER to exit...")))

if __name__ == "__main__":
    ban_hammer = UltimateBanHammer()
    ban_hammer.get_inputs()