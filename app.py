import streamlit.components.v1 as components
from keras.models import load_model
import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import pandas_datareader as data
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import plotly.graph_objs as go
import plotly.express as px
import requests
from datetime import datetime
from streamlit_lottie import st_lottie
from yfinance import shared


start = '2010-01-01'
end = datetime.now()


def main():
    st.set_page_config(page_title="Predictbay",page_icon=":chart_with_upwards_trend:" ,layout="wide")

if __name__ == "__main__":
    main()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

css = '''
h1 {
    color: white;
    font-size: 50px;
    align: center;
    
}

p {
    color: white;
    font-size: 20px;
}

.sidebar .sidebar-content {
    background-color: #333;
    color: white;
}

.sidebar .sidebar-title, .sidebar .sidebar-item {
    color: white;
}
body {
    font-family: SaxMono;
    # font-size: 16px;
}
.stTextInput > div > div > input {
    width: 300px;
}
.main {
    # background-color: #eee;
    padding: 20px;
}
'''
class InvalidTickerError(Exception):
    pass
def get_data(ticker, start_data, end_date):
    try:
        df = yf.download(ticker, start=start_data, end=end_date)
        if df.empty:
            raise InvalidTickerError(f"Invalid ticker: {ticker}")
        return df
    except Exception as e:
        raise InvalidTickerError(f"Invalid ticker: {ticker}") from e


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_stocks = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_kuhijlvx.json")
lottie_stocks2 = load_lottieurl("https://assets5.lottiefiles.com/private_files/lf30_F3v2Nj.json")
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


# st.set_page_config(layout="wide")
st.title(':chart_with_upwards_trend: Predictbay')
st.subheader('Welcome to our _Stocks Prediction_ WebApp')
st.markdown("<a href='https://github.com/deepraj21/Realtime-Stock-Predictor'><img src='https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'></a>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
left_col, right_col = st.columns(2)
with left_col:
    st.subheader('- Project Description')
    st.markdown("<p style= font-size:19px;>This is a Python script for a web application that uses deep learning techniques to predict stock prices. The script uses the Keras library for deep learning, Streamlit for the web interface, Pandas and Pandas Datareader for data handling, Plotly for data visualization, and requests for HTTP requests.</p>", unsafe_allow_html=True)
    st.markdown("<p style= font-size:19px;>The application displays general information about the stock market, including how it works, and allows users to enter a stock ticker to retrieve historical data from Yahoo Finance. The data is then used to generate charts displaying the stock's closing price over time, as well as charts with moving averages to provide a more comprehensive analysis of the stock's performance.</p>", unsafe_allow_html=True)
    st.markdown("<p style= font-size:19px;>The application uses a deep learning model to predict future stock prices based on historical data. The model is trained on a dataset of historical stock prices and is loaded into the application using Keras. The predicted values are then plotted alongside the historical data to provide users with a visual representation of the predicted trend.</p>", unsafe_allow_html=True)
    st.markdown("<p style= font-size:19px;>The web application also includes interactive elements, such as text input fields and lottie animations, to make the user experience more engaging. The app is responsive and can be accessed on different devices.</p>", unsafe_allow_html=True)
# Add a stock image in the right column
with right_col:
    st_lottie(lottie_stocks)
st.markdown("<hr>",unsafe_allow_html=True)
st.subheader("- What is the stock market?")
st.write("The stock market is a place where publicly traded companies' stocks or shares are bought and sold. Investors purchase stocks in the hope of making a profit, either by selling them at a higher price or by earning dividends on their investment.")
st.subheader("- How does the stock market work?")
st.write("Companies issue stocks when they want to raise capital, or money, to fund their operations or expansion plans. These stocks are then traded on stock exchanges, which are platforms where buyers and sellers can trade stocks.")
st.write("The price of a stock is determined by supply and demand. If there are more buyers than sellers, the price of the stock goes up. If there are more sellers than buyers, the price of the stock goes down.")

st.markdown("<br><br>",unsafe_allow_html=True)

col1,col2 =st.columns(2)
with col1:
    st_lottie(lottie_stocks2)   
with col2:
    user_input = st.text_input('Enter a Valid stock Ticker', 'AAPL')
    try:
        df = get_data(user_input, start, end)
        st.subheader('Data from 2010 - 2023')
        st.write(df.describe())
    except InvalidTickerError as e:
        st.markdown("<p style= color:red;>Invalid ticker! Please enter a valid ticker.</p>",unsafe_allow_html=True)
    except ValueError:
        st.markdown("<p style= color:red;>Invalid ticker! Please enter a valid ticker.</p>", unsafe_allow_html=True)


try:
    st.subheader('- Closing Price')
    st.write("The closing price is reported by stock exchanges at the end of each trading day and is widely available through financial news outlets, online trading platforms, and other financial resources. It is important for investors to keep track of the closing price of stocks they are interested in to make informed investment decisions.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines'))
    fig.update_layout(title='Closing Price vs Time Chart',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    width=1000,
                    height=600)
    st.plotly_chart(fig, use_container_width=True)

    c1,c2=st.columns(2)

    with c1:
        ma100 = df.Close.rolling(100).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name='MA100'))
        fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Close'))
        fig.update_layout(title='Closing Price vs Time Chart with 100MA',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    width=1000,
                    height=600)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ma100 = df.Close.rolling(100).mean()
        ma200 = df.Close.rolling(200).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name='MA100'))
        fig.add_trace(go.Scatter(x=df.index, y=ma200, mode='lines', name='MA200'))
        fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Close'))
        fig.update_layout(title='Closing Price vs Time Chart with 100MA & 200MA',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    width=1000,
                    height=600)
        st.plotly_chart(fig, use_container_width=True)


    data_training = pd.DataFrame(df['Close'][0:int(len(df)*70)])
    data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

    scaler = MinMaxScaler(feature_range=(0, 1))

    data_training_array = scaler.fit_transform(data_training)

    x_train = []
    y_train = []

    for i in range(100, data_training_array.shape[0]):
        x_train.append(data_training_array[i-100: i])
        y_train.append(data_training_array[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    # load model
    model = load_model('keras_model.h5')

    past_100_days = data_training.tail(100)

    final_df = past_100_days.append(data_testing, ignore_index=True)

    input_data = scaler.fit_transform(final_df)

    x_test = []
    y_test = []

    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100:i])
        y_test.append(input_data[i, 0])

    x_test, y_test = np.array(x_test), np.array(y_test)

    y_predict = model.predict(x_test)

    scaler = scaler.scale_

    scale_factor = 1/scaler[0]
    y_predict = y_predict * scale_factor
    y_test = y_test * scale_factor

    st.subheader('Original VS predicted')
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df.index[int(len(df)*0.70):], y=y_test, name='Original Price'))
    fig2.add_trace(go.Scatter(x=df.index[int(len(df)*0.70):], y=y_predict[:, 0], name='Predict'))
    fig2.update_layout(
                    xaxis_title='Date',
                    yaxis_title='Price',
                    width=1000,
                    height=600)

    st.plotly_chart(fig2, use_container_width=True)

    last_100_days = data_testing[-100:].values

    # Instantiate a scaler object and fit_transform the data
    scaler = MinMaxScaler()
    last_100_days_scaled = scaler.fit_transform(last_100_days)

    # Create an empty list to store the predicted prices
    predicted_prices = []

    # Make predictions for the next day using the last 100 days of data
    for i in range(1):
        X_test = np.array([last_100_days_scaled])
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predicted_price = model.predict(X_test)
        predicted_prices.append(predicted_price)
        last_100_days_scaled = np.append(last_100_days_scaled, predicted_price)
        last_100_days_scaled = np.delete(last_100_days_scaled, 0)

    # Invert the scaling of the predicted price
    predicted_prices = np.array(predicted_prices)
    predicted_prices = predicted_prices.reshape(
        predicted_prices.shape[0], predicted_prices.shape[2])
    predicted_prices = scaler.inverse_transform(predicted_prices)

    st.header('- Prediction')
    st.write('Predicted price for the next day:', predicted_prices[0][0])
except InvalidTickerError as e:
    st.write(e)
except:
    st.write('\n')

st.markdown("<hr>", unsafe_allow_html=True)

st.header("- About US")

col1,padding, col2 = st.columns((10,2,10))
with col1:
    st.subheader(':chart_with_upwards_trend: Predictbay')
    st.markdown("<p style= font-size:18px; >Looking to stay one step ahead of the stock market game? Look no further than our cutting-edge stock market prediction project! Using advanced algorithms and time-series data analysis, our platform provides predictions on stock prices, along with clear, easy-to-read graphs that make it simple to understand market trends. Simply enter your desired ticker symbol and watch as our platform works its magic, delivering accurate insights into future stock prices that you can rely on. Stay ahead of the curve and make informed investment decisions with our stock market prediction project.</p>", unsafe_allow_html=True)

with col2:
    st.subheader('Our Team')
    cols1,cols2,cols3,cols4=st.columns(4)
    with cols1:
        st.markdown("<p style= font-size:16px;>Deepraj Bera</p><p style= font-size:10px;>Full stack Web Developer</p><a href='https://github.com/deepraj21'><img src='https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'></a>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style= font-size:16px;>Abhishek Mallick</p><p style= font-size:10px;>ML | Full stack</p><a href='https://github.com/Abhishek-Mallick'><img src='https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'></a>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    with cols2:
        st.markdown("<p style= font-size:16px;>Mayukh Mondal</p><p style= font-size:10px;>Python | DevOps</p><a href='https://github.com/Mayukh026'><img src='https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'></a>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style= font-size:16px;>Harshit Mania</p><p style= font-size:10px;>React Developer</p><a href='https://github.com/Harshitm14'><img src='https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'></a>", unsafe_allow_html=True)
      

st.markdown("<br><br>",unsafe_allow_html=True)
st.markdown("<center><p>© 2023 Predictbay</p><center>",unsafe_allow_html=True)
