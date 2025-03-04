import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import db.db  # Certifique-se de que db.py está no mesmo diretório

# Inicializar dicionário de dados
data = {
    "CreditScore": [],
    "Gender": [],
    "Age": [],
    "Balance": [],
    "EstimatedSalary": [],
    "Class": []
}

# Obter dados do banco de dados
mysql = db.db.DB()
customers = mysql.get_customers()

# Popular o dicionário de dados
for c in customers:
    data['CreditScore'].append(c[0])
    data['Gender'].append(c[1])
    data['Age'].append(c[2])
    data['Balance'].append(c[3])
    data['EstimatedSalary'].append(c[4])
    data['Class'].append(c[5])

# Criar DataFrame do Pandas
df = pd.DataFrame(data)

# Barra lateral (sidebar)
st.sidebar.header("Filtros")
unique_classes = df['Class'].unique()
selected_class = st.sidebar.selectbox("Selecionar Classe", ["Todas"] + list(unique_classes))

# Filtrar dados com base na seleção da barra lateral
if selected_class == "Todas":
    filtered_df = df
else:
    filtered_df = df[df['Class'] == selected_class]

# Dashboard Streamlit
st.title("Dashboard de Dados do Cliente")

# Criar colunas para os gráficos
col1, col2 = st.columns(2)

st.subheader("Gênero")
gender_counts = filtered_df['Gender'].value_counts()
st.bar_chart(gender_counts)
# Distribuição de gênero (gráfico de barras)
# Distribuição de classe (gráfico de pizza)
with col1:
    st.subheader("Classe")
    class_counts = filtered_df['Class'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

# Distribuição de idade (histograma)
with col2:
    st.subheader("Idade")
    fig2, ax2 = plt.subplots()
    sns.histplot(filtered_df['Age'], ax=ax2)
    st.pyplot(fig2)

# Criar colunas para os próximos gráficos
col4, col5 = st.columns(2)

# Distribuição de pontuação de crédito (histograma)
with col4:
    st.subheader("Pontuação de Crédito")
    fig3, ax3 = plt.subplots()
    sns.histplot(filtered_df['CreditScore'], ax=ax3)
    st.pyplot(fig3)
with col5:
    st.subheader("Saldo vs. Salário Estimado")
    fig4, ax4 = plt.subplots()
    ax4.scatter(filtered_df['EstimatedSalary'], filtered_df['Balance'], s=5)
    st.pyplot(fig4)

# Classe vs. Idade (boxplot)

# Criar colunas para os últimos gráficos

# Saldo vs. Salário estimado (gráfico de dispersão)

# Classe vs. Pontuação de crédito (boxplot)

col6, col7 = st.columns(2)
with col6:
    st.subheader("Classe vs. Idade")
    fig5, ax5 = plt.subplots()
    sns.boxplot(x='Class', y='Age', data=filtered_df, ax=ax5, hue='Class')
    st.pyplot(fig5)
with col7:    
    st.subheader("Classe vs. Crédito")
    fig6, ax6 = plt.subplots()
    sns.boxplot(x='Class', y='CreditScore', data=filtered_df, ax=ax6, hue='Class')
    st.pyplot(fig6)