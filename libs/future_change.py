import streamlit as st
import datetime
import numpy as np
import pandas as pd


def highlight_negative(s):
    return ['color: red;'] * len(s) if s.Change < 0 else ['color: green'] * len(s)


def display_future_change(data, filtered_prediction):
    last_day_price = data[data["ds"] == data["ds"].max()].iloc[0]["y"]
    next_day_price = filtered_prediction[filtered_prediction["ds"] == filtered_prediction["ds"].min()].iloc[0][
        "yhat"]
    last_future_day_price = \
        filtered_prediction[filtered_prediction["ds"] == filtered_prediction["ds"].max()].iloc[0]["yhat"]

    last_day_date = datetime.datetime.date(data["ds"].max())
    next_day_price_date = datetime.datetime.date(filtered_prediction["ds"].min())
    last_future_day_price_date = datetime.datetime.date(filtered_prediction["ds"].max())

    next_day_change = next_day_price - last_day_price
    next_day_change_percentage = (next_day_change / last_day_price) * 100

    future_day_change = last_future_day_price - last_day_price
    future_day_change_percentage = (future_day_change / last_day_price) * 100

    df_future_change = pd.DataFrame(
        np.array([[next_day_price_date, float(next_day_price), float(next_day_change), float(next_day_change_percentage)],
                  [last_future_day_price_date, float(last_future_day_price), float(future_day_change),
                   float(future_day_change_percentage)]]),
        columns=['Date', 'New Price', 'Change', 'Change %'])

    df_future_change = df_future_change.style.format({"New Price": "{:.2f}",
                                                      "Change": "{:.2f}",
                                                      "Change %": "{:.2f}%"}) \
        .apply(highlight_negative, axis=1)
    st.write(f"Base line ({last_day_date}): {last_day_price:,.2f}")
    st.write(df_future_change)