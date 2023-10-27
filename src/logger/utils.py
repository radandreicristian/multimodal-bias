def get_logging_config(**env):
    mode = env.get("MODE")
    if mode == "DEBUG":
        return "src/config/logging_config_prod.json"
    return "src/config/logging_config_debug.json"
