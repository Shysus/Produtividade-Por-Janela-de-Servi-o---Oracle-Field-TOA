import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Função para calcular a produtividade das atividades por janela de serviço e cidade
def calcular_produtividade_por_janela(df_input):
    df = df_input.copy()
    colunas = ['Cidade', 'Intervalo de Tempo', 'Tipo de Atividade', 'Status da O.S 1']
    df['Status da O.S 1'] = df['Status da O.S 1'].map({'Executada': 'Produtivo', 'Não Executada': 'Improdutivo'})
    grupo = df.groupby(colunas[:3] + ['Status da O.S 1']).size().unstack(fill_value=0)
    
    # Certifique-se de que as colunas 'Produtivo' e 'Improdutivo' existem
    if 'Produtivo' not in grupo.columns:
        grupo['Produtivo'] = 0
    if 'Improdutivo' not in grupo.columns:
        grupo['Improdutivo'] = 0
        
    grupo['Total Atividades'] = grupo.sum(axis=1)
    grupo['Produtividade'] = (grupo['Produtivo'] / grupo['Total Atividades']).fillna(0).apply(lambda x: f"{x:.2%}")
    return grupo.reset_index()

# Função atualizada para calcular a produtividade de cada colaborador por cidade e tipo de atividade
def calcular_produtividade_por_colaborador_e_cidade(df_input):
    df = df_input.copy()
    colunas = ['Cidade', 'Recurso', 'Tipo de Atividade', 'Status da O.S 1']
    df['Status da O.S 1'] = df['Status da O.S 1'].map({'Executada': 'Produtivo', 'Não Executada': 'Improdutivo'})
    grupo = df.groupby(colunas).size().reset_index(name='Quantidade')
    grupo_total = grupo.groupby(['Cidade', 'Recurso', 'Tipo de Atividade'])['Quantidade'].sum().reset_index(name='Total Atividades')
    grupo_produtivo = grupo[grupo['Status da O.S 1'] == 'Produtivo']
    resultado_final = pd.merge(grupo_total, grupo_produtivo[['Cidade', 'Recurso', 'Tipo de Atividade', 'Quantidade']], on=['Cidade', 'Recurso', 'Tipo de Atividade'], how='left').fillna(0)
    resultado_final.rename(columns={'Quantidade': 'Produtivo'}, inplace=True)
    resultado_final['Produtividade'] = (resultado_final['Produtivo'] / resultado_final['Total Atividades']).apply(lambda x: f"{x:.2%}")
    return resultado_final

# Função para criar gráficos de produtividade por colaborador
def criar_grafico_produtividade_por_colaborador(df, cidade):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Recurso'],
        y=df['Produtividade'],
        text=df['Produtividade'],
        textposition='auto',
        marker_color='rgba(55, 128, 191, 0.7)'
    ))
    fig.update_layout(
        title=f'Produtividade dos Colaboradores em {cidade}',
        xaxis_title='Colaborador',
        yaxis_title='Produtividade',
        template='plotly_white'
    )
    return fig

# Função para criar gráficos de produtividade por janela de serviço
def criar_grafico_produtividade_por_janela(df, cidade):
    fig = go.Figure()
    for tipo_atividade in df['Tipo de Atividade'].unique():
        df_filtrado = df[df['Tipo de Atividade'] == tipo_atividade]
        fig.add_trace(go.Bar(
            x=df_filtrado['Intervalo de Tempo'],
            y=df_filtrado['Produtividade'],
            name=tipo_atividade,
            marker_color=np.random.rand(3,),
            hoverinfo='y+name'
        ))
    fig.update_layout(
        title=f'Produtividade por Janela de Serviço em {cidade}',
        xaxis_title='Intervalo de Tempo',
        yaxis_title='Produtividade (%)',
        legend_title='Tipo de Atividade',
        template='plotly_white',
        font=dict(family="Arial, sans-serif", size=12, color="RebeccaPurple")
    )
    return fig

# Interface do Usuário no Streamlit para Upload, Visualização de Dados e Gráficos
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Definição das funções de cálculo...

def interface_usuario():
    st.title('Dashboard de Produtividade')
    uploaded_file = st.file_uploader("Escolha o arquivo de planilha", type=['xlsx'])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        df.dropna(subset=['Cidade', 'Recurso'], inplace=True)  # Certifique-se de que 'Recurso' também não tem NaN
        
        # Cria uma caixa de seleção com os nomes dos colaboradores
        colaboradores = df['Recurso'].unique()
        colaborador_selecionado = st.selectbox('Escolha um colaborador para visualizar suas informações', ['Todos'] + list(colaboradores))
        
        if colaborador_selecionado != 'Todos':
            # Filtra o DataFrame para o colaborador selecionado
            df = df[df['Recurso'] == colaborador_selecionado]
            st.write(f"Informações do colaborador: {colaborador_selecionado}")

        # Identifica e processa dados por cidade
        cidades = df['Cidade'].unique()
        for cidade in cidades:
            if pd.notna(cidade):
                st.markdown(f"### Produtividade na cidade: {cidade}")
                df_cidade = df[df['Cidade'] == cidade]
                exibir_informacoes_cidade(df_cidade, colaborador_selecionado, cidade)  # Passando cidade como argumento

# Defina uma nova função para exibir as informações por cidade
def exibir_informacoes_cidade(df_cidade, colaborador_selecionado, cidade):  # Cidade como parâmetro
    # Produtividade por Janela de Serviço e Cidade
    resultado_janela = calcular_produtividade_por_janela(df_cidade)
    if not resultado_janela.empty:
        st.write("Produtividade por Janela de Serviço:")
        st.dataframe(resultado_janela)

    # Produtividade por Colaborador e Tipo de Atividade
    resultado_colaborador = calcular_produtividade_por_colaborador_e_cidade(df_cidade)
    if not resultado_colaborador.empty and colaborador_selecionado == 'Todos':
        st.write("Produtividade por Colaborador e Tipo de Atividade:")
        st.dataframe(resultado_colaborador)

    # Gera e exibe gráficos
    if not resultado_janela.empty:
        grafico_janela = criar_grafico_produtividade_por_janela(resultado_janela, cidade)
        st.plotly_chart(grafico_janela)
    if not resultado_colaborador.empty and colaborador_selecionado == 'Todos':
        grafico_colaborador = criar_grafico_produtividade_por_colaborador(resultado_colaborador, cidade)
        st.plotly_chart(grafico_colaborador)

# As demais funções de cálculo e criação de gráficos...

if __name__ == "__main__":
    interface_usuario()

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

# Função placeholder para gerar PDF
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
