import robin_stocks.robinhood as rh
import config
import json


time_logged_in = 60*60*24
rh.authentication.login(username=config.USERNAME, 
                        password=config.PASSWORD,
                        expiresIn=time_logged_in, 
                        scope='internal', 
                        by_sms=True, 
                        store_session=True, 
                        mfa_code=None, 
                        pickle_name='')

investment_profile = rh.profiles.load_investment_profile(info=None)
# print(json.dumps(investment_profile, indent=4))

portfoliio_profile = rh.profiles.load_portfolio_profile(account_number=None, info=None)
# print(json.dumps(portfoliio_profile, indent=4))

sp500_top_movers = rh.markets.get_top_movers_sp500(direction='up', info=None)
# print(json.dumps(sp500_top_movers, indent=4))

build_holdings = rh.account.build_holdings(with_dividends=False)
# print(json.dumps(build_holdings, indent=4))

all_positions = rh.account.get_all_positions(info=None)
# print(json.dumps(all_positions, indent=4))


# Try automatic transfer of funds if required
# Fetch ACH relationships
# ach_relationships = rh.account.get_ach_relationships()
# print(ach_relationships)
# rh.account.deposit_funds_to_robinhood_account(ach_relationship, 1, info=None)

