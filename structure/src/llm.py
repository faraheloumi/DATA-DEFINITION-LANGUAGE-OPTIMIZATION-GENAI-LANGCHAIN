from langchain_huggingface.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def create_llm_pipeline(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    return HuggingFacePipeline(pipeline=pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=150, return_full_text=False))

def create_instruct_pipeline(instruct_model_id):
    tokenizer = AutoTokenizer.from_pretrained(instruct_model_id)
    model = AutoModelForCausalLM.from_pretrained(instruct_model_id)
    return HuggingFacePipeline(pipeline=pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=350, return_full_text=False))
