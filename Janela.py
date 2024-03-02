# Produtividade-Por-Janela-de-Servi-o---Oracle-Field-TOA
import streamlit as st
import pandas as pd
import plotly.express as px

# Definição das Janelas de Serviço e Cidades
janelas_de_servico = ["08:00 - 12:00", "12:00 - 15:00", "15:00 - 18:00"]
cidades = ["Dourados - MS", "Naviraí - MS", "Ponta Porã - MS"]

# Função para obter a sessão atual do usuário
def get_session_state():
    if 'dados_atividades' not in st.session_state:
        st.session_state['dados_atividades'] = []
    return st.session_state['dados_atividades']

# Adiciona uma nova atividade à sessão atual
def adicionar_atividade(cidade, janela, nome_atividade, total, executado):
    produtividade = (executado / total) * 100 if total > 0 else 0
    get_session_state().append({
        "Cidade": cidade,
        "Janela": janela,
        "Atividade": nome_atividade,
        "Total": total,
        "Executado": executado,
        "Produtividade": produtividade
    })

# Função para criar gráficos com Plotly
def criar_grafico_plotly(df, janela):
    fig = px.bar(df, x='Atividade', y='Produtividade',
                 title=f'Produtividade por Atividade - {janela}',
                 labels={'Produtividade': 'Produtividade (%)', 'Atividade': 'Atividade'},
                 color='Produtividade',
                 color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

# Função placeholder para gerar PDF // Não finalizado. Ignorar. 
def gerar_pdf():
    st.write("A função para gerar PDF será implementada em seu ambiente local.")

# Interface do Usuário
st.title('Dashboard de Produtividade - Telecomunicações')

# Sidebar para inserção de dados
with st.sidebar:
    st.header('Adicionar Dados de Atividade')
    cidade_selecionada = st.selectbox('Selecione a Cidade', cidades)
    janela_selecionada = st.selectbox('Selecione a Janela de Serviço', janelas_de_servico)
    nome_atividade = st.text_input('Nome da Atividade')
    total_atividade = st.number_input('Total da Atividade', min_value=0)
    total_executado = st.number_input('Total Executado', min_value=0)
    if st.button('Adicionar Atividade'):
        adicionar_atividade(cidade_selecionada, janela_selecionada, nome_atividade, total_atividade, total_executado)
        st.success('Atividade adicionada com sucesso!')

# Botão para gerar PDF 
if st.button('Gerar PDF'):
    gerar_pdf()

# Processamento dos dados para visualização
df_atividades = pd.DataFrame(get_session_state())

# Exibição dos dados e gráficos
if not df_atividades.empty:
    st.write("Dados de Atividades:")
    st.dataframe(df_atividades)

    # Gráficos de Produtividade por Cidade e Janela de Serviço
    for cidade in cidades:
        st.write(f"Cidade: {cidade}")
        df_cidade = df_atividades[df_atividades['Cidade'] == cidade]
        for janela in janelas_de_servico:
            df_janela = df_cidade[df_cidade['Janela'] == janela]
            if not df_janela.empty:
                grafico = criar_grafico_plotly(df_janela, janela)
                st.plotly_chart(grafico)
else:
    st.write("Nenhuma atividade adicionada ainda.")
