import asyncio
import aiohttp
import os
import random
import time
from pystyle import Colors, Colorate, Center

class DiscordWebhookCreator:
    def __init__(self):
        self.banner = r"""
 ▄█     █▄     ▄████████ ▀█████████▄     ▄█    █▄     ▄██████▄   ▄██████▄     ▄█   ▄█▄ 
███     ███   ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███ ▄███▀ 
███     ███   ███    █▀    ███    ███   ███    ███   ███    ███ ███    ███   ███▐██▀   
███     ███  ▄███▄▄▄      ▄███▄▄▄██▀   ▄███▄▄▄▄███▄▄ ███    ███ ███    ███  ▄█████▀    
███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀██▄  ▀▀███▀▀▀▀███▀  ███    ███ ███    ███ ▀▀█████▄    
███     ███   ███    █▄    ███    ██▄   ███    ███   ███    ███ ███    ███   ███▐██▄   
███ ▄█▄ ███   ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███ ▀███▄ 
 ▀███▀███▀    ██████████ ▄█████████▀    ███    █▀     ▀██████▀   ▀██████▀    ███   ▀█▀ 
                                                                             ▀         
        """

        self.token = ""
        self.guild_id = ""
        self.channel_id = ""
        self.delay = 0.5
        self.session = None
        self.webhook_count = 0
        self.max_webhooks = 70

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("by vantixt")))
        print("\n")

    async def create_webhook(self):
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }

        webhook_name = f"Webhook-{random.randint(1000, 9999)}"
        payload = {
            "name": webhook_name
        }

        retry_delay = 1
        while self.webhook_count < self.max_webhooks:
            try:
                async with self.session.post(
                    f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks",
                    headers=headers,
                    json=payload
                ) as resp:
                    if resp.status == 201:
                        webhook_data = await resp.json()
                        self.webhook_count += 1
                        print(Colorate.Horizontal(Colors.red_to_white,
                            Center.XCenter(f"[+] Webhook created: {webhook_data['url']} [+]")))
                    elif resp.status == 429:
                        retry_after = float(resp.headers.get('Retry-After', retry_delay))
                        print(Colorate.Horizontal(Colors.red_to_white,
                            Center.XCenter(f"[!] Rate limited. Retrying after {retry_after} seconds [!]")))
                        await asyncio.sleep(retry_after)
                        retry_delay = min(retry_delay * 2, 60) 
                    elif resp.status == 400:
                        error_data = await resp.json()
                        if error_data.get("code") == 30007:
                            print(Colorate.Horizontal(Colors.red_to_white,
                                Center.XCenter("[!] Maximum number of webhooks reached [!]")))
                            return
                        else:
                            print(Colorate.Horizontal(Colors.red_to_white,
                                Center.XCenter(f"[!] Failed to create webhook (Status {resp.status}): {error_data} [!]")))
                            await asyncio.sleep(self.delay)
                    else:
                        error_data = await resp.text()
                        print(Colorate.Horizontal(Colors.red_to_white,
                            Center.XCenter(f"[!] Failed to create webhook (Status {resp.status}): {error_data} [!]")))
                        await asyncio.sleep(self.delay)
            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_white,
                    Center.XCenter(f"[!] Error creating webhook: {str(e)} [!]")))
                await asyncio.sleep(self.delay)

    async def run(self):
        self.session = aiohttp.ClientSession()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\n[!] WEBHOOK CREATION WAVE INCOMING! [!]\n")))

        await self.create_webhook()

        await self.session.close()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(f"\n[+] WEBHOOK CREATION COMPLETED! {self.webhook_count} WEBHOOKS CREATED! [+]")))

    def get_inputs(self):
        self.display_menu()
        self.token = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Bot Token: "))).strip()

        self.display_menu()
        self.guild_id = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Server ID: "))).strip()
        self.display_menu()
        self.channel_id = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Channel ID: "))).strip()

        self.display_menu()
        self.delay = float(input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("⏱ Delay Between Creations (Default: 0.5): ")) or "0.5"))

        self.display_menu()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" WARNING THIS WILL CREATE WEBHOOKS IN THE CHANNEL! ")))
        time.sleep(2)

        confirm = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nStart Webhook Creation Wave? (y/n): "))).lower()

        if confirm == 'y':
            asyncio.run(self.run())
        else:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\n[!] OPERATION ABORTED [!]\n")))

if __name__ == "__main__":
    creator = DiscordWebhookCreator()
    creator.get_inputs()
    input(Colorate.Horizontal(Colors.red_to_white,
        Center.XCenter("\nPress ENTER to exit...")))
