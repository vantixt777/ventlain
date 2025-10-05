import discord
import asyncio
import os
import sys
from pystyle import Colors, Colorate, Center

class VoiceChannelJoiner:
    def __init__(self):
        self.tokens = []
        self.channel_id = None
        self.banner = r"""
 ▄█    █▄   ▄██████▄   ▄█   ▄████████    ▄████████ 
███    ███ ███    ███ ███  ███    ███   ███    ███ 
███    ███ ███    ███ ███▌ ███    █▀    ███    █▀  
███    ███ ███    ███ ███▌ ███         ▄███▄▄▄     
███    ███ ███    ███ ███▌ ███        ▀▀███▀▀▀     
███    ███ ███    ███ ███  ███    █▄    ███    █▄  
███    ███ ███    ███ ███  ███    ███   ███    ███ 
 ▀██████▀   ▀██████▀  █▀   ████████▀    ██████████ 
                                                   
                                                                               
        """
        self.intents = discord.Intents.default()
        self.intents.guilds = True          
        self.intents.voice_states = True    
        self.intents.members = True


    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("by vantixt")))
        print("\n")
        print("\n") 


    def load_tokens(self):
        token_file = "tokens.txt"
        if not os.path.exists(token_file):
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] Token file '{token_file}' not found [!]")))
            return False

        with open(token_file, "r", encoding="utf-8") as f:
            self.tokens = [line.strip() for line in f.readlines() if line.strip()]

        if not self.tokens:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] No tokens found in tokens.txt. Make sure valid user tokens are included. [!]")))
            return False

        return True

    def get_channel_id(self):
        try:
            self.channel_id = int(input(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(" Enter the Channel ID to join: "))))
            return self.channel_id
        except ValueError:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Invalid Channel ID. Please enter a numeric ID. [!]")))
            return None

    async def _run_client(self, token):
        """Internal method to run a single Discord client (user token)."""
        client = discord.Client(intents=self.intents)

        @client.event
        async def on_ready():
            print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(f"[+] Logged in as {client.user} [+]")))
            try:
                channel = client.get_channel(self.channel_id)
                
                if not channel:
                    print(Colorate.Horizontal(Colors.yellow, Center.XCenter(f"[*] Channel {self.channel_id} not in cache, attempting to fetch for {client.user} [*]")))
                    try:
                        channel = await client.fetch_channel(self.channel_id)
                    except discord.NotFound:
                        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] Channel with ID {self.channel_id} not found or inaccessible for {client.user} [-]")))
                        await client.close()
                        return
                    except discord.Forbidden:
                        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] No permission to view or fetch channel with ID {self.channel_id} for {client.user} [-]")))
                        await client.close()
                        return
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] Error fetching channel for {client.user}: {type(e).__name__}: {e} [-]")))
                        await client.close()
                        return

                if isinstance(channel, discord.VoiceChannel):
                    if client.voice_clients:
                        for vc in client.voice_clients:
                            if vc.channel.id == self.channel_id:
                                print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"[*] {client.user} is already in {channel.name} [*]")))
                                return 
                            await vc.disconnect()
                            print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"[*] {client.user} has left the previous voice channel [*]")))
                    
                    try:
                        voice_client = await channel.connect(reconnect=True, timeout=60)
                        print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(f"[+] {client.user} has joined voice channel: {channel.name} ({channel.guild.name}) [+]")))
                    except asyncio.TimeoutError:
                        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] Timeout while connecting to channel {channel.name} for {client.user}. Maybe no slot available or network issue. [-]")))
                        await client.close()
                    except discord.Forbidden:
                        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] {client.user} does not have permission to join {channel.name} (Forbidden). [-]")))
                        await client.close()
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] Unexpected error joining voice channel for {client.user}: {type(e).__name__}: {e} [-]")))
                        await client.close()

                else:
                    print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] Channel {self.channel_id} is not a voice channel for {client.user} [-]")))
                    await client.close()
            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] Error in on_ready for {client.user}: {type(e).__name__}: {e} [-]")))
                await client.close()

        try:
            await client.start(token) 
        except discord.LoginFailure:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] LoginFailure: Token {token[:25]}... is invalid or incorrectly formatted. Check the token and ensure it is a user token. [-]")))
        except discord.HTTPException as e:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] HTTP error with token {token[:25]}...: {type(e).__name__}: {e} [-]")))
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[-] An unexpected error occurred with token {token[:25]}...: {type(e).__name__}: {e} [-]")))
        finally:
            if not client.is_closed():
                await client.close()
                print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"[*] Client for {token[:25]}... closed cleanly. [*]")))


    async def join_voice_channel(self):
        self.display_menu() 
        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"[*] {len(self.tokens)} Tokens loaded [*]")))

        tasks = []
        if not self.tokens:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] No tokens found to join. Please check tokens.txt. [!]")))
            return

        for token in self.tokens:
            tasks.append(asyncio.create_task(self._run_client(token)))
        
        await asyncio.gather(*tasks, return_exceptions=True)

        print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter("[+] All join attempts completed. [+]")))


    def run(self):
        self.display_menu() 
        if not self.load_tokens():
            sys.exit(1)

        if self.get_channel_id() is None:
            sys.exit(1)

        asyncio.run(self.join_voice_channel())

if __name__ == "__main__":
    joiner = VoiceChannelJoiner()
    joiner.run()