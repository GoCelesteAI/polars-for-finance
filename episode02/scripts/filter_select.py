"""Episode 2 demo: filter_select.py — narrow rows and columns with Polars expressions.

Run:
  python filter_select.py
"""
import polars as pl

df = pl.read_parquet("data/prices.parquet")

# 1. Filter — AAPL closes above $200.
aapl_high = df.filter(
  (pl.col("Ticker") == "AAPL") & (pl.col("Close") > 200)
)
print("=== AAPL Close > $200 ===")
print(aapl_high.head())
print(aapl_high.shape)

# 2. Select — three columns out of eight.
slim = df.select(["Date", "Ticker", "Close"])
print("\n=== Date / Ticker / Close ===")
print(slim.head())
print(slim.shape)

# 3. Chain — high-volume days, four interesting columns.
big = (
  df.filter(pl.col("Volume") > 100_000_000)
    .select(["Date", "Ticker", "Close", "Volume"])
)
print("\n=== Volume > 100M ===")
print(big.head())
print(big.shape)
