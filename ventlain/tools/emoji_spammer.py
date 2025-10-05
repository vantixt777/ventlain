import discord
from discord.ext import commands
import os
import random
import time
import asyncio
from pystyle import Colors, Colorate, Center

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

class EmojiSpammer:
    def __init__(self):
        self.banner = r"""
   ▄████████   ▄▄▄▄███▄▄▄▄    ▄██████▄       ▄█  ▄█  
  ███    ███ ▄██▀▀▀███▀▀▀██▄ ███    ███     ███ ███  
  ███    █▀  ███   ███   ███ ███    ███     ███ ███▌ 
 ▄███▄▄▄     ███   ███   ███ ███    ███     ███ ███▌ 
▀▀███▀▀▀     ███   ███   ███ ███    ███     ███ ███▌ 
  ███    █▄  ███   ███   ███ ███    ███     ███ ███  
  ███    ███ ███   ███   ███ ███    ███     ███ ███  
  ██████████  ▀█   ███   █▀   ▀██████▀  █▄ ▄███ █▀   
                                        ▀▀▀▀▀▀       
        """

        self.emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂", "🙃", "😉", "😊", "😇", "🥰", "😍", "🤩", "😘", "😗", "😙", "😚", "😋", "😛", "😝", "🤗", "🤔", "🤨", "😐", "😑", "😶", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣", "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "😈", "👿", "💀", "", "👽", "👾", "🤖", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿"]

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("vantixt emoji spammer")))
        print("\n")

    async def send_emojis(self, ctx, count: int = 50):
        for channel in ctx.guild.text_channels:
            for _ in range(count):
                emoji = random.choice(self.emojis)
                await channel.send(emoji)

    async def get_inputs(self):
        self.display_menu()
        bot_token = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Bot Token: "))).strip()

        self.display_menu()
        guild_id = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Server ID: "))).strip()

        self.display_menu()
        count = int(input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Number of Emojis (Default: 50): ")) or "50"))

        self.display_menu()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" THIS WILL SEND EMOJIS TO ALL CHANNELS IN THE SERVER! ")))
        time.sleep(2)

        confirm = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nStart Emoji Spam Wave? (y/n): "))).lower()

        if confirm == 'y':
            bot.run(bot_token)
            guild = bot.get_guild(int(guild_id))
            if guild:
                ctx = await bot.get_context(guild.text_channels[0].last_message) if guild.text_channels else None
                if ctx:
                    await self.send_emojis(ctx, count)
            else:
                print(Colorate.Horizontal(Colors.red_to_white,
                    Center.XCenter("\n[!] INVALID SERVER ID [!]\n")))
        else:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\n[!] OPERATION ABORTED [!]\n")))

if __name__ == "__main__":
    spammer = EmojiSpammer()
    asyncio.run(spammer.get_inputs())
    input(Colorate.Horizontal(Colors.red_to_white,
        Center.XCenter("\nPress ENTER to exit...")))
