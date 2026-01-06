import torch 
from transformers import Pipeline, pipeline
device= torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_text_model():
    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
        dtype=torch.bfloat16,
        device=device
    )
    return pipe
    

from jinja2 import Environment,FileSystemLoader

env = Environment(loader=FileSystemLoader("async_scrapper_ai/templates"))

# Create template directly from a string
template= env.get_template("prompt.j2")



def generate_text(pipe: Pipeline, prompt: str, temperature: float = 0.7) -> str:
    
    system_prompt = template.render(value="system_prompt" )
    user_prompt= template.render(value="user"  , raw_text = prompt)

    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
            ]

    prompt = pipe.tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
    )
    predictions = pipe(
    prompt,
    temperature=temperature,
    max_new_tokens=256,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    )
    output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
    return output