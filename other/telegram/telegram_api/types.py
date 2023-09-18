import base64
import os


def check_type(name: str, obj: object):
    if name.lower() != obj.__class__.__name__[2:].lower():
        raise TypeError(f"TgType error: get type {name}")


def update_object(obj1: object, obj2: object):
    for key, item in obj2.__dict__.items():
        setattr(obj1, key, item)


def get_tg_option(data: dict, client):
    if data['@type'] == 'optionValueString':
        return TgOptionValueString(data, client)
    if data['@type'] == 'optionValueInteger':
        return TgOptionValueInteger(data, client)
    if data['@type'] == 'optionValueBoolean':
        return TgOptionValueBoolean(data, client)
    raise TypeError(f"Unknown option type {data['@type']}")


def get_authorization_state(data: dict, client):
    if data['@type'] == 'authorizationStateWaitPhoneNumber':
        return TgAuthorizationStateWaitPhoneNumber(data, client)
    if data['@type'] == 'authorizationStateWaitTdlibParameters':
        return TgAuthorizationStateWaitTdlibParameters(data, client)
    if data['@type'] == 'authorizationStateReady':
        return TgAuthorizationStateReady(data, client)
    if data['@type'] == 'authorizationStateWaitEmailAddress':
        return TgAuthorizationStateWaitEmailAddress(data, client)
    if data['@type'] == 'authorizationStateWaitEmailCode':
        return TgAuthorizationStateWaitEmailCode(data, client)
    if data['@type'] == 'authorizationStateWaitRegistration':
        return TgAuthorizationStateWaitRegistration(data, client)
    if data['@type'] == 'authorizationStateWaitPassword':
        return TgAuthorizationStateWaitPassword(data, client)
    if data['@type'] == 'authorizationStateWaitCode':
        return TgAuthorizationStateWaitCode(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_connection_state(data: dict, client):
    if data['@type'] == "connectionStateUpdating":
        return TgConnectionStateUpdating(data, client)
    if data['@type'] == "connectionStateReady":
        return TgConnectionStateReady(data, client)
    if data['@type'] == "connectionStateConnecting":
        return TgConnectionStateConnecting(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_user_status(data: dict, client):
    if data['@type'] == "userStatusRecently":
        return TgUserStatusRecently(data, client)
    if data['@type'] == "userStatusEmpty":
        return TgUserStatusEmpty(data, client)
    if data['@type'] == "userStatusOffline":
        return TgUserStatusOffline(data, client)
    if data['@type'] == "userStatusOnline":
        return TgUserStatusOnline(data, client)
    if data['@type'] == "userStatusLastMonth":
        return TgUserStatusLastMonth(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_user_type(data: dict, client):
    if data['@type'] == "userTypeBot":
        return TgUserTypeBot(data, client)
    if data['@type'] == "userTypeRegular":
        return TgUserTypeRegular(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_chat_member_status(data: dict, client):
    if data['@type'] == "chatMemberStatusMember":
        return TgChatMemberStatusMember(data, client)
    if data['@type'] == "chatMemberStatusLeft":
        return TgChatMemberStatusLeft(data, client)
    if data['@type'] == "chatMemberStatusBanned":
        return TgChatMemberStatusBanned(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_message_sender(data: dict, client):
    if data['@type'] == "messageSenderUser":
        return TgMessageSenderUser(data, client)
    if data['@type'] == "messageSenderChat":
        return TgMessageSenderChat(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_chat_type(data: dict, client):
    if data['@type'] == "chatTypeSupergroup":
        return TgChatTypeSupergroup(data, client)
    if data['@type'] == "chatTypePrivate":
        return TgChatTypePrivate(data, client)
    if data['@type'] == "chatTypeBasicGroup":
        return TgChatTypeBasicGroup(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_message_content(data: dict, client):
    if data['@type'] == "messageText":
        return TgMessageText(data, client)
    if data['@type'] == "messagePhoto":
        return TgMessagePhoto(data, client)
    if data['@type'] == "messageDocument":
        return TgMessageDocument(data, client)
    if data['@type'] == "messageChatUpgradeTo":
        return TgMessageChatUpgradeTo(data, client)
    if data['@type'] == "messageContactRegistered":
        return TgMessageContactRegistered(data, client)
    if data['@type'] == "messageVideo":
        return TgMessageVideo(data, client)
    if data['@type'] == "messageSticker":
        return TgMessageSticker(data, client)
    if data['@type'] == "messageAnimation":
        return TgMessageAnimation(data, client)
    if data['@type'] == "messageAnimatedEmoji":
        return TgMessageAnimatedEmoji(data, client)
    if data['@type'] == "messageChatChangeTitle":
        return TgMessageChatChangeTitle(data, client)
    if data['@type'] == "messageGameScore":
        return TgMessageGameScore(data, client)
    if data['@type'] == "messageGame":
        return TgMessageGame(data, client)
    if data['@type'] == "messageChatJoinByLink":
        return TgMessageChatJoinByLink(data, client)
    if data['@type'] == "messageChatAddMembers":
        return TgMessageChatAddMembers(data, client)
    raise TypeError(f"Unknown message content {data['@type']}")


def get_chat_available_reactions(data: dict, client):
    if data['@type'] == "chatAvailableReactionsSome":
        return TgChatAvailableReactionsSome(data, client)
    if data['@type'] == "chatAvailableReactionsAll":
        return TgChatAvailableReactionsAll(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_chat_list(data: dict, client):
    if data['@type'] == "chatListArchive":
        return TgChatListArchive(data, client)
    if data['@type'] == "chatListMain":
        return TgChatListMain(data, client)
    if data['@type'] == "chatListFilter":
        return TgChatListFilter(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_sticker_format(data: dict, client):
    if data['@type'] == "stickerFormatTgs":
        return TgStickerFormatTgs(data, client)
    if data['@type'] == "stickerFormatWebp":
        return TgStickerFormatWebp(data, client)
    if data['@type'] == "stickerFormatWebm":
        return TgStickerFormatWebm(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_thumbnail_format(data: dict, client):
    if data['@type'] == "thumbnailFormatJpeg":
        return TgThumbnailFormatJpeg(data, client)
    if data['@type'] == "thumbnailFormatPng":
        return TgThumbnailFormatPng(data, client)
    if data['@type'] == "thumbnailFormatWebp":
        return TgThumbnailFormatWebp(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


def get_chat_action(data: dict, client):
    if data['@type'] == "chatActionTyping":
        return TgChatActionTyping(data, client)
    if data['@type'] == "chatActionCancel":
        return TgChatActionCancel(data, client)
    if data['@type'] == "chatActionUploadingDocument":
        return TgChatActionUploadingDocument(data, client)
    raise TypeError(f"Unknown authorization state {data['@type']}")


class TgOptionValueString:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.value = data.get('value')


class TgAuthorizationStateWaitTdlibParameters:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgOptionValueInteger:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.value = int(data.get('value'))


class TgReactionTypeEmoji:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.emoji = data.get('emoji')


class TgOptionValueBoolean:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.value = data.get('value')


class TgAuthorizationStateReady:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgNotificationSettingsScopeChannelChats:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgScopeNotificationSettings:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.mute_for = data.get('mute_for')
        self.sound_id = data.get('sound_id')
        self.show_preview = data.get('show_preview')
        self.disable_pinned_message_notifications = data.get('disable_pinned_message_notifications')
        self.disable_mention_notifications = data.get('disable_mention_notifications')


class TgChatListMain:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgChatListFilter:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.chat_filter_id = data.get('chat_filter_id')


class TgChatListArchive:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgConnectionStateConnecting:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgUser:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.phone_number = data.get('phone_number')
        self.status = get_user_status(data.get('status'), client)
        self.is_contact = data.get('is_contact')
        self.is_mutual_contact = data.get('is_mutual_contact')
        self.is_verified = data.get('is_verified')
        self.is_premium = data.get('is_premium')
        self.is_support = data.get('is_support')
        self.has_anonymous_phone_number = data.get('has_anonymous_phone_number')
        self.restriction_reason = data.get('restriction_reason')
        self.is_scam = data.get('is_scam')
        self.is_fake = data.get('is_fake')
        self.have_access = data.get('have_access')
        self.type = get_user_type(data.get('type'), client)
        self.language_code = data.get('language_code')
        self.added_to_attachment_menu = data.get('added_to_attachment_menu')

    def set_status(self, status):
        self.status = status


class TgUserStatusEmpty:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgUserTypeRegular:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgProfilePhoto:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        self.small = TgFile(data.get('small'), client)
        self.big = TgFile(data.get('big'), client)
        self.minithumbnail = TgMinithumbnail(data.get('minithumbnail'), client)
        self.has_animation = data.get('has_animation')


class TgFile:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        self.size = data.get('size')
        self.expected_size = data.get('expected_size')
        self.local = TgLocalFile(data.get('local'), client)
        self.remote = TgRemoteFile(data.get('remote'), client)

        self._client = client
        self._client.update_file(self)

    def download(self):
        self._client.download_file(self)


class TgLocalFile:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.path = data.get('path')
        self.can_be_downloaded = data.get('can_be_downloaded')
        self.can_be_deleted = data.get('can_be_deleted')
        self.is_downloading_active = data.get('is_downloading_active')
        self.is_downloading_completed = data.get('is_downloading_completed')
        self.download_offset = data.get('download_offset')
        self.downloaded_prefix_size = data.get('downloaded_prefix_size')
        self.downloaded_size = data.get('downloaded_size')


class TgRemoteFile:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        self.unique_id = data.get('unique_id')
        self.is_uploading_active = data.get('is_uploading_active')
        self.is_uploading_completed = data.get('is_uploading_completed')
        self.uploaded_size = data.get('uploaded_size')


class TgMinithumbnail:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.width = data.get('width')
        self.height = data.get('height')
        self.data = data.get('data')
        self._client = client

    def load(self, path=None):
        if path is None:
            path = self._client.temp_path
        path = os.path.join(path, 'minithumbnail.jpeg')
        with open(path, 'bw') as f:
            f.write(base64.b64decode(self.data))
        return path


class TgSupergroup:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        # self.usernames = TgUsernames(data.get('usernames'), client)
        self.date = data.get('date')
        self.status = get_chat_member_status(data.get('status'), client)
        self.member_count = data.get('member_count')
        self.has_linked_chat = data.get('has_linked_chat')
        self.has_location = data.get('has_location')
        self.sign_messages = data.get('sign_messages')
        self.join_to_send_messages = data.get('join_to_send_messages')
        self.join_by_request = data.get('join_by_request')
        self.is_slow_mode_enabled = data.get('is_slow_mode_enabled')
        self.is_channel = data.get('is_channel')
        self.is_broadcast_group = data.get('is_broadcast_group')
        self.is_forum = data.get('is_forum')
        self.is_verified = data.get('is_verified')
        self.restriction_reason = data.get('restriction_reason')
        self.is_scam = data.get('is_scam')
        self.is_fake = data.get('is_fake')


class TgUsernames:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.active_usernames = data.get('active_usernames')
        self.disabled_usernames = data.get('disabled_usernames')
        self.editable_username = data.get('editable_username')


class TgChatMemberStatusMember:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgChat:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        self.type = get_chat_type(data.get('type'), client)
        self.title = data.get('title')
        self.photo = None if 'photo' not in data else TgChatPhotoInfo(data.get('photo'), client)
        self.permissions = TgChatPermissions(data.get('permissions'), client)
        self.positions = data.get('positions')
        self.has_protected_content = data.get('has_protected_content')
        self.is_marked_as_unread = data.get('is_marked_as_unread')
        self.is_blocked = data.get('is_blocked')
        self.has_scheduled_messages = data.get('has_scheduled_messages')
        self.can_be_deleted_only_for_self = data.get('can_be_deleted_only_for_self')
        self.can_be_deleted_for_all_users = data.get('can_be_deleted_for_all_users')
        self.can_be_reported = data.get('can_be_reported')
        self.default_disable_notification = data.get('default_disable_notification')
        self.unread_count = data.get('unread_count')
        self.last_read_inbox_message_id = data.get('last_read_inbox_message_id')
        self.last_read_outbox_message_id = data.get('last_read_outbox_message_id')
        self.unread_mention_count = data.get('unread_mention_count')
        self.unread_reaction_count = data.get('unread_reaction_count')
        self.notification_settings = TgChatNotificationSettings(data.get('notification_settings'), client)
        self.available_reactions = get_chat_available_reactions(data.get('available_reactions'), client)
        self.message_ttl = data.get('message_ttl')
        self.theme_name = data.get('theme_name')
        self.video_chat = TgVideoChat(data.get('video_chat'), client)
        self.reply_markup_message_id = data.get('reply_markup_message_id')
        self.client_data = data.get('client_data')

        self._messages = dict()
        self.first_message = None
        self.last_message = None
        self.last_message_count = 0

    def append_message(self, message: 'TgMessage'):
        self._messages[message.id] = message
        self.set_last_message(message)
        if self.first_message is None:
            self.set_first_message(message)

    def insert_message(self, message: 'TgMessage'):
        self._messages[message.id] = message
        self.set_first_message(message)

    def set_first_message(self, message: 'TgMessage'):
        self.first_message = message

    def set_last_message(self, message: 'TgMessage'):
        self.last_message = message

    def message_count(self):
        return len(self._messages)


class TgChatTypeSupergroup:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.supergroup_id = data.get('supergroup_id')
        self.is_channel = data.get('is_channel')


class TgChatPhotoInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.small = TgFile(data.get('small'), client)
        self.big = TgFile(data.get('big'), client)
        self.minithumbnail = TgMinithumbnail(data.get('minithumbnail'), client)
        self.has_animation = data.get('has_animation')


class TgChatPermissions:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.can_send_messages = data.get('can_send_messages')
        self.can_send_media_messages = data.get('can_send_media_messages')
        self.can_send_polls = data.get('can_send_polls')
        self.can_send_other_messages = data.get('can_send_other_messages')
        self.can_add_web_page_previews = data.get('can_add_web_page_previews')
        self.can_change_info = data.get('can_change_info')
        self.can_invite_users = data.get('can_invite_users')
        self.can_pin_messages = data.get('can_pin_messages')
        self.can_manage_topics = data.get('can_manage_topics')


class TgChatNotificationSettings:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.use_default_mute_for = data.get('use_default_mute_for')
        self.mute_for = data.get('mute_for')
        self.use_default_sound = data.get('use_default_sound')
        self.sound_id = data.get('sound_id')
        self.use_default_show_preview = data.get('use_default_show_preview')
        self.show_preview = data.get('show_preview')
        self.use_default_disable_pinned_message_notifications = data.get(
            'use_default_disable_pinned_message_notifications')
        self.disable_pinned_message_notifications = data.get('disable_pinned_message_notifications')
        self.use_default_disable_mention_notifications = data.get('use_default_disable_mention_notifications')
        self.disable_mention_notifications = data.get('disable_mention_notifications')


class TgChatAvailableReactionsSome:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.reactions = data.get('reactions')


class TgVideoChat:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.group_call_id = data.get('group_call_id')
        self.has_participants = data.get('has_participants')


class TgChatMemberStatusLeft:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgUserStatusOffline:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.was_online = data.get('was_online')


class TgChatAvailableReactionsAll:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgMessage:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        self.sender_id = get_message_sender(data.get('sender_id'), client)
        self.chat_id = data.get('chat_id')
        self.is_outgoing = data.get('is_outgoing')
        self.is_pinned = data.get('is_pinned')
        self.can_be_edited = data.get('can_be_edited')
        self.can_be_forwarded = data.get('can_be_forwarded')
        self.can_be_saved = data.get('can_be_saved')
        self.can_be_deleted_only_for_self = data.get('can_be_deleted_only_for_self')
        self.can_be_deleted_for_all_users = data.get('can_be_deleted_for_all_users')
        self.can_get_added_reactions = data.get('can_get_added_reactions')
        self.can_get_statistics = data.get('can_get_statistics')
        self.can_get_message_thread = data.get('can_get_message_thread')
        self.can_get_viewers = data.get('can_get_viewers')
        self.can_get_media_timestamp_links = data.get('can_get_media_timestamp_links')
        self.can_report_reactions = data.get('can_report_reactions')
        self.has_timestamped_media = data.get('has_timestamped_media')
        self.is_channel_post = data.get('is_channel_post')
        self.is_topic_message = data.get('is_topic_message')
        self.contains_unread_mention = data.get('contains_unread_mention')
        self.date = data.get('date')
        self.edit_date = data.get('edit_date')
        self.unread_reactions = data.get('unread_reactions')
        self.reply_in_chat_id = data.get('reply_in_chat_id')
        self.reply_to_message_id = data.get('reply_to_message_id')
        self.message_thread_id = data.get('message_thread_id')
        self.ttl = data.get('ttl')
        self.ttl_expires_in = data.get('ttl_expires_in')
        self.via_bot_user_id = data.get('via_bot_user_id')
        self.author_signature = data.get('author_signature')
        self.media_album_id = data.get('media_album_id')
        self.restriction_reason = data.get('restriction_reason')
        self.content = get_message_content(data.get('content'), client)


class TgMessageSenderUser:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.user_id = data.get('user_id')


class TgMessageText:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.text = TgFormattedText(data.get('text'), client)


class TgFormattedText:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.text = data.get('text')
        self.entities = data.get('entities')


class TgSupergroupFullInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.photo = None if 'photo' not in data else TgChatPhoto(data.get('photo'), client)
        self.description = data.get('description')
        self.member_count = data.get('member_count')
        self.administrator_count = data.get('administrator_count')
        self.restricted_count = data.get('restricted_count')
        self.banned_count = data.get('banned_count')
        self.linked_chat_id = data.get('linked_chat_id')
        self.slow_mode_delay = data.get('slow_mode_delay')
        self.slow_mode_delay_expires_in = data.get('slow_mode_delay_expires_in')
        self.can_get_members = data.get('can_get_members')
        self.can_set_username = data.get('can_set_username')
        self.can_set_sticker_set = data.get('can_set_sticker_set')
        self.can_set_location = data.get('can_set_location')
        self.can_get_statistics = data.get('can_get_statistics')
        self.is_all_history_available = data.get('is_all_history_available')
        self.is_aggressive_anti_spam_enabled = data.get('is_aggressive_anti_spam_enabled')
        self.sticker_set_id = data.get('sticker_set_id')
        self.bot_commands = data.get('bot_commands')
        self.upgraded_from_basic_group_id = data.get('upgraded_from_basic_group_id')
        self.upgraded_from_max_message_id = data.get('upgraded_from_max_message_id')


class TgChatPhoto:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        self.added_date = data.get('added_date')
        self.minithumbnail = None if 'minithumbnail' not in data else TgMinithumbnail(data.get('minithumbnail'), client)
        self.sizes = data.get('sizes')


class TgMessageSenderChat:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.chat_id = data.get('chat_id')


class TgMessageInteractionInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.view_count = data.get('view_count')
        self.forward_count = data.get('forward_count')
        self.reply_info = None if 'replay_info' not in data else TgMessageReplyInfo(data.get('reply_info'), client)
        self.reactions = data.get('reactions')


class TgMessageReplyInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.reply_count = data.get('reply_count')
        self.recent_replier_ids = data.get('recent_replier_ids')
        self.last_read_inbox_message_id = data.get('last_read_inbox_message_id')
        self.last_read_outbox_message_id = data.get('last_read_outbox_message_id')
        self.last_message_id = data.get('last_message_id')


class TgMessagePhoto:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.photo = TgPhoto(data.get('photo'), client)
        self.caption = TgFormattedText(data.get('caption'), client)
        self.is_secret = data.get('is_secret')


class TgPhoto:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.has_stickers = data.get('has_stickers')
        self.minithumbnail = None if 'minithumbnail' not in data else TgMinithumbnail(data.get('minithumbnail'), client)
        self.sizes = list(map(lambda size: TgPhotoSize(size, client), data.get('sizes', [])))


class TgUserStatusRecently:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgDraftMessage:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.reply_to_message_id = data.get('reply_to_message_id')
        self.date = data.get('date')
        self.input_message_text = TgInputMessageText(data.get('input_message_text'), client)


class TgInputMessageText:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.text = TgFormattedText(data.get('text'), client)
        self.disable_web_page_preview = data.get('disable_web_page_preview')
        self.clear_draft = data.get('clear_draft')


class TgMessageForwardInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.origin = TgMessageForwardOriginChannel(data.get('origin'), client)
        self.date = data.get('date')
        self.public_service_announcement_type = data.get('public_service_announcement_type')
        self.from_chat_id = data.get('from_chat_id')
        self.from_message_id = data.get('from_message_id')


class TgMessageForwardOriginChannel:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.chat_id = data.get('chat_id')
        self.message_id = data.get('message_id')
        self.author_signature = data.get('author_signature')


class TgWebPage:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.url = data.get('url')
        self.display_url = data.get('display_url')
        self.type = data.get('type')
        self.site_name = data.get('site_name')
        self.title = data.get('title')
        self.description = TgFormattedText(data.get('description'), client)
        self.photo = TgPhoto(data.get('photo'), client)
        self.embed_url = data.get('embed_url')
        self.embed_type = data.get('embed_type')
        self.embed_width = data.get('embed_width')
        self.embed_height = data.get('embed_height')
        self.duration = data.get('duration')
        self.author = data.get('author')
        self.instant_view_version = data.get('instant_view_version')


class TgChatPosition:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.list = get_chat_list(data.get('list'), client)
        self.order = data.get('order')
        self.is_pinned = data.get('is_pinned')


class TgChatTypePrivate:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.user_id = data.get('user_id')


class TgUserStatusOnline:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.expires = data.get('expires')


class TgUserTypeBot:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.can_join_groups = data.get('can_join_groups')
        self.can_read_all_group_messages = data.get('can_read_all_group_messages')
        self.is_inline = data.get('is_inline')
        self.inline_query_placeholder = data.get('inline_query_placeholder')
        self.need_location = data.get('need_location')
        self.can_be_added_to_attachment_menu = data.get('can_be_added_to_attachment_menu')


class TgEmojiStatus:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.custom_emoji_id = data.get('custom_emoji_id')


class TgBasicGroup:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.id = data.get('id')
        self.member_count = data.get('member_count')
        self.status = get_chat_member_status(data.get('status'), client)
        self.is_active = data.get('is_active')
        self.upgraded_to_supergroup_id = data.get('upgraded_to_supergroup_id')


class TgChatTypeBasicGroup:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.basic_group_id = data.get('basic_group_id')


class TgMessageForwardOriginUser:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.sender_user_id = data.get('sender_user_id')


class TgMessageDocument:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.document = TgDocument(data.get('document'), client)
        self.caption = TgFormattedText(data.get('caption'), client)


class TgDocument:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.file_name = data.get('file_name')
        self.mime_type = data.get('mime_type')
        self.document = TgFile(data.get('document'), client)


class TgMessageForwardOriginHiddenUser:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        self.sender_name = data.get('sender_name')


class TgConnectionStateUpdating:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgConnectionStateReady:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError(f"TgType error: get type {data['@type']}")
        pass


class TgAuthorizationStateWaitPhoneNumber:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgAuthorizationStateWaitCode:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.code_info = TgAuthenticationCodeInfo(data.get('code_info'), client)


class TgAuthorizationStateWaitRegistration:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgAuthorizationStateWaitPassword:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgAuthorizationStateWaitEmailAddress:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgAuthorizationStateWaitEmailCode:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgAuthenticationCodeInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.phone_number = data.get('phone_number')
        self.type = TgAuthenticationCodeTypeTelegramMessage(data.get('type'), client)
        self.timeout = data.get('timeout')


class TgAuthenticationCodeTypeTelegramMessage:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.length = data.get('length')


class TgChatMemberStatusBanned:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.banned_until_date = data.get('banned_until_date')


class TgMessageContactRegistered:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgVideo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.duration = data.get('duration')
        self.width = data.get('width')
        self.height = data.get('height')
        self.file_name = data.get('file_name')
        self.mime_type = data.get('mime_type')
        self.has_stickers = data.get('has_stickers')
        self.supports_streaming = data.get('supports_streaming')
        self.minithumbnail = TgMinithumbnail(data.get('minithumbnail'), client)
        self.thumbnail = TgThumbnail(data.get('thumbnail'), client)
        self.video = TgFile(data.get('video'), client)


class TgThumbnail:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.format = get_thumbnail_format(data.get('format'), client)
        self.width = data.get('width')
        self.height = data.get('height')
        self.file = TgFile(data.get('file'), client)


class TgThumbnailFormatJpeg:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgMessageChatUpgradeTo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.supergroup_id = data.get('supergroup_id')


class TgUserFullInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.photo = None if 'photo' not in data else TgChatPhoto(data.get('photo'), client)
        self.is_blocked = data.get('is_blocked')
        self.can_be_called = data.get('can_be_called')
        self.supports_video_calls = data.get('supports_video_calls')
        self.has_private_calls = data.get('has_private_calls')
        self.has_private_forwards = data.get('has_private_forwards')
        self.has_restricted_voice_and_video_note_messages = data.get('has_restricted_voice_and_video_note_messages')
        self.need_phone_number_privacy_exception = data.get('need_phone_number_privacy_exception')
        self.bio = None if 'bio' not in data else TgFormattedText(data.get('bio'), client)
        self.premium_gift_options = data.get('premium_gift_options')
        self.group_in_common_count = data.get('group_in_common_count')


class TgUserStatusLastMonth:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgBasicGroupFullInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.photo = None if 'photo' not in data else TgChatPhoto(data.get('photo'), client)
        self.description = data.get('description')
        self.creator_user_id = data.get('creator_user_id')
        self.members = data.get('members')
        self.bot_commands = data.get('bot_commands')


class TgBotInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.share_text = data.get('share_text')
        self.description = data.get('description')
        self.commands = data.get('commands')


class TgChatActionTyping:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgMessageVideo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.video = TgVideo(data.get('video'), client)
        self.caption = TgFormattedText(data.get('caption'), client)
        self.is_secret = data.get('is_secret')


class TgMessageAnimatedEmoji:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.animated_emoji = TgAnimatedEmoji(data.get('animated_emoji'), client)
        self.emoji = data.get('emoji')


class TgAnimatedEmoji:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.sticker = TgSticker(data.get('sticker'), client)
        self.sticker_width = data.get('sticker_width')
        self.sticker_height = data.get('sticker_height')
        self.fitzpatrick_type = data.get('fitzpatrick_type')


class TgSticker:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.set_id = data.get('set_id')
        self.width = data.get('width')
        self.height = data.get('height')
        self.emoji = data.get('emoji')
        self.format = get_sticker_format(data.get('format'), client)
        self.type = TgStickerTypeRegular(data.get('type'), client)
        self.custom_emoji_id = data.get('custom_emoji_id')
        self.outline = data.get('outline')
        self.thumbnail = TgThumbnail(data.get('thumbnail'), client)
        self.is_premium = data.get('is_premium')
        self.sticker = TgFile(data.get('sticker'), client)


class TgStickerFormatTgs:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgStickerTypeRegular:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgThumbnailFormatWebp:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgMessageSticker:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.sticker = TgSticker(data.get('sticker'), client)
        self.is_premium = data.get('is_premium')


class TgStickerFormatWebp:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgAnimatedChatPhoto:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.length = data.get('length')
        self.file = TgFile(data.get('file'), client)
        self.main_frame_timestamp = data.get('main_frame_timestamp')


class TgChatTheme:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.name = data.get('name')
        self.light_settings = TgThemeSettings(data.get('light_settings'), client)
        self.dark_settings = TgThemeSettings(data.get('dark_settings'), client)


class TgThemeSettings:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.accent_color = data.get('accent_color')
        self.background = TgBackground(data.get('background'), client)
        self.outgoing_message_fill = TgBackgroundFillGradient(data.get('outgoing_message_fill'), client)
        self.animate_outgoing_message_fill = data.get('animate_outgoing_message_fill')
        self.outgoing_message_accent_color = data.get('outgoing_message_accent_color')


class TgBackground:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.id = data.get('id')
        self.is_default = data.get('is_default')
        self.is_dark = data.get('is_dark')
        self.name = data.get('name')
        self.document = TgDocument(data.get('document'), client)
        self.type = TgBackgroundTypePattern(data.get('type'), client)


class TgThumbnailFormatPng:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgBackgroundTypePattern:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.fill = TgBackgroundFillFreeformGradient(data.get('fill'), client)
        self.intensity = data.get('intensity')
        self.is_inverted = data.get('is_inverted')
        self.is_moving = data.get('is_moving')


class TgBackgroundFillFreeformGradient:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.colors = data.get('colors')


class TgBackgroundFillGradient:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.top_color = data.get('top_color')
        self.bottom_color = data.get('bottom_color')
        self.rotation_angle = data.get('rotation_angle')


class TgBackgroundFillSolid:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.color = data.get('color')


class TgChatFilterInfo:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.id = data.get('id')
        self.title = data.get('title')
        self.icon_name = data.get('icon_name')


class TgPhotoSize:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.type = data.get('type')
        self.photo = TgFile(data.get('photo'), client)
        self.width = data.get('width')
        self.height = data.get('height')
        self.progressive_sizes = data.get('progressive_sizes')


class TgMessageReaction:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.type = TgReactionTypeEmoji(data.get('type'), client)
        self.total_count = data.get('total_count')
        self.is_chosen = data.get('is_chosen')
        self.recent_sender_ids = data.get('recent_sender_ids')


class TgTextEntity:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.offset = data.get('offset')
        self.length = data.get('length')
        self.type = TgTextEntityTypeTextUrl(data.get('type'), client)


class TgTextEntityTypeTextUrl:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.url = data.get('url')


class TgTextEntityTypeBold:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgTextEntityTypeUrl:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgTextEntityTypePre:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgTextEntityTypeEmailAddress:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgTextEntityTypeMention:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgTextEntityTypeCode:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgMessageAnimation:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.animation = TgAnimation(data.get('animation'), client)
        self.caption = TgFormattedText(data.get('caption'), client)
        self.is_secret = data.get('is_secret')


class TgAnimation:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.duration = data.get('duration')
        self.width = data.get('width')
        self.height = data.get('height')
        self.file_name = data.get('file_name')
        self.mime_type = data.get('mime_type')
        self.has_stickers = data.get('has_stickers')
        self.minithumbnail = TgMinithumbnail(data.get('minithumbnail'), client)
        self.thumbnail = TgThumbnail(data.get('thumbnail'), client)
        self.animation = TgFile(data.get('animation'), client)


class TgClosedVectorPath:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.commands = data.get('commands')


class TgVectorPathCommandCubicBezierCurve:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.start_control_point = TgPoint(data.get('start_control_point'), client)
        self.end_control_point = TgPoint(data.get('end_control_point'), client)
        self.end_point = TgPoint(data.get('end_point'), client)


class TgPoint:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.x = data.get('x')
        self.y = data.get('y')


class TgVectorPathCommandLine:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.end_point = TgPoint(data.get('end_point'), client)


class TgTextEntityTypeItalic:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgTextEntityTypeCustomEmoji:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.custom_emoji_id = data.get('custom_emoji_id')


class TgTextEntityTypeHashtag:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgPremiumPaymentOption:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.currency = data.get('currency')
        self.amount = data.get('amount')
        self.discount_percentage = data.get('discount_percentage')
        self.month_count = data.get('month_count')
        self.store_product_id = data.get('store_product_id')
        self.payment_link = TgInternalLinkTypeInvoice(data.get('payment_link'), client)


class TgInternalLinkTypeInvoice:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.invoice_name = data.get('invoice_name')


class TgChatMember:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.member_id = TgMessageSenderUser(data.get('member_id'), client)
        self.inviter_user_id = data.get('inviter_user_id')
        self.joined_chat_date = data.get('joined_chat_date')
        self.status = TgChatMemberStatusMember(data.get('status'), client)


class TgChatMemberStatusCreator:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.custom_title = data.get('custom_title')
        self.is_anonymous = data.get('is_anonymous')
        self.is_member = data.get('is_member')


class TgReplyMarkupInlineKeyboard:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        self.rows = data.get('rows')


class TgTextEntityTypeBotCommand:
    def __init__(self, data: dict, client):
        if data['@type'].lower() != self.__class__.__name__[2:].lower():
            raise TypeError('TgType error')
        pass


class TgMessageSendingStatePending:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        pass


class TgChatActionCancel:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        pass


class TgMessageChatAddMembers:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.member_user_ids = data.get('member_user_ids')


class TgMessageChatChangeTitle:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.title = data.get('title')
class TgMessageGameScore:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.game_message_id = data.get('game_message_id')
        self.game_id = data.get('game_id')
        self.score = data.get('score')


class TgMessageGame:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.game = None if 'game' not in data else TgGame(data.get('game'), client)


class TgGame:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.id = data.get('id')
        self.short_name = data.get('short_name')
        self.title = data.get('title')
        self.text = None if 'text' not in data else TgFormattedText(data.get('text'), client)
        self.description = data.get('description')
        self.photo = None if 'photo' not in data else TgPhoto(data.get('photo'), client)
        self.animation = None if 'animation' not in data else TgAnimation(data.get('animation'), client)


class TgMessageChatJoinByLink:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        pass

class TgStickerFormatWebm:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        pass

class TgChatActionUploadingDocument:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.progress = data.get('progress')


class TgMessagePoll:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.poll = None if 'poll' not in data else TgPoll(data.get('poll'), client)


class TgPoll:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.id = data.get('id')
        self.question = data.get('question')
        self.options = data.get('options')
        self.total_voter_count = data.get('total_voter_count')
        self.recent_voter_user_ids = data.get('recent_voter_user_ids')
        self.is_anonymous = data.get('is_anonymous')
        self.type = None if 'type' not in data else TgPollTypeRegular(data.get('type'), client)
        self.open_period = data.get('open_period')
        self.close_date = data.get('close_date')
        self.is_closed = data.get('is_closed')


class TgPollTypeRegular:
    def __init__(self, data: dict, client):
        check_type(data['@type'], self)
        self.allow_multiple_answers = data.get('allow_multiple_answers')


