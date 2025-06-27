import config
import trade_strat
import robin_stocks.robinhood as rh
import datetime as dt
import time
import pandas as pd

def login(days):
    time_logged_in = 60*60*24
    rh.authentication.login(username=config.USERNAME, 
                            password=config.PASSWORD,
                            expiresIn=time_logged_in, 
                            scope='internal', 
                            by_sms=True, 
                            store_session=True, 
                            mfa_code=None, 
                            pickle_name='')
    
def logout():
    rh.authentication.logout()    

def get_stocks():
    # List of S&P 500 symbols
    spy_symbols = [
    "A", "AAPL", "ABBV", "ABNB", "ABT", "ACGL", "ACN", "ADBE", "ADI", "ADM", "ADP", 
    "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALGN", 
    "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", "AMTM", "AMZN", 
    "ANET", "ANSS", "AON", "AOS", "APA", "APD", "APH", "APTV", "ARE", "ATO", "AVB", 
    "AVGO", "AVY", "AWK", "AXON", "AXP", "AZO", "BA", "BAC", "BALL", "BAX", "BBY", 
    "BDX", "BEN", "BF.B", "BG", "BIIB", "BK", "BKNG", "BKR", "BLDR", "BLK", "BMY", 
    "BR", "BRK.B", "BRO", "BSX", "BWA", "BX", "BXP", "C", "CAG", "CAH", "CARR", "CAT", 
    "CB", "CBOE", "CBRE", "CCI", "CCL", "CDNS", "CDW", "CE", "CEG", "CF", "CFG", "CHD", 
    "CHRW", "CHTR", "CI", "CINF", "CL", "CLX", "CMCSA", "CME", "CMG", "CMI", "CMS", 
    "CNC", "CNP", "COF", "COO", "COP", "COR", "COST", "CPAY", "CPB", "CPRT", "CPT", 
    "CRL", "CRM", "CRWD", "CSCO", "CSGP", "CSX", "CTAS", "CTLT", "CTRA", "CTSH", "CTVA", 
    "CVS", "CVX", "CZR", "D", "DAL", "DAY", "DD", "DE", "DECK", "DELL", "DFS", "DG", 
    "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR", "DOC", "DOV", "DOW", "DPZ", "DRI", "DTE", 
    "DUK", "DVA", "DVN", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EG", "EIX", "EL", 
    "ELV", "EMN", "EMR", "ENPH", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ERIE", "ES", 
    "ESS", "ETN", "ETR", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F", "FANG", 
    "FAST", "FCX", "FDS", "FDX", "FE", "FFIV", "FI", "FICO", "FIS", "FITB", "FMC", 
    "FOX", "FOXA", "FRT", "FSLR", "FTNT", "FTV", "GD", "GDDY", "GE", "GEHC", "GEN", 
    "GEV", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOG", "GOOGL", "GPC", "GPN", 
    "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD", "HES", "HIG", "HII", 
    "HLT", "HOLX", "HON", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUBB", "HUM", 
    "HWM", "IBM", "ICE", "IDXX", "IEX", "IFF", "INCY", "INTC", "INTU", "INVH", "IP", 
    "IPG", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JBL", "JCI", 
    "JKHY", "JNJ", "JNPR", "JPM", "K", "KDP", "KEY", "KEYS", "KHC", "KIM", "KKR", 
    "KLAC", "KMB", "KMI", "KMX", "KO", "KR", "KVUE", "L", "LDOS", "LEN", "LH", "LHX", 
    "LIN", "LKQ", "LLY", "LMT", "LNT", "LOW", "LRCX", "LULU", "LUV", "LVS", "LW", 
    "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDLZ", 
    "MDT", "MET", "META", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM", "MNST", 
    "MO", "MOH", "MOS", "MPC", "MPWR", "MRK", "MRNA", "MS", "MSCI", "MSFT", "MSI", 
    "MTB", "MTCH", "MTD", "MU", "NCLH", "NDAQ", "NDSN", "NEE", "NEM", "NFLX", "NI", 
    "NKE", "NOC", "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NVR", "NWS", 
    "NWSA", "NXPI", "O", "ODFL", "OKE", "OMC", "ON", "ORCL", "ORLY", "OTIS", "OXY", 
    "PANW", "PARA", "PAYC", "PAYX", "PCAR", "PCG", "PEG", "PEP", "PFE", "PFG", "PG", 
    "PGR", "PH", "PHM", "PKG", "PLD", "PLTR", "PM", "PNC", "PNR", "PNW", "PODD", 
    "POOL", "PPG", "PPL", "PRU", "PSA", "PSX", "PTC", "PWR", "PYPL", "QCOM", "QRVO", 
    "RCL", "REG", "REGN", "RF", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", 
    "RSG", "RTX", "RVTY", "SBAC", "SBUX", "SCHW", "SHW", "SJM", "SLB", "SMCI", "SNA", 
    "SNPS", "SO", "SOLV", "SPG", "SPGI", "SRE", "STE", "STLD", "STT", "STX", "STZ", 
    "SW", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TECH", "TEL", 
    "TER", "TFC", "TFX", "TGT", "TJX", "TMO", "TMUS", "TPL", "TPR", "TRGP", "TRMB", 
    "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTWO", "TXN", "TXT", "TYL", "UAL", 
    "UBER", "UDR", "UHS", "ULTA", "UNH", "UNP", "UPS", "URI", "USB", "V", "VICI", 
    "VLO", "VLTO", "VMC", "VRSK", "VRSN", "VRTX", "VST", "VTR", "VTRS", "VZ", "WAB", 
    "WAT", "WBA", "WBD", "WDC", "WEC", "WELL", "WFC", "WM", "WMB", "WMT", "WRB", 
    "WST", "WTW", "WY", "WYNN", "XEL", "XOM", "XYL", "YUM", "ZBH", "ZBRA", "ZTS"
    ]

    # Function definition for getting historical prices
    def get_historical_price(stock, span):
        # Map span to interval
        span_interval = {
            'day': '5minute', 'week': '5minute', 'month': 'hour', 
            '3month': 'hour', 'year': 'day', '5year': 'week'
        }
        interval = span_interval[span]

        try:
            historical_data = rh.stocks.get_stock_historicals(stock, interval, span, bounds='regular')
            df = pd.DataFrame(historical_data).drop(['volume', 'session', 'interpolated', 'symbol'], axis=1)
            df['begins_at'] = pd.to_datetime(df['begins_at']).dt.tz_convert('US/Eastern').dt.tz_localize(None)
            df.set_index('begins_at', inplace=True)

            df['close_price'] = df['close_price'].astype(float)
            df.rename(columns={'close_price': 'Close'}, inplace=True)

            # Calculate moving averages
            df['MA_100'] = df['Close'].rolling(window=100).mean()
            df['MA_50'] = df['Close'].rolling(window=50).mean()
            df['MA_20'] = df['Close'].rolling(window=20).mean()

            return df.tail(200).copy()

        except Exception as e:
            print(f"Error processing data for {stock}: {e}")
            return None

    watchlist = []

    # Iterate through symbols and filter based on moving averages
    for stock in spy_symbols:
        df_hp = get_historical_price(stock, span='week')
        if df_hp is not None:
            try:
                MA_20 = df_hp['MA_20'].iloc[-1]
                MA_50 = df_hp['MA_50'].iloc[-1]
                MA_100 = df_hp['MA_100'].iloc[-1]

                if MA_20 > MA_100 and MA_50 > MA_100 and MA_20 < MA_50:
                    watchlist.append(stock)
            except Exception as e:
                print(f"Error analyzing {stock}: {e}")

    return watchlist

def open_market():
    market = True    
    time_now = dt.datetime.now().time()
    
    market_open = dt.time(9, 30, 0) #9:30 am
    market_close = dt.time(16, 00, 0) #4:00 pm
    
    if time_now >= market_open and time_now < market_close:
        market = True
    else:
        print('Market Closed')
        pass       
    return (market)

def get_cash():
    rh_cash = rh.account.build_user_profile()
    print("Cash Available to Trade:", rh_cash['cash'])
    cash = float(rh_cash['cash'])
    equity = float(rh_cash['equity'])
    return (cash, equity)

def get_holdings_and_bought_price(stocks):
    # holdings = {stocks[i]: 0 for i in range(0, len(stocks))}
    # bought_price = {stocks[i]: 0 for i in range(0, len(stocks))}
    holdings = {stock: 0 for stock in stocks}
    bought_price = {stock: 0 for stock in stocks}
    rh_holdings = rh.account.build_holdings()
    
    for stock in stocks:
        try:
            # Enable trading fractional quantities
            holdings[stock] = float((rh_holdings[stock]['quantity']))
            bought_price[stocks] = float((rh_holdings[stock]['average_buy_price']))
        except:
            holdings[stock] = 0
            bought_price[stock] = 0
    
    return (holdings, bought_price)

def sell(stock, holdings, price):
    # Enables selling entire holdings at market or limit price
    # sell_price = round((price-0.10), 2)
    sell_order = rh.orders.order_sell_market(symbol=stock, quantity=holdings, timeInForce='gfd')
    # sell_order = rh.orders.order_sell_limit(symbol=stock, 
    #                                          quantity=holdings, 
    #                                          limitPrice=sell_price,
    #                                          timeInForce='gfd')
    print(sell_order)
    # gfd is Good for Day
    print('### Trying to SELL {} at ${}'.format(stock, price))

def buy(stock, allowable_holdings, price):
    # Enables filling entire order at market or limit price
    # buy_price = round((price+0.10), 2)
    buy_order = rh.orders.order_buy_market(symbol=stock, quantity=allowable_holdings, timeInForce='gfd')
    # buy_order = rh.orders.order_buy_limit(symbol=stock, 
    #                                          quantity=allowable_holdings, 
    #                                          limitPrice=buy_price,
    #                                          timeInForce='gfd')
    print(buy_order)
    print('### Trying to BUY {} at ${}'.format(stock, price))

def build_dataframes(df_trades, trade_dict, df_prices, price_dict, df_details, details_dict):
    time_now = str(dt.datetime.now().time())[:8]
    df_trades.loc[time_now] = trade_dict
    df_prices.loc[time_now] =  price_dict
    df_details.loc[time_now] = details_dict
    return df_trades, df_prices, df_details

if __name__ == "__main__":
        
    # Login to Robinhood
    login(days=1)

    stocks = get_stocks()
    print('stocks:', stocks)
    cash, equity = get_cash()
    
    ts = trade_strat.trader(stocks)

    trade_dict = {stocks[i]: 0 for i in range(0, len(stocks))}
    price_dict = {stocks[i]: 0 for i in range(0, len(stocks))}
    details_dict = {stock: "" for stock in stocks}

    df_trades = pd.DataFrame(columns=stocks)
    df_prices = pd.DataFrame(columns=stocks)
    df_details = pd.DataFrame(columns=stocks)


    # Check if market is open
    while open_market():        
        prices = rh.stocks.get_latest_price(stocks)
        print('prices:', prices)
        holdings, bought_price = get_holdings_and_bought_price(stocks)
        print('holdings:', holdings)

        for i, stock in enumerate(stocks):
            # Try Except block to continue if incorrect stock checker is in this list
            try:
                price = float(prices[i])
                print('{} = ${}'. format(stock, price))

                trade, stoploss, target_price = ts.trade_option(stock, price)
                
                # if trade == "BUY":
                #     # allowable_holdings = float(1/price)
                #     allowable_holdings = float((cash/100)/price)
                #     if allowable_holdings > 0 and holdings[stock] == 0:
                #         buy(stock, allowable_holdings, price)    
                                       
                if trade == "BUY":
                    # Calculate allowable holdings with cash and price
                    allowable_holdings = float((cash / 100) / price)
                    
                    # Ensure allowable_holdings has no more than 4 decimal places
                    allowable_holdings = round(allowable_holdings, 4)
                    
                    # Check conditions for buying
                    if allowable_holdings > 0 and holdings[stock] == 0:
                        buy(stock, allowable_holdings, price)

                
                # for stock in holdings:
                if holdings[stock] > 0:  # Check if there are holdings for the stock
                    if price >= target_price or price <= stoploss:  # Check if target or stoploss condition is met
                        trade = "SELL"  
                        sell(stock, holdings[stock], price)
    
                price_dict[stock] = price
                
                if holdings[stock] > 0 and trade != "SELL":
                    trade = "HOLD"
                elif holdings[stock] == 0 and trade != "BUY":
                    trade = "WAIT"
                
                
                # print(f"Trade: {trade}, Stop-loss: {stoploss}, Target Price: {target_price}".format(trade, stoploss, target_price))
                # trade_dict[stock] = trade
                
                details_dict[stock] = f"Trade: {trade}, Stop-loss: {stoploss}, Target Price: {target_price}"
                print(details_dict[stock])
                trade_dict[stock] = trade
         
            except Exception as e:
                print(f"Error processing stock {stock}: {e}")
                continue
    
        # # Once the for loop ends, save the dataframe    
        # df_trades, df_prices = build_dataframes(df_trades, trade_dict, df_prices, price_dict)        
        # print(df_trades)
        # # print(df_prices)
        # time.sleep(30)
        
        # Once the for loop ends, save the dataframe    
        df_trades, df_prices, df_details = build_dataframes(df_trades, trade_dict, df_prices, price_dict, df_details, details_dict)        
        # print(df_trades.tail(1))
        # print(df_details.tail(1))
        time.sleep(30)
    
    # Logout from Robinhood
    # logout()
