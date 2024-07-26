from fastapi import FastAPI, File, UploadFile
from transformers import BartForConditionalGeneration, BartTokenizer
import torch
from PyPDF2 import PdfReader
import io

app = FastAPI()

model_name = "siddheshtv/bart-multi-lexsum"

model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

def generate_summary(text, max_length=512):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    inputs = inputs.to(device)
    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=3,
        forced_bos_token_id=0,
        forced_eos_token_id=2
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(io.BytesIO(file))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@app.post("/summarize_text")
async def summarize_text(text: str):
    summary = generate_summary(text)
    return {"summary": summary}

@app.post("/summarize_pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_pdf(contents)
    summary = generate_summary(text)
    return {"summary": summary}