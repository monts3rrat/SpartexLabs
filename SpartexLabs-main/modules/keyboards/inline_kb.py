from aiogram import types
import asyncio
from aiogram.types import InlineKeyboardMarkup


def session_list1():
    buttons = [
        [
            types.InlineKeyboardButton(text="Вперед", callback_data="num_incr")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def session_list2():
    buttons = [
        [
            types.InlineKeyboardButton(text="Назад", callback_data="num_decr"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def session_list3():
    buttons = [
        [
            types.InlineKeyboardButton(text="Назад", callback_data="num_decr"),
            types.InlineKeyboardButton(text="Вперед", callback_data="num_incr")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def projects_inline():
    buttons = [
        [
            types.InlineKeyboardButton(text="Base", callback_data="base"),
            types.InlineKeyboardButton(text="Linea", callback_data="linea")
        ],
        [
            types.InlineKeyboardButton(text="Scroll", callback_data="scroll"),
            types.InlineKeyboardButton(text="Zora", callback_data="zora")
        ],
        [
            types.InlineKeyboardButton(text="Hyperlane", callback_data="hyperlane"),
            types.InlineKeyboardButton(text="Чекер", callback_data="checker")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def projects_checker_inline():
    buttons = [
        [
            types.InlineKeyboardButton(text="arbitrum", callback_data="arbitrum_checker"),
            types.InlineKeyboardButton(text="blast", callback_data="blast_checker")
        ],
        [
            types.InlineKeyboardButton(text="bnb", callback_data="bnb_checker"),
            types.InlineKeyboardButton(text="ethereum", callback_data="ethereum_checker")
        ],
        [
            types.InlineKeyboardButton(text="linea", callback_data="linea_checker"),
            types.InlineKeyboardButton(text="optimism", callback_data="optimism_checker"),
        ],
        [
            types.InlineKeyboardButton(text="polygon", callback_data="polygon_checker"),
            types.InlineKeyboardButton(text="scroll", callback_data="scroll_checker")
        ],
        [
            types.InlineKeyboardButton(text="zora", callback_data="zora_checker"),
            types.InlineKeyboardButton(text="base", callback_data="base_checker"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def net_hl1():
    buttons = [
        [
            types.InlineKeyboardButton(text="Base", callback_data="base_hl1"),
            types.InlineKeyboardButton(text="Optimism", callback_data="optimism_hl1")
        ],
        [
            types.InlineKeyboardButton(text="Arbitrum", callback_data="arbitrum_hl1"),
            types.InlineKeyboardButton(text="Scroll", callback_data="scroll_hl1")
        ],
        [
            types.InlineKeyboardButton(text="BSC", callback_data="bnb_hl1"),
            types.InlineKeyboardButton(text="Linea", callback_data="linea_hl1"),
        ],
        [
            types.InlineKeyboardButton(text="Polygon", callback_data="polygon_hl1"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def net_hl2():
    buttons = [
        [
            types.InlineKeyboardButton(text="Base", callback_data="base_hl2"),
            types.InlineKeyboardButton(text="Optimism", callback_data="optimism_hl2")
        ],
        [
            types.InlineKeyboardButton(text="Arbitrum", callback_data="arbitrum_hl2"),
            types.InlineKeyboardButton(text="Scroll", callback_data="scroll_hl2")
        ],
        [
            types.InlineKeyboardButton(text="BSC", callback_data="bnb_hl2"),
            types.InlineKeyboardButton(text="Linea", callback_data="linea_hl2"),
        ],
        [
            types.InlineKeyboardButton(text="Polygon", callback_data="polygon_hl2"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def hl_time():
    buttons = [
        [types.InlineKeyboardButton(text="30 - 90", callback_data="30_90_hl")],
        [types.InlineKeyboardButton(text="120 - 600", callback_data="120_600_hl")],
        [types.InlineKeyboardButton(text="600 - 3600", callback_data="600_3600_hl")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def next_inline():
    buttons = [
        [types.InlineKeyboardButton(text="Продолжить", callback_data="next_privates")],
        [types.InlineKeyboardButton(text="В Меню Услуг", callback_data="menu_services")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def functions_inline_0():
    buttons = [
        [
            types.InlineKeyboardButton(text="1", callback_data="bridge"),
            types.InlineKeyboardButton(text="2", callback_data="swap")
        ],
        [
            types.InlineKeyboardButton(text="3", callback_data="protocol"),
            types.InlineKeyboardButton(text="4", callback_data="collector")
        ],
        [
            types.InlineKeyboardButton(text="5", callback_data="route")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def functions_inline_zora():
    buttons = [
        [types.InlineKeyboardButton(text="1", callback_data="bridge_zora")],
        [types.InlineKeyboardButton(text="2", callback_data="mint_zora")],
        [types.InlineKeyboardButton(text="3", callback_data="light_trans")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def functions_inline_hl():
    buttons = [
        [types.InlineKeyboardButton(text="1", callback_data="hl_hft")],
        [types.InlineKeyboardButton(text="2", callback_data="hl_token")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def two_bridge_inline_zora():
    buttons = [
        [types.InlineKeyboardButton(text="1", callback_data="off_bridge")],
        [types.InlineKeyboardButton(text="2", callback_data="instant_bridge")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def bridge_inline_zora():
    buttons = [
        [types.InlineKeyboardButton(text="1", callback_data="arb_zora")],
        [types.InlineKeyboardButton(text="2", callback_data="op_zora")],
        [types.InlineKeyboardButton(text="3", callback_data="base_zora")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def mint_inline_zora():
    buttons = [
        [types.InlineKeyboardButton(text="1", callback_data="zora_mint_zora")],
        [types.InlineKeyboardButton(text="2", callback_data="base_mint_zora")],
        [types.InlineKeyboardButton(text="3", callback_data="op_mint_zora")],
        [types.InlineKeyboardButton(text="4", callback_data="custom_mint_zora")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def sleep_inline_zora():
    buttons = [
        [types.InlineKeyboardButton(text="30 - 90", callback_data="30_90_zora")],
        [types.InlineKeyboardButton(text="120 - 600", callback_data="120_600_zora")],
        [types.InlineKeyboardButton(text="600 - 3600", callback_data="600_3600_zora")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def functions_inline_hyperlane():
    buttons = [
        [types.InlineKeyboardButton(text="1", callback_data="nft_hl")],
        [types.InlineKeyboardButton(text="2", callback_data="token_hl")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def sleep_inline():
    buttons = [
        [types.InlineKeyboardButton(text="30 - 90", callback_data="30_90")],
        [types.InlineKeyboardButton(text="120 - 600", callback_data="120_600")],
        [types.InlineKeyboardButton(text="600 - 3600", callback_data="600_3600")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def chain_bridge_inline():
    buttons = [
        [types.InlineKeyboardButton(text="Native", callback_data="native_bridge")],
        [types.InlineKeyboardButton(text="Rhino", callback_data="rhino_bridge")],
        [types.InlineKeyboardButton(text="Orbiter", callback_data="orbiter_bridge")],
        [types.InlineKeyboardButton(text="Relay", callback_data="relay_bridge")],
        [types.InlineKeyboardButton(text="Owlto", callback_data="owlto_bridge")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def chain_from_bridge_inline():
    buttons = [
        [types.InlineKeyboardButton(text="Arbitrum", callback_data="arbitrum_bridge")],
        [types.InlineKeyboardButton(text="Base", callback_data="base_bridge")],
        [types.InlineKeyboardButton(text="Optimism", callback_data="optimism_bridge")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def tariff_plan():
    buttons = [
        [
            types.InlineKeyboardButton(text="10", callback_data="10_dollars"),
            types.InlineKeyboardButton(text="30", callback_data="30_dollars")
        ],
        [
            types.InlineKeyboardButton(text="50", callback_data="50_dollars"),
            types.InlineKeyboardButton(text="100", callback_data="100_dollars")
        ],
        [
            types.InlineKeyboardButton(text="150", callback_data="150_dollars"),
            types.InlineKeyboardButton(text="250", callback_data="250_dollars"),
        ],
        [
            types.InlineKeyboardButton(text="Своё значение", callback_data="other_dollars")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def check_invoice():
    buttons = [
        [
            types.InlineKeyboardButton(text="Проверить платёж", callback_data="check_status"),
        ],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
