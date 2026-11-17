import re
import streamlit as st
from transformers import pipeline

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

@st.cache_resource(show_spinner=False)
def load_summarizer():
    """Load model once and cache it for the lifetime of the Streamlit process."""
    summarizer = pipeline(
        "summarization",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        device=-1,  # CPU; change to 0 only if a compatible CUDA setup is installed
    )
    return summarizer, summarizer.tokenizer

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_into_chunks(text: str, tokenizer, max_input_tokens: int = 900):
    """Split text by tokenizer tokens, not approximate character counts."""
    token_ids = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    for start in range(0, len(token_ids), max_input_tokens):
        piece = token_ids[start:start + max_input_tokens]
        if piece:
            chunks.append(tokenizer.decode(piece, skip_special_tokens=True))
    return chunks

def _summary_settings(level: str):
    return {
        "Short": (35, 90),
        "Medium": (70, 150),
        "Detailed": (110, 200),
    }.get(level, (70, 150))

def summarize_long_text(text: str, summarizer, tokenizer, level: str = "Medium") -> str:
    """Summarize chunks, then summarize their combined summaries if needed."""
    text = clean_text(text)
    if not text:
        return ""

    min_len, max_len = _summary_settings(level)
    chunks = split_into_chunks(text, tokenizer)
    partial_summaries = []

    for chunk in chunks:
        # Very short chunks may not support the configured minimum summary length.
        input_tokens = len(tokenizer.encode(chunk, add_special_tokens=True))
        if input_tokens < 45:
            partial_summaries.append(chunk)
            continue
        local_max = min(max_len, max(40, input_tokens - 5))
        local_min = min(min_len, max(10, local_max - 15))
        result = summarizer(
            chunk,
            max_length=local_max,
            min_length=local_min,
            do_sample=False,
            truncation=True,
        )
        partial_summaries.append(result[0]["summary_text"].strip())

    combined = " ".join(partial_summaries)
    # If many chunks produced a long intermediate text, summarize it in a second pass.
    combined_tokens = len(tokenizer.encode(combined, add_special_tokens=False))
    if combined_tokens > 900:
        second_chunks = split_into_chunks(combined, tokenizer)
        second_pass = []
        for chunk in second_chunks:
            result = summarizer(
                chunk,
                max_length=min(max_len, 180),
                min_length=min(min_len, 60),
                do_sample=False,
                truncation=True,
            )
            second_pass.append(result[0]["summary_text"].strip())
        combined = " ".join(second_pass)

    return combined
