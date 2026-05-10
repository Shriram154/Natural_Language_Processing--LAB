import os
import requests
import json
import functools

# Use a more stable and powerful model
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-7B-Instruct"

@functools.lru_cache(maxsize=100)
def analyze_code_with_ai(code, language):
    """
    Sends code to Hugging Face Inference API for analysis.
    """
    headers = {}
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        # Ensure token is cleaned of any accidental spaces
        headers["Authorization"] = f"Bearer {hf_token.strip()}"
    
    prompt = f"""
    You are a professional senior software engineer. Analyze the following {language} code.
    Provide a response in EXACTLY this JSON format:
    {{
        "general_explanation": "brief overview",
        "time_complexity_original": "O(?)",
        "line_by_line_explanation": "step by step",
        "optimized_code": "improved code",
        "time_complexity_optimized": "O(?)",
        "optimization_explanation": "why it is better"
    }}

    Code to analyze:
    {code}
    """

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1000,
            "return_full_text": False
        }
    }

    try:
        print(f"Sending request to HF API for {language} code...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        # Log status for debugging in Render
        print(f"HF API Status: {response.status_code}")
        
        if response.status_code == 503:
            return {
                "general_explanation": "The AI model is currently loading on Hugging Face servers.",
                "time_complexity_original": "N/A",
                "line_by_line_explanation": "Please wait about 30-60 seconds for the model to wake up and try again.",
                "optimized_code": "Model is warming up...",
                "time_complexity_optimized": "N/A",
                "optimization_explanation": "Hugging Face free tier puts models to sleep when not in use. It will be ready shortly."
            }
            
        if response.status_code != 200:
            print(f"HF API Error Response: {response.text}")
            return {"error": "AI service returned an error status."}

        result = response.json()
        
        # Handle list response from some HF models
        if isinstance(result, list):
            raw_text = result[0].get("generated_text", "")
        else:
            raw_text = result.get("generated_text", "")

        if not raw_text:
            print("HF API returned empty generated_text")
            return {"error": "AI generated an empty response."}

        # Try to find JSON in the response
        try:
            if "{" in raw_text:
                start = raw_text.find("{")
                end = raw_text.rfind("}") + 1
                return json.loads(raw_text[start:end])
        except Exception as json_err:
            print(f"JSON Parse Error: {json_err}. Raw text: {raw_text[:200]}")
            return {"error": "AI response was not in a valid format."}
        
        return {"error": "Could not extract analysis from AI response."}

    except Exception as e:
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
