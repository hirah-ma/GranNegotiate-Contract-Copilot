
# GranNegotiate: Contract Negotiation Copilot

## Problem Statement

**Contract negotiation** is often a slow, manual, and complex process that involves interpreting lengthy documents, understanding legal terminology, and making decisions about terms that can impact a company's operations. Traditional methods are time-consuming, prone to human error, and require significant expertise. **GranNegotiate** aims to automate the analysis and negotiation process by helping businesses efficiently review and negotiate contracts with the help of **AI**.

---

## Solution

**GranNegotiate** is a web-based application that streamlines the contract negotiation process. By leveraging **IBM Granite** and **Granite Guardian** models, our solution automatically analyzes contract clauses, highlights potential issues, and provides actionable insights for negotiation. Users can either upload a contract or use a sample contract, and the tool will provide suggestions for improvements based on the analysis.

### Features:
- **Contract Upload:** Upload PDFs or DOCX files.
- **Sample Contract:** Quick start with a pre-loaded sample contract.
- **Clause-Level Analysis:** Breaks down the contract into smaller chunks for easier analysis.
- **Negotiation Suggestions:** Provides actionable recommendations for improving contract terms.
- **Compliance Check:** Identifies any missing or non-compliant clauses.
- **Safer Contracts:** Generates a safer, improved version of the contract for the user.

---

## IBM Granite Models Used

1. **Granite-3-3-8b-Instruct**: This model is used for clause-level analysis of the uploaded contract. It helps understand the contract's language and context, identify risks, and highlight key clauses.

2. **Granite Guardian**: This model performs a safety check on the contract. It flags any potentially harmful or abusive language and ensures that the contract complies with ethical and legal standards.

---

## Architecture

**Frontend:**
- Built with **Streamlit** to provide a simple, intuitive, and interactive user interface.

**Backend:**
- **LangChain** for splitting and chunking large contracts into manageable sections.
- **IBM Granite** API for contract analysis.
- **Granite Guardian** for safety and compliance checks.

**Workflow:**
1. The user uploads a contract or uses a sample contract.
2. The contract is split into smaller chunks for analysis.
3. The contract is analyzed using IBM Granite models.
4. The user receives detailed feedback, including risky clauses, missing clauses, negotiation suggestions, and compliance checks.
5. The user can download an improved version of the contract in markdown format.

---

## How It Works

1. **Contract Upload**: You can upload your own contract in PDF or DOCX format, or you can choose to use a pre-loaded sample contract.
2. **Contract Conversion**: The app converts the contract into markdown for analysis.
3. **AI Analysis**: Using IBM Granite, the contract is analyzed, broken down into smaller chunks, and each chunk is processed to provide negotiation suggestions and highlight potential issues.
4. **Download Markdown**: After analysis, users can download the improved contract in markdown format.

---

## Key Features

- **Clause-Level Breakdown**: Each contract is split into smaller, more manageable chunks for detailed analysis.
- **Granular Feedback**: The app provides insights such as risky clauses, missing clauses, negotiation suggestions, and a compliance checklist.
- **Improved Contract Draft**: The app generates an improved version of the contract based on the analysis.

---

## Technologies Used

- **Streamlit**: For building the web interface.
- **IBM Granite**: For contract analysis and insights.
- **LangChain**: For splitting the contract into chunks for analysis.
- **Granite Guardian**: For safety checks and compliance.

---

## Example

1. Upload or select a sample contract.
2. The app will process the contract and provide an analysis of the content.
3. You will receive suggestions for improving the contract, including compliance checks and negotiation points.
4. You can download an improved version of the contract in markdown format.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repository.git
```

2. Install dependencies:

```bash
cd GranNegotiate
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

---

## Conclusion

GranNegotiate helps businesses optimize their contract negotiation process by leveraging AI to analyze contracts, offer suggestions, and ensure compliance. By using IBM Granite and Granite Guardian, we can provide a comprehensive tool to automate tedious and time-consuming tasks involved in contract management.

---

### Download [GranNegotiate Demo](https://grannegotiate-contract-copilot-ahjdasfj7bpkjc8bucwjh4.streamlit.app/) and try out the analysis!

