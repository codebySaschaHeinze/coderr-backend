def normalize_none_to_empty_str(data: dict, keys: tuple) -> dict:
    for key in keys:
        if data.get(key) is None:
            data[key] = ''
    return data