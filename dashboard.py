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

st.markdown("""
<style>
    *{
        text-align: left;
    }
    .stMain{
        background: radial-gradient(white, whitesmoke, lightgray, grey);   
    }            
</style>
""", unsafe_allow_html=True)

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
st.title("Dados do Cliente")

# Criar colunas para os gráficos

col1, col2, col3 = st.columns(3)
# Distribuição de gênero (gráfico de barras)
# Distribuição de classe (gráfico de pizza)
with col1:
    class_counts = filtered_df['Class'].value_counts()
    fig1, ax1 = plt.subplots()
    fig1.patch.set_alpha(0)
    ax1.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Distribuição de Classe')
    ax1.axis('equal')
    st.pyplot(fig1)

# Distribuição de idade (histograma)
with col2:
    # Cria o histograma com seaborn
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    sns.histplot(data=filtered_df, x='Age', hue='Gender', palette='bright', kde=True, ax=ax)
    ax.set_title('Distribuição de Idades por Gênero')
    # Exibe o gráfico no Streamlit
    st.pyplot(fig)
with col3:
    fig5, ax5 = plt.subplots()
    fig5.patch.set_alpha(0)
    sns.boxplot(x='Class', y='Age', data=filtered_df, ax=ax5, hue='Class', palette='bright')
    ax5.set_title('Classe x Idade')
    st.pyplot(fig5)

# Criar colunas para os próximos gráficos
st.title('Dados Financeiros')
col4, col5, col6 = st.columns(3)

# Distribuição de pontuação de crédito (histograma)
with col4:
    fig3, ax3 = plt.subplots()
    fig3.patch.set_alpha(0)
    sns.histplot(filtered_df['CreditScore'], ax=ax3, palette='bright')
    ax3.set_title('Pontuação de Crédito')
    st.pyplot(fig3)
with col5:
    fig4, ax4 = plt.subplots()
    fig4.patch.set_alpha(0)
    ax4.scatter(filtered_df['EstimatedSalary'], filtered_df['Balance'], s=5)
    ax4.set_title("Saldo x Salário Estimado")
    st.pyplot(fig4)
with col6:    
    fig6, ax6 = plt.subplots()
    fig6.patch.set_alpha(0)
    sns.boxplot(x='Class', y='CreditScore', data=filtered_df, ax=ax6, hue='Class', palette='bright')
    ax6.set_title("Classe vs. Crédito")
    st.pyplot(fig6)

# Classe vs. Idade (boxplot)

# Criar colunas para os últimos gráficos

# Saldo vs. Salário estimado (gráfico de dispersão)

# Classe vs. Pontuação de crédito (boxplot)
