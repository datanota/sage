
from utilities.common import Common
from pyspark.sql import SparkSession
from tabulate import tabulate
import pandas as pd
import sqlite3
import subprocess
import time
tabulate.PRESERVE_WHITESPACE = True


class DatabaseEngines(Common):
    def __init__(self):
        super().__init__()

# ############################################################### engine dictionary

    def dict_engines_functions(self):
        return {
            'sqlite': [self.df_to_sqlite_db, self.query_to_df_sqlite],
            'apache-hive': [self.df_to_hive_db]
        }
# ###############################################################
# ############################################################### Sage Database
# ###############################################################

    def df_to_sqlite_db(self):
        """
        :return: first creates the tables then populates them
        """
        self.sqlite_create_shopping_db_tables()
        self.sqlite_populate_shopping_db_tables()

    def sqlite_create_shopping_db_tables(self):
        db_conn = sqlite3.connect(f'{self.db_path}shopping.db')
        c = db_conn.cursor()
        c.execute(self.create_customers_table())
        c.execute(self.create_products_table())
        c.execute(self.create_orders_table())
        db_conn.commit()
        db_conn.close()

    @staticmethod
    def create_customers_table():
        table = """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id STRING PRIMARY KEY, 
                full_nm STRING, 
                age INTEGER,
                location STRING,
                loyalty_points INTEGER,
                gender STRING,
                last_login_date datetime
                );
             """
        return table

    @staticmethod
    def create_products_table():
        table = """
            CREATE TABLE IF NOT EXISTS products (
                product_id STRING PRIMARY KEY,  
                prd_name STRING,
                prd_category STRING,
                unit_price DECIMAL,
                prd_description STRING
                );
             """
        return table

    @staticmethod
    def create_orders_table():
        table = """
            CREATE TABLE IF NOT EXISTS orders (
                order_id STRING PRIMARY KEY,
                product_id STRING, 
                customer_id STRING, 
                order_quantity INTEGER,
                purchased_via STRING,
                order_delivered STRING, 
                order_returned BOOLEAN, 
                order_date datetime
                );
             """
        return table

    def sqlite_populate_shopping_db_tables(self):
        db_conn = sqlite3.connect(f'{self.db_path}shopping.db')

        customers = pd.read_csv(f'{self.generated_data_path}customers.csv')
        customers.to_sql(name='customers', con=db_conn, if_exists='replace', index=False)

        products = pd.read_csv(f'{self.generated_data_path}products.csv')
        products.to_sql(name='products', con=db_conn, if_exists='replace', index=False)

        orders = pd.read_csv(f'{self.generated_data_path}orders.csv')
        orders.to_sql(name='orders', con=db_conn, if_exists='replace', index=False)

        db_conn.commit()
        db_conn.close()

# ################################# Apache-Hive

    def df_to_hive_db(self):
        """
        :return: first checks hadoop services start if not already then stops after db is created
        """
        self.check_start_stop_hadoop_services('start')
        spark_session = self.initiate_spark_session()
        self.df_to_hive_table(spark_session=spark_session, table_list=['customers', 'products', 'orders'])
        self.check_start_stop_hadoop_services('stop')

    def df_to_hive_table(self, spark_session, table_list):
        for table_name in table_list:
            pandas_df = pd.read_csv(f"{self.generated_data_path}{table_name}.csv")
            df = spark_session.createDataFrame(pandas_df)
            df.write.option("path", f"{self.hdfs_hive_path}{table_name}").mode("overwrite").saveAsTable(table_name, format="parquet")
        print('=============== all tables are populated - updating the privileges ===============')
        time.sleep(1)
        self.chmod_directory(path_to_directory={self.hdfs_hive_path}, mode='777')

# ###############################################################
# ############################################################### sage-insight
# ###############################################################

    def query_to_df_sqlite(self, *args):
        """
        :param args: args[0] is the provided response for a query question
        :return: based on selected engine, runs the response query
        """
        response_query = args[0]
        query_return, df, df_size = None, None, None
        if self.engine == 'sqlite':
            db_conn = sqlite3.connect(f'{self.db_path}shopping.db')
            try:
                df = pd.read_sql_query(response_query, db_conn)
                query_return = tabulate(df.head(2), headers='keys', tablefmt='presto', showindex=False)
                df = df
                df_size = len(df)
            except pd.errors.DatabaseError:
                query_return = 'try again!'
                df = None
                df_size = None
            db_conn.close()
        return query_return, df, df_size

    # ###############################################################
# ############################################################### services and session
    # ###############################################################

    def check_start_stop_hadoop_services(self, service_type):
        try:
            print('==========> checking hadoop services <==========')
            result = subprocess.run(['jps'], check=True, text=True, capture_output=True)
            print(f"JPS returns:{result.stdout}")
            if ((service_type == 'start' and 'NameNode' in result.stdout)
                    or (service_type == 'stop' and 'NameNode' not in result.stdout)):
                print(f'==========> there is no need to {service_type} hadoop services <==========')
            if ((service_type == 'start' and 'NameNode' not in result.stdout)
                    or (service_type == 'stop' and 'NameNode' in result.stdout)):
                print(f'===============> hadoop services is in-progress to {service_type} ...')
                subprocess.run(
                    [f"{self.hadoop_sbin_path}{service_type}-dfs.sh"], check=True, text=True, capture_output=True
                )
        except subprocess.CalledProcessError as e:
            print(f"!!!!!! an error occurred while trying to check and {service_type} hadoop services\n{e}")
        finally:
            print('================> end of the call to hadoop services <================')

    @staticmethod
    def initiate_spark_session():
        spark_session = SparkSession.builder \
            .appName("HiveExample") \
            .config("spark.sql.warehouse.dir", "hdfs://localhost:9000/user/hive/warehouse") \
            .config("hive.metastore.uris", "") \
            .config("spark.sql.catalogImplementation", "hive") \
            .enableHiveSupport() \
            .getOrCreate()
        return spark_session



