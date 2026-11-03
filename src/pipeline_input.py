import os
import subprocess

def get_last_modified_file() -> str:
    """
    Descobre dinamicamente qual foi o último ficheiro Python (.py) 
    modificado no repositório, adaptado para ambientes locais e GitHub Actions.
    """
    try:
        # 1. Tenta ver todos os ficheiros alterados no último commit de forma limpa
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", "HEAD"],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split('\n')
        
        for f in files:
            f = f.strip()
            if f.endswith('.py') and os.path.exists(f):
                # Garante que ignora a pasta do auditor (src), testes e ambientes virtuais
                if not any(f.startswith(p) for p in ['src/', 'tests/', '.venv', 'venv']):
                    return f

        # 2. Se o passo anterior falhar ou não trouxer nada (ex: merge commits complexos),
        # lista os ficheiros Python alterados recentemente ordenados por data de modificação no Git
        result = subprocess.run(
            ["git", "log", "-n", "5", "--name-only", "--pretty=format:"],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split('\n')
        for f in files:
            f = f.strip()
            if f.endswith('.py') and os.path.exists(f):
                if not any(f.startswith(p) for p in ['src/', 'tests/', '.venv', 'venv']):
                    return f

    except Exception as e:
        print(f"[Aviso Git]: Falha ao ler histórico do Git ({e}). A tentar varredura local...")

    # 3. Fallback Local Sem Git: Procura qualquer ficheiro .py solto na raiz do projeto (ex: segredo.py)
    # excluindo ficheiros de configuração conhecidos
    for item in os.listdir('.'):
        if item.endswith('.py') and item not in ['segredo.py_backup']: 
            if os.path.isfile(item):
                return item

    # Se mesmo assim não encontrar nada, usa o ficheiro padrão de testes
    return os.path.join("tests", "test_vulnerable.py")

def read_code_file(file_path: str) -> str:
    """Lê o conteúdo de um ficheiro de código local."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"O ficheiro alvo não foi encontrado em: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def format_code_for_ai(file_name: str, code_content: str) -> str:
    """Embrulha o código em Markdown para o LLM."""
    file_extension = file_name.split('.')[-1] if '.' in file_name else ''
    formatted_prompt = f"--- INÍCIO DO FICHEIRO: {file_name} ---\n"
    formatted_prompt += f"```{file_extension}\n"
    formatted_prompt += f"{code_content}\n"
    formatted_prompt += "```\n"
    formatted_prompt += f"--- FIM DO FICHEIRO: {file_name} ---"
    return formatted_prompt