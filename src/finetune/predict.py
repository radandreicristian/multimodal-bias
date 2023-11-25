import logging

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from src.finetune.train import predict

logger = logging.getLogger()

load_path = ".training/google/flan-t5-base/output/checkpoint-2"


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(load_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(load_path)
    while True:
        sentence = input("Sentence:")
        adjectives = input("Adjectives:")
        print(f"Result: {predict(sentence, adjectives)}")
