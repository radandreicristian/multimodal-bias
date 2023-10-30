from src.caption.model_modifier import ModelBasedModifier
from src.caption.rule_modifier import RuleBasedModifier


class ModifierFactory:
    """A factory for modifiers."""

    @classmethod
    def get_modifier(cls, *args, **kwargs):
        """Get a specific modifier based on the config/kwargs.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Modifier: A modifier instance.
        """
        modifier_name = kwargs.get("MODIFIER")
        if modifier_name == "RULE":
            return RuleBasedModifier(**kwargs)
        elif modifier_name == "MODEL":
            return ModelBasedModifier(**kwargs)
        else:
            raise ValueError(f"Modifier {modifier_name} not supported. Use RULE or MODEL.")
