import os
import json
import re

from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai import APIClient
load_dotenv()
# Load from .env or environment
API_KEY = os.environ.get("WATSONX_APIKEY")
print(API_KEY)
PROJECT_ID = os.environ.get("WATSONX_PROJECT_ID")
ENDPOINT_URL = os.environ.get("WATSONX_URL")


credentials = {
    "apikey": API_KEY,
    "url": ENDPOINT_URL,
}

client = APIClient(
    credentials=credentials,
    project_id=PROJECT_ID,
)

granite_model = Model(
    model_id="ibm/granite-3-3-8b-instruct",
    params={"decoding_method": "greedy", "max_new_tokens": 1500},
    credentials=credentials,
    project_id=PROJECT_ID,
)

guardian_model = Model(
    model_id="ibm/granite-guardian-3-8b",
    params={"decoding_method": "greedy", "max_new_tokens": 500},
    credentials=credentials,
    project_id=PROJECT_ID,
)

def extract_last_json_block(text: str) -> dict:
    from json import JSONDecoder
    decoder = JSONDecoder()
    idx = 0
    last = None
    while idx < len(text):
        try:
            obj, end = decoder.raw_decode(text[idx:])
            # only accept dicts
            if isinstance(obj, dict):
                last = obj
            idx += end
        except Exception:
            idx += 1

    if last:
        # Patch: standardize severity_table to always be a list
        if "severity_table" in last:
            if isinstance(last["severity_table"], dict):
                # flatten dict into a list of rows
                flat = []
                for key, val in last["severity_table"].items():
                    flat.append({
                        "clause": key,
                        "severity": val,
                        "rationale": ""
                    })
                last["severity_table"] = flat
        return last
    else:
        return {
            "summary": "No valid JSON found.",
            "risky_clauses": [],
            "missing_clauses": [],
            "negotiation_suggestions": [],
            "compliance_checklist": [],
            "severity_table": [],
        }


def analyze_chunk(chunk):
    prompt = f"""
You are a contract negotiation assistant.
Respond strictly in JSON with these fields:
- summary
- risky_clauses
- missing_clauses
- negotiation_suggestions
- compliance_checklist
- severity_table
NO explanations before or after.
CONTRACT:
{chunk}
"""
    result = granite_model.generate(
        prompt=prompt,
        params={"decoding_method": "greedy","max_new_tokens":1500}
    )
    text = result["results"][0]["generated_text"]
    print("======= RAW GRANITE OUTPUT =======")
    print(text)
    print("======= END RAW GRANITE OUTPUT =======")
    return extract_last_json_block(text)

def guardian_check(text: str) -> dict:
    """
    Checks any text for HAP/risk issues using Granite Guardian
    """
    prompt = f"""
You are a safety auditor. Scan this text for hate, abuse, or profanity, returning JSON with:
{{
  "issues": ["list of any HAP or risky language spotted"]
}}
Here is the text:
{text}
"""
    try:
        result = guardian_model.generate(
            prompt=prompt,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 500
            }
        )
        text = result["results"][0]["generated_text"]
        print("======= RAW GUARDIAN OUTPUT =======")
        print(text)
        print("======= END RAW GUARDIAN OUTPUT =======")
        parsed = extract_last_json_block(text)
        return parsed

    except Exception as e:
        print(f"[ERROR] Guardian check failed: {e}")
        return {"issues": []}
