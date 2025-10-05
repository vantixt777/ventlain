import asyncio
import aiohttp
import os
import re
import time
from pystyle import Colors, Colorate, Center

class UltimateTokenJoiner:
    def __init__(self):
        self.banner = r"""
     ▄█  ▄██████▄   ▄█  ███▄▄▄▄      ▄████████    ▄████████ 
    ███ ███    ███ ███  ███▀▀▀██▄   ███    ███   ███    ███ 
    ███ ███    ███ ███▌ ███   ███   ███    █▀    ███    ███ 
    ███ ███    ███ ███▌ ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
    ███ ███    ███ ███▌ ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
    ███ ███    ███ ███  ███   ███   ███    █▄  ▀███████████ 
    ███ ███    ███ ███  ███   ███   ███    ███   ███    ███ 
█▄ ▄███  ▀██████▀  █▀    ▀█   █▀    ██████████   ███    ███ 
▀▀▀▀▀▀                                           ███    ███ 
                   by vantixt
                          
          """
        self.tokens = []
        self.valid_tokens = []
        self.invite_code = ""
        self.captcha_api_key = ""
        self.session = None
        self.join_count = 0
        self.success_count = 0
        self.failed_count = 0

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(self.banner)))
        print("\n")
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("token joiner by vantuxt")))
        print("\n")

    def clean_token(self, token):
       
        cleaned = re.sub(r'#.*$', '', token).strip()
       
        cleaned = re.sub(r'[^\x20-\x7E]', '', cleaned)
        return cleaned

    def load_tokens(self):
        token_file = "tokens.txt"
        if not os.path.exists(token_file):
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter(f"[!] Token file '{token_file}' not found [!]")))
            return False

        with open(token_file, "r", encoding="utf-8") as f:
            raw_tokens = f.readlines()

        self.tokens = [self.clean_token(t) for t in raw_tokens if self.clean_token(t)]
        self.valid_tokens = [t for t in self.tokens if self.validate_token(t)]

        if not self.valid_tokens:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("[!] No valid tokens found in tokens.txt [!]")))
            return False

        return True

    def validate_token(self, token):
        # Basic token validation
        return len(token) >= 59 and "." in token

    async def solve_captcha(self, captcha_type="hcaptcha"):
        if captcha_type == "hcaptcha":
          
            return "CAPTCHA_SOLUTION_TOKEN"
        else:
          
            return "CAPTCHA_SOLUTION_TOKEN"

    async def join_with_token(self, token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        try:
            async with self.session.get(
                f"https://discord.com/api/v9/invites/{self.invite_code}",
                headers=headers
            ) as resp:
                if resp.status == 200:
                    server_info = await resp.json()
                    server_name = server_info.get('guild', {}).get('name', "Unknown Server")
                else:
                    server_name = "Unknown Server"
        except:
            server_name = "Unknown Server"

        try:
            async with self.session.post(
                f"https://discord.com/api/v9/invites/{self.invite_code}",
                headers=headers,
                json={}
            ) as resp:
                if resp.status == 200:
                    print(Colorate.Horizontal(Colors.green_to_white,
                        Center.XCenter(f"[+] Successfully joined with token: {token[:25]}... [+]")))
                    self.success_count += 1
                    return True

                response_data = await resp.json()
                if resp.status == 400 and response_data.get('captcha_key'):
                    captcha_key = await self.solve_captcha()
                    payload = {"captcha_key": captcha_key}

                    async with self.session.post(
                        f"https://discord.com/api/v9/invites/{self.invite_code}",
                        headers=headers,
                        json=payload
                    ) as captcha_resp:
                        if captcha_resp.status == 200:
                            print(Colorate.Horizontal(Colors.green_to_white,
                                Center.XCenter(f"[+] Successfully joined with captcha: {token[:25]}... [+]")))
                            self.success_count += 1
                            return True
                        else:
                            error_data = await captcha_resp.text()
                            print(Colorate.Horizontal(Colors.red_to_white,
                                Center.XCenter(f"[!] Failed to join with captcha (Status {captcha_resp.status}): {token[:25]}... [!]")))
                            self.failed_count += 1
                            return False
                else:
                    error_data = await resp.text()
                    print(Colorate.Horizontal(Colors.red_to_white,
                        Center.XCenter(f"[!] Failed to join (Status {resp.status}): {token[:25]}... [!]")))
                    self.failed_count += 1
                    return False
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter(f"[!] Error with token {token[:25]}...: {str(e)} [!]")))
            self.failed_count += 1
            return False

    async def run_joiner(self):
        if not self.load_tokens():
            return

        self.display_menu()
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"[*] Loaded {len(self.valid_tokens)} valid tokens [*]")))

        # Token selection options
        print("\n" + Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("1. Use all valid tokens")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("2. Select specific tokens")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter("3. Use first N tokens")))

        choice = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nSelect option (1-3): "))).strip()

        tokens_to_use = []
        if choice == "1":
            tokens_to_use = self.valid_tokens
        elif choice == "2":
            self.display_menu()
            print(Colorate.Horizontal(Colors.blue_to_white,
                Center.XCenter("Available tokens:")))
            for i, token in enumerate(self.valid_tokens, 1):
                print(Colorate.Horizontal(Colors.blue_to_white,
                    Center.XCenter(f"{i}. {token[:25]}...")))
            selections = input(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\nEnter token numbers to use (e.g., 1,3,5 or 1-5): "))).strip()

            # Parse selections
            selected_indices = set()
            for part in selections.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    selected_indices.update(range(start, end + 1))
                else:
                    selected_indices.add(int(part))

            tokens_to_use = [self.valid_tokens[i-1] for i in selected_indices if 0 < i <= len(self.valid_tokens)]
        elif choice == "3":
            self.display_menu()
            n = input(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter(f"Enter number of tokens to use (1-{len(self.valid_tokens)}): "))).strip()
            n = min(int(n), len(self.valid_tokens)) if n.isdigit() else len(self.valid_tokens)
            tokens_to_use = self.valid_tokens[:n]
        else:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("[!] Invalid selection [!]")))
            return

        if not tokens_to_use:
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("[!] No tokens selected [!]")))
            return

        self.display_menu()
        invite_url = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(" Invite URL (e.g., https://discord.gg/abc123): "))).strip()
        self.invite_code = invite_url.split("/")[-1]

        self.display_menu()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter(f" WARNING: THIS WILL ATTEMPT TO JOIN WITH {len(tokens_to_use)} TOKENS! ")))
        time.sleep(2)

        confirm = input(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\nStart Joiner? (y/n): "))).lower()

        if confirm != 'y':
            print(Colorate.Horizontal(Colors.red_to_white,
                Center.XCenter("\n[!] OPERATION CANCELLED [!]\n")))
            return

        self.session = aiohttp.ClientSession()
        print(Colorate.Horizontal(Colors.red_to_white,
            Center.XCenter("\n[!] TOKEN JOINER ACTIVATED! [!]\n")))

        self.join_count = len(tokens_to_use)
        self.success_count = 0
        self.failed_count = 0

        # Run joins concurrently with rate limiting
        semaphore = asyncio.Semaphore(5)  # Limit concurrent joins
        async def limited_join(token):
            async with semaphore:
                return await self.join_with_token(token)

        await asyncio.gather(*[limited_join(token) for token in tokens_to_use])
        await self.session.close()

        print(Colorate.Horizontal(Colors.green_to_white,
            Center.XCenter(f"\n[+] JOINING COMPLETE [+]")))
        print(Colorate.Horizontal(Colors.blue_to_white,
            Center.XCenter(f"Success: {self.success_count} | Failed: {self.failed_count} | Total: {self.join_count}")))

if __name__ == "__main__":
    joiner = UltimateTokenJoiner()
    asyncio.run(joiner.run_joiner())
    input(Colorate.Horizontal(Colors.red_to_white,
        Center.XCenter("\nPress ENTER to exit...")))