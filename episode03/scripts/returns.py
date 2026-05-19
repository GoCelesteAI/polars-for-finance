"""Episode 3 demo: returns.py — daily and log returns with .over("Ticker").

Run:
  python returns.py
"""
import polars as pl

df = pl.read_parquet("data/prices.parquet").sort(["Ticker", "Date"])

result = df.with_columns(
  daily_ret=pl.col("Close").pct_change().over("Ticker"),
  log_ret=(pl.col("Close").log() - pl.col("Close").log().shift(1)).over("Ticker"),
)

print("=== Daily and log returns (first 8 rows) ===")
print(result.head(8).select(["Date", "Ticker", "Close", "daily_ret", "log_ret"]))

null_count = result.filter(pl.col("daily_ret").is_null()).shape[0]
print(f"\nNull returns (one per ticker): {null_count}")
print(f"Total tickers: {result['Ticker'].n_unique()}")
