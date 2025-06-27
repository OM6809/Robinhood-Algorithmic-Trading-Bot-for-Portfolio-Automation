import robin_stocks.robinhood as rh
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

rh.authentication.login(username=None, 
                        password=None, 
                        expiresIn=86400, scope='internal', 
                        by_sms=True, 
                        store_session=True, 
                        mfa_code=None, 
                        pickle_name='')


# Example: Fetch historical data for TSLA
historical_data = rh.stocks.get_stock_historicals('TSLA', interval='5minute', span='week', bounds='regular')
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
df_tail = df.tail(200).copy()

# Rename columns to match mplfinance requirements
df_tail.rename(columns={
    'open_price': 'Open', 
    'close_price': 'Close', 
    'high_price': 'High', 
    'low_price': 'Low'
}, inplace=True)

# Calculate moving averages
df_tail['MA_100'] = df_tail['Close'].rolling(window=100).mean()
df_tail['MA_50'] = df_tail['Close'].rolling(window=50).mean()
df_tail['MA_20'] = df_tail['Close'].rolling(window=20).mean()

print('data: \n', df_tail.tail(2))

# Extract the last two rows of the DataFrame for analysis
row_1 = df_tail.iloc[-2]
row_2 = df_tail.iloc[-1]

# Initialize variables
i1 = None
i2 = None
trade = None

# Trading strategy logic
if row_1['MA_20'] < row_1['MA_50']:  # Condition in row 1
    if row_2['MA_20'] > row_2['MA_50']:  # Condition in row 2
        if row_2['MA_20'] > row_2['MA_100']:  # Condition in row 2
            i1 = "BUY"
            entry_point = row_2['High']  # Entry point is the 'High' of row 2
            print(f"i1 signal: {i1}, Entry Point: {entry_point}")

# Assume current_price is available
current_price = 338.00  # Replace with actual current price

if i1 == "BUY" and current_price > entry_point:  # Confirmation signal
    i2 = "BUY"
    print(f"i2 signal: {i2}")

# Final trade decision
if i1 == "BUY" and i2 == "BUY":
    trade = "BUY"
    stoploss = row_2['MA_50']  # Stop-loss is MA_50 of row 2
    target_price = entry_point + (entry_point - stoploss)  # Calculate target price
    print(f"Trade: {trade}, Stop-loss: {stoploss}, Target Price: {target_price}")
else:
    trade = "HOLD"
    print(f"Trade: {trade}")

# Generate the candlestick chart and return the figure and axes
fig, axlist = mpf.plot(
    df_tail,
    type='candle',
    style='yahoo',
    title='TSLA Candlestick Chart with Moving Averages',
    ylabel='Price',
    volume=False,
    mav=(20, 50, 100),  # Add moving averages
    mavcolors=['blue', 'green', 'red'],  # Specify colors for 20, 50, and 100 MAs
    show_nontrading=False,
    returnfig=True
)

# Add color-coded text to the top-left corner of the main chart    
axlist[0].text(
    0.01, 0.99, "20 MA (Blue)", transform=axlist[0].transAxes, fontsize=10,
    color='blue', verticalalignment='top', horizontalalignment='left'
)
axlist[0].text(
    0.01, 0.95, "50 MA (Green)", transform=axlist[0].transAxes, fontsize=10,
    color='green', verticalalignment='top', horizontalalignment='left'
)
axlist[0].text(
    0.01, 0.91, "100 MA (Red)", transform=axlist[0].transAxes, fontsize=10,
    color='red', verticalalignment='top', horizontalalignment='left'
)
# Show the plot using plt.show()
plt.show()

