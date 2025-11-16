def unification_names(raw_name: str) -> str:
    result = raw_name.strip().lower()
    return f"{result[0].upper()}{result[1:]}"
