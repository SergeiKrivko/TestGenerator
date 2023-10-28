import g4f


def simple_response(messages: list[dict[str: str]]):
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=messages,
        timeout=120,
        stream=True
    )
    for el in response:
        yield el

