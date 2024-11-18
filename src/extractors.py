import re
import sqlparse
from langchain_core.runnables import RunnableLambda
from functools import partial


def extract_ddl_queries(file_path):
    with open(file_path, 'r') as file:
        sql_content = file.read()
    # Remove single-line and block comments
    sql_content = re.sub(r'--.*?$', '', sql_content, flags=re.MULTILINE)
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
    # Use sqlparse to split and filter out DDL queries
    statements = sqlparse.split(sql_content)
    ## UTILIZE BELOW INCASE OF HYBRID FILE
    # ddl_queries = [stmt for stmt in statements if stmt.strip().upper().startswith(('CREATE', 'ALTER', 'DROP'))]
    ddl_queries = [stmt for stmt in statements]
    
    return ddl_queries

def gen_pattern(section, last=False):
    sub_pattern = section.replace(" ", r"\s*")
    
    if last:
        # Use the pattern similar to where_pattern
        return re.compile(
            r"(?i)"
            fr"(?:[\*\*]*|\#{{1,3}})\s*{sub_pattern}\s*[\*\*]*:*\s*[\*\*]*\n*([\s\S]*?)(?=(?:\n-\s*|\n\*\*|\n\#{{1,3}}|\Z))",
            re.VERBOSE | re.DOTALL
        )
    else:
        # Use the original pattern
        return re.compile(
            r"(?i)"
            fr"(?:[\*\*]*|\#{{1,3}})\s*{sub_pattern}\s*[\*\*]*:*\s*[\*\*]*\n*([\s\S]*?)(?=\n(?:-\s*|\*\*|\#{{1,3}}|\Z))",
            re.VERBOSE | re.DOTALL
        )

def extract_info(text, sub_patterns):
    # Define patterns for each section
    patterns = []
    extraction = ""
    # Generate patterns for each section
    for i, sub_p in enumerate(sub_patterns):
        last = (i == len(sub_patterns) - 1)  # Apply 'last' parameter only to the last element
        try:
            patterns += [gen_pattern(sub_p, last).search(text).group(1).strip()]
        except:
            patterns += ["N/A"] 
        extraction += f"{sub_p}: {patterns[i]}\n" 
    return extraction

def extract_info_runnable(sub_patterns):
    return RunnableLambda(partial(extract_info, sub_patterns=sub_patterns))

def extract_ddls(file_path):
    """Extrait les DDLs d'un fichier."""
    try:
        with open(file_path, 'r') as file:
            data = file.read()
        ddl_statements = re.findall(r"CREATE TABLE.*?;", data, re.DOTALL)
        return ddl_statements
    except FileNotFoundError:
        return []

def extract_sql_context(file_path):
    """Extrait les requêtes SQL à partir d'un fichier."""
    try:
        with open(file_path, 'r') as file:
            data = file.read()
        queries = re.split(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\b', data, flags=re.IGNORECASE)
        sql_queries = []
        for i in range(1, len(queries), 2):  # Parcourir par groupes de mots-clés et requêtes
            keyword = queries[i].strip()
            query_body = queries[i + 1].strip()
            sql_queries.append(f"{keyword} {query_body}")
        return [query.strip() for query in sql_queries if query.strip()]
    except FileNotFoundError:
        return []

def extract_optimized_ddl(ddl_code):
    """
    Corrige les erreurs communes et optimise le code SQL.
    """
    # 1. Supprimer les virgules inutiles
    ddl_code = re.sub(r',\s*,', ',', ddl_code)
    
    # 2. Vérifier les déclarations PRIMARY KEY
    ddl_code = re.sub(r'SERIAL PRIMARY KEY,', 'SERIAL PRIMARY KEY', ddl_code)

    # 3. Supprimer les répétitions de ON DELETE CASCADE et ON UPDATE CASCADE
    ddl_code = re.sub(r'(ON DELETE CASCADE\s+)+', 'ON DELETE CASCADE ', ddl_code)
    ddl_code = re.sub(r'(ON UPDATE CASCADE\s+)+', 'ON UPDATE CASCADE ', ddl_code)

    # 4. Ajouter des NOT NULL si nécessaire
    ddl_code = re.sub(r'(\bINT\b|VARCHAR\(\d+\))(\s*,|\s*\))', r'\1 NOT NULL\2', ddl_code)

    # 5. Vérifier les contraintes UNIQUE et INDEX
    ddl_code = re.sub(r'UNIQUE\s*\((.*?)\)\s*INDEX', r'UNIQUE (\1)', ddl_code)

    # 6. Supprimer les colonnes ajoutées avec ALTER TABLE si elles existent dans CREATE TABLE
    ddl_code = re.sub(r'ALTER TABLE \w+ ADD COLUMN IF NOT EXISTS \w+ .*?;', '', ddl_code)

    # 7. Supprimer les espaces multiples et lignes inutiles
    ddl_code = re.sub(r'\s+', ' ', ddl_code).strip()
    ddl_code = re.sub(r'\s*;\s*', ';\n', ddl_code)

    # 8. Formater correctement le code SQL (optionnel : identation simplifiée)
    ddl_code = re.sub(r'(CREATE TABLE|INSERT INTO|ALTER TABLE)', r'\n\1', ddl_code)

    return ddl_code