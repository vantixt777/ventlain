import discord
import asyncio
import aiohttp
import time
import random
import os
from pystyle import Colors, Colorate, Center

class PowerfulChannelCreatorAndSpammer:
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
                                                                                      ███    ███ 
                                        by vantixt
          """
        self.token = ""
        self.guild_id = ""
        self.channel_name_prefix = "nuked"
        self.message = "@everyone GET NUKED"
        self.channel_count = 50
        self.spam_amount = 3  
        self.create_concurrency = 20
        self.spam_concurrency_per_channel = 5
        self.initial_delay = 0.2
        self.max_retries = 5
        self.session = None

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("rape the server with channels")))
        print("\n")

    async def create_single_channel(self, i, headers):
        payload = {
            "name": f"{self.channel_name_prefix}-{i}",
            "type": 0
        }
        try:
            async with self.session.post(
                f"https://discord.com/api/v9/guilds/{self.guild_id}/channels",
                headers=headers,
                json=payload
            ) as resp:
                if resp.status == 201:
                    channel = await resp.json()
                    channel_id = channel['id']
                    channel_name = channel['name']
                    print(Colorate.Horizontal(Colors.green_to_white,
                                            Center.XCenter(f"[+] Created channel: {channel_name} ({channel_id}) [+]")))
                    asyncio.create_task(self.spam_messages(channel_id, headers))
                    return True
                elif resp.status == 429:
                    retry_after = (await resp.json()).get('retry_after', 1)
                    print(Colorate.Horizontal(Colors.yellow_to_red,
                                            Center.XCenter(f"[!] Rate limited on channel creation! Retrying in {retry_after} seconds (Attempt 1/{self.max_retries})... [!]")))
                    await asyncio.sleep(retry_after)
                    return await self.create_single_channel(i, headers)
                else:
                    print(Colorate.Horizontal(Colors.red_to_white,
                                            Center.XCenter(f"[!] Error creating channel (Status: {resp.status}) [!]")))
                    return False
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white,
                                        Center.XCenter(f"[!] Error creating channel: {str(e)} [!]")))
            return False

    async def create_channels(self, headers):
        semaphore = asyncio.Semaphore(self.create_concurrency)

        async def bounded_create(i):
            async with semaphore:
                return await self.create_single_channel(i, headers)

        tasks = [bounded_create(i) for i in range(self.channel_count)]
        await asyncio.gather(*tasks)
        print(Colorate.Horizontal(Colors.green_to_white,
                                    Center.XCenter(f"[+] Created {self.channel_count} channels [+]")))

    async def send_single_message(self, channel_id, headers, retry=0):
        payload = {
            "content": self.message
        }
        try:
            async with self.session.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=headers,
                json=payload
            ) as resp:
                if resp.status == 200:
                    print(Colorate.Horizontal(Colors.white_to_green,
                                            Center.XCenter(f"[+] Message sent to {channel_id} [+]")))
                    return True
                elif resp.status == 429:
                    retry_after = (await resp.json()).get('retry_after', 1)
                    print(Colorate.Horizontal(Colors.yellow_to_red,
                                            Center.XCenter(f"[!] Rate limited on messages! Retrying in {retry_after} seconds (Attempt {retry+1}/{self.max_retries})... [!]")))
                    await asyncio.sleep(retry_after)
                    return await self.send_single_message(channel_id, headers, retry + 1)
                else:
                    print(Colorate.Horizontal(Colors.red_to_white,
                                            Center.XCenter(f"[!] Error sending message to {channel_id} (Status: {resp.status}) [!]")))
                    return False
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white,
                                        Center.XCenter(f"[!] Error sending message to {channel_id}: {str(e)} [!]")))
            return False

    async def spam_messages(self, channel_id, headers):
        semaphore = asyncio.Semaphore(self.spam_concurrency_per_channel)

        async def bounded_send(i):
            async with semaphore:
                return await self.send_single_message(channel_id, headers)

        tasks = [bounded_send(i) for i in range(self.spam_amount)]
        await asyncio.gather(*tasks)
        await asyncio.sleep(self.initial_delay)

    async def run(self):
        self.session = aiohttp.ClientSession()
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        print(Colorate.Horizontal(Colors.red_to_white,
                                    Center.XCenter("\n[!] STARTING POWERFUL CHANNEL CREATION AND SPAM [!]\n")))
        await self.create_channels(headers)
        print(Colorate.Horizontal(Colors.green_to_white,
                                    Center.XCenter("\n[+] CHANNEL CREATION AND INITIAL SPAM COMPLETED [+]")))
        await self.session.close()

    def get_inputs(self):
        self.display_menu()
        token_prompt = Colorate.Horizontal(Colors.red_to_white,
                                            Center.XCenter(" Bot Token: "))
        self.token = input(token_prompt).strip()

        self.display_menu()
        guild_id_prompt = Colorate.Horizontal(Colors.red_to_white,
                                               Center.XCenter(" Server ID: "))
        self.guild_id = input(guild_id_prompt).strip()

        self.display_menu()
        channel_prefix_prompt = Colorate.Horizontal(Colors.red_to_white,
                                                     Center.XCenter(" Channel Name Prefix (Default: nuked): "))
        self.channel_name_prefix = input(channel_prefix_prompt).strip() or "nuked"

        self.display_menu()
        message_prompt = Colorate.Horizontal(Colors.red_to_white,
                                              Center.XCenter(" Message to Send (Default: @everyone GET NUKED): "))
        self.message = input(message_prompt).strip() or "@everyone GET NUKED"

        self.display_menu()
        channel_count_prompt = Colorate.Horizontal(Colors.red_to_white,
                                                    Center.XCenter(" Number of Channels to Create (Default: 50): "))
        self.channel_count = int(input(channel_count_prompt) or "50")

        self.display_menu()
        spam_amount_prompt = Colorate.Horizontal(Colors.red_to_white,
                                                   Center.XCenter(" Number of Times to Send Message per Channel (Default: 3): "))
        self.spam_amount = int(input(spam_amount_prompt) or "3")

        self.display_menu()
        create_concurrency_prompt = Colorate.Horizontal(Colors.red_to_white,
                                                        Center.XCenter(f" Channel Creation Concurrency (Default: {self.create_concurrency}): "))
        self.create_concurrency = int(input(create_concurrency_prompt) or str(self.create_concurrency))

        self.display_menu()
        spam_concurrency_prompt = Colorate.Horizontal(Colors.red_to_white,
                                                      Center.XCenter(f" Message Spam Concurrency per Channel (Default: {self.spam_concurrency_per_channel}): "))
        self.spam_concurrency_per_channel = int(input(spam_concurrency_prompt) or str(self.spam_concurrency_per_channel))

        self.display_menu()
        warning_message = Colorate.Horizontal(Colors.red_to_white,
                                               Center.XCenter(" WARNING: THIS WILL CREATE AND SPAM CHANNELS! "))
        print(warning_message)
        time.sleep(2)

        confirm_prompt = Colorate.Horizontal(Colors.red_to_white,
                                              Center.XCenter("\nSTART CHANNEL CREATION AND SPAM? (y/n): "))
        confirm = input(confirm_prompt).lower()

        if confirm == 'y':
            asyncio.run(self.run())
        else:
            cancelled_message = Colorate.Horizontal(Colors.red_to_white,
                                                    Center.XCenter("\n[!] OPERATION CANCELLED [!]\n"))
            print(cancelled_message)

if __name__ == "__main__":
    creator_spammer = PowerfulChannelCreatorAndSpammer()
    creator_spammer.get_inputs()
    exit_message = Colorate.Horizontal(Colors.red_to_white,
                                         Center.XCenter("\nPress ENTER to exit..."))
    input(exit_message)