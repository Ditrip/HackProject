from transformers import AutoModelForCausalLM, AutoTokenizer
checkpoint = "HuggingFaceTB/SmolLM2-360M-Instruct"

device = "cpu" # for GPU usage or "cpu" for CPU usage
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# for multiple GPUs install accelerate and do `model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")`
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

messages = [
    {"role": "system", "content": "You are a helpful, concise AI assistant that always explains things clearly using bullet points."},
    {"role": "user", "content": "Explain the main differences between renewable and non-renewable energy sources."}
]
input_text=tokenizer.apply_chat_template(messages, tokenize=False)
print(input_text)
inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=150, temperature=0.2, top_p=0.9, do_sample=True)
for output in outputs:
    print(tokenizer.decode(output))
#print(tokenizer.decode(outputs[0]))