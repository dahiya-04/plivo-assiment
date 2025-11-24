

python src/generate_data.py
python src/train.py --model_name distilbert-base-uncased --train data/train.jsonl --dev data/dev.jsonl --out_dir out
python src/predict.py --model_dir out --input data/dev.jsonl --output out/dev_pred.json
python src/eval_span_f1.py --gold data/dev.jsonl --pred out/dev_pred.json
python src/measure_latency.py --model_dir out --runs 50
