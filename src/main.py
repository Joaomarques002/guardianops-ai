import os
import shutil
from src.pipeline_input import get_last_modified_file, read_code_file, format_code_for_ai
from src.agents import run_advanced_crew_audit
from src.output_handler import save_security_report

def main():
    print("🚀 A iniciar a auditoria AVANÇADA com CrewAI...")
    
    # 0. Limpeza preventiva da pasta reports para não misturar artefactos antigos
    if os.path.exists("reports"):
        shutil.rmtree("reports")
    os.makedirs("reports", exist_ok=True)
    
    # 1. Identificar o ficheiro alvo
    target_file = get_last_modified_file()
    filename = os.path.basename(target_file)
    
    print(f"🎯 FICHEIRO SELECIONADO PELO PIPELINE: {target_file}")
    print(f"📄 NOME BASE DO ALVO: {filename}")
    
    try:
        # 2. Pipeline de Entrada
        print(f"📦 A carregar o conteúdo de: {target_file}")
        raw_code = read_code_file(target_file)
        formatted_code = format_code_for_ai(filename, raw_code)
        
        # 3. Cérebro da IA
        print("👥 A iniciar o debate dos agentes sobre o ficheiro atual...")
        report = run_advanced_crew_audit(formatted_code)
        
        # 4. Pipeline de Saída
        print("💾 A gerar o novo relatório...")
        report_path = save_security_report(report, filename)
        
        print("\n" + "="*40 + " SUCESSO " + "="*40)
        print(f"✅ Auditoria concluída! Novo relatório em: {report_path}")
        print("="*89)
        
    except Exception as e:
        print(f"❌ Ocorreu um erro durante a execução: {e}")

if __name__ == "__main__":
    main()
