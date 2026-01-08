import argparse
import os
import re
import emoji
import tempfile
from pathlib import Path

import pandas as pd
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

MODEL_PATH = "./Model/distilbert-sentiment"
RAW_DIR = "./Dataset"
PROCESSED_DIR = "./Processed_Datasets"
BATCH_SIZE = 32
MAX_LEN = 128
ID2LABEL = {0: "negative", 1: "neutral", 2: "positive"}

os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_text(t):
    t = re.sub(r"http\S+|www\S+|https\S+", " <url> ", str(t))
    t = re.sub(r"@\w+", " <user> ", t)
    t = re.sub(r"#(\w+)", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r'(.)\1{2,}', r'\1\1', t)
    t = re.sub(r"[^a-zA-Z0-9\s.,!?@#<>:;'\-]", " ", t)
    return t

def convert_emojis(t):
    return emoji.demojize(str(t), delimiters=(" ", " "))

def atomic_write_csv(df, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(prefix=out_path.stem, suffix=".tmp", dir=out_path.parent)
    os.close(tmp_fd)
    df.to_csv(tmp_path, index=False)
    os.replace(tmp_path, out_path)

def process_keyword(keyword: str):
    raw_path = Path(RAW_DIR) / f"{keyword}.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {raw_path}")

    df = pd.read_csv(raw_path)

    for c in ["tweet_id", "writer"]:
        if c in df.columns:
            df = df.drop(columns=[c])

    required = ["post_date", "body", "comment_num", "retweet_num", "like_num"]
    for c in required:
        if c not in df.columns:
            raise KeyError(f"Missing required column: {c}")
    df = df.dropna(subset=required)

    df['body'] = df['body'].astype(str).str.lower()
    df['body'] = df['body'].apply(clean_text)
    df['body'] = df['body'].apply(convert_emojis)

    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    preds = []
    for i in range(0, len(df), BATCH_SIZE):
        batch_texts = df["body"].iloc[i:i+BATCH_SIZE].tolist()
        enc = tokenizer(batch_texts, padding=True, truncation=True, max_length=MAX_LEN, return_tensors="pt")
        enc = {k: v.to(device) for k, v in enc.items()}
        with torch.no_grad():
            out = model(**enc)
            batch_preds = torch.argmax(out.logits, dim=-1).cpu().numpy()
            preds.extend(batch_preds.tolist())

    df["sentiment"] = [ID2LABEL.get(int(p), "neutral") for p in preds]

    out_path = Path(PROCESSED_DIR) / f"{keyword}_processed.csv"
    atomic_write_csv(df, out_path)
    print(f"[processor_simple] wrote {out_path} ({len(df)} rows)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", "-k", required=True)
    args = parser.parse_args()
    process_keyword(args.keyword)

if __name__ == "__main__":
    main()
