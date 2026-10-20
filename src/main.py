import os
from pipeline_input import read_code_file, format_code_for_ai
from agents import run_security_audit

def main():
    print("🚀 A iniciar a auditoria do GuardianOps AI...")
    
    # Caminho para o nosso ficheiro cobaia vulnerável
    target_file = os.path.join("tests", "test_vulnerable.py")
    
    try:
        # 1. Pipeline de Entrada: Ler o ficheiro
        print(f"📦 A carregar o ficheiro: {target_file}")
        raw_code = read_code_file(target_file)
        formatted_code = format_code_for_ai("test_vulnerable.py", raw_code)
        
        # 2. Cérebro da IA: Correr a auditoria
        print("🧠 A analisar o código com o agente DevSecOps (Gemini 3.8)...")
        report = run_security_audit(formatted_code)
        
        # 3. Exibir o Relatório Inicial no Terminal
        print("\n" + "="*40 + " RELATÓRIO DE SEGURANÇA " + "="*40)
        print(report)
        print("="*104)
        
    except Exception as e:
        print(f"❌ Ocorreu um erro durante a execução: {e}")

if __name__ == "__main__":
    main()
