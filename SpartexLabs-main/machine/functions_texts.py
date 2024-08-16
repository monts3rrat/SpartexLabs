# SWAPS

SWAP_BASE = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_odos', 'swap_sushiswap', 'swap_uniswap'],
    ['swap_odos', 'swap_sushiswap', 'swap_uniswap'],
    ['swap_odos', 'swap_sushiswap', 'swap_uniswap', None],
    ['swap_odos', 'swap_sushiswap', 'swap_uniswap', None],
]
'''

SWAP_SCROLL = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_izumi', 'swap_syncswap', 'swap_ambient'],
    ['swap_izumi', 'swap_syncswap', 'swap_ambient'],
    ['swap_izumi', 'swap_syncswap', 'swap_ambient', None],
    ['swap_izumi', 'swap_syncswap', 'swap_ambient', None],
]
'''

SWAP_LINEA = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_syncswap', 'swap_pancake', 'swap_woofi'],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi'],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', None],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', None],
]
'''

# PROTOCOL

PROTOCOL_SCROLL = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', 'swap_rango'],
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', 'swap_rango'],
    ['create_omnisea', None],
    ['deposit_layerbank'], ['withdraw_layerbank'],
    ['wrap_eth'],
    ['unwrap_eth'],
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', 'swap_rango'],
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', 'swap_rango'],
    ['check_in_owlto'],
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', 'swap_rango'],
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', 'swap_rango'],
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', 'swap_rango'],
]
'''

PROTOCOL_BASE = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_pancake', 'swap_uniswap', 'swap_sushiswap', 'swap_woofi', 'swap_maverick', 'swap_izumi', 'swap_odos', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance'],
    ['swap_pancake', 'swap_uniswap', 'swap_sushiswap', 'swap_woofi', 'swap_maverick', 'swap_izumi', 'swap_odos', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance'],
    ['create_safe', None],
    ['deposit_seamless'], ['withdraw_seamless'],
    ['wrap_eth'],
    ['unwrap_eth'],
    ['swap_pancake', 'swap_uniswap', 'swap_sushiswap', 'swap_woofi', 'swap_maverick', 'swap_izumi', 'swap_odos', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance'],
    ['swap_pancake', 'swap_uniswap', 'swap_sushiswap', 'swap_woofi', 'swap_maverick', 'swap_izumi', 'swap_odos', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance'],
    ['mint_mintfun'],
    ['swap_pancake', 'swap_uniswap', 'swap_sushiswap', 'swap_woofi', 'swap_maverick', 'swap_izumi', 'swap_odos', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance'],
    ['deposit_usdbc_seamless'], ['withdraw_usdbc_seamless'],
    ['swap_pancake', 'swap_uniswap', 'swap_sushiswap', 'swap_woofi', 'swap_maverick', 'swap_izumi', 'swap_odos', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance'],
    ['deposit_moonwell'], ['enable_collateral_moonwell'], ['disable_collateral_moonwell'], ['withdraw_moonwell'],
    ['swap_pancake', 'swap_uniswap', 'swap_sushiswap', 'swap_woofi', 'swap_maverick', 'swap_izumi', 'swap_odos', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance'],
    ['swap_pancake', 'swap_uniswap', 'swap_sushiswap', 'swap_woofi', 'swap_maverick', 'swap_izumi', 'swap_odos', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance'],

]
'''

PROTOCOL_LINEA = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance'],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance'],
    ['create_omnisea', None],
    ['deposit_layerbank'], ['withdraw_layerbank'],
    ['wrap_eth'],
    ['unwrap_eth'],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance'],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance'],
    ['check_in_owlto'],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance'],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance'],
    ['swap_syncswap', 'swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance'],
]
'''

# COLLECTOR

COLLECTOR = '''CLASSIC_ROUTES_MODULES_USING = [
    ['collector_eth'],
]
'''

# ROUTE

ROUTE_SCROLL = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', None],
    ['check_in_owlto', None],
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', None],
    ['wrap_eth'],
    ['add_liquidity_syncswap', None],
    ['unwrap_eth', None],
    ['swap_ambient', 'swap_zebra', 'swap_sushiswap', 'swap_skydrome', 'swap_syncswap', 'swap_spacefi', 'swap_izumi', 'swap_openocean', 'swap_xyfinance', None],
    [vote_rubyscore, None],
]
'''

ROUTE_BASE = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_odos', 'swap_sushiswap', 'swap_maverick', 'swap_izumi', 'swap_woofi', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance', 'swap_uniswap'],
    ['deposit_seamless', 'deposit_moonwell', None],
    ['swap_odos', 'swap_sushiswap', 'swap_maverick', 'swap_izumi', 'swap_woofi', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance', 'swap_uniswap'],
    ['withdraw_seamless', 'withdraw_moonwell', None],
    ['swap_odos', 'swap_sushiswap', 'swap_maverick', 'swap_izumi', 'swap_woofi', 'swap_oneinch', 'swap_openocean', 'swap_xyfinance', 'swap_uniswap'],
    ['mint_mintfun', None],
    ['vote_rubyscore', None],

]
'''

ROUTE_LINEA = '''CLASSIC_ROUTES_MODULES_USING = [
    ['swap_syncswap'],
    ['swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance', None],
    ['check_in_owlto', None],
    ['swap_syncswap'],
    ['swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance', None],
    ['wrap_eth'],                      
    ['unwrap_eth', None],
    ['swap_syncswap'],
    ['swap_pancake', 'swap_woofi', 'swap_velocore', 'swap_izumi', 'swap_rango', 'swap_openocean', 'swap_xyfinance', None],
    ['vote_rubyscore', None]
]
'''

HYPERLANE_NFT = '''CLASSIC_ROUTES_MODULES_USING = [
    ['bridge_hyperlane_nft']
]
'''

HYPERLANE_TOKEN = '''CLASSIC_ROUTES_MODULES_USING = [
    ['bridge_hyperlane_token']
]
'''
