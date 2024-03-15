
from utilities.common import Common
import pandas as pd


class AmberAnalytics(Common):
    """
    buy and sell analytics
    """
    def __init__(self):
        super().__init__()
        self.file_path = '/'
        self.stocks_file = 'amber.xlsx'

    # ################################################## stock summary

    @staticmethod
    def df_get_summary_data(stock_list, df):
        table_data = []
        for ticker in stock_list:
            t = df[df['ticker'] == ticker]
            total = t['quantity'].sum()
            min_max = str(t['unit_price'].min()) + '-' + str(t['unit_price'].max())
            current_price = t['current_price'].iloc[0]
            ticker_results = [ticker, total, min_max, current_price]
            table_data.append(ticker_results)
        return table_data

    # ################################################## buy invest

    def get_investment_recommendations(self, inv_dollar, df):
        df = self.df_buy_computations(inv_dollar, df)
        df = df[['ticker', 'current_q', 'current_price', 'pr_change']].drop_duplicates()
        df = df.sort_values(by=['pr_change'], ascending=True)
        buy_list = df.values.tolist()
        return buy_list

    @staticmethod
    def df_buy_computations(inv_dollar, df):
        final_df = []
        df.insert(9, 'current_q', round(inv_dollar / df['current_price']))
        df.insert(10, 'current_pq', df['current_price'] * df['current_q'])
        tickers = df['ticker'].unique().tolist()
        for ticker in tickers:
            df1 = df[df['ticker'] == ticker]
            pq_sum = df1['pq'].sum()
            q_sum = df1['quantity'].sum()
            current_pq = df1['current_pq'].iloc[0]
            current_q = df1['current_q'].iloc[0]
            df1.insert(6, 'wa', round(pq_sum / q_sum, 2))
            df1.insert(7, 'wa_c', round((pq_sum + current_pq) / (q_sum + current_q), 2))
            wa = df1['wa'].iloc[0]
            wa_c = df1['wa_c'].iloc[0]
            df1.insert(8, 'pr_change', round(round((wa_c - wa) / wa, 4) * 100, 2))
            final_df.append(df1)
        results_df = pd.concat(final_df)
        return results_df

    # ################################################## sell recommendation

    def get_cash_recommendations(self, df):
        df = self.df_sell_computations(df)
        df = df[['ticker', 'oldest_price', 'oldest_q', 'current_price', 'pr_change']].drop_duplicates()
        df = df.sort_values(by=['pr_change'], ascending=True)
        sell_list = df.values.tolist()
        return sell_list

    @staticmethod
    def df_sell_computations(df):
        final_df = []
        tickers = df['ticker'].unique().tolist()
        for ticker in tickers:
            df1 = df[df['ticker'] == ticker]
            df1 = df1.sort_values(by=['date'], ascending=True)
            oldest_date= df1['date'].iloc[0]
            oldest_price = df1['unit_price'].iloc[0]
            df1.insert(6, 'oldest_price', oldest_price)
            oldest_q = df1['quantity'].iloc[0]
            df1.insert(7, 'oldest_q', oldest_q)
            pq_sum1 = df1['pq'].sum()
            q_sum1 = df1['quantity'].sum()
            wa1 = round(pq_sum1 / q_sum1, 2)
            df1.insert(8, 'wa1', wa1)
            df2 = df1[df1['date'] != oldest_date]
            if len(df2) != 0:
                pq_sum2 = df2['pq'].sum()
                q_sum2 = df2['quantity'].sum()
                wa2 = round(pq_sum2 / q_sum2, 2)
                df1.insert(9, 'wa2', wa2)
                pr_change = round(round((wa2 - wa1) / wa1, 4) * 100, 2)
                df1.insert(10, 'pr_change', pr_change)
            else:
                df1.insert(10, 'pr_change', 0)
            final_df.append(df1)
        results_df = pd.concat(final_df)
        return results_df

    def get_df_available_stocks_data(self):
        df = self.get_df_stocks_data()
        df = df[df['sold'] == 0]
        df.insert(6, 'pq', df['unit_price'] * df['quantity'])  # unit_price times quantity
        return df

    def get_df_stocks_data(self):
        stocks_df = pd.read_excel(self.file_path + self.stocks_file, sheet_name=0, index_col=None)
        for str_col in ['transaction_id', 'stock_id', 'date', 'ticker']:
            stocks_df[str_col] = stocks_df[str_col].astype('string')
        for float_col in ['unit_price', 'quantity']:
            stocks_df[float_col] = stocks_df[float_col].astype('float')
        updates_df = pd.read_excel(self.file_path + self.stocks_file, sheet_name=1, index_col=None)
        for str_col in ['stock_id', 'ticker', 'updated_date']:
            updates_df[str_col] = updates_df[str_col].astype('string')
        df = pd.merge(stocks_df, updates_df, on=['stock_id', 'ticker'])
        return df



