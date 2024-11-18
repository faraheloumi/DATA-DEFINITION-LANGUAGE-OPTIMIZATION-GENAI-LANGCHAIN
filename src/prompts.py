from langchain_core.prompts import PromptTemplate

def get_sql_analysis_prompt():
    template = (
    "You are tasked with analyzing a SQL operation. "
    "read the SQL statement carefully and provide a clear, concise summary addressing the following questions in the format provided down below:\n"
    "- Which tables are involved?\n"
    "- What types of operations (e.g., SELECT, INSERT, UPDATE) are being performed?\n"
    "- Identify any JOINs, WHERE conditions, or filtering that could impact performance.\n\n"
    "Respond in bullet point format, adhering STRICTLY to the following response structure:\n"
    "- **Tables involved**: List the tables used in the query.\n"
    "- **Operation type**: Specify the type of SQL operation being performed.\n"
    "- **JOIN conditions**: Describe any JOIN operations (if applicable). If none, state 'None'.\n"
    "- **WHERE conditions**: Detail any filtering criteria specified in the query. If none, state 'None'\n"
    # "- **Column usage patterns**: Discuss the columns being used for filtering or conditions.\n\n"
    "### SQL Operation:\n"
    "{sql_statement}\n\n" 
    )
    return PromptTemplate.from_template(template)

def get_pattern_analysis_prompt():
    template = (
    "You have been provided with a summary of multiple SQL operations, describing the tables involved, operation types, JOIN conditions, and WHERE clauses.\n"
    "Your task is to analyze the entire set of descriptions to detect any common patterns, redundancies, or optimization opportunities that wouldn't be noticeable from analyzing the queries individually.\n"
    "Specifically, focus on identifying in the format provided down below:\n"
    "- Repeated access patterns to specific tables or columns.\n"
    "- Opportunities to optimize JOINs or filtering conditions.\n"
    "- Any indications of missing indexes or inefficient queries.\n"
    "- Insights that can inform optimizations for the underlying DDL (table definitions).\n\n"
    "### SQL Operations Summary:\n"
    "{combined_descriptions}\n\n"
    "Respond in bullet point format, adhering STRICTLY to the following response structure:\n"
    "- **Repeated access patterns**: List any repeated access patterns across tables or columns.\n"
    "- **JOIN optimization**: Identify any potential JOIN improvements.\n"
    "- **WHERE condition improvements**: Highlight any opportunities to enhance WHERE conditions.\n"
    "- **Suggested indexes**: Suggest any indexes that could improve performance.\n"
    )
    return PromptTemplate.from_template(template)

def get_optimized_ddl_prompt():
    optimization_template = (
    "Optimize the following DDL query based on the provided SQL context. "
    "Focus on indexing, foreign key constraints, and data type optimization. "
    "Ensure to maintain the necessary relationships between tables.\n\n"
    "Context:\n{context}\n\n"
    "DDL Query:\n{sql_statement}\n\n"
    "Optimized DDL:\n"
    )
    return PromptTemplate.from_template(optimization_template)
