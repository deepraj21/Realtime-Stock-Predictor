from flask import Flask, request, jsonify
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
import datetime as dt

app = Flask(__name__)

# Load your trained LSTM model
model = load_model('keras_model.h5')

# Define a function to make predictions using your trained model


def predict_price(ticker):
    # Load historical data for the given ticker
    df = pd.read_csv(
        f'https://finance.yahoo.com/quote/{ticker}/history?p={ticker}')
    # Convert the 'Date' column to a datetime object
    df['Date'] = pd.to_datetime(df['Date'])
    # Sort the dataframe by date in ascending order
    df = df.sort_values('Date')
    # Extract the 'Close' column as a series
    data = df['Close'].values.reshape(-1, 1)
    # Split the data into training and validation sets
    split_index = int(0.8 * len(data))
    train_data = data[:split_index]
    valid_data = data[split_index:]
    # Define the lookback and batch size for the generator
    lookback = 60
    batch_size = 32
    # Create a TimeseriesGenerator for the training data
    train_gen = TimeseriesGenerator(
        train_data, train_data, length=lookback, batch_size=batch_size)
    # Create a TimeseriesGenerator for the validation data
    valid_gen = TimeseriesGenerator(
        valid_data, valid_data, length=lookback, batch_size=batch_size)
    # Make predictions using the validation generator
    predictions = model.predict(valid_gen)
    # Extract the last 60 days of historical data
    last_60_days = data[-lookback:]
    # Create a TimeseriesGenerator for the last 60 days of historical data
    pred_gen = TimeseriesGenerator(
        last_60_days, last_60_days, length=lookback, batch_size=batch_size)
    # Make predictions for the next 30 days using the last 60 days of historical data
    future_predictions = []
    for i in range(30):
        future_pred = model.predict(pred_gen)[0]
        future_predictions.append(future_pred)
        # Shift the predicted value into the next prediction window
        last_60_days = last_60_days[1:]
        last_60_days = np.append(
            last_60_days, future_pred.reshape(1, -1), axis=0)
        pred_gen = TimeseriesGenerator(
            last_60_days, last_60_days, length=lookback, batch_size=batch_size)
    # Format the predictions and return as a list of dictionaries
    prediction_dates = pd.date_range(
        start=df['Date'].iloc[-1], periods=30, freq='D')[1:]
    predictions = [p[0] for p in predictions]
    future_predictions = [p[0] for p in future_predictions]
    predicted_data = [{'date': str(d.date()), 'price': p} for d, p in zip(
        prediction_dates, predictions+future_predictions)]
    return predicted_data


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        ticker = data["ticker"]
        prediction = predict_price(ticker)
        return jsonify({"predictedData": prediction})
    except Exception as e:
        return jsonify({"error": str(e)})
    # ticker = request.json['ticker']
    # predicted_data = predict_price(ticker)
    # return jsonify({'predictions': predicted_data})
