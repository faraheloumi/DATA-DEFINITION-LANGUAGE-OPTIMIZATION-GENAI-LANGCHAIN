from langchain_core.runnables.base import RunnableEach

class DDLOptimizer:
    def __init__(self, hf_pipeline, prompts):
        self.hf_pipeline = hf_pipeline
        self.prompts = prompts
    
    def optimize_ddl(self, ddl_queries, sql_contexts):
        if ddl_queries and sql_contexts:
            input_data = [{
                "context": f"Table: {context} | Operation type: CREATE TABLE",
                "sql_statement": ddl
            } for context, ddl in zip(sql_contexts, ddl_queries)]
            chain = self.prompts | self.hf_pipeline
            runnable_each = RunnableEach(bound=chain)

            try:
                optimized_ddls = runnable_each.invoke(input_data)
            except Exception as e:
                print(f"Erreur lors de l'optimisation : {e}")
                optimized_ddls = []