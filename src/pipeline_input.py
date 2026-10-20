import os

def read_code_file(file_path: str) -> str:
    """
    Lê o conteúdo de um ficheiro de código local.
    Em fases futuras, esta função será expandida para capturar o 'git diff'.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"O ficheiro alvo não foi encontrado em: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    return content

def format_code_for_ai(file_name: str, code_content: str) -> str:
    """
    Embrulha o código em Markdown estruturado para garantir que o LLM
    compreende a linguagem e o contexto do ficheiro enviado.
    """
    # Identifica a extensão para ajudar a sintaxe do LLM
    file_extension = file_name.split('.')[-1] if '.' in file_name else ''
    
    formatted_prompt = f"--- INÍCIO DO FICHEIRO: {file_name} ---\n"
    formatted_prompt += f"```{file_extension}\n"
    formatted_prompt += f"{code_content}\n"
    formatted_prompt += "```\n"
    formatted_prompt += f"--- FIM DO FICHEIRO: {file_name} ---"
    
    return formatted_prompt
