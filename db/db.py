import mysql.connector
import pandas as pd
import random

import random
import numpy as np

def categorize_with_inaccuracy_v2(balance, age, income):
    err = 0.1  # Margem de erro base
    age_factor = (age - 18) / 60  # Normaliza a idade (18-78 anos)
    income_factor = income / 100000  # Normaliza a renda (ex: até 100k)

    # Margem de erro ajustada por idade e renda
    err_adjusted = err * (1 - age_factor * 0.3 + income_factor * 0.2)

    # Probabilidades de erro variáveis por categoria
    if balance > 100000:
        error_prob = err_adjusted * (1 - balance / 1000000)  # Menos erro para saldos muito altos
        if random.random() >= error_prob:
            return "high"
        else:
            return "medium"
    elif 10000 < balance <= 100000:
        error_prob = err_adjusted
        if random.random() >= error_prob:
            return "medium"
        else:
            return "low"
    else:
        error_prob = err_adjusted * (1 - balance / 10000) # Menos erro para saldos muito baixos
        if random.random() >= error_prob:
            return "low"
        else:
            return "medium"


class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="123456", database="labtech"
        )
        self.cursor = self.conn.cursor()

    def get_customers(self):
        sql = "select CreditScore, Gender, Age, Balance, EstimatedSalary, Class from customers_training limit 150"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_customers(self):
        data = pd.read_csv("bank.csv")
        print('ok')
        for index, row in data.iterrows():
            classe = categorize_with_inaccuracy_v2(row["Balance"], row['Age'], row["EstimatedSalary"])
            query = """
            INSERT INTO customers_training (RowNumber, CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited, Class)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
            values = (
                row["RowNumber"],
                row["CustomerId"],
                row["Surname"],
                row["CreditScore"],
                row["Geography"],
                row["Gender"],
                row["Age"],
                row["Tenure"],
                row["Balance"],
                row["NumOfProducts"],
                row["HasCrCard"],
                row["IsActiveMember"],
                row["EstimatedSalary"],
                row["Exited"],
                classe,
            )
            self.cursor.execute(query, values)
        self.conn.commit()

    def spend(self):
        sql = """
      SELECT 
        customerNumber, 
        SUM(priceEach * quantityOrdered) as total_spent, 
        COUNT(orderNumber) as num_orders 
      FROM orderdetails JOIN orders USING (orderNumber)
        GROUP BY customerNumber
    """
        self.cursor.execute(sql)
        return self.cursor.fetchall()


if __name__ == "__main__":
    db = DB()
    db.insert_customers()