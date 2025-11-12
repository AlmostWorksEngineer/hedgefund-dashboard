import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Hedge Fund Dashboard", layout="wide")

st.title("📈 Hedge Fund Dashboard")
st.write("Welcome! If you can read this, the app is working.")

# ---------- SIDEBAR ----------
st.sidebar.header("🔍 Select Your Companies")
symbols_input = st.sidebar.text_input("Enter 3–5 Stock Symbols (comma separated):", "AAPL,TSLA,GOOGL")
symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]

weeks = st.sidebar.slider("Select number of weeks:", 1, 12, 4)

st.sidebar.markdown("---")
st.sidebar.write("Built by Mridul 🚀")

# ---------- DATE RANGE ----------
end_date = datetime.now()
start_date = end_date - timedelta(weeks=weeks)
st.write(f"### 📅 Data Range: {start_date.date()} → {end_date.date()}")

# ---------- FETCH STOCK DATA ----------
try:
    st.subheader("📊 Fetching Stock Data...")
    data_raw = yf.download(symbols, start=start_date, end=end_date, group_by="ticker", progress=False)

    # CASE 1: If only one ticker
    if len(symbols) == 1:
        if "Adj Close" in data_raw.columns:
            data = data_raw["Adj Close"].to_frame(symbols[0])
        else:
            data = data_raw["Close"].to_frame(symbols[0])

    # CASE 2: If multiple tickers — MultiIndex columns or flat columns
    else:
        if isinstance(data_raw.columns, pd.MultiIndex):
            # Extract Adj Close if exists, otherwise use Close
            data = pd.concat(
                {sym: (data_raw[sym]["Adj Close"] if "Adj Close" in data_raw[sym].columns else data_raw[sym]["Close"])
                 for sym in symbols if sym in data_raw.columns or sym in data_raw.keys()},
                axis=1
            )
        else:
            # Flattened columns
            data = data_raw[[col for col in data_raw.columns if "Close" in col]]

    st.success("✅ Data fetched successfully!")
    st.write("Available Columns:", list(data.columns))

    # ---------- PLOT STOCK PRICES ----------
    st.subheader("📈 Weekly Stock Prices")
    fig, ax = plt.subplots(figsize=(10, 4))
    data.plot(ax=ax)
    ax.set_title("Stock Prices Over Time")
    ax.set_ylabel("Price ($)")
    st.pyplot(fig)

except Exception as e:
    st.error(f"⚠️ Could not fetch stock data: {e}")
    st.stop()

# ---------- SIMULATED SENTIMENT DATA ----------
st.subheader("💬 Weekly Sentiment Summary")

weeks_range = pd.date_range(start=start_date, end=end_date, freq="W")
sentiment_data = pd.DataFrame({
    "Week End": weeks_range,
    "Mean Sentiment (0=Neg,1=Pos)": [0.2, 0.5, 0.8, 0.6][:len(weeks_range)]
})

fig2, ax2 = plt.subplots(figsize=(8, 3))
ax2.bar(sentiment_data["Week End"], sentiment_data["Mean Sentiment (0=Neg,1=Pos)"])
ax2.set_ylim(0, 1)
ax2.set_title("Simulated Weekly News Sentiment")
st.pyplot(fig2)

st.success("🎉 Dashboard loaded successfully! Extend this with live news sentiment later.")
