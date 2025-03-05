from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import db.db as db

def predict_customer_class(balance, estimated_salary, scaler, model):
    customer_data = np.array([[balance, estimated_salary]])
    scaled_customer_data = scaler.transform(customer_data)
    prediction = model.predict(scaled_customer_data)
    return prediction[0]

#CreditScore, Age, Balance, EstimatedSalary
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

# Criar DataFrame
df = pd.DataFrame(dados)

X = df[['Balance', 'EstimatedSalary']]
Y = df[['Class']]

X_train,X_test,y_train,y_test = train_test_split(X,Y, shuffle = True, test_size=0.2, random_state=0)

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#preparando as configurações do KNN
knn_classifier = KNeighborsClassifier(n_neighbors = 3)
knn_classifier.fit(X_train, y_train)
y_pred = knn_classifier.predict(X_test)

param_grid = {'n_neighbors': list(range(1, 51))}

# Aplicar o GridSearchCV para encontrar o melhor valor de n_neighbors
grid_search = GridSearchCV(knn_classifier, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train.values.ravel())
print("Best n_neighbors found:", grid_search.best_params_)
print("Best cross-validation accuracy:", grid_search.best_score_)

#gerando a métrica de avaliação
print(metrics.classification_report(y_test, y_pred))

#parte de tentar prever a classe de um cliente
#customer_balance = 500000
#customer_salary = 750000
#best_model = grid_search.best_estimator_ #get the best model.
#predicted_class = predict_customer_class(customer_balance, customer_salary, scaler, best_model)
#print(f"A classe prevista para o cliente é: {predicted_class}")

#Matriz de confusão
metrics.ConfusionMatrixDisplay(confusion_matrix=metrics.confusion_matrix(y_test, y_pred), display_labels=knn_classifier.classes_).plot()
plt.grid(False)
plt.show()

error = []
# Calculating error for K values between 1 and 10
"""
for i in range(1, 10):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error.append(np.mean(pred_i!= y_test))

plt.figure(figsize=(12, 6))
plt.plot(range(1, 10), error, color='red', linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error') """