import logging

import spacy

from src.caption.base_modifier import BaseModifier

logger = logging.getLogger()


class RuleBasedModifier(BaseModifier):
    """A rule-based caption modifier."""

    def __init__(self, language_model: str = "en_core_web_md"):
        """Initialize the caption generator.

        Args:
            language_model: A SpaCy language model.
        """
        # Disable NER and textcat for faster inference.
        self.nlp = spacy.load(language_model, disable=["ner", "textcat"])
        self.vowels_list = {"a", "e", "i", "o", "u"}

    def get_subject(self, caption: str) -> (str | None, int):
        """Extract the subject / root of a caption.

        Args:
            caption: A caption.

        Returns: The grammatical or syntactical subject/root of the caption and its start position.
        """
        # Apply the POS tagging pipeline
        doc = self.nlp(caption)
        subject = None
        root = None
        start_pos = 0
        for token in doc:
            logger.debug(f"{token.text}, {token.pos_}, {token.tag_}, {token.dep_}")
            # Check for NSUBJ and NSUBJPART
            if token.pos_ == "NOUN" and token.morph:
                if "nsubj" in token.dep_:
                    if subject is not None:
                        logger.warning("Multiple nsubj detected. Keeping the first one.")
                    else:
                        subject = token.text
                        start_pos = token.idx
                if "ROOT" in token.dep_:
                    # There's a single ROOT in the dep parse tree
                    root = token.text
                    start_pos = token.idx
        # If subject is not None, return it
        if subject:
            return subject, start_pos
        # Otherwise, return the Root. We make the assumption that captions do not have verbs as ROOT
        return root, start_pos

    def modify(self, caption: str, adjectives: str) -> str:
        """Modify a caption by inserting the adjectives before the grammatical subject/root of the sentence.

        Additionally, alter any other construct from the caption to achieve grammatical correctness.

        Args:
            caption: A string representing a description of an image. It is not necessarily a full sentence.
            adjectives: A string that represents a concatenated list of adjectives in correct order.

        Returns: The caption with the inserted adjectives.
        """
        subject, start_index = self.get_subject(caption=caption)

        if not subject:
            logger.warning(f"Unable to find subject/root in {caption}")

        # Split the sentence based on the start of the subject
        pre_subject, post_subject = caption[:start_index].strip(), caption[start_index:]

        # Update the pre-modifier if needed
        pre_subject, modifier, post_subject = self.apply_grammatical_rules(pre_subject, adjectives, post_subject)

        # Put the modifier before the subject
        modified_caption = f"{pre_subject} {modifier} {post_subject}"

        return modified_caption.strip()

    def apply_grammatical_rules(self, pre_subject, adjectives, post_subject):
        """Update the pre-modifier of a caption.

        This handles grammatical gender, articles, etc.

        Args:
            pre_subject: The part of the caption before the subject.
            adjectives: A list of adjectives.
            post_subject: The part of the caption after the subject/

        Returns: The pre-subject part of the caption, updated for grammatical accord if necessary.
        """
        # Step 1 - Update a/an
        if adjectives[0] in self.vowels_list:
            if pre_subject[-2:] == " a":
                pre_subject = f"{pre_subject}n"
            elif pre_subject.lower() == "a":
                pre_subject = f"{pre_subject}n"
            # The last word of the modifier ends in "a", but it's not a singular word.

        # Step 2 - Update capitalization
        if pre_subject == "":
            adjectives = adjectives.capitalize()
            post_subject = post_subject[0].lower() + post_subject[1:]

        return pre_subject, adjectives, post_subject
