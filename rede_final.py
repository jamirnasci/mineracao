import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler


def find_by_model(balance, estimated_salary, scaler, model):
    customer_data = np.array([[balance, estimated_salary]])
    scaled_customer_data = scaler.transform(customer_data)
    prediction = model.predict(scaled_customer_data)
    return prediction[0]

def predict_customer_class(balance, salary):
    try:
        with open('mlp_model.pkl', 'rb') as file:
            loaded_mlp = pickle.load(file)

        with open('scaler.pkl', 'rb') as file:
            loaded_scaler = pickle.load(file)

        print("Modelo e scaler carregados com sucesso.")

    except FileNotFoundError:
        print("Erro: Arquivos mlp_model.pkl ou scaler.pkl não encontrados. Certifique-se de que o modelo foi treinado e salvo.")
        exit()

    predicted_class = find_by_model(balance, salary, loaded_scaler, loaded_mlp)
    return predicted_class