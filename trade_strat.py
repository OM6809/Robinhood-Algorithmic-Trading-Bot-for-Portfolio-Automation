import pandas as pd
import robin_stocks.robinhood as rh

class trader:
    def __init__(self, stocks):
        self.stocks = stocks
        # self.run_time = 0
        self.buffer = 0.005  # 0.5%
        self.last_target = {stock: None for stock in stocks}
        self.last_stoploss = {stock: None for stock in stocks}
        
    def get_historical_prices(self, stock, span):
        span_interval = {'day': '5minute', 'week': '5minute', 'month': 'hour', '3month': 'hour', 'year': 'day', '5year': 'week'}
        interval = span_interval[span]
        
        historical_data = rh.stocks.get_stock_historicals(stock, interval, span, bounds='regular') 
        # bounds = 'regular' for all spans except day and 'extended' for span = day
        
        df = pd.DataFrame(historical_data)
        df = df.drop(['volume', 'session', 'interpolated', 'symbol'], axis=1)

        # Convert 'begins_at' to datetime and then to Eastern Standard Time
        df['begins_at'] = pd.to_datetime(df['begins_at'])
        df['begins_at'] = df['begins_at'].dt.tz_convert('US/Eastern')
        df['begins_at'] = df['begins_at'].dt.tz_localize(None)
        df.set_index('begins_at', inplace=True)

        # Convert price columns to float and volume to int
        price_columns = ['open_price', 'close_price', 'high_price', 'low_price']
        df[price_columns] = df[price_columns].astype(float)

        # Create a new DataFrame for the last 200 rows to avoid slicing issues
        df_price = df.tail(200).copy()

        # Rename columns to match mplfinance requirements
        df_price.rename(columns={
            'open_price': 'Open', 
            'close_price': 'Close', 
            'high_price': 'High', 
            'low_price': 'Low'
        }, inplace=True)

        # Calculate moving averages 
        df_price['MA_100'] = df_price['Close'].rolling(window=100).mean()
        df_price['MA_50'] = df_price['Close'].rolling(window=50).mean()
        df_price['MA_20'] = df_price['Close'].rolling(window=20).mean()

        # Extract the last two rows of the DataFrame for analysis
        # print('data: \n', df_price.tail(2))
        return(df_price.tail(2))
    
    def get_trade_signal(self, df_prices):
        # Last two rows represent the last two candlesticks
        row_1 = df_prices.iloc[-2]
        row_2 = df_prices.iloc[-1]
        
        # Initialize variables
        i1 = None
        entry_point = None
        
        # Trading strategy logic
        if row_1['MA_20'] < row_1['MA_50']:  # Condition in row 1
            print('2nd last candle: MA 20 < MA_50')
            if row_2['MA_20'] > row_2['MA_50']:  # Condition in row 2
                print('last candle: MA 20 > MA_50')
                if row_2['MA_20'] > row_2['MA_100']:  # Condition in row 2
                    print("Buy signal!")
                    i1 = "BUY"
                    entry_point = row_2['High']  # Entry point is the 'High' of row 2
                    print(f"i1 signal: {i1}, Entry Point: {entry_point}")            
        return(i1, entry_point)
        
    def get_trade_confirmation(self, current_price, entry_point):
        # Initialize variables
        i2 = None
        if current_price < entry_point:  # Confirmation signal
            i2 = "BUY"
            print(f"i2 signal: {i2}")
        return(i2)
    
    def get_target(self, df_prices, entry_point):
        if entry_point is None:
            return None
        row_2 = df_prices.iloc[-1]
        stoploss = row_2['MA_50']  # Stop-loss is MA_50 of row
        target = entry_point + (2 * (entry_point - stoploss))  # Calculate target price
        return(target)
    
    def get_stoploss(self, df_prices, entry_point):
        if entry_point is None:
            return None
        row_2 = df_prices.iloc[-1]
        stoploss = row_2['MA_50']  # Stop-loss is MA_50 of row 2
        return(stoploss)
        
    def trade_option(self, stock, price):
        # if self.run_time % 5 == 0:
        df_historical_prices = self.get_historical_prices(stock, span='week')
        
        i1, entry_point = self.get_trade_signal(df_historical_prices)
        
        if i1 == "BUY" and self.get_trade_confirmation(price, entry_point) == "BUY":
            print(i1)
            trade = "BUY"
            target = self.get_target(df_historical_prices, entry_point)
            stoploss = self.get_stoploss(df_historical_prices, entry_point)
            self.last_target[stock] = target
            self.last_stoploss[stock] = stoploss
        else:
            trade = "HOLD"
            target = self.last_target.get(stock)
            stoploss = self.last_stoploss.get(stock)
        
        return trade, stoploss, target
        
# 9 & 20 ema strategy
# rsi
