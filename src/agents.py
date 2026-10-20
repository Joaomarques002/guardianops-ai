import os
from dotenv import load_dotenv # type: ignore (caso o linter reclame)
from crewai import LLM, Agent, Task, Crew, Process

# Carrega as variáveis de ambiente (.env)
load_dotenv()

# 1. Configurar os Motores de IA (LLMs) usando o padrão moderno do CrewAI
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("ERRO: GEMINI_API_KEY não encontrada no ficheiro .env!")

# Modelo ultra-especializado em cibersegurança e deteção de falhas
cyber_llm = LLM(
    model="gemini/gemini-3.8-flash",
    api_key=api_key,
    temperature=0.1
)

# Modelo geral focado em excelente raciocínio e revisão de software
software_llm = LLM(
    model="gemini/gemini-3.8-flash",
    api_key=api_key,
    temperature=0.2
)

def run_advanced_crew_audit(code_content: str) -> str:
    """
    Orquestra a equipa de agentes (Auditor + Revisor) usando o CrewAI
    para gerar um relatório de segurança ultra-preciso.
    """
    
    # -------------------------------------------------------------
    # 2. DEFINIÇÃO DOS AGENTES
    # -------------------------------------------------------------
    
    auditor_agent = Agent(
        role="Hacker Ético & Auditor de Segurança",
        goal="Identificar agressivamente falhas críticas de segurança (OWASP Top 10) no código fornecido.",
        backstory=(
            "És um especialista em testes de penetração em código (SAST). O teu olho clínico "
            "deteta vulnerabilidades ocultas como injeções, segredos expostos em texto limpo, "
            "e falhas de controlo de acessos. A tua postura é implacável para garantir risco zero."
        ),
        llm=cyber_llm,
        verbose=True
    )

    revisor_agent = Agent(
        role="Engenheiro DevSecOps Sénior & Revisor de Código",
        goal="Analisar os riscos apontados pelo Auditor, eliminar falsos positivos e formatar a solução ideal.",
        backstory=(
            "És um experiente arquiteto de software focado em segurança de pipelines. O teu papel "
            "é filtrar os alertas do Auditor para garantir que a equipa só recebe avisos legítimos. "
            "Sabes como escrever código seguro, eficiente e conheces as melhores práticas de remediação."
        ),
        llm=software_llm,
        verbose=True
    )

    # -------------------------------------------------------------
    # 3. DEFINIÇÃO DAS TAREFAS
    # -------------------------------------------------------------
    
    task_audit = Task(
        description=(
            f"Analisa minuciosamente o seguinte código:\n\n{code_content}\n\n"
            "Cria uma lista detalhada de todas as possíveis falhas de segurança encontradas. "
            "Anota o ficheiro, a linha aproximada e a razão do perigo."
        ),
        expected_output="Uma lista estruturada contendo apenas as vulnerabilidades potenciais e os seus vetores de ataque.",
        agent=auditor_agent
    )

    task_review = Task(
        description=(
            "Examina a lista gerada pelo Auditor de Segurança. Valida se os riscos são reais. "
            "Para cada risco confirmado, cria um bloco estruturado contendo:\n"
            "- Nível de Risco (Crítico, Alto, Médio, Baixo)\n"
            "- Descrição Clara do Problema\n"
            "- Código Corrigido e Seguro que resolve a falha.\n\n"
            "Importante: Filtra quaisquer alarmes falsos. Responde estritamente em Português e formato Markdown limpo."
        ),
        expected_output="Um relatório final unificado em Markdown contendo os riscos validados e as respetivas correções.",
        agent=revisor_agent
    )

    # -------------------------------------------------------------
    # 4. CRIAÇÃO DA EQUIPA (CREW) E EXECUÇÃO
    # -------------------------------------------------------------
    
    security_crew = Crew(
        agents=[auditor_agent, revisor_agent],
        tasks=[task_audit, task_review],
        process=Process.sequential, # O Auditor corre primeiro, o Revisor corre a seguir
        verbose=True
    )

    # Inicia o fluxo de trabalho da equipa
    result = security_crew.kickoff()
    
    # O CrewAI devolve um objeto CrewOutput, convertemos para string de forma segura
    return str(result)
