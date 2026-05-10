import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json

# Back to the fast 0.5B model
MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

# Load the model and tokenizer
print(f"Loading Fast AI model ({MODEL_NAME}). Please wait...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype="auto", device_map="auto")
# Fix the pad token warning
tokenizer.pad_token = tokenizer.eos_token
print("AI Model loaded successfully!")

def analyze_code_with_ai(code, language):
    """
    Analyzes code locally using 0.5B model with few-shot examples.
    """
    prompt = f"""
    Analyze the following {language} code. 
    You MUST follow this exact format:

    EXAMPLE RESPONSE:
    {{
        "general_explanation": "This is a recursive function.",
        "time_complexity_original": "O(2^n)",
        "line_by_line_explanation": "The function calls itself twice.",
        "optimized_code": "def fib(n):\\n    a, b = 0, 1\\n    for _ in range(n): a, b = b, a + b\\n    return a",
        "time_complexity_optimized": "O(n)",
        "optimization_explanation": "Using iteration is much faster than recursion."
    }}

    REAL CODE TO ANALYZE:
    {code}
    """

    messages = [
        {"role": "system", "content": "You are a senior dev. You only output valid JSON. No conversational text."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # Fast generation settings
    generated_ids = model.generate(
        model_inputs.input_ids, 
        max_new_tokens=512, 
        do_sample=False,
        pad_token_id=tokenizer.pad_token_id
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    raw_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # Cleaner Logic
    try:
        if "{" in raw_text:
            start = raw_text.find("{")
            end = raw_text.rfind("}") + 1
            data = json.loads(raw_text[start:end])
            return data
    except Exception as e:
        print(f"Format Error: {e}")
    
    return {
        "general_explanation": "AI generated a response.",
        "time_complexity_original": "N/A",
        "line_by_line_explanation": "Formatting issue with the small model.",
        "optimized_code": raw_text,
        "time_complexity_optimized": "N/A",
        "optimization_explanation": "Raw AI output shown above."
    }
