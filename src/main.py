import os
from pipeline_input import get_last_modified_file, read_code_file, format_code_for_ai
from agents import run_advanced_crew_audit
from output_handler import save_security_report

def main():
    print("🚀 A iniciar a auditoria AVANÇADA com CrewAI (Gemini 3.8)...")
    
    target_file = get_last_modified_file()
    filename = os.path.basename(target_file)
    
    print(f"🎯 Ficheiro identificado para análise: {target_file}")
    
    try:
        # 1. Pipeline de Entrada
        print(f"📦 A carregar o ficheiro: {target_file}")
        raw_code = read_code_file(target_file)
        formatted_code = format_code_for_ai(filename, raw_code)
        
        # 2. Cérebro da IA
        print("👥 A iniciar o debate entre o Hacker e o DevSecOps...")
        report = run_advanced_crew_audit(formatted_code)
        
        # 3. Pipeline de Saída
        print("💾 A gerar e guardar o relatório Markdown...")
        report_path = save_security_report(report, filename)
        
        print("\n" + "="*40 + " SUCESSO " + "="*40)
        print(f"✅ Auditoria concluída! Relatório guardado em: {report_path}")
        print("="*89)
        
    except Exception as e:
        print(f"❌ Ocorreu um erro durante a execução: {e}")

if __name__ == "__main__":
    main()
