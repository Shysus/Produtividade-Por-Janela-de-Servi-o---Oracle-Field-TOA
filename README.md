/////////////////////////////////////////////////////
Descrição Geral:

O script inicia importando as bibliotecas necessárias: Streamlit para a construção da interface do usuário web, Pandas para manipulação de dados, e Plotly Express para a criação de gráficos interativos.

Estrutura e Funcionalidades:

Definição de Variáveis Iniciais: São definidas duas listas, uma para as janelas de serviço (janelas_de_servico) e outra para as cidades (cidades), que serão utilizadas para a entrada de dados na interface.

Gerenciamento de Sessão: 
A função get_session_state() é usada para acessar ou inicializar um espaço de armazenamento na sessão atual do usuário, onde os dados das atividades são mantidos.

Adição de Atividades: 
A função adicionar_atividade() permite adicionar novas atividades à sessão atual. Ela calcula a produtividade como a porcentagem do total executado em relação ao total da atividade e armazena os dados de cada atividade em um dicionário dentro da lista de sessão.

Criação de Gráficos: 
A função criar_grafico_plotly() utiliza a biblioteca Plotly Express para criar gráficos de barras que exibem a produtividade por atividade dentro de uma janela de serviço específica. Os gráficos são coloridos com base na produtividade e ordenados por atividade.

Geração de PDF: 
Há uma função placeholder gerar_pdf(), que indica onde a funcionalidade de geração de PDF deverá ser implementada pelo usuário para exportar os dados e gráficos gerados.

Interface do Usuário com Streamlit: 
O script utiliza vários componentes do Streamlit para criar a interface do usuário, 

incluindo:

Um título para a aplicação.
Uma barra lateral para entrada de dados da atividade (cidade, janela de serviço, nome da atividade, total da atividade, total executado).
Botões para adicionar atividades e gerar PDF.
Visualização dos dados de atividades em uma tabela e gráficos de produtividade por cidade e janela de serviço.
