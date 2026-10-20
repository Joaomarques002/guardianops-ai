# 🛡️ Relatório de Auditoria GuardianOps AI
    
> **Ficheiro Auditado:** `test_vulnerable.py`  
> **Data da Análise:** 2026-10-20 19:51:03  
> **Motor de IA:** `Gemini-3.8-Flash`  

---

Aqui está o relatório técnico da auditoria de segurança estática (SAST) realizada ao ficheiro `test_vulnerable.py`.

---

# Relatório de Auditoria de Segurança de Código

Foram identificadas duas vulnerabilidades de severidade crítica/alta com base no **OWASP Top 10**.

---

### 1. Exposição de Credenciais no Código-Fonte (Hardcoded Secret)

* **Classificação OWASP:** A07:2021 – *Identification and Authentication Failures* (CWE-798: *Use of Hard-coded Credentials*)
* **Nível de Risco:** **Crítico**
* **Descrição Técnica:**
  A chave de autenticação (`AWS_SECRET_KEY`) está codificada diretamente no código-fonte. Caso este ficheiro seja adicionado a um sistema de controlo de versões (como o Git), a credencial fica exposta a qualquer pessoa com acesso de leitura ao repositório ou através de fugas acidentais de código. Isto permite que terceiros não autorizados obtenham acesso e controlo sobre recursos na infraestrutura de nuvem.

#### Correção Recomendada:
Credenciais e segredos devem ser externalizados e injetados via variáveis de ambiente ou através de um gestor de segredos (Secrets Manager / HashiCorp Vault), garantindo que nunca residem em texto simples no repositório.

---

### 2. Injeção de SQL (SQL Injection)

* **Classificação OWASP:** A03:2021 – *Injection* (CWE-89: *Improper Neutralization of Special Elements used in an SQL Command*)
* **Nível de Risco:** **Alto**
* **Descrição Técnica:**
  O parâmetro `user_id` é interpolado diretamente na instrução SQL através de uma *f-string* sem qualquer validação ou parametrização:
  ```python
  query = f"SELECT * FROM users WHERE id = '{user_id}'"
  ```
  Esta prática permite a manipulação da estrutura semântica da consulta SQL através de dados introduzidos pelo utilizador. Um atacante pode alterar a lógica da pesquisa para aceder a registos de outros utilizadores, extrair a totalidade dos dados da tabela ou contornar restrições de controlo de acessos.

#### Correção Recomendada:
Utilizar **queries parametrizadas** (*Prepared Statements*). O motor da base de dados trata os parâmetros estritamente como literais de dados e nunca como comandos executáveis.

---

## Código Corrigido

Abaixo encontra-se a versão corrigida, implementando:
1. Obtenção de segredos a partir de variáveis de ambiente.
2. Parametrização segura da consulta SQL (`?`).
3. Gestão segura de ligações utilizando context managers (`with`) para evitar fugas de recursos e garantir o fecho correto da base de dados.

```python
import os
import sqlite3

# 1. Carregar segredos via variáveis de ambiente
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

def get_user_data(user_id: str):
    """
    Obtém dados de utilizador de forma segura utilizando queries parametrizadas.
    """
    # 2. Utilização de context manager para gerir a ligação e fechar o cursor
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        
        # 3. Query parametrizada (evita injeção de SQL)
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        
        return cursor.fetchall()
```

---
*Relatório gerado automaticamente por GuardianOps AI. Reveja sempre as sugestões antes de aplicar em produção.*
