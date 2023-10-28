import logging

import spacy

logger = logging.getLogger()


class CaptionGenerator:
    """A class that generates/alters captions."""

    def __init__(self, language_model: str = "en_core_web_md"):
        """Initialize the caption generator.

        Args:
            language_model: A SpaCy language model.
        """
        # Disable NER and textcat for faster inference.
        self.nlp = spacy.load(language_model, disable=["ner", "textcat"])

    def get_subject(self, caption: str) -> str:
        """Extract the subject / root of a caption.

        Args:
            caption: A caption.

        Returns: The grammatical or syntactical subject/root of the caption.

        """
        # Apply the POS tagging pipeline
        doc = self.nlp(caption)
        subject = None
        root = None
        for token in doc:
            logger.debug(f"{token.text}, {token.pos_}, {token.tag_}, {token.dep_}")
            # Check for NSUBJ and NSUBJPART
            if "nsubj" in token.dep_:
                if subject is not None:
                    logger.warning("Multiple nsubj detected. Keeping the first one.")
                else:
                    subject = token.text
            if "ROOT" in token.dep_:
                # There's a single ROOT in the dep parse tree
                root = token.text
        # If subject is not None, return it
        if subject:
            return subject
        # Otherwise, return the Root. We make the assumption that captions do not have verbs as ROOT
        return root
