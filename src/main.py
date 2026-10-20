import os
from pipeline_input import read_code_file, format_code_for_ai
from agents import run_security_audit
from output_handler import save_security_report  # Importa o novo bloco

def main():
    print("🚀 A iniciar a auditoria do GuardianOps AI...")
    
    filename = "test_vulnerable.py"
    target_file = os.path.join("tests", filename)
    
    try:
        # 1. Pipeline de Entrada
        print(f"📦 A carregar o ficheiro: {target_file}")
        raw_code = read_code_file(target_file)
        formatted_code = format_code_for_ai(filename, raw_code)
        
        # 2. Cérebro da IA
        print("🧠 A analisar o código com o agente DevSecOps (Gemini 3.8)...")
        report = run_security_audit(formatted_code)
        
        # 3. Pipeline de Saída: Guardar o Relatório
        print("💾 A gerar e guardar o relatório Markdown...")
        report_path = save_security_report(report, filename)
        
        print("\n" + "="*40 + " SUCESSO " + "="*40)
        print(f"✅ Auditoria concluída! Relatório guardado em: {report_path}")
        print("="*89)
        
    except Exception as e:
        print(f"❌ Ocorreu um erro durante a execução: {e}")

if __name__ == "__main__":
    main()
