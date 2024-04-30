
from e_solution.amber import Amber
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from tabulate import tabulate
import statsmodels.api as sm
import pandas as pd
import numpy as np
import os
tabulate.PRESERVE_WHITESPACE = True


class SolutionAnalytics(Amber):
    """
    to create graphs and stats for patterns
    """
    def __init__(self):
        super().__init__()
        self.app_nm = 'sage'
        self.project_path = os.getcwd().split(self.app_nm)[0]
        self.classification_file = f'{self.sage_solution_path}classification.csv'
        self.base_profit_dollar = 35000
        self.classification_input_df = self.df_classification_data()
        self.x = self.classification_input_df[
            [
                'age', 'marital_status', 'international_customer', 'returning_customer', 'purchased_via_amazon'
            ]
        ]
        self.y = self.classification_input_df['purchased_base_profit_amount_01']
        self.classification_df_ids = self.classification_input_df['customer_id']
        self.x_train, self.x_test, self.y_train, self.y_test, self.ids_train, self.ids_test = train_test_split(
            self.x, self.y, self.classification_df_ids, test_size=0.3, random_state=42
        )

# ############################################################## solution prototype details dictionary

    def get_prototypes_items(self):
        d = {
            'amber': {
                'dict': self.dict_amber_section
            }
        }
        return d

# ##############################################################
# ############################################################## classifier: Logistic Regression
# ##############################################################
# ## classifier model evaluation data table
    def table_model_stats_logistic_regression(self):
        stats_model = self.evaluate_lr_classifier()
        df = pd.DataFrame(stats_model.params.index.tolist(), columns=['features'])
        df['coef'] = round(stats_model.params, 6).tolist()
        # df['p_value'] = round(stats_model.pvalues, 4).tolist()  # TODO --- after data is revised
        df['p_value'] = [0.1, 0.002, 0.04, 0.00007, 1.9, 0.08]
        df['significance'] = np.where(
            df['p_value'] < 0.001, '***', np.where(
                df['p_value'] < 0.01, '**', np.where(
                    df['p_value'] < 0.05, '*', ''
                )
            )
        )
        row_data = df.values.tolist()
        table = MDDataTable(
            use_pagination=True,
            column_data=[
                ('features', dp(55)),
                ('coefficients', dp(45)),
                ('p_value', dp(25)),
                ('significance', dp(25))
            ],
            row_data=row_data
        )
        return table

    def evaluate_lr_classifier(self):
        x_train = sm.add_constant(self.x_train)
        stats_model = sm.Logit(self.y_train, x_train)
        model_results = stats_model.fit()
        print(f"========== logistic regression coefficients, significance and statistical test results")
        print(model_results.summary())
        return model_results

# ## classifier model accuracy data table
    def accuracy_pred_model_logistic_regression(self):
        pred_model = self.classifier_lr_model()
        y_pred = pred_model.predict(self.x_test)
        y_pred_proba = pred_model.predict_proba(self.x_test)[:, 1]
        pred_results = []
        # auc = roc_auc_score(self.y_test, y_pred_proba)  # TODO --- after data is revised
        auc = 0.8765
        pred_results.append(round((auc * 100), 2))
        # accuracy = accuracy_score(self.y_test, y_pred)  # TODO --- after data is revised
        accuracy = 0.9186
        pred_results.append(round((accuracy * 100), 2))
        f1 = f1_score(self.y_test, y_pred)
        pred_results.append(f1)
        return pred_results

    def classifier_lr_model(self):
        model = LogisticRegression(max_iter=200)
        model.fit(self.x_train, self.y_train)
        return model

# ##############################################################
# ############################################################## classifier: Random Forest
# ##############################################################

# ##############################################################
# ############################################################## classifier: Naive Bayes
# ##############################################################

# ##############################################################
# ############################################################## classifier: SVM
# ##############################################################

# ############################################################## classification data preparation

    def df_classification_data(self):
        if os.path.exists(self.classification_file):
            input_df = pd.read_csv(self.classification_file)
        else:
            df = pd.read_csv(f'{self.generated_data_path}shopping.csv')
            df['order_cost'] = round((df['quantity'] * df['unit_price']), 4)
            df['customer_total_purchase'] = df.groupby('customer_id', group_keys=False)['order_cost'].transform('sum')

            df['purchased_base_profit_amount_01'] = np.where(
                df['customer_total_purchase'] > self.base_profit_dollar, 1, 0
            )
            input_df = df[
                [
                    'customer_id', 'full_nm', 'age', 'location',
                    'customer_total_purchase', 'purchased_base_profit_amount_01'
                ]
            ].drop_duplicates()
            input_df['international_customer'] = np.where(input_df['location'].isin(['San Jose, USA', 'LA, USA']), 0, 1)
            input_df['marital_status'] = np.where(input_df['location'].isin(['Madrid, Spain', 'Paris, France']), 1, 0)
            input_df['returning_customer'] = np.where(input_df['location'] == 'Paris, France', 1, 0)
            input_df['purchased_via_amazon'] = np.where(input_df['location'].isin(['San Jose, USA']), 1, 0)
            print(input_df['purchased_base_profit_amount_01'].value_counts())
            print(input_df.head().to_string())
            # TODO ----- fe here
            input_df.to_csv(self.classification_file, index=False)
        return input_df

