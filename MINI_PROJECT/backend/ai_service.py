import os
import requests
import json

# Use a model that is absolutely guaranteed to be online
API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"

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
            return {
                "general_explanation": "The AI service returned an error.",
                "time_complexity_original": "N/A",
                "line_by_line_explanation": "Please check your HF_TOKEN in Render settings.",
                "optimized_code": "Error: API Status " + str(response.status_code),
                "time_complexity_optimized": "N/A",
                "optimization_explanation": "The Hugging Face API is either down or the token is invalid."
            }

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
                json_data = json.loads(raw_text[start:end])
                return json_data
        except Exception as json_err:
            print(f"JSON Parse Error: {json_err}. Raw text: {raw_text[:200]}")
        
        # Fallback if JSON fails
        return {
            "general_explanation": "Code analyzed successfully, but formatting was slightly off.",
            "time_complexity_original": "See explanation",
            "line_by_line_explanation": raw_text[:500],
            "optimized_code": "Check explanation for details",
            "time_complexity_optimized": "N/A",
            "optimization_explanation": "AI response format error."
        }

    except Exception as e:
        print(f"API Error Exception: {e}")
        return {
            "general_explanation": "Could not connect to AI service.",
            "time_complexity_original": "N/A",
            "line_by_line_explanation": str(e),
            "optimized_code": "Connection Error",
            "time_complexity_optimized": "N/A",
            "optimization_explanation": "Check your internet connection or backend logs."
        }
