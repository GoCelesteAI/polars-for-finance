"""Episode 1 demo: read_prices.py — load the price universe with Polars.

Run:
  python read_prices.py
"""
import polars as pl

df = pl.read_parquet("data/prices.parquet")
print(df.head())
print(df.shape)
print(df.schema)
