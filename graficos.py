import streamlit as st
import plotly.express as px

# Adicione a função configure_page aqui
def configure_page():
    st.set_page_config(layout="wide", page_title="Dashboard", page_icon=":bar_chart:")

# Chame a função configure_page imediatamente após defini-la
configure_page()

def show_charts(data):
    st.title("Análise dos Milagres da Bíblia")

    st.divider()

    # Filtros
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
