# SmartSummarizer

## AI-Powered PDF Summarization System Using a BART-Family Transformer

**Project type:** Generative AI mini project\
**Application:** Local web application\
**Primary language:** Python\
**Interface:** Streamlit\
**AI model:** `sshleifer/distilbart-cnn-12-6`\
**Document support:** Text-based PDF files\
**Inference:** Local CPU execution in the supplied implementation

------------------------------------------------------------------------

## 1. Project overview

SmartSummarizer is a local application that accepts a PDF document,
extracts its selectable text, and generates a shorter natural-language
summary using a pretrained BART-family transformer model.

The purpose is to reduce the time needed to read long documents while
retaining their main ideas. A user uploads a PDF, chooses a summary
detail level, starts summarization, reviews the generated summary, and
downloads it as a `.txt` file.

The application is built with Streamlit. PyMuPDF extracts text from PDF
pages. Hugging Face Transformers loads the pretrained DistilBART
summarization pipeline, and PyTorch runs the model locally.

### Important scope clarification

The current implementation **reads PDF files and generates a text
summary**. It does not create a new PDF file. The download feature
exports the summary as a plain-text `.txt` file. Exporting summaries to
PDF or DOCX can be added as a future enhancement.

## 2. Problem statement

Long academic notes, research papers, articles, and reports can take
considerable time to read. Readers often need a concise overview before
deciding which sections deserve closer attention.

The project addresses this by automating the summarization process:

-   Accept a PDF document as input.
-   Extract its text.
-   Process long text in manageable token-based chunks.
-   Generate abstractive summaries with a pretrained transformer.
-   Display and allow the user to download the result.

## 3. Objectives

1.  Build a simple local web interface for PDF upload.
2.  Extract selectable text from PDF documents.
3.  Integrate a pretrained BART-family summarization model.
4.  Support long documents through chunk-based processing.
5.  Allow users to select Short, Medium, or Detailed output.
6.  Display the generated summary and a preview of extracted source
    text.
7.  Provide a downloadable text summary.
8.  Evaluate output quality and execution time using sample documents.

## 4. Features in the current implementation

  -----------------------------------------------------------------------
  Feature                             Description
  ----------------------------------- -----------------------------------
  PDF upload                          Upload one PDF through Streamlit's
                                      file uploader.

  PDF text extraction                 Extract text page by page using
                                      PyMuPDF.

  Summary detail                      Choose Short, Medium, or Detailed.

  Transformer summarization           Generate summaries using
                                      DistilBART.

  Long-document support               Split text into tokenizer-aware
                                      chunks and summarize them.

  Second summarization pass           Further condense combined partial
                                      summaries if the intermediate text
                                      is still long.

  Source preview                      Display up to the first 10,000
                                      characters of extracted text.

  Summary download                    Download the generated result as a
                                      `.txt` file.

  Local inference                     Run model inference on the local
                                      machine without a paid LLM API.
  -----------------------------------------------------------------------

### Not included in the current version

-   OCR for scanned/image-only PDFs.
-   PDF or DOCX summary export.
-   Multiple-document comparison.
-   Chat with the uploaded PDF.
-   User accounts, authentication, or cloud storage.
-   Model fine-tuning.
-   A vector database or RAG retrieval pipeline.

These should be described as possible extensions, not as implemented
features.

## 5. Technology stack

  -----------------------------------------------------------------------
  Layer                   Technology              Role
  ----------------------- ----------------------- -----------------------
  Programming language    Python                  Application and
                                                  processing logic

  Frontend                Streamlit               Local interactive web
                                                  interface

  PDF parsing             PyMuPDF (`fitz`)        Extract text from PDF
                                                  pages

  NLP/model integration   Hugging Face            Load and invoke the
                          Transformers            summarization pipeline

  Deep learning runtime   PyTorch                 Execute neural-network
                                                  inference

  Model/tokenizer         DistilBART CNN 12-6     Generate abstractive
                                                  summaries

  Text processing         Python `re` and         Normalize whitespace
                          tokenizer utilities     and split text

  Model cache             Hugging Face local      Reuse downloaded model
                          cache                   files
  -----------------------------------------------------------------------

No LangChain, FAISS, vector database, external LLM API, or fine-tuning
framework is used in this version.

## 6. AI model details

### 6.1 Selected model

The application uses:

``` text
sshleifer/distilbart-cnn-12-6
```

This is a distilled BART-family model fine-tuned for summarization on
CNN/DailyMail-style news data. It is available through the Hugging Face
model ecosystem.

The model is loaded through the Transformers summarization pipeline:

``` python
from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    tokenizer="sshleifer/distilbart-cnn-12-6",
    device=-1
)
```

`device=-1` explicitly selects CPU inference. A compatible CUDA-enabled
environment and code change would be required to use an NVIDIA GPU.

### 6.2 What does BART do?

BART stands for **Bidirectional and Auto-Regressive Transformers**. It
is an encoder-decoder transformer architecture.

-   The **encoder** reads the input sequence and builds contextual
    representations.
-   The **decoder** generates the output sequence token by token.
-   Attention mechanisms allow the model to use contextual information
    from the input while generating each output token.

BART is suitable for text generation tasks such as abstractive
summarization.

### 6.3 Abstractive versus extractive summarization

**Extractive summarization** selects important sentences or phrases
directly from the original document.

**Abstractive summarization** generates new wording that expresses the
main ideas of the source. The selected DistilBART model performs
abstractive summarization.

An abstractive summary can be more readable and compact, but generated
text may occasionally omit details or state something inaccurately.
Important information should be checked against the source document.

### 6.4 Pretrained model versus fine-tuning

The current project uses a pretrained model for inference. It does
**not** train or fine-tune BART on a custom dataset. This keeps the
project simpler and avoids the need for a training dataset and GPU
training workflow.

## 7. System architecture

### 7.1 High-level architecture

``` text
                  USER
                   |
                   v
        +------------------------+
        | Streamlit Web Interface|
        | PDF upload + settings  |
        +------------------------+
                   |
                   v
        +------------------------+
        | PDF Text Extraction    |
        | PyMuPDF / fitz         |
        +------------------------+
                   |
                   v
        +------------------------+
        | Text Preprocessing     |
        | Whitespace cleanup     |
        +------------------------+
                   |
                   v
        +------------------------+
        | Tokenizer-based        |
        | Chunking               |
        | 900 tokens per chunk   |
        +------------------------+
                   |
                   v
        +------------------------+
        | DistilBART Summarizer  |
        | Hugging Face + PyTorch |
        +------------------------+
                   |
                   v
        +------------------------+
        | Partial Summary        |
        | Aggregation            |
        +------------------------+
                   |
          If combined text
          exceeds 900 tokens
                   |
                   v
        +------------------------+
        | Second summarization   |
        | pass (when required)   |
        +------------------------+
                   |
                   v
        +------------------------+
        | Final Summary          |
        | Display + TXT download |
        +------------------------+
```

### 7.2 Component responsibilities

**Streamlit interface (`app.py`)** - Configures the page and visual
theme. - Provides the PDF uploader. - Provides the summary detail
selector. - Calls the PDF extraction and summarization modules. -
Displays word counts, compression percentage, summary text, and source
preview. - Provides a TXT download button.

**PDF extractor (`modules/pdf_extractor.py`)** - Receives PDF bytes from
the uploaded file. - Opens the PDF from memory using PyMuPDF. - Iterates
through pages. - Extracts selectable text from each page. - Joins the
page text and returns one string.

**Summarizer (`modules/summarizer.py`)** - Loads and caches the model
pipeline. - Normalizes whitespace. - Tokenizes and splits long text into
chunks. - Summarizes each eligible chunk. - Combines partial
summaries. - Runs a second pass if the combined summaries exceed the
configured token threshold.

### 7.3 Data flow

1.  The user uploads a PDF through Streamlit.
2.  Streamlit reads the uploaded file bytes.
3.  `extract_pdf_text()` extracts text from the PDF.
4.  The application checks whether usable text was extracted.
5.  `load_summarizer()` loads the model pipeline if it is not already
    cached.
6.  `summarize_long_text()` cleans and tokenizes the text.
7.  The text is split into chunks of up to 900 tokenizer tokens.
8.  The summarization pipeline generates a partial summary for each
    sufficiently long chunk.
9.  Partial summaries are joined together.
10. If the combined text contains more than 900 tokens, another
    summarization pass is applied to its chunks.
11. The final summary is shown in the interface and made available as a
    TXT download.

## 8. Long-document processing and chunking

Transformer models have maximum input sequence lengths. Passing an
entire lengthy PDF as one input can exceed the model's supported input
length or cause truncation.

SmartSummarizer uses tokenizer-aware chunking rather than splitting by
an arbitrary number of characters.

The implemented function is conceptually:

``` python
token_ids = tokenizer.encode(text, add_special_tokens=False)

for start in range(0, len(token_ids), 900):
    piece = token_ids[start:start + 900]
    chunk = tokenizer.decode(piece, skip_special_tokens=True)
```

Each chunk contains at most 900 token IDs before special tokens are
added by the model pipeline.

### Why use tokens instead of characters?

A token can represent a word, part of a word, punctuation, or another
text unit. The relationship between characters and tokens is not fixed.
Token-based chunking is therefore more aligned with the model's actual
input constraints.

### Partial summarization

Each chunk is passed to the summarization pipeline. Very short chunks
with fewer than 45 tokens after special-token accounting are kept as
text rather than being sent to the model with an unsuitable minimum
summary length.

### Aggregation and second pass

The partial summaries are joined into one intermediate text. If this
text exceeds 900 tokens, it is split again and summarized in a second
pass.

This is a simple hierarchical summarization strategy:

``` text
Original document
    |
    +--> Chunk 1 --> Summary 1
    |
    +--> Chunk 2 --> Summary 2
    |
    +--> Chunk 3 --> Summary 3
                       |
                       v
             Combine partial summaries
                       |
              More than 900 tokens?
                 /          \
               Yes           No
                |             |
        Summarize again       |
                \             /
                 Final summary
```

This implementation performs at most one additional aggregation pass. It
is not an unlimited recursive summarizer.

### Summary length settings

The application maps the selected detail level to generation limits:

  UI setting     Minimum length   Maximum length
  ------------ ---------------- ----------------
  Short                      35               90
  Medium                     70              150
  Detailed                  110              200

These values are passed as generation parameters to the summarization
pipeline. The code adjusts the local values for shorter chunks so the
requested minimum does not exceed a reasonable length for the input.

The values are model generation limits, not guaranteed exact word
counts. They should not be interpreted as exact numbers of words.

## 9. Code architecture and file structure

``` text
SmartSummarizer/
│
├── app.py
│
├── modules/
│   ├── __init__.py
│   ├── pdf_extractor.py
│   └── summarizer.py
│
├── sample_pdfs/
│   ├── sample1_climate_change.pdf
│   ├── sample2_healthy_learning.pdf
│   ├── sample3_cybersecurity_basics.pdf
│   └── sample4_renewable_energy.pdf
│
├── report/
│   └── project_outline.md
│
├── requirements.txt
├── README.md
└── .gitignore
```

The first two sample PDFs are included in the original project archive.
The additional cybersecurity and renewable-energy sample PDFs were
supplied separately and can be copied into `sample_pdfs/`.

### 9.1 `app.py`

Main application entry point.

Responsibilities: - Streamlit page configuration. - CSS styling and page
layout. - Sidebar summary settings. - PDF upload. - Calling extraction
and summarization functions. - Error handling and progress indicators. -
Displaying summary statistics and result. - Downloading the summary as a
`.txt` file.

### 9.2 `modules/pdf_extractor.py`

The core extraction function:

``` python
import fitz

def extract_pdf_text(pdf_bytes: bytes) -> str:
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    try:
        for page in document:
            page_text = page.get_text("text")
            if page_text:
                pages.append(page_text)
    finally:
        document.close()
    return "\n\n".join(pages).strip()
```

The PDF is opened from uploaded bytes, so the application does not need
to save the uploaded PDF to a permanent server-side file.

### 9.3 `modules/summarizer.py`

Contains: - `MODEL_NAME`: model identifier. - `load_summarizer()`: loads
and caches the model. - `clean_text()`: normalizes whitespace. -
`split_into_chunks()`: creates tokenizer-based chunks. -
`_summary_settings()`: maps the selected detail level to generation
limits. - `summarize_long_text()`: performs chunk summarization and
aggregation.

The model is cached using Streamlit's `@st.cache_resource`, preventing
it from being reloaded on every Streamlit rerun within the running
process.

### 9.4 `requirements.txt`

``` text
streamlit>=1.32
transformers>=4.38,<5
torch>=2.1
pymupdf>=1.23
sentencepiece>=0.1.99
```

These are minimum/version-range requirements, not exact pinned versions.
Pip resolves compatible package versions for the active Python
environment.

## 10. Setup and installation

### 10.1 Prerequisites

-   Windows, Linux, or macOS.
-   Python installation.
-   Internet access for installing packages and downloading the model
    for the first time.
-   Sufficient RAM and CPU capacity to load and run the model.
-   A modern web browser.

Python 3.10 or 3.11 is a conservative choice for broad package
compatibility. The project owner has also successfully installed the
listed dependencies in a Python 3.15 virtual environment in the
development environment used for this project. Package compatibility can
change over time, so a clean environment should be tested if reproducing
the setup.

### 10.2 Windows setup

Open PowerShell in the project directory:

``` powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Start the application:

``` powershell
streamlit run app.py
```

If PowerShell blocks virtual-environment activation, run:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

### 10.3 Linux or macOS setup

``` bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
streamlit run app.py
```

### 10.4 Open the application

Streamlit normally displays a local address such as:

``` text
http://localhost:8501
```

Open this address in a browser.

### 10.5 First model run

The first summarization request downloads the model and tokenizer from
the Hugging Face model repository. This requires internet access and can
take time depending on network speed.

After the model is successfully cached, subsequent runs can load it from
the local Hugging Face cache. For a fully offline run, all required
model files must already be present in the cache.

## 11. How to use the application

1.  Start the virtual environment.
2.  Run `streamlit run app.py`.
3.  Open the local Streamlit URL.
4.  Upload a text-based PDF.
5.  Select Short, Medium, or Detailed in the sidebar.
6.  Click **Generate my summary**.
7.  Wait for extraction and model inference to complete.
8.  Review the generated summary and extracted text preview.
9.  Review the source-word count, summary-word count, and estimated
    compression percentage.
10. Click the download button to save the summary as a `.txt` file.

## 12. Testing plan

The project includes sample PDFs covering different subject areas:

  Sample                               Subject               Suggested test
  ------------------------------------ --------------------- ----------------
  `sample1_climate_change.pdf`         Climate change        Medium
  `sample2_healthy_learning.pdf`       Learning and memory   Short
  `sample3_cybersecurity_basics.pdf`   Cybersecurity         Short
  `sample4_renewable_energy.pdf`       Renewable energy      Detailed

### Functional test cases

  -----------------------------------------------------------------------
  Test ID                 Test                    Expected result
  ----------------------- ----------------------- -----------------------
  TC-01                   Upload a valid          File is accepted.
                          text-based PDF          

  TC-02                   Upload a non-PDF file   File type is rejected
                                                  by uploader.

  TC-03                   Generate a summary from Summary is displayed.
                          a valid PDF             

  TC-04                   Select Short, Medium,   Corresponding
                          Detailed                generation limits are
                                                  selected.

  TC-05                   Download generated      TXT file downloads.
                          summary                 

  TC-06                   Upload a PDF with no    Application displays a
                          selectable text         no-text message.

  TC-07                   Upload a long PDF       Text is split into
                                                  chunks and processed.

  TC-08                   Run a second            Cached model resource
                          summarization request   is reused in the same
                                                  app process.
  -----------------------------------------------------------------------

## 13. Evaluation methodology

A college project should evaluate summary quality, not only whether the
application runs.

### 13.1 ROUGE metrics

ROUGE compares a generated summary with a human-written reference
summary.

-   **ROUGE-1:** Overlap of individual tokens/words.
-   **ROUGE-2:** Overlap of two-token sequences.
-   **ROUGE-L:** Based on the longest common subsequence.

To calculate these metrics, create a human-written reference summary for
each test PDF. Compare the generated summary with the reference using
the same evaluation setup.

ROUGE measures lexical overlap and does not prove that every generated
statement is factually correct.

### 13.2 Inference time

Record the time from the start of model summarization to completion.
Separate the first run (which may include model loading) from later runs
where the model is cached.

### 13.3 Compression ratio

The current interface calculates:

``` text
Compression percentage =
(1 - summary word count / original word count) * 100
```

This indicates how much shorter the output is by word count. It does not
measure summary correctness or information retention.

### 13.4 Human review

Review whether the summary: - Captures the main subject and important
points. - Avoids major factual changes. - Is readable and coherent. -
Avoids excessive repetition. - Does not omit critical qualifications or
conclusions.

Do not invent evaluation scores in the project report. Run the tests and
record actual results.

## 14. Limitations

1.  **Scanned PDFs:** PyMuPDF text extraction does not perform OCR in
    this project. A scanned PDF may return no usable text.
2.  **Model domain:** The selected model was fine-tuned for news
    summarization and may not perform equally well on every academic or
    technical subject.
3.  **Hallucination and omission:** Abstractive generation can omit
    details or generate inaccurate statements.
4.  **Input size:** Chunking helps with long documents, but chunk
    boundaries may separate related ideas.
5.  **Context across chunks:** Each first-pass chunk is summarized
    independently, so relationships across distant sections may not be
    fully represented.
6.  **CPU speed:** Local CPU inference may be slow for large PDFs.
7.  **Language:** The selected model is primarily intended for English
    summarization.
8.  **PDF layout:** Tables, multi-column layouts, diagrams, equations,
    and headers/footers may not extract into clean reading order.
9.  **Export format:** The current download is TXT, not PDF or DOCX.
10. **No source citations:** The generated summary does not currently
    provide page-level citations back to the source PDF.

## 15. Security and privacy considerations

-   PDF bytes are processed by the local Streamlit application.
-   Model inference runs locally using the installed model.
-   No paid external LLM API is called by the application.
-   The model must be downloaded from Hugging Face during initial setup
    unless its files are already cached.
-   The interface imports Google Fonts through CSS, so the browser may
    contact Google Fonts to load those fonts when internet access is
    available. This is a presentation dependency, not an inference API.
-   Only upload documents that you are authorized to process.
-   The current application is intended for local use and does not
    implement authentication or multi-user access controls.

## 16. Troubleshooting

  -----------------------------------------------------------------------
  Problem                 Possible cause          Suggested action
  ----------------------- ----------------------- -----------------------
  `streamlit` command not Virtual environment not Activate `venv`, then
  found                   active or dependency    install requirements.
                          missing                 

  Package build failure   Python/package wheel    Check the failing
                          compatibility           package and Python
                                                  version; use a
                                                  supported Python
                                                  release if needed.

  Model download fails    Network, proxy, or      Check internet access
                          Hugging Face            and retry.
                          connectivity            

  Model loading is slow   First-time model        Wait for initial load;
                          download or CPU loading subsequent runs use
                                                  cache.

  Summary takes a long    CPU inference or long   Test with a shorter PDF
  time                    document                and allow processing
                                                  time.

  No text extracted       Scanned/image-only PDF  Use a text-based PDF;
                          or unusual              OCR is a future
                          encoding/layout         enhancement.

  Browser cannot connect  Streamlit process       Check terminal output
                          stopped or wrong port   and open the URL
                                                  printed by Streamlit.

  Out-of-memory error     Model and document      Close other
                          exceed available memory applications and test
                                                  with a smaller PDF.
  -----------------------------------------------------------------------

## 17. Future enhancements

The following are possible future improvements and are not part of the
current implementation:

1.  OCR integration for scanned PDFs.
2.  Download summaries as PDF and DOCX.
3.  Add a summary history for the current session.
4.  Add batch PDF summarization.
5.  Add page-level references for summary statements.
6.  Compare BART with other summarization models.
7.  Add evaluation automation using ROUGE.
8.  Add a question-answering feature grounded in the uploaded PDF.
9.  Add a table-aware extraction pipeline.
10. Add optional GPU inference when compatible hardware is available.
11. Add multilingual PDF summarization using an appropriate multilingual
    model.
12. Improve factuality checking and source traceability.

## 18. Suggested project demonstration

A short college demonstration can follow this sequence:

1.  Introduce the problem of reading lengthy documents.
2.  Explain the BART encoder-decoder architecture.
3.  Show the SmartSummarizer interface.
4.  Upload `sample1_climate_change.pdf`.
5.  Select Medium and generate the summary.
6.  Show extracted text and generated summary.
7.  Download the TXT result.
8.  Upload a different sample PDF and select another summary detail.
9.  Explain token-based chunking and the second-pass aggregation.
10. Present the evaluation plan, limitations, and future scope.

## 19. Viva preparation: likely questions

**Q1. What is BART?**\
BART is a transformer encoder-decoder model that combines a
bidirectional encoder with an autoregressive decoder. It can be used for
text generation tasks such as abstractive summarization.

**Q2. What is abstractive summarization?**\
It generates a concise version in new wording instead of only selecting
sentences from the original document.

**Q3. Why did you use DistilBART?**\
It is a distilled BART-family summarization model that offers a lighter
inference option than a larger BART model.

**Q4. Why is chunking needed?**\
The model has a limited input token length. Chunking allows longer
documents to be processed in smaller pieces.

**Q5. Why split by tokens instead of characters?**\
Model input limits are based on tokens, and character count does not map
consistently to token count.

**Q6. What is the role of PyMuPDF?**\
It extracts selectable text from PDF pages.

**Q7. What is the role of Streamlit?**\
It provides the user interface and connects user actions to the Python
processing functions.

**Q8. Is the model trained by your project?**\
No. The application uses a pretrained model for inference. It does not
fine-tune the model.

**Q9. Does the project use RAG?**\
No. The current implementation is a summarization pipeline, not a
Retrieval-Augmented Generation system. It does not use embeddings or a
vector database.

**Q10. Can it summarize scanned PDFs?**\
Not in the current version. OCR would be required to extract text from
page images.

**Q11. How do you evaluate the summary?**\
Use human-written reference summaries and ROUGE-1, ROUGE-2, and ROUGE-L,
along with inference time, compression ratio, and human review.

**Q12. What are the limitations of abstractive summarization?**\
It can omit important details, change nuance, or generate inaccurate
statements. Outputs should be checked against the source.

## 20. Conclusion

SmartSummarizer demonstrates an end-to-end local Generative AI
application for PDF summarization. It combines PDF text extraction,
tokenizer-aware chunking, pretrained transformer inference, staged
summary aggregation, and an interactive Streamlit interface.

The project is intentionally scoped to be achievable as an individual
mini project while demonstrating relevant concepts from natural language
processing and transformer-based text generation. Its current
limitations provide clear opportunities for future development.

------------------------------------------------------------------------

## Reference links

-   Hugging Face model page:
    https://huggingface.co/sshleifer/distilbart-cnn-12-6
-   Hugging Face Transformers documentation:
    https://huggingface.co/docs/transformers/
-   BART paper: https://arxiv.org/abs/1910.13461
-   Streamlit documentation: https://docs.streamlit.io/
-   PyMuPDF documentation: https://pymupdf.readthedocs.io/
-   PyTorch documentation: https://pytorch.org/docs/
