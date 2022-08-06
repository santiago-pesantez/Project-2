def forecaster(): # TODO Decide whether code will load a csv or be given parameter 

    # importing libraries and dependecies
    import pandas as pd
    from pathlib import Path
    from fbprophet import Prophet
    #import numpy as np
    import os
    from dotenv import load_dotenv
    import alpaca_trade_api as tradeapi

    # Pulling Api Keys and creating environment
    load_dotenv()
    alpaca_api_key = os.getenv('ALPACA_API_KEY')
    alpaca_secret_key = os.getenv('ALPACA_SECRET_KEY')
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version='v2'
    )

    # Reading tweet sentiment from csv created by twf_v2
    tweets_df = pd.read_csv(
        Path('stock_market_crash_2022.csv'),
        index_col='created_at',
        infer_datetime_format=True,
        parse_dates=True
    )
    tweets_df.index = tweets_df.index.date

    # creating dataframe including sentiment from tweets
    sentiment_df = pd.DataFrame()
    sentiment_df['sentiment'] = tweets_df[['text_sentiment']]

    # Encoding sentiment
    sentiment_ordering = ['Negative', 'Neutral', 'Positive']
    sentiment_df['sentiment'] = sentiment_df['sentiment'].apply(lambda x: sentiment_ordering.index(x))

    # Pulling average sentiment for each day
    sentiment_df['date'] = pd.to_datetime(sentiment_df.index)
    sentiment_df = sentiment_df.groupby(sentiment_df.date.dt.date).mean()

    # Forecasting sentiment for days_out period
    sentiment_data = sentiment_df.reset_index()[['date', 'sentiment']].rename({'date':'ds','sentiment':'y'},axis='columns')
    sentiment_model = Prophet(yearly_seasonality=True,daily_seasonality=True)
    sentiment_model.fit(sentiment_data)
    future = sentiment_model.make_future_dataframe(periods=60, freq='d')
    sentiment_forecast = sentiment_model.predict(future)

    # Creating dataframe from forecast to be used in the future
    sentiment_predicted = pd.DataFrame()
    sentiment_predicted['ds'] = future['ds'].loc[((sentiment_data.index.max() +1)):(future.index.max())]
    sentiment_predicted['sentiment'] = sentiment_forecast['yhat'].loc[((sentiment_data.index.max() +1)):(future.index.max())]

    # Setting variables for crypto API, then pulling and formatting data
    ticker = 'BTCUSD'
    start_date = sentiment_data['ds'].min()
    end_date = sentiment_data['ds'].max()
    timeframe = '1Day'
    crypto_df = alpaca.get_crypto_bars(
        ticker,
        timeframe,
        start_date,
        end_date,
        limit = 10000,
        exchanges = 'CBSE'
        ).df
    crypto_df = crypto_df[['close']]
    crypto_df.index = crypto_df.index.date
    # Creating features dataframe for price forecaster
    features_df = pd.concat([sentiment_df, crypto_df], axis=1).reset_index()[['index', 'sentiment', 'close']].rename({'index':'ds','close':'y','sentiment':'sentiment'},axis='columns')

    # Creating price model
    price_model = Prophet(yearly_seasonality=True,daily_seasonality=True)
    price_model.add_regressor('sentiment')
    price_model.fit(features_df)

    # Forecasting closing price based off predicted sentiments
    price_forecast = price_model.predict(sentiment_predicted)

    #Pulling starting price and final forecasted price of crypto
    starting_price = features_df.loc[(features_df.index.max()), 'y']
    final_price = price_forecast.loc[(price_forecast.index.max()), 'yhat']

    print(final_price)
    print(starting_price)

    # # Returning needed variables
    # return starting_price, final_price

forecaster()