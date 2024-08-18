import re


def sanitization_data(data: str) -> str:
    data = data.casefold().strip()
    data = re.sub(r'[^a-zà-ú\s]', '', data)
    data = ' '.join(data.split())
    return data
