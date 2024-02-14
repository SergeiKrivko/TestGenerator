import config

with open(r"build/setup.iss", encoding='utf-8') as f:
    text = f.read()

    index = text.index('#define MyAppVersion ') + len('#define MyAppVersion ')
    text = text[:index] + f'"{config.APP_VERSION}"' + text[index:][text[index:].index('\n'):]

with open(r"build/setup.iss", 'w', encoding='utf-8') as f:
    f.write(text)
