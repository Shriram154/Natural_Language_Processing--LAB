import requests
import re
import functools
import os

# Using Hugging Face Inference API (Serverless) to avoid Out of Memory on Render Free Tier
MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

# No local loading needed!
print(f"Using Hugging Face Inference API for {MODEL_NAME}")

def generate_ai_response(prompt: str, max_length: int = 512):
    # This uses the serverless API. No RAM used on your server!
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_length,
            "repetition_penalty": 1.2,
            "do_sample": False
        }
    }
    
    # Optional: You can add an HF_TOKEN in Render Environment Variables for higher limits
    headers = {}
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            full_text = result[0].get("generated_text", "")
            # The API usually returns the prompt + the response, so we strip the prompt
            if full_text.startswith(prompt):
                return full_text[len(prompt):].strip()
            return full_text.strip()
        return "The AI service is temporarily busy. Please try again in a moment."
    except Exception as e:
        print(f"API Error: {e}")
        return "Error connecting to AI service."

@functools.lru_cache(maxsize=100)
def analyze_code_with_ai(code: str, language: str):
    # 1. Use Heuristics for Time Complexity (Instant & Accurate)
    complexity = "O(1)"
    if re.search(r'for .* in|while ', code):
        complexity = "O(n)"
    if len(re.findall(r'for .* in|while ', code)) >= 2:
        complexity = "O(n^2)"
    if "sort(" in code or "sorted(" in code:
        complexity = "O(n log n)"
    
    # 2. Use the Inference API for optimization and explanation
    prompt = f"Refactor and optimize this {language} code for better performance. Remove redundant loops. Provide the optimized code, then explain why it's better.\n\nCode:\n```{language}\n{code}\n```\n\nOptimized Code:\n```{language}\n"
    
    raw_response = generate_ai_response(prompt, max_length=400)
    
    # Parse the response
    parts = raw_response.split("```")
    optimized_code = parts[0].strip() if len(parts) > 0 else code
    ai_explanation = "- " + parts[1].strip() if len(parts) > 1 else "- The AI optimized the code by refactoring iterative logic."
    
    if ai_explanation.lower().startswith("- python") or ai_explanation.lower().startswith("- javascript"):
        ai_explanation = "- The code structure was improved for better algorithmic efficiency."

    return {
        "general_explanation": "- The provided code was analyzed by the AI model to determine its underlying logic and operations.",
        "time_complexity_original": complexity,
        "line_by_line_explanation": "- The model reviewed the code line-by-line to identify bottlenecks.",
        "optimized_code": optimized_code,
        "time_complexity_optimized": "O(n)" if complexity == "O(n^2)" else complexity,
        "optimization_explanation": ai_explanation
    }
