from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import db.db as db

dados = {
    'CreditScore': [],
    'Age': [],
    'Balance': [],
    'EstimatedSalary': [],
    'Class': []
}

mysql = db.DB()
customers = mysql.get_customers()

for customer in customers:
    dados['CreditScore'].append(customer[0])
    dados['Age'].append(customer[1])
    dados['Balance'].append(customer[2])
    dados['EstimatedSalary'].append(customer[3])
    dados['Class'].append(customer[4])

df = pd.DataFrame(dados)

X = df[['Balance', 'EstimatedSalary']]
Y = df[['Class']]

X_train, X_test, y_train, y_test = train_test_split(X, Y, shuffle=True, test_size=0.2, random_state=0)

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

svm_classifier = SVC(random_state=0, C=1)

param_grid = {
    'C': [0.1, 1, 10],  # Regularização
    'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],  # Tipos de kernel
    'gamma': ['scale', 'auto'],  # Parâmetros de kernel
}

grid_search = GridSearchCV(svm_classifier, param_grid, cv=6, scoring='accuracy')
grid_search.fit(X_train, y_train.values.ravel())

print("Best parameters found:", grid_search.best_params_)
print("Best cross-validation accuracy:", grid_search.best_score_)

best_svm = grid_search.best_estimator_
y_pred = best_svm.predict(X_test)
print(metrics.classification_report(y_test, y_pred))

#desempenho
metrics.ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
plt.grid(False) #Optional, removes gridlines.
plt.show()