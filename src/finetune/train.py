import logging

from datasets import Dataset, DatasetDict
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

logger = logging.getLogger()


input_template = """
Add the adjectives to the subject of the sentence:
Sentence: {}
Adjectives: {}
Output:
"""


def predict(caption: str, adjectives: str) -> str:
    """Predict the output for a given sentence and adjectives.

    Args:
        caption: A caption.
        adjectives: A list of adjectives.

    Returns: The model prediction for adding the adjectives to the caption.
    """
    inputs = tokenizer(input_template.format(caption, adjectives), return_tensors="pt")

    caption_tokens = len(tokenizer(caption)["input_ids"])
    adjective_tokens = len(tokenizer(adjectives)["input_ids"])

    min_new_tokens = caption_tokens + adjective_tokens - 1
    max_new_tokens = caption_tokens + adjective_tokens + 1

    logger.debug(f"Generating {min_new_tokens} - {max_new_tokens} tokens.")

    outputs = model.generate(
        **inputs, num_beams=8, do_sample=True, min_new_tokens=min_new_tokens, max_new_tokens=max_new_tokens
    )
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return decoded


def make_pair(caption: str, adjectives: str, expected_output: str) -> dict[str, str]:
    """Create a dataset entry from the caption, adjectives and expected output.

    Args:
        caption: A caption.
        adjectives: A list of adjectives.
        expected_output: The expected output of adding the adjective to the caption.

    Returns: A dictionary.
    """
    return {"text": input_template.format(caption, adjectives), "labels": expected_output}


raw_train_data = [
    ("An athletic woman jogging in the park", "young", "A young athletic woman jogging in the park."),
    (
        "A cheerful man is gardening in his backyard",
        "old black",
        "A cheerful old black man is gardening in his backyard.",
    ),
    ("A gentleman reading a newspaper", "old asian", "An old asian gentleman is reading a newspaper."),
    (
        "Under a tall tree, a woman stretching",
        "young latino",
        "Under a tall tree, a young latina woman stretching",
    ),
    (
        "A man skateboarding in the street during sunset",
        "middle-aged black",
        "A middle-aged black man skateboarding in the street during sunset",
    ),
    (
        "In a cozy living room, a woman is watching tv",
        "old asian",
        "In a cozy living room, an old asian woman is watching tv",
    ),
]

raw_test_data = [
    (
        "A person in kimono meditation before aikido competition in sport hall.",
        "old white male",
        "An old white male person in kimono meditation before aikido competition in sports hall",
    ),
    (
        "Smiling girl with a party wig -- Stock Photo",
        "young black",
        "Young black smiling girl with a party wig -- Stock Photo",
    ),
    (
        "The beautiful bride with the sunlight shining on her",
        "middle-aged white",
        "The beautiful middle-aged white bride with the sunlight shining on her",
    ),
    (
        "True African beauty. Beautiful black woman wearing a headscarf and posing against black background",
        "old black",
        "True African beauty. Beautiful old black woman wearing a headscarf and posing against black background.",
    ),
]

train_data = [make_pair(caption, adjectives, label) for caption, adjectives, label in raw_train_data]
test_data = [make_pair(caption, adjectives, label) for caption, adjectives, label in raw_test_data]


batch_size = 2
model_name = "google/flan-t5-base"
model_dir = f".training/{model_name}/output"
logs_dir = f".training/{model_name}/logs"


dataset_dict = DatasetDict({"train": Dataset.from_list(train_data), "test": Dataset.from_list(test_data)})


def preprocess_data(examples: Dataset) -> dict:
    """Tokenize the input and output texts.

    Args:
        examples: A dataset containing entries with "text" and "labels"

    Returns: A list of tokens for the input and the output.
    """
    model_inputs = tokenizer(examples["text"], max_length=512, truncation=True)

    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples["labels"], max_length=512, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    args = Seq2SeqTrainingArguments(
        output_dir=model_dir,
        logging_dir=logs_dir,
        evaluation_strategy="steps",
        eval_steps=2,
        logging_strategy="steps",
        logging_steps=2,
        save_strategy="steps",
        save_steps=2,
        learning_rate=1e-3,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        weight_decay=0.1,
        save_total_limit=1,
        num_train_epochs=2,
        predict_with_generate=True,
    )

    collator = DataCollatorForSeq2Seq(tokenizer)

    tokenized_datasets = dataset_dict.map(preprocess_data, batched=True)

    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        data_collator=collator,
        tokenizer=tokenizer,
    )

    trainer.train()

    model = trainer.model.cpu()

    model.eval()

    for caption, adjectives, expected in raw_test_data:
        prediction = predict(caption, adjectives)

        print(f"E: {expected}\nA: {prediction}")
