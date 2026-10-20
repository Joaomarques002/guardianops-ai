import os
from dotenv import load_dotenv # type: ignore (caso o linter reclame)

from google import genai
from google.genai import types

# Carrega as variáveis do ficheiro .env
load_dotenv()


def get_gemini_client():
    """Inicializa o cliente oficial do Gemini usando a API Key do .env"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("ERRO: GEMINI_API_KEY não encontrada no ficheiro .env!")
    return genai.Client(api_key=api_key)

def run_security_audit(code_snippet: str) -> str:
    """
    Submete o código ao Gemini com um System Prompt altamente especializado
    que força a IA a atuar como um Hacker Ético / Auditor DevSecOps.
    """
    client = get_gemini_client()
    
    system_instruction = """
    Tu és um Engenheiro de DevSecOps Sénior e Hacker Ético Especialista em Auditoria de Código (SAST).
    O teu trabalho é analisar o código fornecido pelo utilizador e identificar falhas graves de segurança baseadas no OWASP Top 10.
    
    Regras estritas de resposta:
    1. Sê direto, técnico e profissional.
    2. Identifica apenas falhas reais de segurança (como segredos expostos, vulnerabilidades de injeção, falhas de lógica). Ignora avisos estéticos ou estilo de código (PEP8).
    3. Para cada falha encontrada, apresenta:
       - Nível de Risco (Crítico, Alto, Médio, Baixo)
       - Descrição Técnica da Vulnerabilidade
       - Exemplo de como corrigir o código de forma segura.
    4. Responde obrigatoriamente em formato Markdown limpo e em Português.
    """
    
    # Chamada oficial usando o SDK moderno da Google (Gemini 3.8 Flash)
    response = client.models.generate_content(
        model='gemini-3.8-flash',
#        model='gemini-3.8-pro',
        contents=f"Por favor, audita o seguinte código:\n\n{code_snippet}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2, # Baixa temperatura para evitar alucinações técnicas
        )
    )
    
    return response.text
