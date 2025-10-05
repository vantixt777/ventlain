import discord
import asyncio
import os
import random
from pystyle import Colors, Colorate, Center

class UltimateFriendSpammer:
    def __init__(self):
        self.banner = r"""
    ███████╗██████╗ ██╗███████╗███╗   ██╗██████╗     ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗
    ██╔════╝██╔══██╗██║██╔════╝████╗  ██║██╔══██╗    ██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝
    █████╗  ██████╔╝██║█████╗  ██╔██╗ ██║██║  ██║    ██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ██████╔╝███████╗
    ██╔══╝  ██╔══██╗██║██╔══╝  ██║╚██╗██║██║  ██║    ██╔══██╗██╔══╝  ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║
    ██║     ██║  ██║██║███████╗██║ ╚████║██████╔╝    ██║  ██║███████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████║
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝
        """
        self.tokens = []
        self.selected_tokens = []
        self.delay = 1.5
        self.stats = {
            'sent': 0,
            'failed': 0,
            'rate_limited': 0
        }

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("by vantixt"))) 
        print("\n")

    def load_tokens(self):
        token_file = "tokens.txt"
        if not os.path.exists(token_file):
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter(f"[!] Token file '{token_file}' not found [!]")))
            return False
        
        with open(token_file, "r", encoding="utf-8") as f:
            self.tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not self.tokens:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("[!] No valid tokens found in tokens.txt [!]")))
            return False
        
        return True

    def select_tokens(self):
        self.display_menu()
        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter("Available tokens:")))
        for i, token in enumerate(self.tokens, 1):
            print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"{i}. {token[:25]}...")))

        selections = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nEnter token numbers to use (e.g., 1,3,5 or 1-5): "))).strip()

        selected_indices = set()
        for part in selections.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                selected_indices.update(range(start, end + 1))
            else:
                selected_indices.add(int(part))

        self.selected_tokens = [self.tokens[i-1] for i in selected_indices if 0 < i <= len(self.tokens)]

        if not self.selected_tokens:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("[!] No tokens selected [!]")))
            return False

        return True

    async def process_token(self, token):
        intents = discord.Intents.default()
        intents.members = True
        
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(Colorate.Horizontal(Colors.green_to_white,
                Center.XCenter(f"[+] Logged in as: {client.user} [+]")))
            
            for guild in client.guilds:
                print(Colorate.Horizontal(Colors.blue_to_white,
                    Center.XCenter(f"[*] Scanning server: {guild.name} [*]")))
                
                for member in guild.members:
                    if member != client.user and not member.bot:
                        try:
                            await member.send(f"Hey {member.name}! Let's be friends?")
                            print(Colorate.Horizontal(Colors.green_to_white,
                                Center.XCenter(f"[+] Request sent to: {member.name} [+]")))
                            self.stats['sent'] += 1
                        except discord.Forbidden:
                            print(Colorate.Horizontal(Colors.yellow_to_white,
                                Center.XCenter(f"[!] Cannot DM: {member.name} [!]")))
                            self.stats['failed'] += 1
                        except Exception as e:
                            print(Colorate.Horizontal(Colors.red_to_white,
                                Center.XCenter(f"[-] Error with {member.name}: {str(e)} [-]")))
                            self.stats['failed'] += 1
                        
                        await asyncio.sleep(random.uniform(2.0, 5.0))
            
            await client.close()

        try:
            await client.start(token)  
        except discord.LoginFailure:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter(f"[-] Invalid token: {token[:25]}... [-]")))
            self.stats['failed'] += 1
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter(f"[-] Error with token {token[:25]}...: {str(e)} [-]")))

    async def run_spammer(self):
        if not self.load_tokens():
            return

        if not self.select_tokens():
            return

        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\n[!] FRIEND REQUEST SPAMMER ACTIVATED [!]\n")))
        
        tasks = [self.process_token(token) for token in self.selected_tokens]
        await asyncio.gather(*tasks)
        
        print(Colorate.Horizontal(Colors.green_to_white,
            Center.XCenter("\n[+] SPAMMING COMPLETE [+]")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"Requests Sent: {self.stats['sent']} | Failed: {self.stats['failed']}")))

    def run(self):
        asyncio.run(self.run_spammer())
        input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nPress ENTER to exit...")))

if __name__ == "__main__":
    spammer = UltimateFriendSpammer()
    spammer.run()