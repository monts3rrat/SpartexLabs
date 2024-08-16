import os
import re
from openpyxl import load_workbook
import asyncio


async def validate_wallets(wallets):
    count = 0
    for i in wallets:
        count += 1
        pattern1 = r"^[0-9a-fA-F]{64}$"
        match1 = re.match(pattern1, i)
        pattern2 = r"^0x[0-9a-fA-F]{40}$"
        match2 = re.match(pattern2, i)

        if match1 or match2:
            pass
        else:
            if "".join(list(i)[0:2]) == "0x":
                return False, i, count, "адрес"
            else:
                return False, i, count, "приватный ключ"


async def validate_excel(path):
    wb = load_workbook(path)
    sheet_ranges = wb['EVM']

    names, privates, proxys = [], [], []

    for i, column_letter in enumerate("ABC", start=1):
        column = sheet_ranges[column_letter]
        for cell in column:
            if cell.value is not None:
                if i == 1:
                    names.append(cell.value)
                elif i == 2:
                    privates.append(cell.value)
                elif i == 3:
                    proxys.append(cell.value)

    if all(len(lst) == len(names) for lst in (privates, proxys)):
        return True
    else:
        return False
