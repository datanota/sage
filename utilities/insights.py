
import pandas as pd
import sqlite3
from utilities.common import Common
from tabulate import tabulate
tabulate.PRESERVE_WHITESPACE = True


class Insights(Common):
    def __init__(self):
        super(Insights, self).__init__()

    def run_query(self, response_query):
        db_conn = sqlite3.connect(f'{self.project_path}{self.data_path}shopping.db')
        try:
            df = pd.read_sql_query(response_query, db_conn)
        except pd.errors.DatabaseError:
            query_return = 'try again!'
            df = None
            df_size = None
        else:
            query_return = tabulate(df.head(), headers='keys', tablefmt='presto', showindex=False)
            df = df
            df_size = len(df)
        db_conn.close()
        return query_return, df, df_size

# ################################################################
# ################################################################
# ################################################################

    @staticmethod
    def insight_sets(q):
        q_dict = {
            'q1': {
                'Q': '''
                Q1: How many customers in our shopping database placed at least one order?
                ''',
                'A': '''
                SELECT 
                    COUNT(DISTINCT(customer_id)) AS num_cust_placed_order 
                FROM 
                    orders;
                '''
            },
            'q2': {
                'Q': '''Q2: ''',
                'A': ''''''
            },
            'q3': {
                'Q': '''Q3: ''',
                'A': ''''''
            },
            'q4': {
                'Q': '''Q4:''',
                'A': ''''''
            },
            'q5': {
                'Q': '''Q5:''',
                'A': ''''''
            },
            'q6': {
                'Q': '''Q6: ''',
                'A': ''''''
            },
            'q7': {
                'Q': '''Q7: ''',
                'A': ''''''
            },
            'q8': {
                'Q': '''Q8: ''',
                'A': ''''''
            },
            'q9': {
                'Q': '''Q9: ''',
                'A': ''''''
            }
        }
        return q_dict.get(q)





