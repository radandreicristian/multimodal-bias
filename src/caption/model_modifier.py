import logging

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from src.caption.base_modifier import BaseModifier
from src.finetune.train import input_template

logger = logging.getLogger()


class ModelBasedModifier(BaseModifier):
    """A modifier based on a fine-tunsed Flan-T5 model."""

    def __init__(
        self, model_path_or_name: str = ".training/google/flan-t5-base/output/checkpoint-6", *args, **kwargs
    ) -> None:
        """Initialize the caption generator.

        Args:
            model_path_or_name: A path to a fine-tuned Flan-T5 model.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns: None.
        """
        super().__init__()

        self.tokenizer = AutoTokenizer.from_pretrained(model_path_or_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path_or_name)

    def modify(self, caption: str, adjectives: str) -> str:
        """Modify a caption by inserting the adjectives before the grammatical subject/root of the sentence.

        Additionally, alter any other construct from the caption to achieve grammatical correctness.

        Args:
            caption: A string representing a description of an image. It is not necessarily a full sentence.
            adjectives: A string that represents a concatenated list of adjectives in correct order.

        Returns: The caption with the inserted adjectives.
        """
        inputs = self.tokenizer(input_template.format(caption, adjectives), return_tensors="pt")

        sentence_tokens = len(self.tokenizer(caption)["input_ids"])
        adjective_tokens = len(self.tokenizer(adjectives)["input_ids"])

        min_new_tokens = sentence_tokens + adjective_tokens - 1
        max_new_tokens = sentence_tokens + adjective_tokens + 1

        logger.debug(f"Generating {min_new_tokens} - {max_new_tokens} tokens.")

        outputs = self.model.generate(
            **inputs, num_beams=8, do_sample=True, min_new_tokens=min_new_tokens, max_new_tokens=max_new_tokens
        )
        decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        return decoded
