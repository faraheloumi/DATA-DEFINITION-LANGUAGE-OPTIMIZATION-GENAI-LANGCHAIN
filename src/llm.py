import torch
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

def create_llm_pipeline_starcoder(MODEL_NAME):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, torch_dtype=torch.float16, device_map="auto" if device == "cuda" else None
    )
    return HuggingFacePipeline(pipeline=pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1, max_new_tokens=150, temperature=0.7, do_sample=True, return_full_text=False,))

