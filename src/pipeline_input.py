import os
import subprocess

def get_last_modified_file() -> str:
    """
    Usa comandos do Git para descobrir qual foi o último ficheiro 
    Python (.py) que foi modificado ou adicionado no repositório.
    Se falhar ou não houver Git, devolve o ficheiro de teste como fallback.
    """
    try:
        # Executa o comando: git diff --name-only HEAD~1 HEAD (vê as mudanças do último commit)
        # Se for no GitHub Actions, HEAD~1 mostra o que mudou no push.
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split('\n')
        
        # Filtra para encontrar apenas ficheiros Python que ainda existem e ignorar a pasta src/ e tests/
        for f in files:
            if f.endswith('.py') and os.path.exists(f) and not f.startswith('src/'):
                if not any(f.startswith(p) for p in ['src/', 'tests/', '.venv', 'venv']):
                    return f
                
    except Exception:
        # Se der erro (ex: primeiro commit ou sem histórico), tenta o git status
        try:
            result = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)
            files = result.stdout.strip().split('\n')
            for f in files:
                if f.endswith('.py') and os.path.exists(f) and not f.startswith('src/'):
                    return f
        except Exception:
            pass

    # Se não encontrar nada modificado, usa o nosso ficheiro cobaia por segurança
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