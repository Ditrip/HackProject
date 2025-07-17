from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Literal

class MyLLM:
    def __init__(self, device: Literal["cpu","cuda"] = "cpu"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(
            "HuggingFaceTB/SmolLM2-360M-Instruct"
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "HuggingFaceTB/SmolLM2-360M-Instruct"
        ).to(device)

        self.system_prompt = {
            "role": "system",
            "content": "You are a helpful, concise AI assistant. Always use only the provided context. If you cannot find the answer, say 'I don't know'."
        }

    def _clean_response(self, full_response: str) -> str:
        # Possible markers before the actual answer starts
        markers = ["Answer:", "assistant\n", "assistant:", "assistant"]

        for marker in markers:
            if marker in full_response:
                # Split on marker, take the part after it
                answer = full_response.split(marker, 1)[1]

                # Strip unwanted whitespace and newlines
                answer = answer.strip()

                # Also remove trailing 'assistant' if present at the start
                if answer.lower().startswith("assistant"):
                    answer = answer[len("assistant"):].strip()

                return answer
    
    def _generate(self, messages, max_new_tokens=200):
        # Convert messages into a chat template
        input_text = self.tokenizer.apply_chat_template(messages, tokenize=False)
        inputs = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)

        outputs = self.model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.2,
            top_p=0.9,
            do_sample=True
        )

        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return self._clean_response(full_response)

    def answer_from_context(self, document: str, question: str):
        # Build a prompt with context
        context_prompt = (
            f"Here is some reference context:\n\n"
            f"{document}\n\n"
            f"Now, answer the following question based ONLY on the context above.\n"
            f"Question: {question}\n\nAnswer:"
        )

        messages = [
            self.system_prompt,
            {"role": "user", "content": context_prompt}
        ]

        return self._generate(messages, max_new_tokens=50)
