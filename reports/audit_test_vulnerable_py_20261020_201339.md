# 🛡️ Relatório de Auditoria GuardianOps AI
    
> **Ficheiro Auditado:** `test_vulnerable.py`  
> **Data da Análise:** 2026-10-20 20:13:39  
> **Motor de IA:** `Gemini-3.8-Flash`  

---

# Relatório de Validação e Remediação DevSecOps

Após a revisão técnica detalhada das vulnerabilidades reportadas pelo Auditor de Segurança no ficheiro `test_vulnerable.py`, **todos os três apontamentos foram validados como riscos reais (verdadeiros positivos)**. Não foram identificados falsos positivos: o código expõe credenciais sensíveis, permite a execução arbitrária de comandos SQL através de interpolação insegura e não gere o ciclo de vida dos descritores de ficheiros/conexões.

Abaixo apresenta-se a validação estruturada de cada risco com as respetivas correções definitivas, seguida da versão final consolidada e segura do módulo.

---

### Item 1: Exposição de Credenciais em Código-Fonte (Hardcoded Secret)

* **Nível de Risco:** Crítico
* **Descrição Clara do Problema:** A inclusão de credenciais (como chaves de acesso a provedores cloud ou APIs) diretamente no código-fonte expõe o ecossistema a fugas de informação. O histórico de commits, forks, registos de CI/CD e cópias locais tornam o segredo acessível a terceiros não autorizados, permitindo a usurpação de identidade do serviço e movimentação lateral na infraestrutura.
* **Código Corrigido e Seguro:**
```python
import os
from typing import Optional

# Obtenção segura da credencial via variáveis de ambiente ou secret manager
API_KEY: Optional[str] = os.getenv("APP_API_KEY")

if not API_KEY:
    raise RuntimeError("A variável de ambiente 'APP_API_KEY' não está configurada.")
```

---

### Item 2: Injeção de SQL (SQL Injection - SQLi)

* **Nível de Risco:** Crítico
* **Descrição Clara do Problema:** A construção de consultas SQL através de concatenação ou interpolação de strings (`f-strings`) com dados controlados pelo utilizador permite que atacantes alterem a semântica da consulta. Isto viabiliza a extração de dados confidenciais, contorno de mecanismos de autenticação, modificação de dados e potencial negação de serviço. A mitigação exige a utilização estrita de *parameterized queries* (consultas parametrizadas).
* **Código Corrigido e Seguro:**
```python
# Utilização de consultas parametrizadas (placeholders '?')
# O motor SQLite trata os argumentos estritamente como dados literais, neutralizando a injeção.
query = "SELECT id, username, email FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
user_data = cursor.fetchone()
```

---

### Item 3: Fuga de Recursos e Má Gestão de Conexões (Resource Leakage)

* **Nível de Risco:** Médio
* **Descrição Clara do Problema:** A abertura manual de conexões e cursores sem mecanismos determinísticos de fecho (como blocos `try...finally` ou gestores de contexto `with`) resulta em descritores de ficheiros e bloqueios de base de dados abertos indefinidamente caso ocorram exceções ou volume elevado de requisições. No SQLite, isso acarreta erros de concorrência (`database is locked`) e potencial esgotamento de descritores no sistema operativo.
* **Código Corrigido e Seguro:**
```python
import sqlite3
from contextlib import closing

# O gestor de contexto garante o encerramento da conexão e commit/rollback automático
with sqlite3.connect("database.db") as conn:
    with closing(conn.cursor()) as cursor:
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
```

---

### Código Final Consolidado (`test_vulnerable.py` corrigido)

Abaixo encontra-se a refatoração completa do ficheiro, integrando a validação de parâmetros, gestão segura de credenciais e encerramento determinístico de recursos:

```python
import os
import sqlite3
from contextlib import closing
from typing import Any, Dict, Optional

# 1. Resolução de Credenciais: Extração a partir do ambiente de execução
API_KEY: Optional[str] = os.getenv("APP_API_KEY")
DATABASE_PATH: str = os.getenv("DATABASE_PATH", "database.db")


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Recupera os dados de um utilizador de forma segura.
    
    :param user_id: Identificador numérico do utilizador.
    :return: Dicionário com os dados do utilizador ou None se não encontrado.
    """
    # Validação de tipo defensiva
    if not isinstance(user_id, int):
        raise ValueError("O parâmetro user_id deve ser um número inteiro.")

    # 2 e 3. Resolução de Resource Leakage e SQL Injection
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.row_factory = sqlite3.Row  # Permite mapeamento limpo dos campos
        with closing(conn.cursor()) as cursor:
            query = "SELECT id, username, email FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None


if __name__ == "__main__":
    # Verificação de arranque
    if not API_KEY:
        raise SystemExit("Erro Crítico: 'APP_API_KEY' não definida no ambiente.")

    # Exemplo de consulta segura
    user = get_user_by_id(1)
    if user:
        print(f"Utilizador carregado: {user['username']}")
    else:
        print("Utilizador não encontrado.")
```

---
*Relatório gerado automaticamente por GuardianOps AI. Reveja sempre as sugestões antes de aplicar em produção.*
