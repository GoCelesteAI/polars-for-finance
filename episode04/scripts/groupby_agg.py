"""Episode 4 demo: groupby_agg.py — per-ticker statistics with group_by + agg.

Run:
  python groupby_agg.py
"""
import polars as pl

df = pl.read_parquet("data/prices.parquet")

result = df.with_columns(
  daily_ret=pl.col("Close").pct_change().over("Ticker"),
).group_by("Ticker").agg([
  pl.col("Close").mean().alias("avg_close"),
  pl.col("Volume").max().alias("max_volume"),
  pl.col("daily_ret").std().alias("ret_std"),
  pl.col("daily_ret").count().alias("days"),
]).sort("avg_close", descending=True)

print(result)
