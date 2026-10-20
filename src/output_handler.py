import os
from datetime import datetime

def save_security_report(report_content: str, target_filename: str, output_dir: str = "reports") -> str:
    """
    Recebe o texto gerado pela IA e guarda-o num ficheiro Markdown estruturado.
    Adiciona um cabeçalho com a data e hora da auditoria.
    """
    # 1. Garante que a pasta de relatórios existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 2. Cria um nome de ficheiro único com base na data/hora e no ficheiro auditado
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = target_filename.replace('.', '_')
    report_file_name = f"audit_{clean_name}_{timestamp}.md"
    full_path = os.path.join(output_dir, report_file_name)
    
    # 3. Estrutura o conteúdo final com metadados úteis para a equipa de DevOps
    final_content = f"""# 🛡️ Relatório de Auditoria GuardianOps AI
    
> **Ficheiro Auditado:** `{target_filename}`  
> **Data da Análise:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **Motor de IA:** `Gemini-3.8-Flash`  

---

{report_content}

---
*Relatório gerado automaticamente por GuardianOps AI. Reveja sempre as sugestões antes de aplicar em produção.*
"""

    # 4. Grava o ficheiro no disco
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(final_content)
        
    return full_path