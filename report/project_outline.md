# SmartSummarizer – Project Report Outline

## Abstract
SmartSummarizer is a local application that generates concise summaries from text-based PDF documents using a pretrained BART-family transformer model. It extracts PDF text, divides long inputs into token-aware chunks, summarizes the chunks, and combines the results into a final summary.

## Problem statement
Reading lengthy documents takes time. The project aims to reduce the time needed to understand a document by generating a shorter version that preserves its central ideas.

## Objectives
1. Extract text from PDF documents.
2. Apply a pretrained transformer summarization model.
3. Support long documents through chunking and staged summarization.
4. Provide selectable summary detail.
5. Display and export the generated summary.

## Methodology
PDF upload → text extraction with PyMuPDF → whitespace normalization → tokenizer-aware chunking → DistilBART summarization → aggregation → display/download.

## Technologies
Python, Streamlit, PyTorch, Hugging Face Transformers, DistilBART, PyMuPDF.

## Evaluation
Use reference summaries written by a human and calculate ROUGE-1, ROUGE-2, and ROUGE-L. Also measure inference time and compression ratio. Record limitations such as hallucinations, loss of fine detail, and lack of OCR for scanned PDFs.

## Limitations
- Scanned PDFs are not supported without OCR.
- Generated summaries may omit details or occasionally introduce inaccuracies.
- CPU inference can be slow for large documents.
- The selected pretrained model may perform differently across technical and non-technical domains.

## Future enhancements
OCR support, batch PDF processing, export to PDF/DOCX, improved factuality checks, and comparison of multiple summarization models.
