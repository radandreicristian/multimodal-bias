def get_logging_config(env: dict) -> str:
    """Return a logging config file path based on the configuration.

    Args:
        env: A dictionary of keyed environment variables.

    Returns: A string with the config path.
    """
    mode = env.get("MODE")
    if mode == "DEBUG":
        return "src/config/logging_config_debug.json"
    return "src/config/logging_config_prod.json"
