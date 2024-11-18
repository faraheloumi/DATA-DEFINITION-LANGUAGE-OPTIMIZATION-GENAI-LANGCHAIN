from src.extractors import extract_ddl_queries, extract_info_runnable, extract_ddls, extract_sql_context, extract_optimized_ddl
from src.llm import create_llm_pipeline, create_instruct_pipeline, create_llm_pipeline_starcoder
from src.sql_analyzer import SQLAnalyzer
from src.ddl_optimizer import DDLOptimizer
from src import prompts
from utils.utils import print_results, export_result_to_file, save_optimized_ddls
from config.config import MODEL_ID, INSTRUCT_MODEL_ID, SQL_FILE_PATH, MODEL_NAME, DDL_FILE_PATH, SQL_CONTEXT_FILE_PATH, OUTPUT_FILE

# Setup pipelines
hf_pipeline = create_llm_pipeline(MODEL_ID)
hf_instruct_pipeline = create_instruct_pipeline(INSTRUCT_MODEL_ID)
hf_starcoder_pipeline = create_llm_pipeline_starcoder(MODEL_NAME)

# Load SQL queries
queries = extract_ddl_queries(SQL_FILE_PATH)

# Load DDL queries
ddl_queries = extract_ddls(DDL_FILE_PATH)

#Load SQL context
sql_context = extract_sql_context(SQL_CONTEXT_FILE_PATH)

# Define extractors
extractor = extract_info_runnable(sub_patterns=["Tables involved", "Operation type", "JOIN conditions", "WHERE conditions"])
global_extractor = extract_info_runnable(sub_patterns=["Repeated access patterns", "JOIN optimization", "WHERE condition improvements", "Suggested indexes"])

# Initialize Analyzer
analyzer = SQLAnalyzer(hf_pipeline, hf_instruct_pipeline, extractor, global_extractor, prompts)

# Initialize Optimizer
optimized_ddls = DDLOptimizer(hf_pipeline, prompts)

# Run full pipeline
results = analyzer.invoke_full_pipeline(queries)

# Correct DDL Errors
corrected_ddls = [extract_optimized_ddl(ddl) for ddl in optimized_ddls]

# Save DDL
save_optimized_ddls(corrected_ddls, OUTPUT_FILE)

# Print context result
print_results(results, "SQL Analysis")

# Print DDL result
print("Le résultat est sauvegardé dans le fichier ddl_optimized.sql")

# Export result to file
export_result_to_file(results, "sql_analysis_results")

# # Reload as a single string
# with open('descriptions.txt', 'r') as f:
#     descriptions = f.read()

# # Run global analysis
# global_analysis = analyzer.analyze_global_patterns(descriptions.split("\n"))

# # Print result
# print_results(global_analysis, "Global Analysis")