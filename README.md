# GuardianOps AI 🛡️🤖

> Um auditor de segurança estática (SAST) dinâmico e automatizado para repositórios Git, potenciado por IA (CrewAI & Gemini).

O **GuardianOps AI** é uma ferramenta inteligente concebida para monitorizar, isolar e analisar vulnerabilidades de segurança em código-fonte em tempo real. Integrado diretamente com pipelines de CI/CD através de GitHub Actions, o sistema utiliza subprocessos do Git para identificar automaticamente quais os ficheiros que foram modificados ou adicionados num commit, submetendo-os a uma auditoria rigorosa conduzida por uma equipa de agentes autónomos de IA.

---

## 🚀 Funcionalidades Dinâmicas

- **Deteção de Alvos Inteligente**: O pipeline de entrada (`src/pipeline_input.py`) interage com o Git do sistema para extrair apenas os ficheiros modificados recentemente, garantindo auditorias rápidas, focadas e eficientes.
- **Análise Multiafente (CrewAI)**: Orquestra um debate ético simulado entre dois perfis especialistas:
  - **Hacker Ético / Auditor de Segurança**: Tenta encontrar falhas críticas (ex: credenciais fixas expostas em código como em `segredo.py`, SQL Injection, má gestão de recursos).
  - **Engenheiro DevSecOps**: Valida os riscos, elimina falsos positivos e desenha planos de mitigação estruturados com base no **OWASP Top 10**.
- **Arquivamento Automatizado**: Limpa o histórico de execuções anteriores a cada ciclo e gera relatórios analíticos limpos e isolados em formato Markdown dentro da diretoria `reports/`.
- **Automação Nativa em Nuvem**: Pipeline CI/CD configurado de raiz utilizando workflows nativos do GitHub Actions.

## 🛠️ Estrutura Arquitetural do Projeto

```text
├── .github/workflows/
│   └── security_audit.yml     # Configuração e automação do pipeline CI/CD na Cloud
├── reports/                   # Arquivo de relatórios de auditoria gerados (.md)
├── src/
│   ├── __init__.py
│   ├── agents.py              # Definição e papéis da equipa de agentes CrewAI
│   ├── main.py                # Orquestrador central e gestor de ciclo de vida do fluxo
│   ├── output_handler.py      # Formatador e escritor de relatórios de saída
│   └── pipeline_input.py      # Sensor dinâmico de deteção de alterações via Git
├── tests/
│   └── test_vulnerable.py     # Script cobaia estático para testes de regressão
└── requirements.txt           # Dependências do ecossistema (CrewAI, LangChain, SDKs)
```

## 📦 Configuração e Instalação Local

### Pré-requisitos
- **Python 3.11** ou superior instalado.
- Uma chave de API válida da Google AI Studio (`GEMINI_API_KEY`).

### Passos para Configuração

1. Clone este repositório:
   ```bash
   git clone https://github.com
   cd guardianops-ai
   ```

2. Crie e ative um ambiente virtual isolado:
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/macOS:
   source venv/bin/activate
   ```

3. Instale as dependências requeridas:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as suas credenciais locais criando um ficheiro `.env` na raiz do projeto:
   ```env
   GEMINI_API_KEY=o_seu_token_aqui
   ```

## ⚙️ Como Executar e Testar

O projeto foi desenhado de forma modular. Para simular o comportamento automático da Cloud na sua máquina local, basta criar ou editar qualquer script Python na raiz (como o `segredo.py`) e executar o orquestrador principal como módulo:

```bash
python -m src.main
```

O sistema detetará a atividade no ficheiro, invocará a equipa de agentes e guardará o resultado em `reports/`.

## 📄 Licença

Este projeto é open-source e está disponível para fins educativos e de demonstração de portfólio SecOps.
