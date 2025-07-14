# Dashboard de Análise Financeira

## Descrição do Projeto

Este projeto é um Dashboard de Análise Financeira desenvolvido como trabalho acadêmico para a disciplina de Programação Avançada. Ele foi idealizado para buscar minimizar a dependência de planilhas estáticas, processos manuais no mercado financeiro, reduzindo tempo e erros, ajudando onde há dificuldade em transformar dados brutos em insights acionáveis rapidamente. O dashboard deve ser uma plataforma que automatiza coleta de dados de ativos, para análise e predição de dados de ativos/ações financeiras.
Desse modo, há a Integração de Yahoo Finance, Alpha Vintage, utilizando Python e Streamlit em prol de tomada de decisões estratégicas, a qual também consegue se integrar como uma ferramenta educacional para disciplinas de Finanças ou Ciência de Dados, que pode ser utilizada por professores ou alunos.

 A aplicação permite visualizar e analisar dados históricos de ativos financeiros, com funcionalidades para:

- Visualização de séries temporais em diferentes formatos (linha, candlestick e barras)
- Comparação entre múltiplos ativos
- Previsão de tendências usando modelo de Regressão Linear

## Documentações

Antes de iniciar a programar, este projeto teve algumas documentações. Foi levantado painel MVP para compreensão inicial do que seria a aplicação, bem como seu intuito; estórias do usuário, para fortificar a necessidade de usuários sobre a aplicação; protótipo da aplicação, para que consigamos entender “na prática” como pode ser nossa aplicação; casos de uso para complementar funcionalidades do projeto; diagrama de atividades para compreensão dos fluxos dos casos de uso; matriz de rastreabilidade contendo dois requisitos funcionais e, por fim, diagrama de classes, contendo o projeto de como irão estar situadas as classes e o que as compõe.

Segue abaixo algumas das documentações produzidas:

### Protótipo principal
![Protótipo](documents/prototip.png)

### Diagrama de Atividade - Análise Histórica
![Diagrama de Atividade - Análise Histórica](documents/AD_analysishistorical.png)

### Diagrama de Atividade - Predição
![Diagrama de Atividade - Predição](documents/AD_Predition.png)

### Matriz de Rastreabilidade

| Requisito Funcional               | Módulo/Classe                   | Fontes de Dados               | Artefatos Gerados               |
|-----------------------------------|---------------------------------|-------------------------------|----------------------------------|
| **RF01** - Coleta resiliente de dados | `FinanceDataService`           | Yahoo Finance, AlphaVantage   | DataFrame com dados para visualização |
| **RF02** - Visualização de dados      | `FinanceUI`                    | Dados processados             | Gráficos Plotly                  |

### Diagrama de Classes
![Diagrama de Classes](documents/ClassDiagram.png)

## Funcionalidades Principais

- ✅ **Múltiplas fontes de dados** 
- ✅ **Visualizações interativas**
- ✅ **Interface intuitiva**
- ✅ **Comparação entre ativos**  
- ✅ **Previsão de séries temporais**  
- ✅ **Responsivo e adaptável**  

## Tecnologias Utilizadas

- Python 3.10+
- Streamlit (interface web)
- Plotly (visualizações interativas)
- yfinance (API Yahoo Finance)
- Alpha Vantage API (fallback)
- Pandas (manipulação de dados)
- Statsmodels (modelo de Regressão Linear para previsão)

## Estrutura do Código

```
FinancialAnalysisDashboard/
├── modules/
│   ├── data_provider.py  # Fontes de dados
│   └── interface.py      # UI e visualizações
├── main.py               # Arquivo para execução
├── requirements.txt      # Dependências do Projeto
└── .env                  # Arquivo com variáveis de ambiente
```

## Como Executar o Projeto

### Pré-requisitos

- Python 3.10 ou superior instalado
- Conta no Alpha Vantage para chave API (opcional, para quantidades maiores de cinco requisições por minuto)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/DomingosFSouza/FinancialAnalysisDashboard.git
cd FinancialAnalysisDashboard
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Configuração

Crie um arquivo `.env` na raiz do projeto com sua chave Alpha Vantage (opcional, já que se pode fazer cinco requisições por minuto sem uso da ALPHA_VANTAGE_KEY):
```
ALPHA_VANTAGE_KEY=sua_chave_aqui
```

# Configure as variáveis de ambiente
```bash
echo "ALPHA_VANTAGE_KEY=sua_chave" > .env #Linux ou Windows
```

### Execução local

Execute o aplicativo Streamlit:
```bash
streamlit run main.py
```

O aplicativo estará disponível em `http://localhost:8501`

## Disponibilidade Online

Poderá acessar a aplicação de maneira online através do seguinte link:
> https://financialanalysisdashboard.streamlit.app/

## Uso Acadêmico

Este projeto foi desenvolvido como parte dos requisitos para conclusão da disciplina de Programação Avançada. Ele demonstra:

- Princípios de POO (Programação Orientada a Objetos) e Programação Modular
- Padrões de projeto
- Consumo de APIs REST
- Visualização de dados
- Desenvolvimento de interfaces web

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

- **Aluno:** Domingos Peixoto
- **Instituição:** Universidade Federal do Rio Grande do Norte (UFRN) 
- **Professor:** Hertz Wilton de Castro Lins
- **Disciplina:** Programação Avançada (2025.1)

---

> *Nota: Este projeto foi desenvolvido exclusivamente para fins acadêmicos e não deve ser usado para decisões de investimento reais.*
