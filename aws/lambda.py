import json
### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests
from datetime import date
#from fbprophet import Prophet
#import code

alpaca_symbols = {"AAVEUSD": "AAVE","ALGOUSD": "ALGO","BATUSD": "BAT","BTCUSD": "BTC","BCHUSD": "BCH","LINKUSD": "LINK","DAIUSD": "DAI","DOGEUSD": "DOGE","ETHUSD": "ETH","GRTUSD": "GRT","LTCUSD": "LTC","MKRUSD": "MKR","MATICUSD": "MATIC","NEARUSD": "NEAR","PAXGUSD": "PAXG","SHIBUSD": "SHIB","SOLUSD": "SOL","SUSHIUSD": "SUSHI","USDTUSD": "USDT","TRXUSD": "TRX","UNIUSD": "UNI","WBTCUSD": "WBTC","YFIUSD": "YFI"}
symbols_to_alpaca = {"AAVE": "AAVEUSD","ALGO": "ALGOUSD","BAT": "BATUSD","BTC": "BTCUSD","BCH": "BCHUSD","LINK": "LINKUSD","DAI": "DAIUSD","DOGE": "DOGEUSD","ETH": "ETHUSD","GRT": "GRTUSD","LTC": "LTCUSD","MKR": "MKRUSD","MATIC": "MATICUSD","NEAR": "NEARUSD","PAXG": "PAXGUSD","SHIB": "SHIBUSD","SOL": "SOLUSD","SUSHI": "SUSHIUSD","USDT": "USDTUSD","TRX": "TRXUSD","UNI": "UNIUSD","WBTC": "WBTCUSD","YFI": "YFIUSD"}
name_to_alpaca={"AAVE" :"AAVEUSD","ALGORAND" :"ALGOUSD","BASIC ATTENTION TOKEN" :"BATUSD","BITCOIN" :"BTCUSD","BITCOIN CASH" :"BCHUSD","CHAINLINK TOKEN" :"LINKUSD","DAI" :"DAIUSD","DOGECOIN" :"DOGEUSD","ETHEREUM" :"ETHUSD","GRAPH TOKEN" :"GRTUSD","LITECOIN" :"LTCUSD","MAKER" :"MKRUSD","MATIC" :"MATICUSD","NEAR PROTOCOL" :"NEARUSD","PAX GOLD" :"PAXGUSD","SHIBA INU" :"SHIBUSD","SOLANA" :"SOLUSD","SUSHI" :"SUSHIUSD","TETHER" :"USDTUSD","TRON" :"TRXUSD","UNISWAP PROTOCOL TOKEN" :"UNIUSD","WRAPPED BTC" :"WBTCUSD","YEARN FINANCE" :"YFIUSD"}

def parse_ticker_to_alpaca(ticker):
    """
    Converts a ticker (user input) to an Alpaca supported symbol.
    """
    ticker = ticker.upper()
    if ticker in alpaca_symbols:
        return ticker
    elif ticker in symbols_to_alpaca:
        return symbols_to_alpaca[ticker]
    elif ticker in name_to_alpaca:
        return name_to_alpaca[ticker]
    return ""

### Functionality Helper Functions ###
def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")


def get_btcprice():
    """
    Retrieves the current price of bitcoin in dollars from the alternative.me Crypto API.
    """
    bitcoin_api_url = "https://api.alternative.me/v2/ticker/bitcoin/?convert=USD"
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    price_dollars = parse_float(response_json["data"]["1"]["quotes"]["USD"]["price"])
    return price_dollars


def get_fg_index():
    """
    Retrieves the current Bitcoin Fear & Greed Index from the alternative.me Crypto API.
    """
    fgi_url = "https://api.alternative.me/fng/"
    response = requests.get(fgi_url)
    response_json = response.json()
    fg_index = parse_float(response_json["data"][0]["value"])
    return fg_index

def get_date_and_price(alpaca_ticker, forecast_days):
    '''
    Gets the information from our prediction model and returns the best date and the ticker price for t
    '''
    predicted_price = 100000
    future_date = "2023-10-21"
    return future_date, predicted_price

def calculate_gains(alpaca_ticker, dollars, future_price):
    '''
    Gets the information from our prediction model and returns the best date and the ticker price for t
    '''
    current_ticker_price = get_ticker_price(alpaca_ticker)
    tickers = dollars/current_ticker_price
    return future_price * tickers

def get_ticker_price(alpaca_ticker):
    """
    Retrieves the current price of the ticker in dollars from the Alpaca Crypto API.
    """
    return 100


def get_recommendation(ticker, dollars, forecast):
    """
    Returns a buying recommendation based on the value of the ticker, and the model's prediction.
    """

    alpaca_ticker = parse_ticker_to_alpaca(ticker)
    future_date, future_price = get_date_and_price(alpaca_ticker, forecast)
    predicted_gains = calculate_gains(alpaca_ticker, dollars, future_price)

    recommendation = """It might be a good time to buy {} on {}, because your {} could turn into {}""".format(ticker, future_date, dollars, predicted_gains)

    return recommendation


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Defines an internal validation message structured as a python dictionary.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


def validate_data(ticker, intent_request):
    """
    Validates the data provided by the user.
    """

    # Validate the ticker, it should be one of the supported tickers of alpaca
    if ticker is not None:
        ticker = parse_ticker_to_alpaca(
            ticker
        )  # Since parameters are strings it's important to cast values
        if ticker == '':
            return build_validation_result(
                False,
                "ticker",
                "Unfortunately this ticker not supported. "
                "List of supported tickers: Aave, Algorand,Basic Attention Token, Bitcoin, Bitcoin Cash, ChainLink Token, Dai, Dogecoin, Ethereum, Graph Token, Litecoin, Maker, Matic, Near Protocol, PAX Gold, Shiba Inu, Solana, Sushi, Tether, Tron, Uniswap Protocol Token, Wrapped BTC, Yearn Finance",
            )

    # Data valid if the ticker is valid
    return build_validation_result(True, None, None)


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def make_prediction(intent_request):
    """
    Performs dialog management and fulfillment for obtaining the ticker, amount and period of time.
    """

    # Gets slots' values
    ticker = get_slots(intent_request)["ticker"]
    forecast = get_slots(intent_request)["forecast"]
    dollars = get_slots(intent_request)["amount"]

    # Gets the invocation source, for Lex dialogs "DialogCodeHook" is expected.
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(ticker, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the current price of the ticker in dollars and make the conversion from dollars to ticker.

    dollars_parsed = parse_float(dollars)
    forecast_parsed = parse_float(forecast)
    alpaca_ticker = parse_ticker_to_alpaca(ticker)
    ticker_value = dollars_parsed / get_ticker_price(alpaca_ticker)
    ticker_value = round(ticker_value,4)

    # Return a message with conversion's result.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"Thank you for your information. At this time, you can get {ticker_value} {ticker} for your ${dollars} dollars. {get_recommendation(ticker, dollars_parsed, forecast_parsed)}"
        },
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # Get the name of the current intent
    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "Main":
        return make_prediction(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)

