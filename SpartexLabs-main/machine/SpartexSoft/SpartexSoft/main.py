import asyncio
import sys

from config import TITLE
from termcolor import cprint
from modules import txchecker
from questionary import Choice, select

from modules.interfaces import SoftwareException
from utils.modules_runner import Runner
from utils.route_generator import RouteGenerator
from utils.tools import create_cex_withdrawal_list, check_progress_file


def are_you_sure(module=None, gen_route: bool = False):
    if gen_route or check_progress_file():
        print('''\n ⚠️⚠️⚠️ THAT ACTION WILL DELETE ALL PREVIOUS PROGRESS FOR CLASSIC-ROUTES ⚠️⚠️⚠️ \n''')
        if module:
            module()


def main():
    print(TITLE)
    cprint(f'\n❤️ My channel for latest updates: https://t.me/SpartexLabs\n', 'light_cyan', attrs=["blink"])
    try:
        print('''What do you want to do?',
🤖 Start running smart routes (c) GOOGLE POWERED
🚀 Start running classic routes for each wallet
📄 Generate classic-route for each wallet
💾 Create and safe CEX withdrawal file
✅  Check the connection of each proxy
📊 Get TX stats for all wallets
❌ Exit\n''')

        runner = Runner()
        generator = RouteGenerator()
        are_you_sure(generator.classic_routes_json_save, gen_route=True)
        print()
        asyncio.run(runner.run_accounts(smart_route=False))
        print()
        
    except SoftwareException as error:
        cprint(f'\n{error}', color='light_red')
        sys.exit()


if __name__ == "__main__":
    main()
