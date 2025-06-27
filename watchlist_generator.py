import robin_stocks.robinhood as rh
import config
import pandas as pd


time_logged_in = 60*60*24
rh.authentication.login(username=config.USERNAME, 
                        password=config.PASSWORD,
                        expiresIn=time_logged_in, 
                        scope='internal', 
                        by_sms=True, 
                        store_session=True, 
                        mfa_code=None, 
                        pickle_name='')


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
def get_historical_prices(stock, span):
    span_interval = {'day': '5minute', 'week': '5minute', 'month': 'hour', '3month': 'hour', 'year': 'day', '5year': 'week'}
    interval = span_interval[span]

    historical_data = rh.stocks.get_stock_historicals(stock, interval, span, bounds='regular') 
    df = pd.DataFrame(historical_data)
    df = df.drop(['volume', 'session', 'interpolated', 'symbol'], axis=1)

    # Convert 'begins_at' to datetime and then to Eastern Standard Time
    df['begins_at'] = pd.to_datetime(df['begins_at'])
    df['begins_at'] = df['begins_at'].dt.tz_convert('US/Eastern')
    df['begins_at'] = df['begins_at'].dt.tz_localize(None)
    df.set_index('begins_at', inplace=True)

    # Convert price columns to float
    price_columns = ['close_price']
    df[price_columns] = df[price_columns].astype(float)

    # Create a new DataFrame for the last 200 rows to avoid slicing issues
    df_price = df.tail(200).copy()

    # Rename columns to match mplfinance requirements
    df_price.rename(columns={
        'close_price': 'Close', 
    }, inplace=True)

    # Calculate moving averages
    df_price['MA_100'] = df_price['Close'].rolling(window=100).mean()
    df_price['MA_50'] = df_price['Close'].rolling(window=50).mean()
    df_price['MA_20'] = df_price['Close'].rolling(window=20).mean()

    return df_price.tail(2).head(1)

# Initialize the watchlist
stocks = []

# Loop through the list of stocks
for stock in spy_symbols:
    try:
        # print(f"Fetching data for {stock}...")
        df_hp = get_historical_prices(stock, span='week')

        # Extract values for the moving averages
        MA_20 = df_hp['MA_20'].iloc[0]
        MA_50 = df_hp['MA_50'].iloc[0]
        MA_100 = df_hp['MA_100'].iloc[0]

        # Check conditions
        if MA_20 > MA_100 and MA_50 > MA_100 and MA_20 < MA_50:
            stocks.append(stock)

    except Exception as e:
        print(f"Error fetching data for {stock}: {e}")

# Print the watchlist
# print("Watchlist:", watchlist)
        

