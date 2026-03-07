# Resume Parsing Framework

A pluggable, object-oriented Python framework for extracting structured information (Name, Email, Skills) from PDF and Word resumes.

## Features

- **Multi-format Support**: Parses `.pdf` and `.docx` files.
- **Pluggable Architecture**: Easily add new parsers or field extractors.
- **Hybrid Extraction**:
  - **Regex**: For deterministic fields like Email.
  - **Heuristics**: For Name extraction.
  - **LLM (Gemini)**: For complex Skills extraction.
- **Robustness**: Validation for API keys and text length.

## Project Structure

```
resume_parser/
├── models.py                   # Data Model (ResumeData)
├── resume_parser/
│   ├── interfaces.py           # Abstract Base Classes
│   ├── pdf_parser.py           # PDF Parser
│   ├── word_parser.py          # Word Parser
│   ├── extractors.py           # Logic for extracting fields
│   └── framework.py            # Main Coordinator
├── utils/                      # Helper utilities
├── tests/                      # Unit and Speed tests
├── sample_resumes/             # Sample data
└── main.py                     # CLI Entry point
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or   
   ```bash
   pip install -e .
   ```

1. **Configure Environment**
   - Configure the `.env` file.
   - Add your [Google Gemini API Key](https://aistudio.google.com/app/apikey).
   ```text
   GEMINI_API_KEY=AIzaSy...
   ```

2. **Generate Sample Data** (Optional)
   The framework includes a script to generate dummy resumes for testing.
   ```bash
   python create_samples.py
   ```

## Usage

### Command Line Interface
Run the tool on any resume file:
```bash
python main.py sample_resumes/sample.pdf
```

### Python API
```python
from resume_parser.framework import ResumeParserFramework

framework = ResumeParserFramework()
data = framework.parse_resume("path/to/resume.pdf")

print(data.name)
print(data.skills)
```
**Convert the ResumeData object to a json object**

```python
from utils import parse_to_json

json_results = parse_to_json.convert_to_json(result_word)
print(json_results)
```
**Save a ResumeData object to a path as a json file**

```python
json_file_name = "WordJson.json"
if os.path.exists(json_path):
  parse_to_json.save_resume_json(result_pdf, json_path + '/'+ json_file_name) 
  print(f"JSON file saved to {json_path}")
```

## Testing

Run all unit tests:
```bash
python tests/run_all_tests.py
```

Run speed benchmarks (requires generated samples):
```bash
python tests/test_speed.py
```

## Design Decisions
- **Separation of Concerns**: Parsers handle *reading* files, Extractors handle *understanding* text.
- **Interfaces**: `FileParser` and `FieldExtractor` allow for easy extension (e.g., adding an OCR parser or a BERT-based extractor).
- **LLM for Skills**: Skills are unstructured and variable. LLMs provide the best flexibility compared to keyword matching.

