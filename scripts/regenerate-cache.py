#!/usr/bin/env python3
"""Download the Polars-for-Finance dataset universe and cache to parquet.

Same universe as Pandas-for-Finance — same tickers, same date window — so
every episode is a side-by-side polars rewrite of pandas idioms viewers
already know.

Usage:
  python scripts/regenerate-cache.py
  python scripts/regenerate-cache.py --start 2018-01-01 --end 2025-12-31

Outputs:
  data/prices.parquet      — long-format DataFrame: Date, Ticker, Open/High/Low/Close/Adj Close/Volume
  data/sector_map.csv      — Ticker -> Sector lookup (used in Ep 5 joins)
"""

import argparse
from pathlib import Path

import polars as pl
import yfinance as yf


TICKERS = [
  "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "JPM", "JNJ",
  "XLK", "XLF", "XLE", "XLV", "XLY",
  "SPY",
]


SECTOR_MAP = {
  "AAPL":  "Technology",
  "MSFT":  "Technology",
  "GOOGL": "Communication Services",
  "AMZN":  "Consumer Discretionary",
  "NVDA":  "Technology",
  "TSLA":  "Consumer Discretionary",
  "JPM":   "Financials",
  "JNJ":   "Health Care",
  "XLK":   "Sector ETF",
  "XLF":   "Sector ETF",
  "XLE":   "Sector ETF",
  "XLV":   "Sector ETF",
  "XLY":   "Sector ETF",
  "SPY":   "Index ETF",
}


def download(start: str, end: str) -> pl.DataFrame:
  raw = yf.download(
    TICKERS,
    start=start,
    end=end,
    auto_adjust=False,
    group_by="ticker",
    progress=False,
  )
  long_pd = (
    raw.stack(level=0, future_stack=True)
       .reset_index()
       .rename(columns={"level_1": "Ticker"})
       .sort_values(["Ticker", "Date"])
       .reset_index(drop=True)
  )
  return pl.from_pandas(long_pd)


def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument("--start", default="2018-01-01")
  parser.add_argument("--end",   default="2025-12-31")
  parser.add_argument(
    "--out",
    default=str(Path(__file__).resolve().parent.parent / "data"),
  )
  args = parser.parse_args()

  out = Path(args.out)
  out.mkdir(parents=True, exist_ok=True)

  print(f"Downloading {len(TICKERS)} tickers from {args.start} to {args.end}...")
  prices = download(args.start, args.end)
  prices_path = out / "prices.parquet"
  prices.write_parquet(prices_path)
  print(f"  prices.parquet  {prices.height:>8,} rows  {prices_path.stat().st_size/1024:.1f} KB")

  sectors = pl.DataFrame(
    [{"Ticker": t, "Sector": s} for t, s in SECTOR_MAP.items()]
  )
  sectors_path = out / "sector_map.csv"
  sectors.write_csv(sectors_path)
  print(f"  sector_map.csv  {sectors.height} rows")

  print("\nDone. Episodes load from data/prices.parquet — no network required.")


if __name__ == "__main__":
  main()
