import streamlit as st
from contract_analysis import analyze_contract
from doc_utils import convert_contract
import os

st.set_page_config(page_title="GranNegotiate: Contract Copilot", layout="wide")

# header at the top
st.markdown(
    """
    <div style='text-align:center; font-size:28px; font-weight:bold; margin-bottom:5px'>
        🤝 GranNegotiate: Contract Copilot
    </div>
    <div style='text-align:center; font-size:15px; margin-bottom:10px'>
        👋 Hi! I’m your Contract Copilot — let’s get negotiating with confidence.
    </div>
    <hr style='margin-top:10px; margin-bottom:25px;'>
    """,
    unsafe_allow_html=True
)

# 2:3 column layout
left_col, right_col = st.columns([2, 3], gap="large")

with left_col:
    st.subheader("🚀 Quick Start with a Sample Contract")
    sample_path = "sample_contracts/sample_contract.pdf"
    if os.path.exists(sample_path):
        st.download_button(
            "⬇️ Download Sample Contract",
            data=open(sample_path, "rb"),
            file_name="sample_contract.pdf"
        )
        if st.button("Use This Sample for Analysis"):
            st.session_state["use_sample"] = True
    else:
        st.error("Sample contract not found.")

    st.markdown("---")

    st.subheader("📄 Or Upload Your Own Contract")
    uploaded = st.file_uploader("Upload a contract (PDF or DOCX)", type=["pdf", "docx"])

    st.markdown("---")
    st.subheader("📥 Download Contract Markdown")

    if st.session_state.get("markdown_text"):
        st.download_button(
            label="Download Contract as Markdown",
            data=st.session_state["markdown_text"],
            file_name="contract.md",
            mime="text/markdown",
            help="Download the uploaded or sample contract converted to markdown"
        )
    else:
        st.info("No markdown to download yet — upload or select a contract first.")

with right_col:
    results = None
    improved_md = None
    file_path = None

    if st.session_state.get("use_sample"):
        file_path = sample_path
    elif uploaded:
        os.makedirs("sample_contracts", exist_ok=True)
        file_path = os.path.join("sample_contracts", uploaded.name)
        with open(file_path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.success("Contract uploaded successfully.")

    if file_path:
        st.info("Converting the contract with Docling...")
        markdown_text = convert_contract(file_path)
        if markdown_text:
            st.session_state["markdown_text"] = markdown_text
            st.info("Analyzing with Granite models...")
            results, improved_md = analyze_contract(markdown_text)

    if results:
        st.divider()
        st.subheader("🔎 Contract Analysis Results")

        for idx, chunk in enumerate(results):
            with st.expander(f"📄 Analysis Section {idx + 1}", expanded=False):
                st.markdown(f"**Summary**:\n{chunk.get('summary', '')}")
                st.markdown("**Risky Clauses:**")
                for clause in chunk.get("risky_clauses", []):
                    st.warning(f"- {clause}")
                st.markdown("**Missing Clauses:**")
                for clause in chunk.get("missing_clauses", []):
                    st.info(f"- {clause}")
                st.markdown("**Negotiation Suggestions:**")
                for sug in chunk.get("negotiation_suggestions", []):
                    st.code(sug, language="markdown")
                st.markdown("**Compliance Checklist:**")
                for item in chunk.get("compliance_checklist", []):
                    st.write(f"- {item}")
                if chunk.get("severity_table"):
                    st.markdown("**Severity Table:**")
                    st.table(chunk["severity_table"])
                if chunk.get("guardian_issues"):
                    st.error(f"🛡 Guardian flagged: {chunk['guardian_issues']}")

        # combined summary button
        if st.button("📝 Generate Full Combined Summary"):
            combined = {
                "summary": "",
                "risky_clauses": [],
                "missing_clauses": [],
                "negotiation_suggestions": [],
                "compliance_checklist": [],
                "severity_table": [],
            }
            for chunk in results:
                combined["summary"] += chunk.get("summary", "") + "\n\n"
                combined["risky_clauses"] += chunk.get("risky_clauses", [])
                combined["missing_clauses"] += chunk.get("missing_clauses", [])
                combined["negotiation_suggestions"] += chunk.get("negotiation_suggestions", [])
                combined["compliance_checklist"] += chunk.get("compliance_checklist", [])
                combined["severity_table"] += chunk.get("severity_table", [])

            st.subheader("📝 Combined Analysis")
            st.markdown(f"**Summary**:\n{combined['summary']}")
            st.markdown("**Risky Clauses:**")
            for clause in combined["risky_clauses"]:
                st.warning(f"- {clause}")
            st.markdown("**Missing Clauses:**")
            for clause in combined["missing_clauses"]:
                st.info(f"- {clause}")
            st.markdown("**Negotiation Suggestions:**")
            for sug in combined["negotiation_suggestions"]:
                st.code(sug, language="markdown")
            st.markdown("**Compliance Checklist:**")
            for item in combined["compliance_checklist"]:
                st.write(f"- {item}")
            if combined["severity_table"]:
                st.markdown("**Severity Table:**")
                st.table(combined["severity_table"])

        # improved contract preview + download
        if improved_md:
            st.subheader("✅ Improved Contract")
            st.download_button(
                "⬇️ Download Improved Contract (Markdown)",
                improved_md,
                file_name="improved_contract.md",
                mime="text/markdown",
                help="Download the improved contract based on analysis suggestions"
            )
            st.markdown(improved_md, unsafe_allow_html=True)

    elif file_path:
        st.error("Conversion failed or no analysis returned. Please check your file.")
    else:
        st.info("No analysis yet. Please choose a sample or upload a contract to get started.")
