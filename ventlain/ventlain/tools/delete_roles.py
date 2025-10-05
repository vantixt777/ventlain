import discord
import asyncio
import aiohttp
import time
import os
from pystyle import Colors, Colorate, Center

class AllRolesDeleter:
    def __init__(self):
        self.banner = r"""
    ▄████████  ▄██████▄   ▄█          ▄████████    ▄████████ 
  ███    ███ ███    ███ ███         ███    ███   ███    ███ 
  ███    ███ ███    ███ ███         ███    █▀    ███    █▀  
 ▄███▄▄▄▄██▀ ███    ███ ███        ▄███▄▄▄       ███        
▀▀███▀▀▀▀▀   ███    ███ ███       ▀▀███▀▀▀     ▀███████████ 
▀███████████ ███    ███ ███         ███    █▄           ███ 
  ███    ███ ███    ███ ███▌    ▄   ███    ███    ▄█    ███ 
  ███    ███  ▀██████▀  █████▄▄██   ██████████  ▄████████▀  
  ███    ███            ▀                                   
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
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("Roles deleter by vantixt")))
        print("\n")

    async def delete_single_role(self, role_id, role_name, headers):
        try:
            async with self.session.delete(
                f"https://discord.com/api/v9/guilds/{self.guild_id}/roles/{role_id}",
                headers=headers
            ) as resp:
                if resp.status == 204:
                    print(Colorate.Horizontal(Colors.green_to_white,
                                                Center.XCenter(f"[+] Deleted role: {role_name} ({role_id}) [+]")))
                    return True
                elif resp.status == 429:
                    retry_after = (await resp.json()).get('retry_after', 1)
                    print(Colorate.Horizontal(Colors.yellow_to_red,
                                                Center.XCenter(f"[!] Rate limited on role deletion! Retrying in {retry_after} seconds... [!]")))
                    await asyncio.sleep(retry_after)
                    return await self.delete_single_role(role_id, role_name, headers)
                elif resp.status == 403:
                    print(Colorate.Horizontal(Colors.red_to_white,
                                                Center.XCenter(f"[!] Error deleting role {role_name}: Missing permissions [!]")))
                    return False
                else:
                    print(Colorate.Horizontal(Colors.red_to_white,
                                                Center.XCenter(f"[!] Error deleting role {role_name} (Status: {resp.status}) [!]")))
                    return False
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white,
                                        Center.XCenter(f"[!] Error deleting role {role_name}: {str(e)} [!]")))
            return False

    async def delete_all_roles(self, headers):
        guild = await self.session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/roles", headers=headers)
        if guild.status != 200:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(f"[!] Error fetching guild roles (Status: {guild.status}) [!]")))
            return

        roles_data = await guild.json()
        roles_to_delete = [role for role in roles_data if role['id'] != self.guild_id]  

        print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(f"[i] Found {len(roles_to_delete)} roles. Attempting to delete... [i]")))

        if not roles_to_delete:
            print(Colorate.Horizontal(Colors.green_to_yellow, Center.XCenter("[!] No roles found to delete (excluding @everyone). [!]")))
            return

        print(Colorate.Horizontal(Colors.green_to_yellow, Center.XCenter(f"[!] Found {len(roles_to_delete)} roles to delete. [!]")))

        confirm_prompt = Colorate.Horizontal(Colors.red_to_white,
                                            Center.XCenter("\n WARNING: THIS WILL DELETE ALL ROLES! ARE YOU SURE? (y/n): "))
        confirm = input(confirm_prompt).lower()

        if confirm == 'y':
            tasks = [self.delete_single_role(role['id'], role['name'], headers) for role in roles_to_delete]
            results = await asyncio.gather(*tasks)
            deleted_count = sum(results)
            print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(f"[+] Successfully deleted {deleted_count} roles. [+]")))
        else:
            print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter("[!] Role deletion cancelled. [!]")))

    async def run(self):
        self.session = aiohttp.ClientSession()
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        print(Colorate.Horizontal(Colors.red_to_white,
                                    Center.XCenter("\n[!] STARTING POWERFUL ALL ROLES DELETION [!]\n")))
        await self.delete_all_roles(headers)
        print(Colorate.Horizontal(Colors.green_to_white,
                                    Center.XCenter("\n[+] ALL ROLES DELETION COMPLETED [+]")))
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
        warning_message = Colorate.Horizontal(Colors.red_to_white,
                                                Center.XCenter(" WARNING: THIS WILL DELETE ALL ROLES! "))
        print(warning_message)
        time.sleep(2)

        confirm_prompt = Colorate.Horizontal(Colors.red_to_white,
                                            Center.XCenter("\nSTART ALL ROLES DELETION? (y/n): "))
        confirm = input(confirm_prompt).lower()

        if confirm == 'y':
            asyncio.run(self.run())
        else:
            cancelled_message = Colorate.Horizontal(Colors.red_to_white,
                                                    Center.XCenter("\n[!] OPERATION CANCELLED [!]\n"))
            print(cancelled_message)

if __name__ == "__main__":
    deleter = AllRolesDeleter()
    deleter.get_inputs()
    exit_message = Colorate.Horizontal(Colors.red_to_white,
                                        Center.XCenter("\nPress ENTER to exit..."))
    input(exit_message)