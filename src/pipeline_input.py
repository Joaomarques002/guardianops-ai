import os
import subprocess

def get_last_modified_file() -> str:
    """
    Descobre dinamicamente qual foi o último ficheiro Python (.py) 
    modificado no repositório, garantindo compatibilidade total com CI/CD.
    """
    root_dir = os.getcwd()
    try:
        # 1. Procura alterações no último commit de forma limpa na raiz do repositório
        result = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", "HEAD"],
            capture_output=True, text=True, check=True, cwd=root_dir
        )
        files = result.stdout.strip().split('\n')
        
        for f in files:
            f = f.strip()
            if f.endswith('.py') and os.path.exists(os.path.join(root_dir, f)):
                if not any(f.startswith(p) for p in ['src/', 'tests/', '.venv', 'venv']):
                    return f

        # 2. Alternativa: Verifica o log recente caso o 'git show HEAD' venha vazio
        result = subprocess.run(
            ["git", "log", "-n", "5", "--name-only", "--pretty=format:"],
            capture_output=True, text=True, check=True, cwd=root_dir
        )
        files = result.stdout.strip().split('\n')
        for f in files:
            f = f.strip()
            if f.endswith('.py') and os.path.exists(os.path.join(root_dir, f)):
                if not any(f.startswith(p) for p in ['src/', 'tests/', '.venv', 'venv']):
                    return f

    except Exception as e:
        print(f"[Aviso Git]: Falha ao ler histórico na cloud ({e}). A tentar varredura direta...")

    # 3. Solução de recurso infalível: Se o Git falhar na Cloud, procura o ficheiro 'segredo.py' ou outro .py na raiz
    for item in os.listdir(root_dir):
        if item.endswith('.py') and item not in ['main.py']:
            if os.path.isfile(os.path.join(root_dir, item)):
                return item

    # Se nada mais funcionar, devolve o ficheiro cobaia padrão
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