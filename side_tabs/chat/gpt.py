import g4f


g4f.version_check = False


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


def try_response(messages: list[dict[str: str]], count=5, handler=None, **kwargs):
    for _ in range(count):
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.default,
                messages=messages,
                timeout=120,
                **kwargs
            )
            if handler is None:
                return response
            return handler(response)
        except RuntimeError:
            pass
    return ''
