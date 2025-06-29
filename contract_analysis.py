from langchain.text_splitter import RecursiveCharacterTextSplitter
from granite_utils import analyze_chunk, guardian_check, granite_model


def split_text(text, chunk_size=1500, overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    return splitter.split_text(text)
def analyze_contract(markdown_text):
    """
    Processes the entire Markdown text:
    1. chunk it
    2. analyze each chunk
    3. guardian check each chunk's suggestions
    4. generate an improved contract version with all suggestions applied
    """
    chunks = split_text(markdown_text)
    results = []

    all_suggestions = []
    all_missing = []
    all_risks = []

    for idx, chunk in enumerate(chunks):
        print(f"Processing chunk {idx+1}/{len(chunks)}")
        parsed = analyze_chunk(chunk)

        # collect for global improvement
        if parsed.get("negotiation_suggestions"):
            all_suggestions.extend(parsed["negotiation_suggestions"])
        if parsed.get("missing_clauses"):
            all_missing.extend(parsed["missing_clauses"])
        if parsed.get("risky_clauses"):
            all_risks.extend(parsed["risky_clauses"])

        # Guardian check
        guardian_report = {}
        if parsed.get("negotiation_suggestions"):
            guardian_report = guardian_check(" ".join(parsed["negotiation_suggestions"]))
        parsed["guardian_issues"] = guardian_report.get("issues", [])
        results.append(parsed)

    # final improved contract in markdown
    improvement_prompt = f"""
You are a contract negotiation assistant.

Rewrite the following contract to:
- incorporate these negotiation suggestions: {all_suggestions}
- fix these missing clauses: {all_missing}
- address these risky clauses: {all_risks}

Return a professional, clean, improved contract in well-formatted markdown.

NO explanations before or after.

Here is the original contract:
{markdown_text}
"""

    try:
        improved_result = granite_model.generate(
            prompt=improvement_prompt,
            params={"decoding_method": "greedy", "max_new_tokens": 4000}
        )
        improved_md = improved_result["results"][0]["generated_text"]
    except Exception as e:
        print(f"[ERROR] Improvement generation failed: {e}")
        improved_md = "# Could not generate improved contract."

    return results, improved_md


