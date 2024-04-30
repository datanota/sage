

class DescriptiveInsights:
    def __init__(self):
        self.m = 'm'

# ################################################################
# ################################################################ descriptive saved_data
# ################################################################

    @staticmethod
    def dict_descriptive_insights(q):
        q_dict = {
            'q1': {
                'Q': '''  
    List all the tables in the database
    ''',
                'A': {
                    'sqlite': '''
    SELECT name FROM sqlite_master WHERE type='table';
    ''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q2': {
                'Q': '''  
    check table schema metadata 
    ''',
                'A': {
                    'sqlite': '''
    PRAGMA table_info('table_name');
    ''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q3': {
                'Q': '''  
    Check the integrity of primary key in customers table (type, no null, no duplicates)
    ''',
                'A': {
                    'sqlite': '''
    WITH a as (
        SELECT 'data_type' AS description, typeof(customer_id) AS results FROM customers limit 1
    ), b as(
        SELECT 'null_count' AS description, count(*) AS results FROM customers WHERE customer_id IS NULL
    ), c as (
        SELECT 'duplicate count' AS description, SUM(id_count) AS results
        FROM (SELECT customer_id, COUNT(*) AS id_count FROM customers GROUP BY customer_id HAVING id_count > 1)
    )
    SELECT * FROM a UNION ALL SELECT * FROM b UNION ALL SELECT * FROM c;
    ''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q4': {
                'Q': '''
    Check data consistency by verifying the validity of foreign keys in orders table (how many invalid product_id)
    ''',
                'A': {
                    'sqlite': '''
    WITH joined_op AS (
        SELECT 
            o.order_id, p.product_id
        FROM 
            orders o
        LEFT JOIN 
            products p ON o.product_id = p.product_id
    )
    SELECT count(*) AS total_invalid_id FROM joined_op WHERE p.product_id IS NULL;
    ''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q5': {
                'Q': '''
    columns statistics null values and percentage of zeros, mean sd 
    ''',
                'A': {
                    'sqlite': '''
                    
    ''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q6': {
                'Q': '''
    How many customers in the shopping databases placed at least one order?
    ''',
                'A': {
                    'sqlite': '''
    WITH per_cust_total AS (
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
    SELECT COUNT(*) AS total_customers_with_at_least_one_order FROM per_cust_total;
    ''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q7': {
                'Q': '''
    top 2 customers with most orders and least 2 customers  
                ''',
                'A': {
                    'sqlite': '''
                    
                    ''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q8': {
                'Q': '''
    Identify top 5 customers who spent the most recently (past 6 months)?
    ''',
                'A': {
                    'sqlite': '''
    WITH o AS (
        SELECT 
            customer_id, 
            SUM(quantity) as total_spent,
            MAX(date) as latest_purchase
        FROM orders 
        WHERE date >= DATE('now', '-6 month')
        GROUP BY customer_id
        ORDER BY total_spent DESC LIMIT 5
    )
    SELECT 
        o.customer_id, 
        customers.full_nm, 
        o.total_spent,
        o.latest_purchase 
    FROM o
    JOIN customers ON o.customer_id = customers.customer_id;
    ''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q9': {
                'Q': '''
    count per year 
                ''',
                'A': {
                    'sqlite': '''''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
            'q10': {
                'Q': '''
                ''',
                'A': {
                    'sqlite': '''''',
                    'hive': '''''',
                    'mongodb': ''''''
                }
            },
        }
        return q_dict.get(q)

