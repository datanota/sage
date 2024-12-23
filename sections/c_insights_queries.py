

class InsightsQueries:

    @staticmethod
    def dict_descriptive_insights(q):
        q_dict = {
            'q1': {
                'Q': '''  
    list all the databases
    ''',
                'A': {
                    'sqlite': '''
    PRAGMA database_list;
    '''
                }
            },
            'q2': {
                'Q': '''  
    list all the tables in the shopping database
    ''',
                'A': {
                    'sqlite': '''
    SELECT name FROM sqlite_master WHERE type='table';
    '''
                }
            },
            'q3': {
                'Q': '''  
    check products table schema metadata 
    ''',
                'A': {
                    'sqlite': '''
    PRAGMA table_info('products');
    '''
                }
            },
            'q4': {
                'Q': '''
    please check the schema and details of table orders
                    ''',
                'A': {
                    'sqlite': '''
    SELECT sql FROM sqlite_master WHERE type='table' AND name='orders';
                    '''
                }
            },
            'q5': {
                'Q': '''  
    check the integrity of primary key in customers table (type, no null, no duplicates)
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
    '''
                }
            },
            'q6': {
                'Q': '''
    check data consistency by verifying the validity of foreign keys in orders table (how many invalid product_id)
    ''',
                'A': {
                    'sqlite': '''
    WITH joined_op AS (
        SELECT 
            o.order_id, 
            p.product_id
        FROM orders o
        LEFT JOIN products p ON o.product_id = p.product_id
    )
    SELECT count(*) AS total_invalid_id FROM joined_op WHERE p.product_id IS NULL;
    '''
                }
            },
            'q7': {
                'Q': '''
    what are the details of the last 10 orders placed by customers? 
    ''',
                'A': {
                    'sqlite': '''
    SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;                
    '''
                }
            },
            'q8': {
                'Q': '''
    how many customers placed at least one order?
    ''',
                'A': {
                    'sqlite': '''
    WITH per_cust_total AS (
        SELECT 
            customer_id, 
            COUNT(order_id) AS total_orders
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
    '''
                }
            },
            'q9': {
                'Q': '''
    how many products do we have in each category?
    ''',
                'A': {
                    'sqlite': '''
    SELECT 
        prd_category, 
        COUNT(*) AS product_count 
    FROM products 
    GROUP BY prd_category;
    '''
                }
            },
            'q10': {
                'Q': '''
    identify top 5 customers who spent the most recently (past 6 months)?
    ''',
                'A': {
                    'sqlite': '''
    WITH o AS (
        SELECT 
            customer_id, 
            SUM(order_quantity) AS total_spent,
            MAX(order_date) AS latest_purchase
        FROM orders 
        WHERE order_date >= DATE('now', '-6 month')
        GROUP BY customer_id
        ORDER BY total_spent DESC LIMIT 5
    )
    SELECT 
        o.customer_id, 
        c.full_nm, 
        o.total_spent,
        o.latest_purchase 
    FROM o
    JOIN customers c ON o.customer_id = c.customer_id;
    '''
                }
            },
            'q11': {
                'Q': '''
    what are the total sales figures for the last quarter broken down by product?
    ''',
                'A': {
                    'sqlite': '''
    SELECT 
        p.prd_name,
        SUM(o.order_quantity * p.unit_price) AS total_sales
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    WHERE 
        o.order_date >= DATE('now', '-3 months')
    GROUP BY p.prd_name;         
    '''
                }
            },
            'q12': {
                'Q': '''
    what is average order value per customer for the last year?
    ''',
                'A': {
                    'sqlite': '''
    WITH op AS (
        SELECT 
            o.customer_id,
            o.order_quantity * p.unit_price AS total_purchased
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_date >= DATE('now', '-1 year')
        )
    SELECT 
        op.customer_id,
        AVG(op.total_purchased) AS average_order_value
    FROM op
    GROUP BY op.customer_id; 
    '''
                }
            },
            'q13': {
                'Q': '''
    what is number of orders received each month for the last 12 months?           
    ''',
                'A': {
                    'sqlite': '''
    SELECT 
        strftime('%Y', o.order_date) AS order_year,
        strftime('%m', o.order_date) AS order_month,
        COUNT(o.order_id) AS orders_count
    FROM 
        orders o
    WHERE 
        o.order_date >= DATE('now', '-12 months')
    GROUP BY order_year, order_month
    ORDER BY order_year, order_month;    
    '''
                }
            },
            'q14': {
                'Q': '''
    what is total orders per year and month (assuming we have small data volume)?    
    ''',
                'A': {
                    'sqlite': '''
    WITH o_per_m AS (
        SELECT 
            strftime('%Y', o.order_date) AS year,
            strftime('%m', o.order_date) AS month,
            COUNT(o.order_id) AS orders_per_month
        FROM 
            orders o
        GROUP BY year, month
        ), o_per_y AS (
        SELECT 
            strftime('%Y', o.order_date) AS year,
            COUNT(o.order_id) AS orders_per_year
        FROM 
            orders o
        GROUP BY 
            year
        )
        SELECT 
            o_per_y.year,
            o_per_y.orders_per_year,
            o_per_m.month,
            o_per_m.orders_per_month
        FROM 
            o_per_m
        JOIN o_per_y ON o_per_m.year = o_per_y.year
        ORDER BY o_per_m.year, o_per_m.month;         
    '''
                }
            },
            'q15': {
                'Q': '''
    what is total orders per year and month for the past 5 years?
    ''',
                'A': {
                    'sqlite': '''
        SELECT 
            strftime('%Y', o.order_date) AS year,
            strftime('%m', o.order_date) AS month,
            COUNT(o.order_id) AS orders_per_month,
            SUM(COUNT(o.order_id)) OVER (PARTITION BY strftime('%Y', o.order_date)) AS orders_per_year
        FROM 
            orders o
        WHERE 
            o.order_date >= DATE('now', '-5 years')
        GROUP BY year, month
        ORDER BY year, month;
    '''
                }
            },
            'q16': {
                'Q': '''
    what is summary of the top 5 customers by revenue, excluding those who made fewer than 3 purchases (at least 3)                 
    ''',
                'A': {
                    'sqlite': '''
    WITH o_r AS (
        SELECT 
            o.customer_id,
            SUM(o.order_quantity * p.unit_price) AS total_revenue,
            COUNT(o.order_id) AS total_orders
        FROM 
            orders o
        JOIN 
            products p ON o.product_id = p.product_id
        GROUP BY o.customer_id
        HAVING COUNT(o.order_id) >= 3
        )
    SELECT 
        c.full_nm,
        o_r.total_orders,
        o_r.total_revenue
    FROM 
        customers c
    JOIN o_r ON c.customer_id = o_r.customer_id
    ORDER BY o_r.total_revenue DESC
    LIMIT 5;           
    '''
                }
            },
            'q17': {
                'Q': '''
    which 5 products have the highest sales volume and what is their contribution to overall revenue?                    
    ''',
                'A': {
                    'sqlite': '''
    WITH op AS (
        SELECT 
            p.product_id,
            p.prd_name,
            SUM(o.order_quantity) AS total_units_sold,
            SUM(o.order_quantity * p.unit_price) AS total_revenue
        FROM 
            products p
        JOIN 
            orders o ON p.product_id = o.product_id
        GROUP BY 
            p.product_id, p.prd_name
    ), tr AS (
    SELECT 
        SUM(total_revenue) AS overall_revenue
    FROM op
    )
    SELECT 
        op.prd_name,
        op.total_units_sold,
        op.total_revenue,
        ROUND((op.total_revenue / tr.overall_revenue) * 100, 2) AS revenue_contribution_percentage
    FROM 
        op, tr
    ORDER BY op.total_units_sold DESC
    LIMIT 5;           
    '''
                }
            },
            'q18': {
                'Q': '''
    what is the moving average of sales over the last 6 months, segmented by product category                    
    ''',
                'A': {
                    'sqlite': '''
    WITH sd AS (
        SELECT 
            o.order_date,
            p.prd_category,
            o.order_quantity * p.unit_price AS total_sales
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
    ), agg_sales AS (
        SELECT
            prd_category,
            DATE(order_date, 'start of month') AS month_start,
            SUM(total_sales) AS monthly_sales
        FROM sd
        GROUP BY prd_category, month_start
        ), ma AS (
        SELECT 
            prd_category,
            month_start,
            AVG(monthly_sales) OVER (PARTITION BY prd_category ORDER BY month_start 
            ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS moving_avg_sales
        FROM agg_sales
        )
        SELECT 
            prd_category,
            month_start,
            moving_avg_sales
        FROM ma
        ORDER BY prd_category, month_start;                
    '''
                }
            },
            'q19': {
                'Q': '''
    find the top 5 customers who logged in at least once in the past 3 months but purchased less than 100 dollars                    
    ''',
                'A': {
                    'sqlite': '''
    WITH rl AS (
        SELECT 
            c.customer_id,
            c.last_login_date
        FROM customers c
        WHERE c.last_login_date >= DATE('now', '-3 months')
        ), cs AS (
        SELECT 
            o.customer_id,
            SUM(o.order_quantity * p.unit_price) AS total_spent
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY o.customer_id
        HAVING total_spent < 100
        )
        SELECT 
            rl.customer_id,
            cs.total_spent
        FROM rl
        JOIN cs ON rl.customer_id = cs.customer_id
        ORDER BY cs.total_spent DESC
        LIMIT 5;                
    '''
                }
            },
            'q20': {
                'Q': '''                   
    ''',
                'A': {
                    'sqlite': '''                
    '''
                }
            }
        }
        return q_dict.get(q)
