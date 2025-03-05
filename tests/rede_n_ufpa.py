from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import db.db as db
import pickle

# Preparação dos dados
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

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, Y, shuffle=True, test_size=0.2, random_state=0)

# Normalizando os dados
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Preparando o classificador MLP (Rede Neural)
mlp_classifier = MLPClassifier(random_state=0)

# Definindo os parâmetros para GridSearch
param_grid = {
    'hidden_layer_sizes': [(50,), (100,), (150,)],  # Tamanhos das camadas ocultas
    'activation': ['relu', 'tanh'],  # Funções de ativação
    'solver': ['adam', 'sgd'],  # Solvers para otimização
    'alpha': [0.0001, 0.001],  # Regularização
    'max_iter': [200, 300],  # Número máximo de iterações
}

# Aplicar o GridSearchCV para encontrar os melhores parâmetros
grid_search = GridSearchCV(mlp_classifier, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train.values.ravel())

print("Best parameters found:", grid_search.best_params_)
print("Best cross-validation accuracy:", grid_search.best_score_)

# Treinando o modelo com os melhores parâmetros encontrados
best_mlp = grid_search.best_estimator_

# Predição nos dados de teste
y_pred = best_mlp.predict(X_test)

# Gerando a métrica de avaliação
print(metrics.classification_report(y_test, y_pred))

# Salvar o modelo em um arquivo .pkl
with open('mlp_model.pkl', 'wb') as file:
    pickle.dump(best_mlp, file)

# Salvar o scaler em um arquivo .pkl
with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

def predict_customer_class(balance, estimated_salary, scaler, model):
    customer_data = np.array([[balance, estimated_salary]])
    scaled_customer_data = scaler.transform(customer_data)
    prediction = model.predict(scaled_customer_data)
    return prediction[0]

# Exemplo de uso
customer_balance = 60000
customer_salary = 80000

predicted_class = predict_customer_class(customer_balance, customer_salary, scaler, best_mlp)
print(f"A classe prevista para o cliente é: {predicted_class}")

#metrics.ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
#plt.grid(False) #Optional, removes gridlines.
#plt.show()