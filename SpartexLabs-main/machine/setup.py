import os
import zipfile
import asyncio
import shutil
import sqlite3
from loguru import logger
import machine.functions_texts as txt


current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file)
current_directory1 = current_directory.split("\\")


async def get_connection():
    return sqlite3.connect(f"{'/'.join(current_directory1[:-1])}/modules/database/SQLdatabase.db")


async def check_sessions(message):
    with await get_connection() as conn:
        cursor = conn.cursor()
        sessions = cursor.execute(
            "SELECT sessions FROM users WHERE id = ?", (message,)
        ).fetchone()
        return sessions[0] if sessions else None


async def unpacking_machine(machine_num):
    session = await check_sessions(machine_num)
    session = session[0]

    with zipfile.ZipFile("machine/SpartexSoft.zip", "r") as fantasy_zip:
        fantasy_zip.extractall(f"machine/SpartexSoft{machine_num}_{session}")

    logger.info(f"SpartexSoft{machine_num}_{session} unpacking complete.")
    await asyncio.sleep(0.5)


async def move_excel(machine_num):
    session = await check_sessions(machine_num)
    session = session[0]

    path_excel = os.path.join(
        "/".join(current_directory1[:-1]), f"accounts_user/accounts_data_{machine_num}.xlsx"
    )
    dest_path = os.path.join(
        current_directory,
        f"SpartexSoft{machine_num}_{session}/SpartexSoft/data/accounts_data.xlsx",
    )

    if os.path.exists(dest_path):
        os.remove(dest_path)

    shutil.move(path_excel, dest_path)

    logger.info(
        f"Excel file {machine_num} has been moved and the original file has been deleted."
    )


async def change_settings_file(
        machine_num, machine_func, project, sleep, bridge, network
):
    session = await check_sessions(machine_num)
    session = session[0]

    settings_path = os.path.join(
        current_directory, f"SpartexSoft{machine_num}_{session}/SpartexSoft/settings.py"
    )
    general_settings_path = os.path.join(
        current_directory,
        f"SpartexSoft{machine_num}_{session}/SpartexSoft/general_settings.py",
    )

    with open(settings_path, "r", encoding="UTF8") as file:
        lines = file.readlines()

    if machine_func == "bridge":
        bridge_dict = {
            "rhino_bridge": 228,
            "orbiter_bridge": 204,
            "relay_bridge": 220,
            "owlto_bridge": 212
        }

        if project == "base":
            project_dict = {
                "zora": 12,
                "scroll": 8,
                "linea": 4,
            }
            network_dict = {"base": 3, "arbitrum": 1, "optimism": 7}

            bridge_split = bridge.split("_")
            network_val = network_dict.get(network.split("_")[0], 0)

            lines[bridge_dict[bridge] - 2] = f"{bridge_split[0].upper()}_CHAIN_ID_FROM = [{network_val}]\n"
            lines[
                bridge_dict[bridge] - 1] = f"{bridge_split[0].upper()}_CHAIN_ID_TO = [{project_dict.get(project, 0)}]\n"
            lines[-2] = f"    ['bridge_{bridge_split[0].lower()}'],\n"

        if project == "linea":
            project_dict = {
                "zora": 12,
                "scroll": 8,
                "base": 3,
            }
            network_dict = {"base": 3, "arbitrum": 1, "optimism": 7}

            bridge_split = bridge.split("_")
            network_val = network_dict.get(network.split("_")[0], 0)

            lines[bridge_dict[bridge] - 2] = f"{bridge_split[0].upper()}_CHAIN_ID_FROM = [{network_val}]\n"
            lines[
                bridge_dict[bridge] - 1] = f"{bridge_split[0].upper()}_CHAIN_ID_TO = [{project_dict.get(project, 0)}]\n"
            lines[-2] = f"    ['bridge_{bridge_split[0].lower()}'],\n"

        if project == "scroll":
            project_dict = {
                "zora": 12,
                "linea": 4,
                "base": 3,
            }
            network_dict = {"base": 3, "arbitrum": 1, "optimism": 7}

            bridge_split = bridge.split("_")
            network_val = network_dict.get(network.split("_")[0], 0)

            lines[bridge_dict[bridge] - 2] = f"{bridge_split[0].upper()}_CHAIN_ID_FROM = [{network_val}]\n"
            lines[
                bridge_dict[bridge] - 1] = f"{bridge_split[0].upper()}_CHAIN_ID_TO = [{project_dict.get(project, 0)}]\n"
            lines[-2] = f"    ['bridge_{bridge_split[0].lower()}'],\n"

    elif machine_func == "swap":
        swap_dict = {
            "base": txt.SWAP_BASE,
            "linea": txt.SWAP_LINEA,
            "scroll": txt.SWAP_SCROLL,
        }
        lines[-3:-1] = "\n"
        lines[-1] = swap_dict.get(project, "")

    elif machine_func == "collector":
        lines[-3:-1] = "\n"
        lines[-1] = txt.COLLECTOR

    elif machine_func == "protocol":
        protocol_dict = {
            "base": txt.PROTOCOL_BASE,
            "linea": txt.PROTOCOL_LINEA,
            "scroll": txt.PROTOCOL_SCROLL,
        }
        lines[-3:-1] = "\n"
        lines[-1] = protocol_dict.get(project, "")

    elif machine_func == "route":
        route_dict = {
            "base": txt.ROUTE_BASE,
            "linea": txt.ROUTE_LINEA,
            "scroll": txt.ROUTE_SCROLL,
        }
        lines[-3:-1] = "\n"
        lines[-1] = route_dict.get(project, "")

    with open(settings_path, "w", encoding="UTF8") as file:
        file.writelines(lines)

    with open(general_settings_path, "r", encoding="UTF8") as file:
        lines1 = file.readlines()

    lines1[15] = (
        "AMOUNT_PERCENT = (80, 93)\n"
        if machine_func != "protocol"
        else "AMOUNT_PERCENT = (5, 15)\n"
    )
    lines1[64] = f"SLEEP_TIME_MODULES = ({sleep})\n"
    lines1[65] = f"SLEEP_TIME_ACCOUNTS = ({sleep})\n"

    with open(general_settings_path, "w", encoding="UTF8") as file:
        file.writelines(lines1)

    logger.info(f"Settings files changed in SpartexSoft{machine_num}_{session}.")


async def start_machine(machine_num):
    session = await check_sessions(machine_num)
    session = session[0]

    batch_path = os.path.join(current_directory, "starting_machine.bat")
    with open(batch_path, "r") as file:
        lines = file.readlines()

    lines[0] = f"cd machine/SpartexSoft{machine_num}_{session}/SpartexSoft/\n"
    lines[2] = f"rd /s /q SpartexSoft{machine_num}_{session}\n"

    with open(batch_path, "w") as file:
        file.writelines(lines)

    os.startfile(batch_path)
    logger.info(f"Starting the SpartexSoft{machine_num}_{session} machine.")


async def change_settings_file_hl(machine_num, func, net1, net2, sleep):
    session = await check_sessions(machine_num)
    session = session[0]

    settings_path = os.path.join(current_directory, f"SpartexSoft{machine_num}_{session}/SpartexSoft/settings.py")
    general_settings_path = os.path.join(current_directory,
                                         f"SpartexSoft{machine_num}_{session}/SpartexSoft/general_settings.py")

    with open(settings_path, "r", encoding="UTF8") as file:
        lines = file.readlines()

    network_dict = {"base": 3, "arbitrum": 1, "optimism": 7, "scroll": 35, "bnb": 6, "linea": 22, "polygon": 33}
    network1 = network_dict.get(net1.split("_")[0], 0)
    network2 = network_dict.get(net2.split("_")[0], 0)

    lines[726] = f"SRC_CHAIN_MERKLY_HYPERLANE = [{network1}]"
    lines[727] = f"DST_CHAIN_MERKLY_HYPERLANE = [{network2}]"

    lines[-3:-1] = "\n"
    if func == "hl_token":
        lines[-1] = txt.HYPERLANE_TOKEN
    else:
        lines[-1] = txt.HYPERLANE_NFT

    with open(settings_path, "w", encoding="UTF8") as file:
        file.writelines(lines)

    with open(general_settings_path, "r", encoding="UTF8") as file:
        lines1 = file.readlines()

    lines1[15] = "AMOUNT_PERCENT = (80, 93)\n"
    lines1[64] = f"SLEEP_TIME_MODULES = ({sleep})\n"
    lines1[65] = f"SLEEP_TIME_ACCOUNTS = ({sleep})\n"

    with open(general_settings_path, "w", encoding="UTF8") as file:
        file.writelines(lines1)

    logger.info(f"Settings files changed in SpartexSoft{machine_num}_{session}.")


async def main_hl(machine_num, func, net1, net2, sleep):
    await unpacking_machine(machine_num)
    await move_excel(machine_num)
    await change_settings_file_hl(machine_num, func, net1, net2, sleep)
    await start_machine(machine_num)


async def main(machine_num, machine_func, project, sleep, bridge, network):
    await unpacking_machine(machine_num)
    await move_excel(machine_num)
    await change_settings_file(
        machine_num, machine_func, project, sleep, bridge, network
    )
    await start_machine(machine_num)


async def download_and_extract_dropbox_file_zora(machine_num, session):
    try:
        with zipfile.ZipFile("machine/ZoraSoft.zip", "r") as zip_ref:
            zip_ref.extractall("machine/ZoraSoft")
        await asyncio.sleep(0.5)
    except Exception as e:
        logger.error(f"Failed to download or extract Dropbox file: {e}")


async def update_settings_file_zora(path, sleep, url_mint=None):
    try:
        with open(path, "r+", encoding="UTF8") as file:
            lines = file.readlines()
            lines[29] = f"TIME_DELAY = [{sleep}]\n"
            lines[30] = f"TIME_ACCOUNT_DELAY = [{sleep}]\n"
            if url_mint:
                lines[97] = f"URL_CUSTOM_NFT = ['{url_mint}']\n"
            file.seek(0)
            file.writelines(lines)
            file.truncate()
    except Exception as e:
        logger.error(f"Failed to update settings file: {e}")


async def execute_batch_script_zora(batch_path, machine_num, session, func_num):
    try:
        if func_num == 000:
            with open(batch_path, "w") as file:
                file.writelines([
                    f"cd machine/Zora{machine_num}_{session}/Zora\n",
                    f"python main.py 22\n",
                    f"python main.py 24\n",
                    f"python main.py 16\n",
                    f"cd ..\n",
                    f"cd ..\n",
                    f"rd /s /q Zora{machine_num}_{session}\n"])

        else:
            with open(batch_path, "w") as file:
                file.writelines([
                    f"cd machine/Zora{machine_num}_{session}/Zora\n",
                    f"python main.py {func_num}\n",
                    f"rd /s /q Zora{machine_num}_{session}\n"
                ])

        os.startfile(batch_path)
        logger.info(f"Starting the ZoraSoft{machine_num}_{session} machine.")
    except Exception as e:
        logger.error(f"Failed to execute batch script: {e}")


async def main_zora(machine_num, func, sleep, url_mint=None):
    session = await check_sessions(machine_num)
    session = session[0]
    current_directory_zora = os.getcwd()

    await download_and_extract_dropbox_file_zora(machine_num, session)

    general_settings_path = os.path.join(current_directory_zora, f"Zora{machine_num}_{session}/Zora/settings.py")
    await update_settings_file_zora(general_settings_path, sleep, url_mint if func == "custom_mint_zora" else None)

    batch_path = os.path.join(current_directory_zora, "starting_machine_zora.bat")
    func_dict = {
        "off_bridge": 1, "arb_zora": 2, "op_zora": 2, "base_zora": 2,
        "zora_mint_zora": 6, "base_mint_zora": 7, "op_mint_zora": 8,
        "custom_mint_zora": 14, "light_trans": 000
    }
    func_num = func_dict.get(func)
    await execute_batch_script_zora(batch_path, machine_num, session, func_num)
