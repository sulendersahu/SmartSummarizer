# SmartSummarizer
An AI-powered, local PDF summarization application using a pretrained BART-family Transformer model.

## Features
- Upload text-based PDF documents.
- Extract text using PyMuPDF.
- Generate Short, Medium, or Detailed summaries.
- Split long documents into tokenizer-aware chunks and summarize them in stages.
- Preview extracted text and download the summary as a TXT file.
- No paid API key or cloud inference service is required.

## Model
`sshleifer/distilbart-cnn-12-6` is a distilled BART-family model fine-tuned for summarization. The model is downloaded from Hugging Face on first use and cached locally. The first download requires internet access. Once cached, inference can run offline.

## Requirements
- Python 3.10 or 3.11 recommended.
- Internet access for the initial dependency/model download.
- RAM and CPU sufficient to load the model. CPU inference may take a few minutes for long documents.
- This starter version extracts selectable PDF text. Scanned/image-only PDFs need OCR, which is not included.

## Windows setup
Open PowerShell in this folder:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run this once for the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## macOS / Linux setup
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open it in your browser.

## Test the application
Use either PDF in `sample_pdfs/`:
- `sample1_climate_change.pdf`
- `sample2_healthy_learning.pdf`

Upload a PDF, choose the summary detail in the sidebar, then click **Generate summary**.

## Project structure
```text
SmartSummarizer/
├── app.py
├── modules/
│   ├── __init__.py
│   ├── pdf_extractor.py
│   └── summarizer.py
├── sample_pdfs/
├── report/
├── requirements.txt
├── README.md
└── .gitignore
```

## Troubleshooting
- **Model download fails:** check internet access, then retry. The model is cached after a successful download.
- **Slow generation:** CPU inference is slower than GPU inference. Test with a shorter PDF first.
- **No text extracted:** the PDF may be scanned. Use a text-based PDF; OCR is a possible future enhancement.
- **Installation errors:** use Python 3.10/3.11 in a fresh virtual environment and install from `requirements.txt`.

## Academic note
This project uses a pretrained model for inference; it does not fine-tune BART. In your report, distinguish abstractive summarization (generating a new concise text) from extractive summarization (selecting existing sentences). For evaluation, compare generated summaries against human-written reference summaries using ROUGE-1, ROUGE-2, and ROUGE-L, and report inference time and compression ratio.
