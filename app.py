import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# Adicione a função configure_page aqui
def configure_page():
    st.set_page_config(layout="wide", page_title="Dashboard", page_icon=":bar_chart:")

# Chame a função configure_page imediatamente após defini-la
configure_page()

# Carregar os dados do arquivo Excel
@st.cache_data
def load_data():
    return pd.read_excel('milagres_biblia_simplificado.xlsx')

data = load_data()

# Configurar a barra lateral para navegação
st.sidebar.title("Navegação")
pages = {
    "Página Principal": "Página Principal",
    "Tabela Completa": "Tabela Completa"
}
page = st.sidebar.radio("Ir para", list(pages.values()))

st.sidebar.markdown("---")
st.sidebar.write("by: Lennon")

# Função para exibir gráficos
def show_charts(data):
    st.title("Análise dos Milagres da Bíblia")

    st.markdown("---")

    # Filtros
    st.sidebar.markdown("### Filtros")
    livro = st.sidebar.multiselect("Filtrar por Livro", options=data['Livro'].unique())
    autor = st.sidebar.multiselect("Filtrar por Autor do Milagre", options=data['Autor do Milagre'].unique())
    tipo = st.sidebar.multiselect("Filtrar por Tipo de Milagre", options=data['Classificação Simplificada'].unique())

    filtered_data = data.copy()
    if livro:
        filtered_data = filtered_data[filtered_data['Livro'].isin(livro)]
    if autor:
        filtered_data = filtered_data[filtered_data['Autor do Milagre'].isin(autor)]
    if tipo:
        filtered_data = filtered_data[filtered_data['Classificação Simplificada'].isin(tipo)]

    # Gráfico: Distribuição dos Milagres por Livro
    st.markdown("### Distribuição dos Milagres por Livro")
    milagres_por_livro = filtered_data['Livro'].value_counts().reset_index()
    milagres_por_livro.columns = ['Livro', 'count']
    fig1 = px.bar(milagres_por_livro, x='Livro', y='count', title='Distribuição dos Milagres por Livro da Bíblia',
                  labels={'Livro': 'Livro', 'count': 'Número de Milagres'})
    st.plotly_chart(fig1)

    st.markdown("---")

    # Gráfico: Distribuição dos Milagres por Autor
    st.markdown("### Distribuição dos Milagres por Autor")
    milagres_por_autor = filtered_data['Autor do Milagre'].value_counts().reset_index()
    milagres_por_autor.columns = ['Autor', 'count']
    fig2 = px.pie(milagres_por_autor, values='count', names='Autor', title='Distribuição dos Milagres por Autor')
    st.plotly_chart(fig2)

    st.markdown("---")

    # Gráfico: Tipos de Milagres Mais Frequentes
    st.markdown("### Tipos de Milagres Mais Frequentes")
    tipos_de_milagres = filtered_data['Classificação Simplificada'].value_counts().reset_index()
    tipos_de_milagres.columns = ['Tipo', 'count']
    fig3 = px.bar(tipos_de_milagres, x='Tipo', y='count', title='Tipos de Milagres Simplificados Mais Frequentes',
                  labels={'Tipo': 'Tipo de Milagre Simplificado', 'count': 'Número de Ocorrências'})
    st.plotly_chart(fig3)

# Função para exibir a tabela completa
def show_table(data):
    st.title("Tabela Completa dos Milagres da Bíblia")

    st.markdown("---")

    # Filtros para a tabela
    st.sidebar.markdown("### Filtros")
    livro = st.sidebar.multiselect("Filtrar por Livro", options=data['Livro'].unique())
    autor = st.sidebar.multiselect("Filtrar por Autor do Milagre", options=data['Autor do Milagre'].unique())
    tipo = st.sidebar.multiselect("Filtrar por Tipo de Milagre", options=data['Classificação Simplificada'].unique())
    colunas = st.sidebar.multiselect("Selecionar Colunas", options=data.columns.tolist(), default=data.columns.tolist())

    filtered_data = data.copy()
    if livro:
        filtered_data = filtered_data[filtered_data['Livro'].isin(livro)]
    if autor:
        filtered_data = filtered_data[filtered_data['Autor do Milagre'].isin(autor)]
    if tipo:
        filtered_data = filtered_data[filtered_data['Classificação Simplificada'].isin(tipo)]

    st.dataframe(filtered_data[colunas], use_container_width=True)

# Navegação entre páginas
if page == "Página Principal":
    show_charts(data)
elif page == "Tabela Completa":
    show_table(data)

# Adicione um componente customizado para os efeitos JavaScript
components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        .fade-in {
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .chart-container {
            opacity: 0;
        }
    </style>
</head>
<body>
    <script>
        document.addEventListener('DOMContentLoaded', (event) => {
            const appElement = document.querySelector('section.main');
            if (appElement) {
                appElement.classList.add('fade-in');
            }

            // Wait for Streamlit to load the charts
            setTimeout(() => {
                const charts = document.querySelectorAll('div[role="figure"]');
                charts.forEach(chart => {
                    chart.classList.add('chart-container');
                    setTimeout(() => {
                        chart.style.opacity = '1';
                    }, 100);
                });
            }, 1000);
        });
    </script>
</body>
</html>
""", height=0)
