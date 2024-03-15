
from utilities.common import Common
import pandas as pd
import sqlite3
from tabulate import tabulate
tabulate.PRESERVE_WHITESPACE = True


class LevelOneQuestions(Common):
    def __init__(self):
        super().__init__()

    def run_query(self, response_query):
        db_conn = sqlite3.connect(f'{self.db_path}shopping.db')
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
                Q1: How many customers in the shopping database placed at least one order?
                ''',
                'A': '''
                WITH o AS (
                    SELECT 
                        customer_id, 
                        count(order_id) as total_orders
                    FROM 
                        orders 
                    GROUP BY 
                        customer_id
                    HAVING 
                        total_orders > 0
                    ORDER BY 
                        total_orders DESC
                )
                SELECT COUNT(*) as total_customers_with_at_least_one_order FROM o;
                '''
            },
            'q2': {
                'Q': '''
                Q2: Identify top 5 customers who spent the most recently (past 6 months)?
                ''',
                'A': '''
                WITH o AS (
                    SELECT 
                        customer_id, 
                        SUM(quantity) as total_spent,
                        MAX(date) as latest_purchase
                    FROM 
                        orders 
                    WHERE
                        date >= DATE('now', '-6 month')
                    GROUP BY 
                        customer_id
                    ORDER BY 
                        total_spent DESC
                    LIMIT 5
                )
                SELECT 
                    o.customer_id, 
                    customers.full_nm, 
                    o.total_spent,
                    o.latest_purchase 
                FROM 
                    o
                JOIN 
                    customers 
                ON o.customer_id = customers.customer_id;
                '''
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
            },
            'q10': {
                'Q': '''Q10: ''',
                'A': ''''''
            },
        }
        return q_dict.get(q)





