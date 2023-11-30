from PyQt6.QtWidgets import QPushButton

from side_tabs.telegram.telegram_api import tg


class Reaction(QPushButton):
    def __init__(self, tm, reaction: tg.ReactionType, count=1):
        super().__init__()
        self.tm = tm

        self.reaction = reaction
        self.count = count
        self.set_text()
        self.set_theme()
        self.setCheckable(True)

    def add(self):
        self.count += 1
        self.set_text()

    def same(self, reaction):
        if isinstance(self.reaction, tg.ReactionTypeEmoji) and isinstance(reaction, tg.ReactionTypeEmoji):
            return self.reaction.emoji == reaction.emoji
        if isinstance(self.reaction, tg.ReactionTypeCustomEmoji) and isinstance(reaction, tg.ReactionTypeCustomEmoji):
            return self.reaction.custom_emoji_id == reaction.custom_emoji_id
        return False

    def set_text(self):
        if isinstance(self.reaction, tg.ReactionTypeEmoji):
            if self.count == 1:
                self.setText(self.reaction.emoji)
            else:
                self.setText(f"{self.reaction.emoji} {self.count}")

    def set_theme(self):
        self.tm.auto_css(self, border=False, palette='Menu', padding=True)


