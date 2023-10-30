from abc import ABC, abstractmethod


class BaseModifier(ABC):
    """The base class for all the caption modifiers."""

    @abstractmethod
    def modify(self, caption: str, adjectives: str) -> str:
        """Modify a caption by inserting the adjectives before the grammatical subject/root of the sentence.

        Additionally, alter any other construct from the caption to achieve grammatical correctness.

        Args:
            caption: A string representing a description of an image. It is not necessarily a full sentence.
            adjectives: A string that represents a concatenated list of adjectives in correct order.

        Returns: The caption with the inserted adjectives.
        """
        pass
