
```md
# 📌 PII Detection on Noisy ASR Text (Plivo Assignment)

This project implements a lightweight **Named Entity Recognition (NER)** system to detect **Personally Identifiable Information (PII)** from noisy speech-like text (similar to Automatic Speech Recognition output).  
The goal is to accurately identify PII while keeping inference latency low enough for real-time deployment.

---

## 🧠 Model Capabilities

The model detects:

| Category | Entities |
|----------|----------|
| **PII** | PHONE, CREDIT_CARD, EMAIL, PERSON_NAME, DATE |
| **Non-PII** | CITY, LOCATION |

### Goals

- 🔍 High precision on PII (primary evaluation metric)
- ⚡ Low latency on **CPU**
- 🧩 Compact, deployable model — **DistilBERT**

---

## 📁 Project Structure

```

.
├── src/
│   ├── generate_data.py
│   ├── train.py
│   ├── predict.py
│   ├── eval_span_f1.py
│   ├── measure_latency.py
│   ├── dataset.py
│   ├── labels.py
│   └── model.py
│
├── data/
│   ├── train.jsonl
│   └── dev.jsonl
│
├── out/
│   ├── dev_pred.json
│   └── saved model files
│
└── README.md

````

---

## 🚀 Setup & Installation

Install dependencies:

```bash
pip install -r requirements.txt
````

OR minimal:

```bash
pip install torch transformers seqeval accelerate
```

---

## 🏗️ Synthetic Dataset Generation

The dataset simulates ASR noise using:

* Disjoint entity pools (names, phone numbers, credit cards, etc.)
* Different templates for train vs dev
* Noise variations like:

  * fillers (`uh`, `umm`)
  * numeric homophones (`oh` as zero)
  * email typos (`gmaill.com`)

Generate training + dev data:

```bash
python src/generate_data.py
```

---

## 🎓 Model Training

Train the DistilBERT token classification model:

```bash
python src/train.py \
  --model_name distilbert-base-uncased \
  --train data/train.jsonl \
  --dev data/dev.jsonl \
  --out_dir out \
  --epochs 6 \
  --batch_size 16
```

---

## 🔍 Run Predictions & Evaluate

Generate predictions:

```bash
python src/predict.py \
  --model_dir out \
  --input data/dev.jsonl \
  --output out/dev_pred.json
```

Evaluate:

```bash
python src/eval_span_f1.py \
  --gold data/dev.jsonl \
  --pred out/dev_pred.json
```

---

## ⚡ Latency (CPU)

```bash
CUDA_VISIBLE_DEVICES="" python src/measure_latency.py \
  --model_dir out \
  --input data/dev.jsonl \
  --runs 50
```

---

## 📊 Final Results

| Metric                             | Score     |
| ---------------------------------- | --------- |
| **PII Precision**                  | **0.859** |
| **PII Recall**                     | 0.957     |
| **PII F1**                         | **0.905** |
| Macro F1                           | 0.70     |
| Latency (p95, CPU, batch size = 1) | ~5 ms     |

✔ Meets assignment requirements.

---

## ⚠️ Known Limitations

* EMAIL and PERSON_NAME are harder under noisy conditions.
* Synthetic dataset doesn't fully capture real ASR variability.

---

## 🔧 Future Improvements

* Augment using synthetic TTS → ASR pipeline
* Convert model to **ONNX / quantized format** for faster inference
* Broader noise and language diversity

---

## 🏁 Submission Info

This work was completed as part of the **Plivo + IIT Madras Machine Learning Assignment (2025)**.

---

### 👤 Author

Feel free to reach out for discussion or issues.

```

---


