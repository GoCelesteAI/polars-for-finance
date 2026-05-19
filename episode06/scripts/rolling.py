"""Episode 6 demo: rolling.py — SMA, rolling stdev, and Bollinger bands per ticker.

Run:
  python rolling.py
"""
import polars as pl

df = pl.read_parquet("data/prices.parquet").sort(["Ticker", "Date"])

result = df.with_columns(
  sma20=pl.col("Close").rolling_mean(window_size=20).over("Ticker"),
  sma50=pl.col("Close").rolling_mean(window_size=50).over("Ticker"),
  std20=pl.col("Close").rolling_std(window_size=20).over("Ticker"),
).with_columns(
  boll_upper=pl.col("sma20") + 2 * pl.col("std20"),
  boll_lower=pl.col("sma20") - 2 * pl.col("std20"),
)

aapl_tail = result.filter(pl.col("Ticker") == "AAPL").select(
  ["Date", "Close", "sma20", "sma50", "boll_upper", "boll_lower"]
).tail(8)

print("=== AAPL — last 8 rolling-window rows ===")
print(aapl_tail)

print(f"\nsma20 nulls (should be 19 × 14 = 266): {result.filter(pl.col('sma20').is_null()).shape[0]}")
print(f"sma50 nulls (should be 49 × 14 = 686): {result.filter(pl.col('sma50').is_null()).shape[0]}")
