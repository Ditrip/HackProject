from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Dict, Literal

tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-360M-Instruct")
model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-360M-Instruct")


class MyLLM:

    device: Literal["cpu","cuda"]  = "cpu"  # for GPU usage or "cpu" for CPU usage

    instr = {
            "role": "system",
            "content": "You are a helpful, concise AI assistant that always explains things clearly using bullet points.",
        }

    def __init__(self, device: Literal["cpu","cuda"] = "cpu" ):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(
            "HuggingFaceTB/SmolLM2-360M-Instruct"
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "HuggingFaceTB/SmolLM2-360M-Instruct"
        )

    def set_question(self, input_text:str):
        message = [self.instr,{
        "role": "user",
        "content": input_text,
        }
                   ]
        input_text = self.tokenizer.apply_chat_template(message, tokenize=False)
        inputs = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            inputs, max_new_tokens=50, temperature=0.2, top_p=0.9, do_sample=True
        )

        return self.tokenizer.decode(outputs[0])
