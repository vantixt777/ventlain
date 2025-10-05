import discord
import asyncio
import aiohttp
import time
import os
from pystyle import Colors, Colorate, Center

class AllChannelDeleter:
    def __init__(self):
        self.banner = r"""
████████▄     ▄████████  ▄█          ▄████████     ███        ▄████████    ▄████████ 
███   ▀███   ███    ███ ███         ███    ███ ▀█████████▄   ███    ███   ███    ███ 
███    ███   ███    █▀  ███         ███    █▀     ▀███▀▀██   ███    █▀    ███    ███ 
███    ███  ▄███▄▄▄     ███        ▄███▄▄▄         ███   ▀  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███    ███ ▀▀███▀▀▀     ███       ▀▀███▀▀▀         ███     ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███    ███   ███    █▄  ███         ███    █▄      ███       ███    █▄  ▀███████████ 
███   ▄███   ███    ███ ███▌    ▄   ███    ███     ███       ███    ███   ███    ███ 
████████▀    ██████████ █████▄▄██   ██████████    ▄████▀     ██████████   ███    ███ 
                        ▀                                                 ███    ███                              
        """
        self.token = ""
        self.guild_id = ""
        self.session = None
        self.max_retries = 5

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("Channel Deleter by vantixt")))
        print("\n")

    async def delete_single_channel(self, channel_id: int, headers: dict, channel_name: str = "Unknown"):
        """
        Deletes a single channel using the Discord API.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                async with self.session.delete(
                    f"https://discord.com/api/v9/channels/{channel_id}",
                    headers=headers
                ) as resp:
                    if resp.status == 200:
                        print(Colorate.Horizontal(Colors.green_to_white,
                                                  Center.XCenter(f"[+] Deleted channel: {channel_name} ({channel_id}) [+]")))
                        return True
                    elif resp.status == 429:
                        response_json = await resp.json()
                        retry_after = response_json.get('retry_after', 1)
                        print(Colorate.Horizontal(Colors.yellow_to_red,
                                                  Center.XCenter(f"[!] Rate limited on channel deletion for {channel_name}! Retrying in {retry_after:.2f} seconds... [!]")))
                        await asyncio.sleep(retry_after)
                        retries += 1
                        continue 
                    elif resp.status == 403:
                        print(Colorate.Horizontal(Colors.red_to_white,
                                                  Center.XCenter(f"[!] Error deleting channel {channel_name}: Missing permissions (403 Forbidden) [!]")))
                        return False
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white,
                                                  Center.XCenter(f"[!] Error deleting channel {channel_name} (Status: {resp.status}, Response: {await resp.text()}) [!]")))
                        return False
            except aiohttp.ClientError as e:
                print(Colorate.Horizontal(Colors.red_to_white,
                                          Center.XCenter(f"[!] Network error deleting channel {channel_name}: {e}. Retrying... [!]")))
                retries += 1
                await asyncio.sleep(2) 
            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_white,
                                          Center.XCenter(f"[!] Unexpected error deleting channel {channel_name}: {str(e)} [!]")))
                return False
        print(Colorate.Horizontal(Colors.red_to_white,
                                  Center.XCenter(f"[!] Failed to delete channel {channel_name} after {self.max_retries} retries. [!]")))
        return False


    async def delete_all_channels(self, headers: dict):
        """
        Fetches all channels from the target guild and attempts to delete them.
        """
        try:
            async with self.session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/channels", headers=headers) as resp:
                if resp.status == 200:
                    channels_data = await resp.json()
                elif resp.status == 403:
                    print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] Bot lacks permissions to fetch channels for guild ID: {self.guild_id}. Ensure 'Manage Channels' permission. [!]")))
                    return
                elif resp.status == 404:
                    print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] Guild with ID: {self.guild_id} not found or bot is not in it. [!]")))
                    return
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] Error fetching channels (Status: {resp.status}, Response: {await resp.text()}) [!]")))
                    return
        except aiohttp.ClientError as e:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] Network error fetching channels: {e} [!]")))
            return
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] Unexpected error fetching channels: {str(e)} [!]")))
            return

        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"[i] Found {len(channels_data)} channels. Attempting to delete... [i]")))

        if not channels_data:
            print(Colorate.Horizontal(Colors.green_to_yellow, Center.XCenter("[!] No channels found to delete. [!]")))
            return

        confirm_prompt = Colorate.Horizontal(Colors.red_to_white,
                                             Center.XCenter("\nWARNING: THIS WILL DELETE ALL CHANNELS! ARE YOU SURE? (y/n): "))
        confirm = input(confirm_prompt).lower()

        if confirm == 'y':
            tasks = []

            for channel_data in channels_data:
                channel_id = int(channel_data['id'])
                channel_name = channel_data.get('name', 'Unnamed Channel')
                tasks.append(self.delete_single_channel(channel_id, headers, channel_name))

            results = await asyncio.gather(*tasks)
            deleted_count = sum(results)
            print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(f"[+] Successfully deleted {deleted_count} channels. [+]")))
        else:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Channel deletion cancelled. [!]")))

    async def run(self):
        """
        Initializes the aiohttp session and starts the deletion process.
        """
       
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        
        print(Colorate.Horizontal(Colors.red_to_white,
                                  Center.XCenter("\n[!] STARTING POWERFUL ALL CHANNEL DELETION [!]\n")))
        await self.delete_all_channels(headers)
        print(Colorate.Horizontal(Colors.green_to_white,
                                  Center.XCenter("\n[+] ALL CHANNEL DELETION COMPLETED [+]")))
        await self.session.close()

    def get_inputs(self):
        """
        Gets bot token and guild ID from the user and initiates the process.
        """
        self.display_menu()
        token_prompt = Colorate.Horizontal(Colors.red_to_white,
                                            Center.XCenter(" Bot Token: "))
        self.token = input(token_prompt).strip()
        while not self.token:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Bot Token cannot be empty!")))
            self.token = input(token_prompt).strip()


        self.display_menu()
        guild_id_prompt = Colorate.Horizontal(Colors.red_to_white,
                                              Center.XCenter(" Server ID: "))
        self.guild_id = input(guild_id_prompt).strip()
        while not self.guild_id.isdigit():
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Server ID must be a number!")))
            self.guild_id = input(guild_id_prompt).strip()


        self.display_menu()
        warning_message = Colorate.Horizontal(Colors.red_to_white,
                                              Center.XCenter("WARNING: THIS WILL DELETE ALL CHANNELS! "))
        print(warning_message)
        time.sleep(2)

        confirm_prompt = Colorate.Horizontal(Colors.red_to_white,
                                              Center.XCenter("\nSTART ALL CHANNEL DELETION? (y/n): "))
        confirm = input(confirm_prompt).lower()

        if confirm == 'y':
            try:
                asyncio.run(self.run())
            except aiohttp.ClientConnectorError as e:
                print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"\n[!] Connection Error: {e}. Check your internet connection or Discord API status. [!]")))
            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"\n[!] An unexpected error occurred during execution: {e} [!]")))
        else:
            cancelled_message = Colorate.Horizontal(Colors.red_to_white,
                                                     Center.XCenter("\n[!] OPERATION CANCELLED [!]\n"))
            print(cancelled_message)

if __name__ == "__main__":
    deleter = AllChannelDeleter()
    deleter.get_inputs()
    exit_message = Colorate.Horizontal(Colors.red_to_white,
                                        Center.XCenter("\nPress ENTER to exit..."))
    input(exit_message)