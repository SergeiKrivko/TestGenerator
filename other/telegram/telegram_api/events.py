import other.telegram.telegram_api.types as _types


class TgEvent:
    pass


def convert_event(data: dict, client) -> TgEvent:
    if data['@type'] == "updateOption":
        return TgUpdateOption(data, client)
    if data['@type'] == "updateAuthorizationState":
        return TgUpdateAuthorizationState(data, client)
    if data['@type'] == "updateDefaultReactionType":
        return TgUpdateDefaultReactionType(data, client)
    if data['@type'] == "updateAnimationSearchParameters":
        return TgUpdateAnimationSearchParameters(data, client)
    if data['@type'] == "ok":
        return TgOk(data, client)
    if data['@type'] == "updateAttachmentMenuBots":
        return TgUpdateAttachmentMenuBots(data, client)
    if data['@type'] == "updateSelectedBackground":
        return TgUpdateSelectedBackground(data, client)
    if data['@type'] == "updateFileDownloads":
        return TgUpdateFileDownloads(data, client)
    if data['@type'] == "updateDiceEmojis":
        return TgUpdateDiceEmojis(data, client)
    if data['@type'] == "updateActiveEmojiReactions":
        return TgUpdateActiveEmojiReactions(data, client)
    if data['@type'] == "updateChatThemes":
        return TgUpdateChatThemes(data, client)
    if data['@type'] == "updateScopeNotificationSettings":
        return TgUpdateScopeNotificationSettings(data, client)
    if data['@type'] == "updateChatFilters":
        return TgUpdateChatFilters(data, client)
    if data['@type'] == "updateUnreadMessageCount":
        return TgUpdateUnreadMessageCount(data, client)
    if data['@type'] == "updateUnreadChatCount":
        return TgUpdateUnreadChatCount(data, client)
    if data['@type'] == "updateHavePendingNotifications":
        return TgUpdateHavePendingNotifications(data, client)
    if data['@type'] == "updateConnectionState":
        return TgUpdateConnectionState(data, client)
    if data['@type'] == "updateUser":
        return TgUpdateUser(data, client)
    if data['@type'] == "updateSupergroup":
        return TgUpdateSupergroup(data, client)
    if data['@type'] == "updateNewChat":
        return TgUpdateNewChat(data, client)
    if data['@type'] == "updateChatLastMessage":
        return TgUpdateChatLastMessage(data, client)
    if data['@type'] == "updateSupergroupFullInfo":
        return TgUpdateSupergroupFullInfo(data, client)
    if data['@type'] == "updateChatPosition":
        return TgUpdateChatPosition(data, client)
    if data['@type'] == "updateBasicGroup":
        return TgUpdateBasicGroup(data, client)
    if data['@type'] == "chats":
        return TgChats(data, client)
    if data['@type'] == "messages":
        return TgMessages(data, client)
    if data['@type'] == "updateUserStatus":
        return TgUpdateUserStatus(data, client)
    if data['@type'] == "updateChatNotificationSettings":
        return TgUpdateChatNotificationSettings(data, client)
    if data['@type'] == "updateChatReadInbox":
        return TgUpdateChatReadInbox(data, client)
    if data['@type'] == "updateChatReadOutbox":
        return TgUpdateChatReadOutbox(data, client)
    if data['@type'] == "updateChatAvailableReactions":
        return TgUpdateChatAvailableReactions(data, client)
    if data['@type'] == "updateMessageInteractionInfo":
        return TgUpdateMessageInteractionInfo(data, client)
    if data['@type'] == "updateUserFullInfo":
        return TgUpdateUserFullInfo(data, client)
    if data['@type'] == "updateChatDraftMessage":
        return TgUpdateChatDraftMessage(data, client)
    if data['@type'] == "updateChatAction":
        return TgUpdateChatAction(data, client)
    if data['@type'] == "updateNewMessage":
        return TgUpdateNewMessage(data, client)
    if data['@type'] == "updateDeleteMessages":
        return TgUpdateDeleteMessages(data, client)
    if data['@type'] == "updateBasicGroupFullInfo":
        return TgUpdateBasicGroupFullInfo(data, client)
    if data['@type'] == "updateFile":
        return TgUpdateFile(data, client)
    if data['@type'] == "error":
        return TgError(data, client)


class TgUpdateOption(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.name = data.get('name')
        self.value = _types.get_tg_option(data.get('value'), client)


class TgUpdateAuthorizationState(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.authorization_state = _types.get_authorization_state(data.get('authorization_state'), client)


class TgUpdateDefaultReactionType(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.reaction_type = _types.TgReactionTypeEmoji(data.get('reaction_type'), client)


class TgUpdateAnimationSearchParameters(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.provider = data.get('provider')
        self.emojis = data.get('emojis')


class TgOk(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgUpdateAttachmentMenuBots(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.bots = data.get('bots')


class TgUpdateSelectedBackground(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.for_dark_theme = data.get('for_dark_theme')


class TgUpdateFileDownloads(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.total_size = data.get('total_size')
        self.total_count = data.get('total_count')
        self.downloaded_size = data.get('downloaded_size')


class TgUpdateDiceEmojis(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.emojis = data.get('emojis')


class TgUpdateActiveEmojiReactions(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.emojis = data.get('emojis')


class TgUpdateChatThemes(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_themes = data.get('chat_themes')


class TgUpdateScopeNotificationSettings(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.scope = _types.TgNotificationSettingsScopeChannelChats(data.get('scope'), client)
        self.notification_settings = _types.TgScopeNotificationSettings(data.get('notification_settings'), client)


class TgUpdateChatFilters(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_filters = data.get('chat_filters')
        self.main_chat_list_position = data.get('main_chat_list_position')


class TgUpdateUnreadMessageCount(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_list = _types.get_chat_list(data.get('chat_list'), client)
        self.unread_count = data.get('unread_count')
        self.unread_unmuted_count = data.get('unread_unmuted_count')


class TgUpdateUnreadChatCount(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_list = _types.get_chat_list(data.get('chat_list'), client)
        self.total_count = data.get('total_count')
        self.unread_count = data.get('unread_count')
        self.unread_unmuted_count = data.get('unread_unmuted_count')
        self.marked_as_unread_count = data.get('marked_as_unread_count')
        self.marked_as_unread_unmuted_count = data.get('marked_as_unread_unmuted_count')


class TgUpdateHavePendingNotifications(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.have_delayed_notifications = data.get('have_delayed_notifications')
        self.have_unreceived_notifications = data.get('have_unreceived_notifications')


class TgUpdateConnectionState(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.state = _types.get_connection_state(data.get('state'), client)


class TgUpdateUser(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.user = _types.TgUser(data.get('user'), client)


class TgUpdateSupergroup(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.supergroup = _types.TgSupergroup(data.get('supergroup'), client)


class TgUpdateNewChat(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat = _types.TgChat(data.get('chat'), client)


class TgUpdateChatLastMessage(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.last_message = None if 'last_message' not in data else _types.TgMessage(data.get('last_message'), client)
        self.positions = data.get('positions')


class TgUpdateSupergroupFullInfo(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.supergroup_id = data.get('supergroup_id')
        self.supergroup_full_info = _types.TgSupergroupFullInfo(data.get('supergroup_full_info'), client)


class TgUpdateChatPosition(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.position = _types.TgChatPosition(data.get('position'), client)


class TgUpdateBasicGroup(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.basic_group = _types.TgBasicGroup(data.get('basic_group'), client)


class TgChats(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.total_count = data.get('total_count')
        self.chat_ids = data.get('chat_ids')


class TgMessages(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.total_count = data.get('total_count')
        self.messages = data.get('messages')


class TgUpdateUserStatus(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.user_id = data.get('user_id')
        self.status = _types.get_user_status(data.get('status'), client)


class TgUpdateChatNotificationSettings(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.notification_settings = _types.TgChatNotificationSettings(data.get('notification_settings'), client)


class TgUpdateChatReadInbox(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.last_read_inbox_message_id = data.get('last_read_inbox_message_id')
        self.unread_count = data.get('unread_count')


class TgUpdateChatReadOutbox(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.last_read_outbox_message_id = data.get('last_read_outbox_message_id')


class TgUpdateChatAvailableReactions(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.available_reactions = _types.get_chat_available_reactions(data.get('available_reactions'), client)


class TgUpdateMessageInteractionInfo(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.message_id = data.get('message_id')
        self.interaction_info = _types.TgMessageInteractionInfo(data.get('interaction_info'), client)


class TgUpdateUserFullInfo(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.user_id = data.get('user_id')
        self.user_full_info = _types.TgUserFullInfo(data.get('user_full_info'), client)


class TgUpdateChatDraftMessage(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.draft_message = _types.TgDraftMessage(data.get('draft_message'), client)
        self.positions = data.get('positions')


class TgUpdateChatAction(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.message_thread_id = data.get('message_thread_id')
        self.sender_id = _types.TgMessageSenderUser(data.get('sender_id'), client)
        self.action = _types.get_chat_action(data.get('action'), client)


class TgUpdateNewMessage(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.message = _types.TgMessage(data.get('message'), client)


class TgUpdateDeleteMessages(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.message_ids = data.get('message_ids')
        self.is_permanent = data.get('is_permanent')
        self.from_cache = data.get('from_cache')


class TgUpdateBasicGroupFullInfo(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.basic_group_id = data.get('basic_group_id')
        self.basic_group_full_info = _types.TgBasicGroupFullInfo(data.get('basic_group_full_info'), client)


class TgUpdateFile(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.file = _types.TgFile(data.get('file'), client)


class TgError(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.code = data.get('code')
        self.message = data.get('message')
class TgUpdateMessageSendSucceeded(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'] .lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.message = None if 'message' not in data else _types.TgMessage(data.get('message'), client)
        self.old_message_id = data.get('old_message_id')


class TgUpdateChatUnreadReactionCount(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'] .lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.unread_reaction_count = data.get('unread_reaction_count')


class TgUpdateMessageContent(TgEvent):
    def __init__(self, data: dict, client):
        if data['@type'] .lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.chat_id = data.get('chat_id')
        self.message_id = data.get('message_id')
        self.new_content = None if 'new_content' not in data else _types.TgMessageDocument(data.get('new_content'), client)


