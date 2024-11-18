import re

def print_results(results, label="Result"):
    print(f"\n=== {label} ===")
    print(results)
    print("="*40)

def export_result_to_file(results, filename):
    with open(filename + ".txt", "w") as f:
        f.write(results)
        f.close()
    print(f"Results exported to {filename}.txt")

def clean_output(output):
    """Nettoie les optimisations générées."""
    output = re.sub(r"[-\*]", "", output).strip()
    if output.count('(') > output.count(')'):
        output += ')'
    return output

def save_optimized_ddls(optimized_ddls, file_path):
    """Sauvegarde les DDL optimisés dans un fichier."""
    try:
        with open(file_path, 'w') as out_file:
            for i, ddl in enumerate(optimized_ddls, 1):
                clean_ddl = clean_output(ddl)
                out_file.write(f"-- Optimized DDL Query {i}:\n{clean_ddl}\n\n")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des DDLs : {e}")