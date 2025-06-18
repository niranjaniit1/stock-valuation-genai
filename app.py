import yfinance as yf
import pandas as pd
import streamlit as st
from transformers import pipeline

# Load GenAI model
generator = pipeline("text-generation", model="tiiuae/falcon-7b-instruct")

# Function to get stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "name": info.get("longName"),
        "sector": info.get("sector"),
        "pe_ratio": info.get("trailingPE"),
        "pb_ratio": info.get("priceToBook"),
        "dividend_yield": info.get("dividendYield"),
        "market_cap": info.get("marketCap")
    }

# Function to classify stock
def classify_stock(pe_ratio, sector_avg_pe):
    if pe_ratio is None:
        return "Data Unavailable"
    if pe_ratio > sector_avg_pe * 1.2:
        return "Overvalued"
    elif pe_ratio < sector_avg_pe * 0.8:
        return "Undervalued"
    else:
        return "Fairly Valued"

# Streamlit UI
st.title("📈 Indian Stock Valuation Tool")

ticker = st.text_input("Enter Indian stock ticker (e.g., RELIANCE.NS):")

if ticker:
    data = get_stock_data(ticker)
    st.write(data)

    sector_avg_pe = 20  # You can replace this with real sector data later
    valuation = classify_stock(data["pe_ratio"], sector_avg_pe)
    st.markdown(f"### Valuation: **{valuation}**")

    if st.button("Explain"):
        explanation = generator(
            f"The stock {data['name']} is classified as {valuation}. Why?",
            max_length=100
        )[0]["generated_text"]
        st.write(explanation)
