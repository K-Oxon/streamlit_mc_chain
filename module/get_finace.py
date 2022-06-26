import datetime as datetime
import sys

import pandas as pd
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError


def get_finance_df(ticker):
    stock = share.Share(ticker)
    symbol_data = None

    # 期間指定 後で引数に入れる
    # 月で指定：share.PERIOD_TYPE_MONTH
    # 年で指定：share.PERIOD_TYPE_YEAR

    try:
        # get_historical(period_type, period, frequency_type, frequency)
        symbol_data = stock.get_historical(
            share.PERIOD_TYPE_MONTH, 12, share.FREQUENCY_TYPE_DAY, 1
        )
    except YahooFinanceError as e:
        print(f">>> [{ticker}] : {e.message}")
        return None

    # 日付処理のためにDataframeに変換
    df_symbol_data = pd.DataFrame(symbol_data)
    # タイムスタンプを変換
    df_symbol_data["datetime"] = pd.to_datetime(df_symbol_data.timestamp, unit="ms")
    # # 日本時間へ変換
    # df_symbol_data["datetime_jst"] = df_symbol_data["datetime"] + datetime.timedelta(
    #     hours=9
    # )
    # # 後でキーに使いやすいように日本時間を文字列に変換
    # df_symbol_data["datetime_jst_str"] = df_symbol_data["datetime_jst"].apply(
    #     lambda x: x.strftime("%Y%m%d")
    # )
    df_cahrt = df_symbol_data.loc[:, ["datetime", "close"]]
    df_cahrt = df_cahrt.set_index("datetime", drop=True)

    return df_cahrt


if __name__ == "__main__":
    ticker = "BZ=F"
    df = get_finance_df(ticker)
    print(df.head())
