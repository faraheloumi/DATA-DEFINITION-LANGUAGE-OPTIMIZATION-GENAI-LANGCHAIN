from src.extractors import extract_ddl_queries, extract_info_runnable
from src.llm import create_llm_pipeline, create_instruct_pipeline
from src.sql_analyzer import SQLAnalyzer
from src import prompts
from utils.utils import print_results, export_result_to_file
from config.config import MODEL_ID, INSTRUCT_MODEL_ID, SQL_FILE_PATH

# Setup pipelines
hf_pipeline = create_llm_pipeline(MODEL_ID)
hf_instruct_pipeline = create_instruct_pipeline(INSTRUCT_MODEL_ID)

# Load SQL queries
queries = extract_ddl_queries(SQL_FILE_PATH)

# Define extractors
extractor = extract_info_runnable(sub_patterns=["Tables involved", "Operation type", "JOIN conditions", "WHERE conditions"])
global_extractor = extract_info_runnable(sub_patterns=["Repeated access patterns", "JOIN optimization", "WHERE condition improvements", "Suggested indexes"])

# Initialize Analyzer
analyzer = SQLAnalyzer(hf_pipeline, hf_instruct_pipeline, extractor, global_extractor, prompts)

# Run full pipeline
results = analyzer.invoke_full_pipeline(queries)

# Print result
print_results(results, "SQL Analysis")

# Export result to file
export_result_to_file(results, "sql_analysis_results")

# # Reload as a single string
# with open('descriptions.txt', 'r') as f:
#     descriptions = f.read()

# # Run global analysis
# global_analysis = analyzer.analyze_global_patterns(descriptions.split("\n"))

# # Print result
# print_results(global_analysis, "Global Analysis")