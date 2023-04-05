import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import pandas_datareader as data
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import plotly.graph_objs as go
import plotly.express as px

start = '2010-01-01'
end = '2023-03-31'


def main():
    st.set_page_config(page_title="My Streamlit App",
                       page_icon=":guardsman:")

    # Create a list of pages
    pages = {
        "Home": page_home,
        "About": page_about,
        "Contact": page_contact
    }

    # Create a sidebar menu
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Display the selected page
    page = pages[selection]
    page()


def page_home():
    st.title("Home Page")
    st.write("Welcome to my Streamlit app!")


def page_about():
    st.title("About Page")
    st.write("This is the about page.")


def page_contact():
    st.title("Contact Page")
    st.write("This is the contact page.")


if __name__ == "__main__":
    main()

css = '''
h1 {
    color: blue;
    font-size: 50px;
    
}

p {
    color: red;
    font-size: 20px;
}

.sidebar .sidebar-content {
    background-color: #333;
    color: white;
}

.sidebar .sidebar-title, .sidebar .sidebar-item {
    color: white;
}

.main {
    # background-color: #eee;
    padding: 20px;
}
'''

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


# st.set_page_config(layout="wide")
st.title("Stock Trend Prediction")

user_input = st.text_input('Enter the stock Ticker', 'AAPL')
df = yf.download(user_input, start, end)

st.subheader('Data from 2010 - 2023')
st.write(df.describe())

st.subheader('Closing Price vs Time Chart')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines'))
fig.update_layout(title='Closing Price vs Time Chart',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  width=1200,
                  height=600)
st.plotly_chart(fig)

st.subheader('Closing Price vs Time Chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name='MA100'))
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Close'))
fig.update_layout(title='Closing Price vs Time Chart with 100MA',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  width=1200,
                  height=600)
st.plotly_chart(fig)

st.subheader('Closing Price vs Time Chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name='MA100'))
fig.add_trace(go.Scatter(x=df.index, y=ma200, mode='lines', name='MA200'))
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Close'))
fig.update_layout(title='Closing Price vs Time Chart with 100MA & 200MA',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  width=1200,
                  height=600)
st.plotly_chart(fig)

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
fig2.update_layout(title='Original VS predicted',
                   xaxis_title='Date',
                   yaxis_title='Price',
                   width=1200,
                   height=600)

st.plotly_chart(fig2)
