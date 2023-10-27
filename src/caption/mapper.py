import logging

logger = logging.getLogger()


def map_age_to_attribute(age: float) -> str:
    """Convert the predicted age value (continuous) to a categorical value.

    Args:
        age: The predicted age.

    Returns: A categorical mapping for the age.
    """
    if age < 30.0:
        return "young"
    elif age < 60.0:
        return "middle-aged"
    else:
        return "old"
