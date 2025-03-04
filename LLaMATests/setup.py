import os
import transformers
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

print("add token")
hf_token = 'xyz'
os.environ['HF_TOKEN'] = hf_token
os.environ['HUGGINGFACEHUB_API_TOKEN'] = hf_token

model_name = "meta-llama/Llama-2-7b-hf"

tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype="auto",
    token=hf_token)

model.eval()
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
