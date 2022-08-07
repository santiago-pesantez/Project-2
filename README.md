# Crypto Bros Robo Forecaster

---

## Background
The Crypto Bros Robo Forecaster is a publicly accessible Facebook Messenger Robo Advisor which uses sentiment analysis of Twitter data and machine learning to forecast predictions on the price and profits of the user’s desired cryptocurrency.

---

## Demo

### Users may interact with the Crypto Bros Robo Forecaster via [Facebook Page](https://www.facebook.com/crypto.bros.robo.forecaster) or [Facebook Messenger](https://m.me/crypto.bros.robo.forecaster)

---

## Technologies

1. Facebook Page: The interface which makes the Robo Advisor accessible to users
2. Facebook App: The application that passes input from page to AWS
3. AWS Lex: Creates the intent, accepts input and returns outputs
4. AWS Lambda: The core functionality that processes input from Lex and returns results to Lex
5. Twitter App: Performs sentiment analysis on user's desired cryptocurrency
6. Facebook Prophet: Forecasts the future prices of user's desired cryptocurrency

---

## Installation

```sh
git clone git@github.com:santiago-pesantez/Project-2.git
cd Project-2
pip install -r requirements.txt
```

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
