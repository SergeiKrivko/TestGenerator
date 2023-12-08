import g4f


def stream_response(messages: list[dict[str: str]], model=None, **kwargs):
    if model is None or model == 'default':
        model = g4f.models.default
    response = g4f.ChatCompletion.create(
        model=model,
        messages=messages,
        timeout=120,
        stream=True,
        **kwargs
    )
    for el in response:
        yield el


def simple_response(messages: list[dict[str: str]], model=None, **kwargs):
    if model is None or model == 'default':
        model = g4f.models.default
    response = g4f.ChatCompletion.create(
        model=model,
        messages=messages,
        timeout=120,
        **kwargs
    )
    return response


def try_response(messages: list[dict[str: str]], model=None, count=5, handler=None, **kwargs):
    if model is None or model == 'default':
        model = g4f.models.default
    for _ in range(count):
        try:
            response = g4f.ChatCompletion.create(
                model=model,
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


def get_models():
    return ['default'] + g4f.models._all_models
