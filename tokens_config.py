class TokenData:
    def __init__(self, name: str,
                 symbol: str,
                 coingecko_id: str,
                 zeros: int,
                 keplr_id: str = None,
                 denom: str = None,
                 is_pos: bool = False):

        """
        Token settings class

        :param name:
        :param symbol:
        :param coingecko_id:
        :param zeros: num of sybmols after comma
        :param keplr_id: Cosmos HUB keplr api id
        :param denom: Only for Cosmos HUB
        :param is_pos: Is token Proof-of-Stake
        """

        self.name = name
        self.denom = denom
        self.symbol = symbol
        self.zeros = zeros
        self.coingecko_id = coingecko_id
        self.price: float = 0.0
        self.keplr_id = keplr_id
        self.is_pos = is_pos


btc = TokenData(name='btc', symbol='BTC', zeros=8, coingecko_id='bitcoin')
ltc = TokenData(name='ltc', symbol='LTC', zeros=8, coingecko_id='litecoin')
eth = TokenData(name='eth', symbol='ETH', zeros=18, coingecko_id='ethereum')
doge = TokenData(name='doge', symbol='DOGE', zeros=8, coingecko_id='dogecoin')
solana = TokenData(name='solana', symbol='SOL', zeros=9, coingecko_id='solana')
ton = TokenData(name='ton', symbol='TON', zeros=9, coingecko_id='the-open-network', is_pos=True)
bnb = TokenData(name='bnb', symbol='BNB', zeros=8, coingecko_id='binancecoin')
bnb_sc = TokenData(name='bnb_sc', symbol='BNBSC', zeros=8, coingecko_id='binancecoin')
busd_bep2 = TokenData(name='busd_bep2', symbol='BUSD', zeros=8, coingecko_id='binance-usd')

cosmos = TokenData(name='cosmos', denom='uatom', symbol='ATOM',
                   zeros=6, coingecko_id='cosmos', keplr_id='lcd-cosmoshub', is_pos=True)

juno = TokenData(name='juno', denom='ujuno', symbol='JUNO',
                 zeros=6, coingecko_id='juno-network', keplr_id='lcd-juno', is_pos=True)

osmosis = TokenData(name='osmosis', denom='uosmo', symbol='OSMO',
                    zeros=6, coingecko_id='osmosis', keplr_id='lcd-osmosis', is_pos=True)

evmos = TokenData(name='evmos', denom='aevmos', symbol='EVMOS',
                  zeros=18, coingecko_id='evmos', keplr_id='lcd-evmos', is_pos=True)

secret = TokenData(name='secret', denom='uscrt', symbol='SCRT',
                   zeros=6, coingecko_id='secret', keplr_id='lcd-secret', is_pos=True)

umee = TokenData(name='umee', denom='uumee', symbol='UMEE',
                 zeros=6, coingecko_id='umee', keplr_id='lcd-umee', is_pos=True)

sifchain = TokenData(name='sifchain', denom='rowan', symbol='ROWAN',
                     zeros=18, coingecko_id='sifchain', keplr_id='lcd-sifchain', is_pos=True)

agoric = TokenData(name='agoric', denom='ubld', symbol='BLD',
                   zeros=6, coingecko_id='agoric', keplr_id='lcd-agoric', is_pos=True)

akash = TokenData(name='akash', denom='uakt', symbol='AKT',
                  zeros=6, coingecko_id='akash-network', keplr_id='lcd-akash', is_pos=True)

cerberys = TokenData(name='cerberys', denom='ucrbrus', symbol='CRBRUS',
                     zeros=6, coingecko_id='cerberus-2', is_pos=False)

crescent = TokenData(name='crescent', denom='ucre', symbol='CRE',
                     zeros=6, coingecko_id='crescent-network', is_pos=False)

terra_classic = TokenData(name='terra_classic', denom='uluna', symbol='LUNC',
                          zeros=6, coingecko_id='terra-luna', keplr_id='lcd-columbus', is_pos=True)

kava = TokenData(name='kava', denom='ukava', symbol='KAVA',
                 zeros=6, coingecko_id='kava', keplr_id='lcd-kava', is_pos=True)


tokens = [btc, cosmos, juno, osmosis, evmos, secret, umee, sifchain, agoric, akash, cerberys, crescent, terra_classic,
          kava, bnb, busd_bep2, ltc, eth, doge, solana, ton]
