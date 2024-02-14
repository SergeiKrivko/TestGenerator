import webbrowser

from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget, QVBoxLayout, QTextBrowser, QPushButton

from side_tabs.telegram.messages.context_menu import ContextMenu
from side_tabs.telegram.messages.document import DocumentWidget
from side_tabs.telegram.messages.emoji import EmojiLabel
from side_tabs.telegram.messages.photo import PhotoLabel
from side_tabs.telegram.messages.reactions import Reaction
from side_tabs.telegram.messages.sticker import StickerWidget
from side_tabs.telegram.messages.text import TgFormattedText
from side_tabs.telegram.messages.video import VideoPlayer
from side_tabs.telegram.messages.voice import VoicePlayer
from side_tabs.telegram.telegram_api import tg
from side_tabs.telegram.telegram_manager import TelegramManager
from ui.flow_layout import FlowLayout


class TelegramChatBubble(QWidget):
    _BORDER_RADIUS = 10
    jumpRequested = pyqtSignal(object, object)

    def __init__(self, tm, message: tg.Message, manager: TelegramManager):
        super().__init__()
        self._tm = tm
        self._message = message
        self._manager = manager
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._run_context_menu)
        self._right_side = isinstance(message.sender_id, tg.MessageSenderUser) and message.sender_id.user_id == \
                           int(self._manager.get('my_id'))
        self._info_message = isinstance(message.content, (tg.MessageBasicGroupChatCreate,
                                                          tg.MessageSupergroupChatCreate,
                                                          tg.MessageChatAddMembers,
                                                          tg.MessageChatDeleteMember,
                                                          tg.MessageChatChangePhoto,
                                                          tg.MessageChatChangeTitle,
                                                          tg.MessagePinMessage,
                                                          tg.MessageChatJoinByLink,))

        if isinstance(message.content, tg.MessageText):
            self._text = TgFormattedText(message.content.text, self._tm, self._message).html
        elif isinstance(message.content, (tg.MessageDocument, tg.MessagePhoto, tg.MessageVideo)):
            self._text = TgFormattedText(message.content.caption, self._tm, self._message).html
        else:
            self._text = ''

        main_layout = QHBoxLayout()
        main_layout.setDirection(QHBoxLayout.Direction.RightToLeft if self._right_side else
                                 QHBoxLayout.Direction.LeftToRight)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter if self._info_message else
                                 Qt.AlignmentFlag.AlignLeft if self._right_side else Qt.AlignmentFlag.AlignRight)
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._main_widget = QWidget()
        main_layout.addWidget(self._main_widget)

        widget = QWidget()
        main_layout.addWidget(widget, 1)

        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(1, 1, 1, 1)
        self._main_widget.setLayout(self._layout)

        if isinstance(self._message.sender_id, tg.MessageSenderUser):
            user = self._manager.get_user(self._message.sender_id.user_id)
            user_name = f"{user.first_name} {user.last_name}"
        elif isinstance(self._message.sender_id, tg.MessageSenderChat):
            chat = self._manager.get_chat(self._message.sender_id.chat_id)
            user_name = chat.title
        else:
            user_name = ""
        self._sender_label = QLabel(user_name)
        self._sender_label.setContentsMargins(10, 2, 10, 2)
        self._layout.addWidget(self._sender_label)

        self._info_label = QLabel()
        self._info_label.setWordWrap(True)
        main_layout.addWidget(self._info_label)

        if self._info_message:
            self._main_widget.hide()
            widget.hide()
        else:
            self._info_label.hide()

        if isinstance(self._message.content, tg.MessageText):
            pass

        elif isinstance(self._message.content, tg.MessagePhoto):
            self._photo_label = PhotoLabel(self._tm, self._message.content.photo.sizes[-1].photo)
            self._manager.updateFile.connect(self._photo_label.update_image)
            self._layout.addWidget(self._photo_label)

        elif isinstance(self._message.content, tg.MessageVideo):
            self._video_player = VideoPlayer(self._tm, self._message.content.video)
            self._manager.updateFile.connect(self._video_player.on_downloaded)
            self._layout.addWidget(self._video_player)

        elif isinstance(self._message.content, tg.MessageVoiceNote):
            self._voice_player = VoicePlayer(self._tm, self._message.content.voice_note)
            self._manager.updateFile.connect(self._voice_player.on_downloaded)
            self._layout.addWidget(self._voice_player)

        elif isinstance(self._message.content, tg.MessageDocument):
            self._document_widget = DocumentWidget(self._tm, self._message.content.document, self._manager)
            self._layout.addWidget(self._document_widget)

        elif isinstance(self._message.content, tg.MessageSticker):
            self._sticker_widget = StickerWidget(self._tm, self._manager, self._message.content.sticker)
            self._layout.addWidget(self._sticker_widget)

        elif isinstance(self._message.content, tg.MessageBasicGroupChatCreate):
            self._info_label.setText(f"{user_name} создал(а) группу \"{self._message.content.title}\"")

        elif isinstance(self._message.content, tg.MessageSupergroupChatCreate):
            self._info_label.setText(f"{user_name} создал(а) группу \"{self._message.content.title}\"")

        elif isinstance(self._message.content, tg.MessageChatChangePhoto):
            self._info_label.setText(f"{user_name} изменил(а) фотографию группы")

        elif isinstance(self._message.content, tg.MessageChatChangeTitle):
            self._info_label.setText(f"{user_name} изменил(а) название группы")

        elif isinstance(self._message.content, tg.MessageChatJoinByLink):
            self._info_label.setText(f"{user_name} вступил(а) в группу по ссылке-приглашению")

        elif isinstance(self._message.content, tg.MessagePinMessage):
            self._info_label.setText(f"{user_name} закрепил(а) сообщение")

        elif isinstance(self._message.content, tg.MessageAnimatedEmoji):
            self._emoji_widget = EmojiLabel(self._tm, self._message.content.emoji)
            tg.downloadFile(self._message.content.animated_emoji.sticker.sticker.id, 1)
            self._layout.addWidget(self._emoji_widget)

        else:
            self._text = f"Неподдерживаемое сообщение: {self._message.content.__class__.__name__}"
            print(self._message.content.__class__.__name__)

        font_metrics = QFontMetrics(self._tm.font_medium)

        self._label = QTextBrowser()
        self._label.anchorClicked.connect(self._on_href_clicked)
        self._label.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._label.setHtml(self._text)
        if not self._text:
            self._label.hide()
        self._label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse |
                                            Qt.TextInteractionFlag.TextSelectableByMouse |
                                            Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self._label.setViewportMargins(4, 1, 4, 4)
        self._label.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._fm_width = font_metrics.size(0, self._text).width() + 20
        self._label.setMaximumWidth(self._fm_width)
        self._layout.addWidget(self._label, 10)

        self._reactions_layout = FlowLayout()
        self._reactions_layout.setContentsMargins(8, 2, 8, 2)
        self._reactions_layout.setSpacing(2)
        self._reactions_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layout.addLayout(self._reactions_layout)
        self._reactions: list[Reaction] = []

        if self._message.is_channel_post:
            self._button_comments = QPushButton("Комментарии")
            self._button_comments.clicked.connect(self._on_jump)
            self._layout.addWidget(self._button_comments)

        self._manager.messageInterationInfoChanged.connect(self._on_interaction_info_changed)
        self._on_interaction_info_changed(self._message.chat_id, self._message.id)

    def _on_jump(self):
        chat_id = self._manager.get_supergroup(self._manager.get_chat(
            self._message.chat_id).type.supergroup_id)[1].linked_chat_id
        tg.getMessageThread(self._message.chat_id, self._message.id)

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self._label.setFixedHeight(10)
        self._label.setFixedHeight(10 + self._label.verticalScrollBar().maximum())

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self._label.setFixedWidth(min(self._fm_width, int(self.width() * 0.73)))
        self._label.setFixedHeight(10)
        self._label.setFixedHeight(10 + self._label.verticalScrollBar().maximum())

    def hide_sender(self):
        self._sender_label.hide()
        self._layout.setContentsMargins(1, 7, 1, 1)

    def set_read(self):
        tg.viewMessages(self._message.chat_id, [self._message.id])

    def set_max_width(self, width):
        self._main_widget.setMaximumWidth(width)
        if hasattr(self, '_photo_label'):
            self._photo_label.setMaximumWidth(width)
            self._photo_label.resize_pixmap()

    def _on_interaction_info_changed(self, chat_id, message_id):
        if message_id != self._message.id or chat_id != self._message.chat_id:
            return

        for r in self._reactions:
            r.setParent(None)
        self._reactions.clear()

        if self._message.interaction_info is None:
            return

        for el in self._message.interaction_info.reactions:
            self._reactions.append(r := Reaction(self._tm, el.type, el.total_count))
            r.setChecked(el.is_chosen)
            self._connect_reaction(r)
            self._reactions_layout.addWidget(r)

    def _connect_reaction(self, reaction: Reaction):
        def func(flag):
            if flag:
                tg.addMessageReaction(self._message.chat_id, self._message.id, reaction.reaction)
            else:
                tg.removeMessageReaction(self._message.chat_id, self._message.id, reaction.reaction)

        reaction.clicked.connect(func)

    def _run_context_menu(self, pos):
        menu = ContextMenu(self._message, self._manager.get_chat(self._message.chat_id), self._manager, self._tm)
        menu.move(self.mapToGlobal(pos))
        menu.exec()
        match menu.action:
            case ContextMenu.DELETE:
                tg.deleteMessages(self._message.chat_id, [self._message.id], revoke=False)
            case ContextMenu.DELETE_FOR_ALL:
                tg.deleteMessages(self._message.chat_id, [self._message.id], revoke=True)
            case ContextMenu.DOWNLOAD_DOCUMENT:
                self._document_widget.download()
            case ContextMenu.SAVE:
                self._document_widget.save()
            case ContextMenu.OPEN_FILE:
                self._document_widget.open_file()
            case ContextMenu.SHOW_IN_FOLDER:
                self._document_widget.show_in_folder()
            case ContextMenu.DOWNLOAD_VIDEO:
                self._video_player.download()
            case ContextMenu.PLAY_VIDEO:
                self._video_player.play()
            case ContextMenu.STOP_VIDEO:
                self._video_player.pause()
            case ContextMenu.ADD_REACTION:
                if menu.data is not None:
                    tg.addMessageReaction(self._message.chat_id, self._message.id,
                                          tg.ReactionTypeEmoji(emoji=menu.data))

    def _on_href_clicked(self, href: QUrl):
        webbrowser.open(href.url())
        self._label.setHtml(self._text)

    def set_theme(self):
        css = f"""color: {self._tm['TextColor']}; 
            background-color: {self._tm['MenuColor']};
            border: 1px solid {self._tm['BorderColor']};
            border-top-left-radius: {TelegramChatBubble._BORDER_RADIUS}px;
            border-top-right-radius: {TelegramChatBubble._BORDER_RADIUS}px;
            border-bottom-left-radius: {0 if not self._right_side else TelegramChatBubble._BORDER_RADIUS}px;
            border-bottom-right-radius: {0 if self._right_side else TelegramChatBubble._BORDER_RADIUS}px;"""
        self._main_widget.setStyleSheet(css)
        self._main_widget.setFont(self._tm.font_medium)
        self._label.setStyleSheet("border: none;")
        self._label.setFont(self._tm.font_medium)
        self._sender_label.setStyleSheet(f"color: {self._tm['TestPassed'].name()}; border: 0px; border-radius: 8px;")
        self._sender_label.setFont(self._tm.font_small)
        self._info_label.setStyleSheet(f"""QLabel: {{
            {self._tm.base_css(palette='Menu', border=False)}
            padding: 8px 3px;
            text-align: center;
            }}""")
        if hasattr(self, '_photo_label'):
            self._photo_label.setStyleSheet("border: none;")
        if hasattr(self, '_document_widget'):
            self._document_widget.set_theme()
        if hasattr(self, '_voice_player'):
            self._voice_player.set_theme()
        if hasattr(self, '_emoji_widget'):
            self._emoji_widget.set_theme()
        if hasattr(self, '_button_comments'):
            self._tm.auto_css(self._button_comments, border=False, palette='Menu', padding=True)
