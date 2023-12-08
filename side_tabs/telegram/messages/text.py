from side_tabs.telegram.telegram_api import tg


class TgFormattedText:
    def __init__(self, formatted_text: tg.FormattedText, tm):
        self._tm = tm
        self.text = formatted_text.text
        self.entities = formatted_text.entities

        self.html = ''
        self._includes = dict()
        self.to_html()

    def to_html(self):
        self.html = self.text
        for entity in self.entities:
            if isinstance(entity.type, tg.TextEntityTypeBold):
                self._include('<b>', entity.offset)
                self._include('</b>', entity.offset + entity.length)
            elif isinstance(entity.type, tg.TextEntityTypeItalic):
                self._include('<i>', entity.offset)
                self._include('</i>', entity.offset + entity.length)
            elif isinstance(entity.type, tg.TextEntityTypeCode):
                self._include("<font face='Courier'>", entity.offset)
                self._include('</font>', entity.offset + entity.length)
            elif isinstance(entity.type, tg.TextEntityTypeUnderline):
                self._include("<ins>", entity.offset)
                self._include('</ins>', entity.offset + entity.length)
            elif isinstance(entity.type, tg.TextEntityTypePre):
                self._include("<pre>", entity.offset)
                self._include('</pre>', entity.offset + entity.length)
            elif isinstance(entity.type, tg.TextEntityTypeTextUrl):
                self._include(f"<a href='{entity.type.url}'>", entity.offset)
                self._include('</a>', entity.offset + entity.length)
            else:
                print(entity.type)

        # for key, item in {'😁': 'emoji/😁',
        #                   '😭': 'emoji/😭',
        #                   # '🤦🏻‍♂': 'emoji/🤷\u200d♂️'
        #                   }.items():
        #     if key in self.html:
        #         self.html = self.html.replace(key, f"<img src=\"{self._tm.get_image(item, mini=True)}\">")

    def _include(self, text, pos):
        index = pos
        for key, value in self._includes.items():
            if key <= pos:
                index += value
        self.html = self.html[:index] + text + self.html[index:]
        if pos in self._includes:
            self._includes[pos] += len(text)
        else:
            self._includes[pos] = len(text)
