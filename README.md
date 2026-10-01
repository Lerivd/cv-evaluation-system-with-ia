# CV Analyzer with AI

An objective and professional candidate evaluation system powered by Google's Gemini AI and LangChain.

## Overview

The CV Analyzer is a Streamlit-based application designed to help recruiters and hiring managers evaluate candidates efficiently. By comparing a candidate's PDF resume against a detailed job description, the system provides a structured analysis, including skill matching, experience evaluation, and a final fit percentage.

## Key Features

- **PDF Text Extraction**: Automatically extracts text from both candidate resumes and job requirements in PDF format.
- **AI-Powered Analysis**: Uses `gemini-2.5-flash` to evaluate candidate suitability.
- **Structured Output**: Provides a comprehensive report with:
  - Job fit percentage.
  - Candidate profile (Name, Experience, Education).
  - Key technical skills identification.
  - Main strengths and development areas.
  - Final hiring recommendation.
- **Clean UI**: A side-by-side interface for easy input and result visualization.

## Project Structure

```text
cv_analyzer/
├── models/
│   └── cv_model.py         # Pydantic data models for structured output
├── prompts/
│   └── cv_prompts.py       # LangChain prompt templates for AI instructions
├── services/
│   ├── cv_evaluator.py     # Core AI evaluation logic (CVEvaluator class)
│   └── pdf_processor.py    # PDF processing and text extraction (PDFProcessor class)
├── ui/
│   └── streamlit_ui.py     # Streamlit interface and UI components
├── app.py                  # Application entry point
├── requirements.txt        # Project dependencies
└── .env                    # Environment variables (API Keys)
```

## Getting Started

### Prerequisites

- Python 3.10+
- A Google AI Studio API Key (Gemini)

### Installation

1. **Clone or download the project** to your local machine.

2. **Activate the environment virtual** (if you have one):
   ```powershell
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your Google API key:
     ```env
     GOOGLE_API_KEY=your_gemini_api_key_here
     ```

### Running the Application

Start the Streamlit server:
```bash
streamlit run app.py
```

## How to Use

1. **Upload a CV**: Drag and drop a candidate's resume in PDF format.
2. **Upload Job Requirements**: Upload the job description/requirements in PDF format.
3. **Analyze**: Click the "Analyze Candidate" button.
4. **Review**: The system will generate a detailed report in the right column.

## Technical Details

- **Framework**: Streamlit
- **LLM Orchestration**: LangChain
- **AI Model**: Google Gemini 2.5 Flash
- **Data Validation**: Pydantic
- **PDF Parsing**: PyPDF2
