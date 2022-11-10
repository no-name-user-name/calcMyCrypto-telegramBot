import asyncio
import platform
import time

from src import db
from src.main_logger import logger
from src.async_req import multi_requests_balance, multi_requests_stake, multi_requests_rewards
from src.tools import get_req
from tokens_config import tokens

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def price_parser():
    while 1:
        try:
            prices = get_req('https://api.coingecko.com/api/v3/simple/price?ids=cosmos,osmosis,ion,terra-luna,terrausd,'
                             'secret,secret,akash-network,regen,sentinel,persistence,pstake-finance,iris-network,'
                             'crypto-com-chain,starname,e-money,e-money-eur,juno-network,neta,marble,hope-galaxy,'
                             'racoon,crescent-network,binancecoin,binance-usd,litecoin,ethereum,dogecoin,solana,'
                             'the-open-network, '
                             'microtick,likecoin,ixo,bitcanna,bitsong,ki,lvn,medibloc,bostrom,comdex,cheqd-network,'
                             'stargaze,chihuahua-token,lum-network,vidulum,desmos,dig-chain,sommelier,sifchain,'
                             'band-protocol,darcmatter-coin,umee,graviton,pstake-finance,wrapped-bitcoin,ethereum,'
                             'usd-coin,dai,tether,decentr,certik,switcheo,injective-protocol,cerberus-2,fetch-ai,'
                             'assetmantle,provenance-blockchain,evmos,terra-luna-2,rizon,kava,kava-lend,kava-swap,usdx,'
                             'kujira,echelon,oraichain-token,cudos,agoric,stride,axelar,usd-coin,frax,tether,dai,weth,'
                             'wrapped-bitcoin,chainlink,aave,apecoin,axie-infinity,maker,rai,shiba-inu,staked-ether,'
                             'uniswap,chain-2,wrapped-moonbeam,polkadot,mars,bitcoin,&vs_currencies=usd')

            if prices['ok']:
                for p in prices['data']:
                    token = [n for n in tokens if n.coingecko_id == p]
                    if token:
                        t = token[0]
                        price = float(prices['data'][p]['usd'])
                        t.price = price

        except Exception as e:
            print(f'Error: {e}')
            logger.error(e)


def parse_addresses_balance():
    while 1:
        try:
            user_tokens = db.get_user_tokens()
            chunk_count = 20
            offset = 0

            while offset < len(user_tokens):
                _user_tokens = user_tokens[offset:offset + chunk_count]

                loop = asyncio.new_event_loop()
                result = loop.run_until_complete(
                    multi_requests_balance(user_tokens=_user_tokens, tokens_data=tokens, timeout=30))

                for each in result:

                    if each is None:
                        continue

                    if each['type'] == 'address':
                        db.update_user_token_balance(user_token_id=each['user_token_id'], balance=each['balance'])

                offset += chunk_count
        except Exception as e:
            print(f'Error: {e}')
            logger.error(e)


def parse_addresses_stake():
    while 1:
        try:
            user_tokens = db.get_user_tokens()
            chunk_count = 20
            offset = 0

            while offset < len(user_tokens):
                _user_tokens = user_tokens[offset:offset + chunk_count]

                loop = asyncio.new_event_loop()
                result = loop.run_until_complete(
                    multi_requests_stake(user_tokens=_user_tokens, timeout=30))

                for each in result:
                    if each is None:
                        continue

                    if each['type'] == 'address':
                        db.update_user_token_stake_balance(each['user_token_id'], each['staked_balance'])

                offset += chunk_count
        except Exception as e:
            print(f'Error: {e}')
            logger.error(e)


def parse_addresses_unstake():
    while 1:
        try:
            user_tokens = db.get_user_tokens()
            chunk_count = 20
            offset = 0

            while offset < len(user_tokens):
                _user_tokens = user_tokens[offset:offset + chunk_count]

                loop = asyncio.new_event_loop()
                result = loop.run_until_complete(
                    multi_requests_stake(user_tokens=_user_tokens, timeout=30))

                for each in result:
                    if each is None:
                        continue

                    if each['type'] == 'address':
                        db.update_user_token_stake_balance(each['user_token_id'], each['staked_balance'])

                offset += chunk_count
        except Exception as e:
            print(f'Error: {e}')
            logger.error(e)


def parse_addresses_rewards():
    while 1:
        try:
            user_tokens = db.get_user_tokens()
            chunk_count = 20
            offset = 0

            while offset < len(user_tokens):
                _user_tokens = user_tokens[offset:offset + chunk_count]

                loop = asyncio.new_event_loop()
                result = loop.run_until_complete(
                    multi_requests_rewards(user_tokens=_user_tokens, timeout=30))

                for each in result:
                    if each is None:
                        continue

                    if each['type'] == 'address':
                        db.update_user_token_rewards_balance(each['user_token_id'], each['rewards_balance'])

                offset += chunk_count
        except Exception as e:
            print(f'Error: {e}')
            logger.error(e)


def loop_parsers():
    price_parser()
    parse_addresses_balance()
    parse_addresses_stake()
    parse_addresses_rewards()

    time.sleep(60)
