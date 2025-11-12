import streamlit as st

st.set_page_config(page_title="Hedge Fund Dashboard", layout="wide")

st.title("📈 Hedge Fund Dashboard")
st.write("Welcome! If you can read this, the app is working.")
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# ---------- PAGE TITLE ----------
st.set_page_config(page_title="Stock & Sentiment Dashboard", layout="wide")
st.title("📊 Stock & News Sentiment Tracker")

# ---------- SIDEBAR ----------
st.sidebar.header("🔍 Select Your Companies")
symbols = st.sidebar.text_input("Enter 3–5 Stock Symbols (comma separated):", "AAPL,TSLA,GOOGL")
symbols = [s.strip() for s in symbols.split(",")]

weeks = st.sidebar.slider("Select number of weeks:", 1, 12, 4)

st.sidebar.markdown("---")
st.sidebar.write("Built by Mridul 🚀")

# ---------- DATA FETCHING ----------
end_date = datetime.now()
start_date = end_date - timedelta(weeks=weeks)

st.write(f"### 📅 Data Range: {start_date.date()} → {end_date.date()}")

# ---------- FETCH STOCK DATA ----------
data = yf.download(symbols, start=start_date, end=end_date, group_by='ticker')

# Extract Adj Close prices safely
if isinstance(symbols, str):
    data = data["Adj Close"]
else:
    # For multiple tickers, make a combined DataFrame
    data = pd.concat({sym: data[sym]["Adj Close"] for sym in symbols}, axis=1)

if isinstance(data, pd.Series):
    data = data.to_frame()

# ---------- PLOT STOCK PRICES ----------
st.subheader("📈 Weekly Stock Prices")
fig, ax = plt.subplots(figsize=(10, 4))
data.plot(ax=ax)
st.pyplot(fig)

# ---------- SIMULATED SENTIMENT DATA ----------
st.subheader("💬 Weekly Sentiment Summary")

sentiment_data = pd.DataFrame({
    "Week End": pd.date_range(start=start_date, end=end_date, freq="W"),
    "Mean Sentiment (0=Neg,1=Pos)": [0.2, 0.5, 0.8, 0.6][:len(pd.date_range(start=start_date, end=end_date, freq='W'))]
})

fig2, ax2 = plt.subplots(figsize=(8, 3))
ax2.bar(sentiment_data["Week End"], sentiment_data["Mean Sentiment (0=Neg,1=Pos)"])
ax2.set_ylim(0, 1)
st.pyplot(fig2)

st.success("✅ Dashboard loaded successfully! Edit and extend with live news data.")

