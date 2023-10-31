import g4f


def stream_response(messages: list[dict[str: str]], **kwargs):
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=messages,
        timeout=120,
        stream=True,
        **kwargs
    )
    for el in response:
        yield el


def simple_response(messages: list[dict[str: str]], **kwargs):
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=messages,
        timeout=120,
        **kwargs
    )
    return response

