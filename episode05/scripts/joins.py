"""Episode 5 demo: joins.py — join prices with sector lookup, then aggregate by sector.

Run:
  python joins.py
"""
import polars as pl

prices = pl.read_parquet("data/prices.parquet")
sectors = pl.read_csv("data/sector_map.csv")

# Left join — keep every price row, attach Sector
joined = prices.join(sectors, on="Ticker", how="left")

print("=== Joined (prices + sector) ===")
print(joined.head())
print(joined.shape)

# Sector-level summary — join then group
sector_stats = joined.with_columns(
  daily_ret=pl.col("Close").pct_change().over("Ticker"),
).group_by("Sector").agg([
  pl.col("Ticker").n_unique().alias("tickers"),
  pl.col("Close").mean().alias("avg_close"),
  pl.col("daily_ret").std().alias("ret_std"),
]).sort("avg_close", descending=True)

print("\n=== Sector statistics ===")
print(sector_stats)
