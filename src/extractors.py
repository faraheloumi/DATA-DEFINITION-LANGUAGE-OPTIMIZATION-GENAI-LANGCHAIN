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