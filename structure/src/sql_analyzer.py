from langchain_core.runnables.base import RunnableEach

class SQLAnalyzer:
    def __init__(self, hf_pipeline, instruct_pipeline, extractor, global_extractor, prompts):
        self.hf_pipeline = hf_pipeline
        self.instruct_pipeline = instruct_pipeline
        self.extractor = extractor
        self.global_extractor = global_extractor
        self.prompts = prompts
    
    def analyze_queries(self, queries):
        sql_prompt = self.prompts.get_sql_analysis_prompt()
        chain = sql_prompt | self.hf_pipeline | self.extractor
        
        runnable_each = RunnableEach(bound=chain)
        descriptions = runnable_each.invoke([{"sql_statement": q} for q in queries])
        
        return descriptions
    
    def analyze_global_patterns(self, descriptions):
        combined_desc = "\n".join(descriptions)
        pattern_prompt = self.prompts.get_pattern_analysis_prompt()
        global_chain = pattern_prompt | self.instruct_pipeline | self.global_extractor
        
        result = global_chain.invoke({"combined_descriptions": combined_desc})
        return result
    
    def invoke_full_pipeline(self, queries, raw = False):
        descriptions = self.analyze_queries(queries)
        global_analysis = self.analyze_global_patterns(descriptions)
        return (
            f"=== Individual Query Analysis ===\n{"\n".join(descriptions)}\n{'='*40}\n"
            f"=== Global Analysis ===\n{global_analysis}"
        ) if not raw else f"{"\n".join(descriptions)}\n{global_analysis}"
                           
