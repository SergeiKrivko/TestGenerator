class TlObject(object):
    def __init__(self, **kwargs):
        super().__init__()
        self._data = kwargs


class TlStorerToString(object):
    def __init__(self, **kwargs):
        super().__init__()
        self._data = kwargs


class Object(TlObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Function(TlObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AccountTtl(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number of days of inactivity before the account will be flagged for deletion; 30-366 days.
        self.days: int = get_object(kwargs.get('days'))


class MessageSender(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReactionType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AddedReaction(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the reaction.
        self.type: ReactionType = get_object(kwargs.get('type'))
        # Identifier of the chat member, applied the reaction.
        self.sender_id: MessageSender = get_object(kwargs.get('sender_id'))
        # Point in time (Unix timestamp) when the reaction was added.
        self.date: int = get_object(kwargs.get('date'))


class AddedReactions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The total number of found reactions.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # The list of added reactions.
        self.reactions: list[AddedReaction] = get_object(kwargs.get('reactions'))
        # The offset for the next request. If empty, there are no more results.
        self.next_offset: str = get_object(kwargs.get('next_offset'))


class Address(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A two-letter ISO 3166-1 alpha-2 country code.
        self.country_code: str = get_object(kwargs.get('country_code'))
        # State, if applicable.
        self.state: str = get_object(kwargs.get('state'))
        # City.
        self.city: str = get_object(kwargs.get('city'))
        # First line of the address.
        self.street_line1: str = get_object(kwargs.get('street_line1'))
        # Second line of the address.
        self.street_line2: str = get_object(kwargs.get('street_line2'))
        # Address postal code.
        self.postal_code: str = get_object(kwargs.get('postal_code'))


class File(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique file identifier.
        self.id: int = get_object(kwargs.get('id'))
        # File size, in bytes; 0 if unknown.
        self.size: int = get_object(kwargs.get('size'))
        # Approximate file size in bytes in case the exact file size is unknown. Can be used to show download/upload progress.
        self.expected_size: int = get_object(kwargs.get('expected_size'))
        # Information about the local copy of the file.
        self.local: LocalFile = get_object(kwargs.get('local'))
        # Information about the remote copy of the file.
        self.remote: RemoteFile = get_object(kwargs.get('remote'))


class AnimatedChatPhoto(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Animation width and height.
        self.length: int = get_object(kwargs.get('length'))
        # Information about the animation file.
        self.file: File = get_object(kwargs.get('file'))
        # Timestamp of the frame, used as a static chat photo.
        self.main_frame_timestamp: float = get_object(kwargs.get('main_frame_timestamp'))


class Sticker(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique sticker identifier within the set; 0 if none.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the sticker set to which the sticker belongs; 0 if none.
        self.set_id: int = get_object(kwargs.get('set_id'))
        # Sticker width; as defined by the sender.
        self.width: int = get_object(kwargs.get('width'))
        # Sticker height; as defined by the sender.
        self.height: int = get_object(kwargs.get('height'))
        # Emoji corresponding to the sticker.
        self.emoji: str = get_object(kwargs.get('emoji'))
        # Sticker format.
        self.format: StickerFormat = get_object(kwargs.get('format'))
        # Sticker's full type.
        self.full_type: StickerFullType = get_object(kwargs.get('full_type'))
        # Sticker's outline represented as a list of closed vector paths; may be empty. The coordinate system origin is in the upper-left corner.
        self.outline: list[ClosedVectorPath] = get_object(kwargs.get('outline'))
        # Sticker thumbnail in WEBP or JPEG format; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))
        # File containing the sticker.
        self.sticker: File = get_object(kwargs.get('sticker'))


class AnimatedEmoji(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Sticker for the emoji; may be null if yet unknown for a custom emoji. If the sticker is a custom emoji, it can have arbitrary format different from stickerFormatTgs.
        self.sticker: Sticker = get_object(kwargs.get('sticker'))
        # Expected width of the sticker, which can be used if the sticker is null.
        self.sticker_width: int = get_object(kwargs.get('sticker_width'))
        # Expected height of the sticker, which can be used if the sticker is null.
        self.sticker_height: int = get_object(kwargs.get('sticker_height'))
        # Emoji modifier fitzpatrick type; 0-6; 0 if none.
        self.fitzpatrick_type: int = get_object(kwargs.get('fitzpatrick_type'))
        # File containing the sound to be played when the sticker is clicked; may be null. The sound is encoded with the Opus codec, and stored inside an OGG container.
        self.sound: File = get_object(kwargs.get('sound'))


class Minithumbnail(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Thumbnail width, usually doesn't exceed 40.
        self.width: int = get_object(kwargs.get('width'))
        # Thumbnail height, usually doesn't exceed 40.
        self.height: int = get_object(kwargs.get('height'))
        # The thumbnail in JPEG format.
        self.data: bytes = get_object(kwargs.get('data'))


class Thumbnail(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Thumbnail format.
        self.format: ThumbnailFormat = get_object(kwargs.get('format'))
        # Thumbnail width.
        self.width: int = get_object(kwargs.get('width'))
        # Thumbnail height.
        self.height: int = get_object(kwargs.get('height'))
        # The thumbnail.
        self.file: File = get_object(kwargs.get('file'))


class Animation(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Duration of the animation, in seconds; as defined by the sender.
        self.duration: int = get_object(kwargs.get('duration'))
        # Width of the animation.
        self.width: int = get_object(kwargs.get('width'))
        # Height of the animation.
        self.height: int = get_object(kwargs.get('height'))
        # Original name of the file; as defined by the sender.
        self.file_name: str = get_object(kwargs.get('file_name'))
        # MIME type of the file, usually &quot;image/gif&quot; or &quot;video/mp4&quot;.
        self.mime_type: str = get_object(kwargs.get('mime_type'))
        # True, if stickers were added to the animation. The list of corresponding sticker set can be received using getAttachedStickerSets.
        self.has_stickers: bool = get_object(kwargs.get('has_stickers'))
        # Animation minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # Animation thumbnail in JPEG or MPEG4 format; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))
        # File containing the animation.
        self.animation: File = get_object(kwargs.get('animation'))


class Animations(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of animations.
        self.animations: list[Animation] = get_object(kwargs.get('animations'))


class ArchiveChatListSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if new chats from non-contacts will be automatically archived and muted. Can be set to true only if the option &quot;can_archive_and_mute_new_chats_from_unknown_users&quot; is true.
        self.archive_and_mute_new_chats_from_unknown_users: bool = get_object(kwargs.get('archive_and_mute_new_chats_from_unknown_users'))
        # True, if unmuted chats will be kept in the Archive chat list when they get a new message.
        self.keep_unmuted_chats_archived: bool = get_object(kwargs.get('keep_unmuted_chats_archived'))
        # True, if unmuted chats, that are always included or pinned in a filter, will be kept in the Archive chat list when they get a new message. Ignored if keep_unmuted_chats_archived == true.
        self.keep_chats_from_filters_archived: bool = get_object(kwargs.get('keep_chats_from_filters_archived'))


class AttachmentMenuBotColor(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Color in the RGB24 format for light themes.
        self.light_color: int = get_object(kwargs.get('light_color'))
        # Color in the RGB24 format for dark themes.
        self.dark_color: int = get_object(kwargs.get('dark_color'))


class AttachmentMenuBot(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the bot.
        self.bot_user_id: int = get_object(kwargs.get('bot_user_id'))
        # True, if the bot supports opening from attachment menu in the chat with the bot.
        self.supports_self_chat: bool = get_object(kwargs.get('supports_self_chat'))
        # True, if the bot supports opening from attachment menu in private chats with ordinary users.
        self.supports_user_chats: bool = get_object(kwargs.get('supports_user_chats'))
        # True, if the bot supports opening from attachment menu in private chats with other bots.
        self.supports_bot_chats: bool = get_object(kwargs.get('supports_bot_chats'))
        # True, if the bot supports opening from attachment menu in basic group and supergroup chats.
        self.supports_group_chats: bool = get_object(kwargs.get('supports_group_chats'))
        # True, if the bot supports opening from attachment menu in channel chats.
        self.supports_channel_chats: bool = get_object(kwargs.get('supports_channel_chats'))
        # True, if the bot supports &quot;settings_button_pressed&quot; event.
        self.supports_settings: bool = get_object(kwargs.get('supports_settings'))
        # True, if the user must be asked for the permission to send messages to the bot.
        self.request_write_access: bool = get_object(kwargs.get('request_write_access'))
        # True, if the bot was explicitly added by the user. If the bot isn't added then on the first bot launch toggleBotIsAddedToAttachmentMenu must be called and the bot must be added or removed.
        self.is_added: bool = get_object(kwargs.get('is_added'))
        # True, if the bot must be shown in the attachment menu.
        self.show_in_attachment_menu: bool = get_object(kwargs.get('show_in_attachment_menu'))
        # True, if the bot must be shown in the side menu menu.
        self.show_in_side_menu: bool = get_object(kwargs.get('show_in_side_menu'))
        # True, if a disclaimer, why the bot is shown in the side menu, is needed.
        self.show_disclaimer_in_side_menu: bool = get_object(kwargs.get('show_disclaimer_in_side_menu'))
        # Name for the bot in attachment menu.
        self.name: str = get_object(kwargs.get('name'))
        # Color to highlight selected name of the bot if appropriate; may be null.
        self.name_color: AttachmentMenuBotColor = get_object(kwargs.get('name_color'))
        # Default icon for the bot in SVG format; may be null.
        self.default_icon: File = get_object(kwargs.get('default_icon'))
        # Icon for the bot in SVG format for the official iOS app; may be null.
        self.ios_static_icon: File = get_object(kwargs.get('ios_static_icon'))
        # Icon for the bot in TGS format for the official iOS app; may be null.
        self.ios_animated_icon: File = get_object(kwargs.get('ios_animated_icon'))
        # Icon for the bot in PNG format for the official iOS app side menu; may be null.
        self.ios_side_menu_icon: File = get_object(kwargs.get('ios_side_menu_icon'))
        # Icon for the bot in TGS format for the official Android app; may be null.
        self.android_icon: File = get_object(kwargs.get('android_icon'))
        # Icon for the bot in SVG format for the official Android app side menu; may be null.
        self.android_side_menu_icon: File = get_object(kwargs.get('android_side_menu_icon'))
        # Icon for the bot in TGS format for the official native macOS app; may be null.
        self.macos_icon: File = get_object(kwargs.get('macos_icon'))
        # Icon for the bot in PNG format for the official macOS app side menu; may be null.
        self.macos_side_menu_icon: File = get_object(kwargs.get('macos_side_menu_icon'))
        # Color to highlight selected icon of the bot if appropriate; may be null.
        self.icon_color: AttachmentMenuBotColor = get_object(kwargs.get('icon_color'))
        # Default placeholder for opened Web Apps in SVG format; may be null.
        self.web_app_placeholder: File = get_object(kwargs.get('web_app_placeholder'))


class Audio(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Duration of the audio, in seconds; as defined by the sender.
        self.duration: int = get_object(kwargs.get('duration'))
        # Title of the audio; as defined by the sender.
        self.title: str = get_object(kwargs.get('title'))
        # Performer of the audio; as defined by the sender.
        self.performer: str = get_object(kwargs.get('performer'))
        # Original name of the file; as defined by the sender.
        self.file_name: str = get_object(kwargs.get('file_name'))
        # The MIME type of the file; as defined by the sender.
        self.mime_type: str = get_object(kwargs.get('mime_type'))
        # The minithumbnail of the album cover; may be null.
        self.album_cover_minithumbnail: Minithumbnail = get_object(kwargs.get('album_cover_minithumbnail'))
        # The thumbnail of the album cover in JPEG format; as defined by the sender. The full size thumbnail is supposed to be extracted from the downloaded audio file; may be null.
        self.album_cover_thumbnail: Thumbnail = get_object(kwargs.get('album_cover_thumbnail'))
        # Album cover variants to use if the downloaded audio file contains no album cover. Provided thumbnail dimensions are approximate.
        self.external_album_covers: list[Thumbnail] = get_object(kwargs.get('external_album_covers'))
        # File containing the audio.
        self.audio: File = get_object(kwargs.get('audio'))


class AuthenticationCodeType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AuthenticationCodeInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A phone number that is being authenticated.
        self.phone_number: str = get_object(kwargs.get('phone_number'))
        # The way the code was sent to the user.
        self.type: AuthenticationCodeType = get_object(kwargs.get('type'))
        # The way the next code will be sent to the user; may be null.
        self.next_type: AuthenticationCodeType = get_object(kwargs.get('next_type'))
        # Timeout before the code can be re-sent, in seconds.
        self.timeout: int = get_object(kwargs.get('timeout'))


class AuthenticationCodeTypeTelegramMessage(AuthenticationCodeType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Length of the code.
        self.length: int = get_object(kwargs.get('length'))


class AuthenticationCodeTypeSms(AuthenticationCodeType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Length of the code.
        self.length: int = get_object(kwargs.get('length'))


class AuthenticationCodeTypeCall(AuthenticationCodeType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Length of the code.
        self.length: int = get_object(kwargs.get('length'))


class AuthenticationCodeTypeFlashCall(AuthenticationCodeType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Pattern of the phone number from which the call will be made.
        self.pattern: str = get_object(kwargs.get('pattern'))


class AuthenticationCodeTypeMissedCall(AuthenticationCodeType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Prefix of the phone number from which the call will be made.
        self.phone_number_prefix: str = get_object(kwargs.get('phone_number_prefix'))
        # Number of digits in the code, excluding the prefix.
        self.length: int = get_object(kwargs.get('length'))


class AuthenticationCodeTypeFragment(AuthenticationCodeType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # URL to open to receive the code.
        self.url: str = get_object(kwargs.get('url'))
        # Length of the code.
        self.length: int = get_object(kwargs.get('length'))


class AuthenticationCodeTypeFirebaseAndroid(AuthenticationCodeType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Nonce to pass to the SafetyNet Attestation API.
        self.nonce: bytes = get_object(kwargs.get('nonce'))
        # Length of the code.
        self.length: int = get_object(kwargs.get('length'))


class AuthenticationCodeTypeFirebaseIos(AuthenticationCodeType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Receipt of successful application token validation to compare with receipt from push notification.
        self.receipt: str = get_object(kwargs.get('receipt'))
        # Time after the next authentication method is supposed to be used if verification push notification isn't received, in seconds.
        self.push_timeout: int = get_object(kwargs.get('push_timeout'))
        # Length of the code.
        self.length: int = get_object(kwargs.get('length'))


class EmailAddressResetState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class EmailAddressAuthenticationCodeInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Pattern of the email address to which an authentication code was sent.
        self.email_address_pattern: str = get_object(kwargs.get('email_address_pattern'))
        # Length of the code; 0 if unknown.
        self.length: int = get_object(kwargs.get('length'))


class TermsOfService(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the terms of service.
        self.text: FormattedText = get_object(kwargs.get('text'))
        # The minimum age of a user to be able to accept the terms; 0 if age isn't restricted.
        self.min_user_age: int = get_object(kwargs.get('min_user_age'))
        # True, if a blocking popup with terms of service must be shown to the user.
        self.show_popup: bool = get_object(kwargs.get('show_popup'))


class AuthorizationState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AuthorizationStateWaitTdlibParameters(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AuthorizationStateWaitPhoneNumber(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AuthorizationStateWaitEmailAddress(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if authorization through Apple ID is allowed.
        self.allow_apple_id: bool = get_object(kwargs.get('allow_apple_id'))
        # True, if authorization through Google ID is allowed.
        self.allow_google_id: bool = get_object(kwargs.get('allow_google_id'))


class AuthorizationStateWaitEmailCode(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if authorization through Apple ID is allowed.
        self.allow_apple_id: bool = get_object(kwargs.get('allow_apple_id'))
        # True, if authorization through Google ID is allowed.
        self.allow_google_id: bool = get_object(kwargs.get('allow_google_id'))
        # Information about the sent authentication code.
        self.code_info: EmailAddressAuthenticationCodeInfo = get_object(kwargs.get('code_info'))
        # Reset state of the email address; may be null if the email address can't be reset.
        self.email_address_reset_state: EmailAddressResetState = get_object(kwargs.get('email_address_reset_state'))


class AuthorizationStateWaitCode(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the authorization code that was sent.
        self.code_info: AuthenticationCodeInfo = get_object(kwargs.get('code_info'))


class AuthorizationStateWaitOtherDeviceConfirmation(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A tg:// URL for the QR code. The link will be updated frequently.
        self.link: str = get_object(kwargs.get('link'))


class AuthorizationStateWaitRegistration(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Telegram terms of service.
        self.terms_of_service: TermsOfService = get_object(kwargs.get('terms_of_service'))


class AuthorizationStateWaitPassword(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Hint for the password; may be empty.
        self.password_hint: str = get_object(kwargs.get('password_hint'))
        # True, if a recovery email address has been set up.
        self.has_recovery_email_address: bool = get_object(kwargs.get('has_recovery_email_address'))
        # True, if some Telegram Passport elements were saved.
        self.has_passport_data: bool = get_object(kwargs.get('has_passport_data'))
        # Pattern of the email address to which the recovery email was sent; empty until a recovery email has been sent.
        self.recovery_email_address_pattern: str = get_object(kwargs.get('recovery_email_address_pattern'))


class AuthorizationStateReady(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AuthorizationStateLoggingOut(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AuthorizationStateClosing(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AuthorizationStateClosed(AuthorizationState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AutoDownloadSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the auto-download is enabled.
        self.is_auto_download_enabled: bool = get_object(kwargs.get('is_auto_download_enabled'))
        # The maximum size of a photo file to be auto-downloaded, in bytes.
        self.max_photo_file_size: int = get_object(kwargs.get('max_photo_file_size'))
        # The maximum size of a video file to be auto-downloaded, in bytes.
        self.max_video_file_size: int = get_object(kwargs.get('max_video_file_size'))
        # The maximum size of other file types to be auto-downloaded, in bytes.
        self.max_other_file_size: int = get_object(kwargs.get('max_other_file_size'))
        # The maximum suggested bitrate for uploaded videos, in kbit/s.
        self.video_upload_bitrate: int = get_object(kwargs.get('video_upload_bitrate'))
        # True, if the beginning of video files needs to be preloaded for instant playback.
        self.preload_large_videos: bool = get_object(kwargs.get('preload_large_videos'))
        # True, if the next audio track needs to be preloaded while the user is listening to an audio file.
        self.preload_next_audio: bool = get_object(kwargs.get('preload_next_audio'))
        # True, if stories needs to be preloaded.
        self.preload_stories: bool = get_object(kwargs.get('preload_stories'))
        # True, if &quot;use less data for calls&quot; option needs to be enabled.
        self.use_less_data_for_calls: bool = get_object(kwargs.get('use_less_data_for_calls'))


class AutoDownloadSettingsPresets(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Preset with lowest settings; supposed to be used by default when roaming.
        self.low: AutoDownloadSettings = get_object(kwargs.get('low'))
        # Preset with medium settings; supposed to be used by default when using mobile data.
        self.medium: AutoDownloadSettings = get_object(kwargs.get('medium'))
        # Preset with highest settings; supposed to be used by default when connected on Wi-Fi.
        self.high: AutoDownloadSettings = get_object(kwargs.get('high'))


class AutosaveSettingsException(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Autosave settings for the chat.
        self.settings: ScopeAutosaveSettings = get_object(kwargs.get('settings'))


class ScopeAutosaveSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if photo autosave is enabled.
        self.autosave_photos: bool = get_object(kwargs.get('autosave_photos'))
        # True, if video autosave is enabled.
        self.autosave_videos: bool = get_object(kwargs.get('autosave_videos'))
        # The maximum size of a video file to be autosaved, in bytes; 512 KB - 4000 MB.
        self.max_video_file_size: int = get_object(kwargs.get('max_video_file_size'))


class AutosaveSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Default autosave settings for private chats.
        self.private_chat_settings: ScopeAutosaveSettings = get_object(kwargs.get('private_chat_settings'))
        # Default autosave settings for basic group and supergroup chats.
        self.group_settings: ScopeAutosaveSettings = get_object(kwargs.get('group_settings'))
        # Default autosave settings for channel chats.
        self.channel_settings: ScopeAutosaveSettings = get_object(kwargs.get('channel_settings'))
        # Autosave settings for specific chats.
        self.exceptions: list[AutosaveSettingsException] = get_object(kwargs.get('exceptions'))


class AutosaveSettingsScope(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AutosaveSettingsScopePrivateChats(AutosaveSettingsScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AutosaveSettingsScopeGroupChats(AutosaveSettingsScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AutosaveSettingsScopeChannelChats(AutosaveSettingsScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class AutosaveSettingsScopeChat(AutosaveSettingsScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))


class AvailableReaction(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the reaction.
        self.type: ReactionType = get_object(kwargs.get('type'))
        # True, if Telegram Premium is needed to send the reaction.
        self.needs_premium: bool = get_object(kwargs.get('needs_premium'))


class AvailableReactions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of reactions to be shown at the top.
        self.top_reactions: list[AvailableReaction] = get_object(kwargs.get('top_reactions'))
        # List of recently used reactions.
        self.recent_reactions: list[AvailableReaction] = get_object(kwargs.get('recent_reactions'))
        # List of popular reactions.
        self.popular_reactions: list[AvailableReaction] = get_object(kwargs.get('popular_reactions'))
        # True, if custom emoji reactions could be added by Telegram Premium subscribers.
        self.allow_custom_emoji: bool = get_object(kwargs.get('allow_custom_emoji'))


class BackgroundType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Document(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Original name of the file; as defined by the sender.
        self.file_name: str = get_object(kwargs.get('file_name'))
        # MIME type of the file; as defined by the sender.
        self.mime_type: str = get_object(kwargs.get('mime_type'))
        # Document minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # Document thumbnail in JPEG or PNG format (PNG will be used only for background patterns); as defined by the sender; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))
        # File containing the document.
        self.document: File = get_object(kwargs.get('document'))


class Background(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique background identifier.
        self.id: int = get_object(kwargs.get('id'))
        # True, if this is one of default backgrounds.
        self.is_default: bool = get_object(kwargs.get('is_default'))
        # True, if the background is dark and is recommended to be used with dark theme.
        self.is_dark: bool = get_object(kwargs.get('is_dark'))
        # Unique background name.
        self.name: str = get_object(kwargs.get('name'))
        # Document with the background; may be null. Null only for filled backgrounds.
        self.document: Document = get_object(kwargs.get('document'))
        # Type of the background.
        self.type: BackgroundType = get_object(kwargs.get('type'))


class BackgroundFill(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BackgroundFillSolid(BackgroundFill):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A color of the background in the RGB24 format.
        self.color: int = get_object(kwargs.get('color'))


class BackgroundFillGradient(BackgroundFill):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A top color of the background in the RGB24 format.
        self.top_color: int = get_object(kwargs.get('top_color'))
        # A bottom color of the background in the RGB24 format.
        self.bottom_color: int = get_object(kwargs.get('bottom_color'))
        # Clockwise rotation angle of the gradient, in degrees; 0-359. Must always be divisible by 45.
        self.rotation_angle: int = get_object(kwargs.get('rotation_angle'))


class BackgroundFillFreeformGradient(BackgroundFill):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of 3 or 4 colors of the freeform gradients in the RGB24 format.
        self.colors: list[int] = get_object(kwargs.get('colors'))


class BackgroundTypeWallpaper(BackgroundType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the wallpaper must be downscaled to fit in 450x450 square and then box-blurred with radius 12.
        self.is_blurred: bool = get_object(kwargs.get('is_blurred'))
        # True, if the background needs to be slightly moved when device is tilted.
        self.is_moving: bool = get_object(kwargs.get('is_moving'))


class BackgroundTypePattern(BackgroundType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Fill of the background.
        self.fill: BackgroundFill = get_object(kwargs.get('fill'))
        # Intensity of the pattern when it is shown above the filled background; 0-100.
        self.intensity: int = get_object(kwargs.get('intensity'))
        # True, if the background fill must be applied only to the pattern itself. All other pixels are black in this case. For dark themes only.
        self.is_inverted: bool = get_object(kwargs.get('is_inverted'))
        # True, if the background needs to be slightly moved when device is tilted.
        self.is_moving: bool = get_object(kwargs.get('is_moving'))


class BackgroundTypeFill(BackgroundType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The background fill.
        self.fill: BackgroundFill = get_object(kwargs.get('fill'))


class Backgrounds(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of backgrounds.
        self.backgrounds: list[Background] = get_object(kwargs.get('backgrounds'))


class BankCardActionOpenUrl(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Action text.
        self.text: str = get_object(kwargs.get('text'))
        # The URL to be opened.
        self.url: str = get_object(kwargs.get('url'))


class BankCardInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title of the bank card description.
        self.title: str = get_object(kwargs.get('title'))
        # Actions that can be done with the bank card number.
        self.actions: list[BankCardActionOpenUrl] = get_object(kwargs.get('actions'))


class ChatMemberStatus(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BasicGroup(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Group identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Number of members in the group.
        self.member_count: int = get_object(kwargs.get('member_count'))
        # Status of the current user in the group.
        self.status: ChatMemberStatus = get_object(kwargs.get('status'))
        # True, if the group is active.
        self.is_active: bool = get_object(kwargs.get('is_active'))
        # Identifier of the supergroup to which this group was upgraded; 0 if none.
        self.upgraded_to_supergroup_id: int = get_object(kwargs.get('upgraded_to_supergroup_id'))


class BotCommands(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Bot's user identifier.
        self.bot_user_id: int = get_object(kwargs.get('bot_user_id'))
        # List of bot commands.
        self.commands: list[BotCommand] = get_object(kwargs.get('commands'))


class ChatInviteLink(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat invite link.
        self.invite_link: str = get_object(kwargs.get('invite_link'))
        # Name of the link.
        self.name: str = get_object(kwargs.get('name'))
        # User identifier of an administrator created the link.
        self.creator_user_id: int = get_object(kwargs.get('creator_user_id'))
        # Point in time (Unix timestamp) when the link was created.
        self.date: int = get_object(kwargs.get('date'))
        # Point in time (Unix timestamp) when the link was last edited; 0 if never or unknown.
        self.edit_date: int = get_object(kwargs.get('edit_date'))
        # Point in time (Unix timestamp) when the link will expire; 0 if never.
        self.expiration_date: int = get_object(kwargs.get('expiration_date'))
        # The maximum number of members, which can join the chat using the link simultaneously; 0 if not limited. Always 0 if the link requires approval.
        self.member_limit: int = get_object(kwargs.get('member_limit'))
        # Number of chat members, which joined the chat using the link.
        self.member_count: int = get_object(kwargs.get('member_count'))
        # Number of pending join requests created using this link.
        self.pending_join_request_count: int = get_object(kwargs.get('pending_join_request_count'))
        # True, if the link only creates join request. If true, total number of joining members will be unlimited.
        self.creates_join_request: bool = get_object(kwargs.get('creates_join_request'))
        # True, if the link is primary. Primary invite link can't have name, expiration date, or usage limit. There is exactly one primary invite link for each administrator with can_invite_users right at a given time.
        self.is_primary: bool = get_object(kwargs.get('is_primary'))
        # True, if the link was revoked.
        self.is_revoked: bool = get_object(kwargs.get('is_revoked'))


class ChatMember(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat member. Currently, other chats can be only Left or Banned. Only supergroups and channels can have other chats as Left or Banned members and these chats must be supergroups or channels.
        self.member_id: MessageSender = get_object(kwargs.get('member_id'))
        # Identifier of a user that invited/promoted/banned this member in the chat; 0 if unknown.
        self.inviter_user_id: int = get_object(kwargs.get('inviter_user_id'))
        # Point in time (Unix timestamp) when the user joined/was promoted/was banned in the chat.
        self.joined_chat_date: int = get_object(kwargs.get('joined_chat_date'))
        # Status of the member in the chat.
        self.status: ChatMemberStatus = get_object(kwargs.get('status'))


class ChatPhoto(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique photo identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Point in time (Unix timestamp) when the photo has been added.
        self.added_date: int = get_object(kwargs.get('added_date'))
        # Photo minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # Available variants of the photo in JPEG format, in different size.
        self.sizes: list[PhotoSize] = get_object(kwargs.get('sizes'))
        # A big (up to 1280x1280) animated variant of the photo in MPEG4 format; may be null.
        self.animation: AnimatedChatPhoto = get_object(kwargs.get('animation'))
        # A small (160x160) animated variant of the photo in MPEG4 format; may be null even the big animation is available.
        self.small_animation: AnimatedChatPhoto = get_object(kwargs.get('small_animation'))
        # Sticker-based version of the chat photo; may be null.
        self.sticker: ChatPhotoSticker = get_object(kwargs.get('sticker'))


class BasicGroupFullInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat photo; may be null if empty or unknown. If non-null, then it is the same photo as in chat.photo.
        self.photo: ChatPhoto = get_object(kwargs.get('photo'))
        # Group description. Updated only after the basic group is opened.
        self.description: str = get_object(kwargs.get('description'))
        # User identifier of the creator of the group; 0 if unknown.
        self.creator_user_id: int = get_object(kwargs.get('creator_user_id'))
        # Group members.
        self.members: list[ChatMember] = get_object(kwargs.get('members'))
        # True, if non-administrators and non-bots can be hidden in responses to getSupergroupMembers and searchChatMembers for non-administrators after upgrading the basic group to a supergroup.
        self.can_hide_members: bool = get_object(kwargs.get('can_hide_members'))
        # True, if aggressive anti-spam checks can be enabled or disabled in the supergroup after upgrading the basic group to a supergroup.
        self.can_toggle_aggressive_anti_spam: bool = get_object(kwargs.get('can_toggle_aggressive_anti_spam'))
        # Primary invite link for this group; may be null. For chat administrators with can_invite_users right only. Updated only after the basic group is opened.
        self.invite_link: ChatInviteLink = get_object(kwargs.get('invite_link'))
        # List of commands of bots in the group.
        self.bot_commands: list[BotCommands] = get_object(kwargs.get('bot_commands'))


class BlockList(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BlockListMain(BlockList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BlockListStories(BlockList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BotCommand(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the bot command.
        self.command: str = get_object(kwargs.get('command'))
        # Description of the bot command.
        self.description: str = get_object(kwargs.get('description'))


class BotCommandScope(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BotCommandScopeDefault(BotCommandScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BotCommandScopeAllPrivateChats(BotCommandScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BotCommandScopeAllGroupChats(BotCommandScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BotCommandScopeChat(BotCommandScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))


class BotCommandScopeChatAdministrators(BotCommandScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))


class BotCommandScopeChatMember(BotCommandScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))


class InternalLinkType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class BotMenuButton(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the button.
        self.text: str = get_object(kwargs.get('text'))
        # URL to be passed to openWebApp.
        self.url: str = get_object(kwargs.get('url'))


class ChatAdministratorRights(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the administrator can get chat event log, get chat statistics, get message statistics in channels, get channel members, see anonymous administrators in supergroups and ignore slow mode. Implied by any other privilege; applicable to supergroups and channels only.
        self.can_manage_chat: bool = get_object(kwargs.get('can_manage_chat'))
        # True, if the administrator can change the chat title, photo, and other settings.
        self.can_change_info: bool = get_object(kwargs.get('can_change_info'))
        # True, if the administrator can create channel posts; applicable to channels only.
        self.can_post_messages: bool = get_object(kwargs.get('can_post_messages'))
        # True, if the administrator can edit messages of other users and pin messages; applicable to channels only.
        self.can_edit_messages: bool = get_object(kwargs.get('can_edit_messages'))
        # True, if the administrator can delete messages of other users.
        self.can_delete_messages: bool = get_object(kwargs.get('can_delete_messages'))
        # True, if the administrator can invite new users to the chat.
        self.can_invite_users: bool = get_object(kwargs.get('can_invite_users'))
        # True, if the administrator can restrict, ban, or unban chat members; always true for channels.
        self.can_restrict_members: bool = get_object(kwargs.get('can_restrict_members'))
        # True, if the administrator can pin messages; applicable to basic groups and supergroups only.
        self.can_pin_messages: bool = get_object(kwargs.get('can_pin_messages'))
        # True, if the administrator can manage topics; applicable to forum supergroups only.
        self.can_manage_topics: bool = get_object(kwargs.get('can_manage_topics'))
        # True, if the administrator can add new administrators with a subset of their own privileges or demote administrators that were directly or indirectly promoted by them.
        self.can_promote_members: bool = get_object(kwargs.get('can_promote_members'))
        # True, if the administrator can manage video chats.
        self.can_manage_video_chats: bool = get_object(kwargs.get('can_manage_video_chats'))
        # True, if the administrator isn't shown in the chat member list and sends messages anonymously; applicable to supergroups only.
        self.is_anonymous: bool = get_object(kwargs.get('is_anonymous'))


class Photo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if stickers were added to the photo. The list of corresponding sticker sets can be received using getAttachedStickerSets.
        self.has_stickers: bool = get_object(kwargs.get('has_stickers'))
        # Photo minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # Available variants of the photo, in different sizes.
        self.sizes: list[PhotoSize] = get_object(kwargs.get('sizes'))


class BotInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The text that is shown on the bot's profile page and is sent together with the link when users share the bot.
        self.short_description: str = get_object(kwargs.get('short_description'))
        # The text shown in the chat with the bot if the chat is empty.
        self.description: str = get_object(kwargs.get('description'))
        # Photo shown in the chat with the bot if the chat is empty; may be null.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Animation shown in the chat with the bot if the chat is empty; may be null.
        self.animation: Animation = get_object(kwargs.get('animation'))
        # Information about a button to show instead of the bot commands menu button; may be null if ordinary bot commands menu must be shown.
        self.menu_button: BotMenuButton = get_object(kwargs.get('menu_button'))
        # List of the bot commands.
        self.commands: list[BotCommand] = get_object(kwargs.get('commands'))
        # Default administrator rights for adding the bot to basic group and supergroup chats; may be null.
        self.default_group_administrator_rights: ChatAdministratorRights = get_object(kwargs.get('default_group_administrator_rights'))
        # Default administrator rights for adding the bot to channels; may be null.
        self.default_channel_administrator_rights: ChatAdministratorRights = get_object(kwargs.get('default_channel_administrator_rights'))
        # The internal link, which can be used to edit bot commands; may be null.
        self.edit_commands_link: InternalLinkType = get_object(kwargs.get('edit_commands_link'))
        # The internal link, which can be used to edit bot description; may be null.
        self.edit_description_link: InternalLinkType = get_object(kwargs.get('edit_description_link'))
        # The internal link, which can be used to edit the photo or animation shown in the chat with the bot if the chat is empty; may be null.
        self.edit_description_media_link: InternalLinkType = get_object(kwargs.get('edit_description_media_link'))
        # The internal link, which can be used to edit bot settings; may be null.
        self.edit_settings_link: InternalLinkType = get_object(kwargs.get('edit_settings_link'))


class CallState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Call(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Call identifier, not persistent.
        self.id: int = get_object(kwargs.get('id'))
        # Peer user identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # True, if the call is outgoing.
        self.is_outgoing: bool = get_object(kwargs.get('is_outgoing'))
        # True, if the call is a video call.
        self.is_video: bool = get_object(kwargs.get('is_video'))
        # Call state.
        self.state: CallState = get_object(kwargs.get('state'))


class CallDiscardReason(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallDiscardReasonEmpty(CallDiscardReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallDiscardReasonMissed(CallDiscardReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallDiscardReasonDeclined(CallDiscardReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallDiscardReasonDisconnected(CallDiscardReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallDiscardReasonHungUp(CallDiscardReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallId(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Call identifier.
        self.id: int = get_object(kwargs.get('id'))


class CallProblem(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemEcho(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemNoise(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemInterruptions(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemDistortedSpeech(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemSilentLocal(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemSilentRemote(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemDropped(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemDistortedVideo(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProblemPixelatedVideo(CallProblem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallProtocol(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if UDP peer-to-peer connections are supported.
        self.udp_p2p: bool = get_object(kwargs.get('udp_p2p'))
        # True, if connection through UDP reflectors is supported.
        self.udp_reflector: bool = get_object(kwargs.get('udp_reflector'))
        # The minimum supported API layer; use 65.
        self.min_layer: int = get_object(kwargs.get('min_layer'))
        # The maximum supported API layer; use 92.
        self.max_layer: int = get_object(kwargs.get('max_layer'))
        # List of supported tgcalls versions.
        self.library_versions: list[str] = get_object(kwargs.get('library_versions'))


class CallServerType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallServer(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Server identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Server IPv4 address.
        self.ip_address: str = get_object(kwargs.get('ip_address'))
        # Server IPv6 address.
        self.ipv6_address: str = get_object(kwargs.get('ipv6_address'))
        # Server port number.
        self.port: int = get_object(kwargs.get('port'))
        # Server type.
        self.type: CallServerType = get_object(kwargs.get('type'))


class CallServerTypeTelegramReflector(CallServerType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A peer tag to be used with the reflector.
        self.peer_tag: bytes = get_object(kwargs.get('peer_tag'))
        # True, if the server uses TCP instead of UDP.
        self.is_tcp: bool = get_object(kwargs.get('is_tcp'))


class CallServerTypeWebrtc(CallServerType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username to be used for authentication.
        self.username: str = get_object(kwargs.get('username'))
        # Authentication password.
        self.password: str = get_object(kwargs.get('password'))
        # True, if the server supports TURN.
        self.supports_turn: bool = get_object(kwargs.get('supports_turn'))
        # True, if the server supports STUN.
        self.supports_stun: bool = get_object(kwargs.get('supports_stun'))


class Error(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Error code; subject to future changes. If the error code is 406, the error message must not be processed in any way and must not be displayed to the user.
        self.code: int = get_object(kwargs.get('code'))
        # Error message; subject to future changes.
        self.message: str = get_object(kwargs.get('message'))


class CallStatePending(CallState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the call has already been created by the server.
        self.is_created: bool = get_object(kwargs.get('is_created'))
        # True, if the call has already been received by the other party.
        self.is_received: bool = get_object(kwargs.get('is_received'))


class CallStateExchangingKeys(CallState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallStateReady(CallState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Call protocols supported by the peer.
        self.protocol: CallProtocol = get_object(kwargs.get('protocol'))
        # List of available call servers.
        self.servers: list[CallServer] = get_object(kwargs.get('servers'))
        # A JSON-encoded call config.
        self.config: str = get_object(kwargs.get('config'))
        # Call encryption key.
        self.encryption_key: bytes = get_object(kwargs.get('encryption_key'))
        # Encryption key emojis fingerprint.
        self.emojis: list[str] = get_object(kwargs.get('emojis'))
        # True, if peer-to-peer connection is allowed by users privacy settings.
        self.allow_p2p: bool = get_object(kwargs.get('allow_p2p'))


class CallStateHangingUp(CallState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallStateDiscarded(CallState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The reason, why the call has ended.
        self.reason: CallDiscardReason = get_object(kwargs.get('reason'))
        # True, if the call rating must be sent to the server.
        self.need_rating: bool = get_object(kwargs.get('need_rating'))
        # True, if the call debug information must be sent to the server.
        self.need_debug_information: bool = get_object(kwargs.get('need_debug_information'))
        # True, if the call log must be sent to the server.
        self.need_log: bool = get_object(kwargs.get('need_log'))


class CallStateError(CallState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Error. An error with the code 4005000 will be returned if an outgoing call is missed because of an expired timeout.
        self.error: Error = get_object(kwargs.get('error'))


class CallbackQueryAnswer(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the answer.
        self.text: str = get_object(kwargs.get('text'))
        # True, if an alert must be shown to the user instead of a toast notification.
        self.show_alert: bool = get_object(kwargs.get('show_alert'))
        # URL to be opened.
        self.url: str = get_object(kwargs.get('url'))


class CallbackQueryPayload(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CallbackQueryPayloadData(CallbackQueryPayload):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Data that was attached to the callback button.
        self.data: bytes = get_object(kwargs.get('data'))


class CallbackQueryPayloadDataWithPassword(CallbackQueryPayload):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The 2-step verification password for the current user.
        self.password: str = get_object(kwargs.get('password'))
        # Data that was attached to the callback button.
        self.data: bytes = get_object(kwargs.get('data'))


class CallbackQueryPayloadGame(CallbackQueryPayload):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A short name of the game that was attached to the callback button.
        self.game_short_name: str = get_object(kwargs.get('game_short_name'))


class CanSendStoryResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CanSendStoryResultOk(CanSendStoryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CanSendStoryResultPremiumNeeded(CanSendStoryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CanSendStoryResultActiveStoryLimitExceeded(CanSendStoryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CanSendStoryResultWeeklyLimitExceeded(CanSendStoryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Time left before the user can send the next story.
        self.retry_after: int = get_object(kwargs.get('retry_after'))


class CanSendStoryResultMonthlyLimitExceeded(CanSendStoryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Time left before the user can send the next story.
        self.retry_after: int = get_object(kwargs.get('retry_after'))


class CanTransferOwnershipResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CanTransferOwnershipResultOk(CanTransferOwnershipResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CanTransferOwnershipResultPasswordNeeded(CanTransferOwnershipResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CanTransferOwnershipResultPasswordTooFresh(CanTransferOwnershipResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Time left before the session can be used to transfer ownership of a chat, in seconds.
        self.retry_after: int = get_object(kwargs.get('retry_after'))


class CanTransferOwnershipResultSessionTooFresh(CanTransferOwnershipResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Time left before the session can be used to transfer ownership of a chat, in seconds.
        self.retry_after: int = get_object(kwargs.get('retry_after'))


class ChatActionBar(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatAvailableReactions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatBackground(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The background.
        self.background: Background = get_object(kwargs.get('background'))
        # Dimming of the background in dark themes, as a percentage; 0-100.
        self.dark_theme_dimming: int = get_object(kwargs.get('dark_theme_dimming'))


class ChatJoinRequestsInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total number of pending join requests.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # Identifiers of at most 3 users sent the newest pending join requests.
        self.user_ids: list[int] = get_object(kwargs.get('user_ids'))


class ChatNotificationSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # If true, mute_for is ignored and the value for the relevant type of chat or the forum chat is used instead.
        self.use_default_mute_for: bool = get_object(kwargs.get('use_default_mute_for'))
        # Time left before notifications will be unmuted, in seconds.
        self.mute_for: int = get_object(kwargs.get('mute_for'))
        # If true, the value for the relevant type of chat or the forum chat is used instead of sound_id.
        self.use_default_sound: bool = get_object(kwargs.get('use_default_sound'))
        # Identifier of the notification sound to be played for messages; 0 if sound is disabled.
        self.sound_id: int = get_object(kwargs.get('sound_id'))
        # If true, show_preview is ignored and the value for the relevant type of chat or the forum chat is used instead.
        self.use_default_show_preview: bool = get_object(kwargs.get('use_default_show_preview'))
        # True, if message content must be displayed in notifications.
        self.show_preview: bool = get_object(kwargs.get('show_preview'))
        # If true, mute_stories is ignored and the value for the relevant type of chat is used instead.
        self.use_default_mute_stories: bool = get_object(kwargs.get('use_default_mute_stories'))
        # True, if story notifications are disabled for the chat.
        self.mute_stories: bool = get_object(kwargs.get('mute_stories'))
        # If true, the value for the relevant type of chat is used instead of story_sound_id.
        self.use_default_story_sound: bool = get_object(kwargs.get('use_default_story_sound'))
        # Identifier of the notification sound to be played for stories; 0 if sound is disabled.
        self.story_sound_id: int = get_object(kwargs.get('story_sound_id'))
        # If true, show_story_sender is ignored and the value for the relevant type of chat is used instead.
        self.use_default_show_story_sender: bool = get_object(kwargs.get('use_default_show_story_sender'))
        # True, if the sender of stories must be displayed in notifications.
        self.show_story_sender: bool = get_object(kwargs.get('show_story_sender'))
        # If true, disable_pinned_message_notifications is ignored and the value for the relevant type of chat or the forum chat is used instead.
        self.use_default_disable_pinned_message_notifications: bool = get_object(kwargs.get('use_default_disable_pinned_message_notifications'))
        # If true, notifications for incoming pinned messages will be created as for an ordinary unread message.
        self.disable_pinned_message_notifications: bool = get_object(kwargs.get('disable_pinned_message_notifications'))
        # If true, disable_mention_notifications is ignored and the value for the relevant type of chat or the forum chat is used instead.
        self.use_default_disable_mention_notifications: bool = get_object(kwargs.get('use_default_disable_mention_notifications'))
        # If true, notifications for messages with mentions will be created as for an ordinary unread message.
        self.disable_mention_notifications: bool = get_object(kwargs.get('disable_mention_notifications'))


class ChatPermissions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the user can send text messages, contacts, invoices, locations, and venues.
        self.can_send_messages: bool = get_object(kwargs.get('can_send_messages'))
        # True, if the user can send music files.
        self.can_send_media_messages: bool = get_object(kwargs.get('can_send_media_messages'))
        # True, if the user can send polls.
        self.can_send_polls: bool = get_object(kwargs.get('can_send_polls'))
        # True, if the user can send animations, games, stickers, and dice and use inline bots.
        self.can_send_other_messages: bool = get_object(kwargs.get('can_send_other_messages'))
        # True, if the user may add a web page preview to their messages.
        self.can_add_web_page_previews: bool = get_object(kwargs.get('can_add_web_page_previews'))
        # True, if the user can change the chat title, photo, and other settings.
        self.can_change_info: bool = get_object(kwargs.get('can_change_info'))
        # True, if the user can invite new users to the chat.
        self.can_invite_users: bool = get_object(kwargs.get('can_invite_users'))
        # True, if the user can pin messages.
        self.can_pin_messages: bool = get_object(kwargs.get('can_pin_messages'))


class ChatPhotoInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A small (160x160) chat photo variant in JPEG format. The file can be downloaded only before the photo is changed.
        self.small: File = get_object(kwargs.get('small'))
        # A big (640x640) chat photo variant in JPEG format. The file can be downloaded only before the photo is changed.
        self.big: File = get_object(kwargs.get('big'))
        # Chat photo minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # True, if the photo has animated variant.
        self.has_animation: bool = get_object(kwargs.get('has_animation'))
        # True, if the photo is visible only for the current user.
        self.is_personal: bool = get_object(kwargs.get('is_personal'))


class ChatPosition(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat list.
        self.list: ChatList = get_object(kwargs.get('list'))
        # A parameter used to determine order of the chat in the chat list. Chats must be sorted by the pair (order, chat.id) in descending order.
        self.order: int = get_object(kwargs.get('order'))
        # True, if the chat is pinned in the chat list.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))
        # Source of the chat in the chat list; may be null.
        self.source: ChatSource = get_object(kwargs.get('source'))


class DraftMessage(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the replied message; 0 if none.
        self.reply_to_message_id: int = get_object(kwargs.get('reply_to_message_id'))
        # Point in time (Unix timestamp) when the draft was created.
        self.date: int = get_object(kwargs.get('date'))
        # Content of the message draft; must be of the type inputMessageText.
        self.input_message_text: InputMessageContent = get_object(kwargs.get('input_message_text'))


class Message(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message identifier; unique for the chat to which the message belongs.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the sender of the message.
        self.sender_id: MessageSender = get_object(kwargs.get('sender_id'))
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The sending state of the message; may be null if the message isn't being sent and didn't fail to be sent.
        self.sending_state: MessageSendingState = get_object(kwargs.get('sending_state'))
        # The scheduling state of the message; may be null if the message isn't scheduled.
        self.scheduling_state: MessageSchedulingState = get_object(kwargs.get('scheduling_state'))
        # True, if the message is outgoing.
        self.is_outgoing: bool = get_object(kwargs.get('is_outgoing'))
        # True, if the message is pinned.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))
        # True, if the message can be edited. For live location and poll messages this fields shows whether editMessageLiveLocation or stopPoll can be used with this message by the application.
        self.can_be_edited: bool = get_object(kwargs.get('can_be_edited'))
        # True, if the message can be forwarded.
        self.can_be_forwarded: bool = get_object(kwargs.get('can_be_forwarded'))
        # True, if content of the message can be saved locally or copied.
        self.can_be_saved: bool = get_object(kwargs.get('can_be_saved'))
        # True, if the message can be deleted only for the current user while other users will continue to see it.
        self.can_be_deleted_only_for_self: bool = get_object(kwargs.get('can_be_deleted_only_for_self'))
        # True, if the message can be deleted for all users.
        self.can_be_deleted_for_all_users: bool = get_object(kwargs.get('can_be_deleted_for_all_users'))
        # True, if the list of added reactions is available through getMessageAddedReactions.
        self.can_get_added_reactions: bool = get_object(kwargs.get('can_get_added_reactions'))
        # True, if the message statistics are available through getMessageStatistics.
        self.can_get_statistics: bool = get_object(kwargs.get('can_get_statistics'))
        # True, if information about the message thread is available through getMessageThread and getMessageThreadHistory.
        self.can_get_message_thread: bool = get_object(kwargs.get('can_get_message_thread'))
        # True, if chat members already viewed the message can be received through getMessageViewers.
        self.can_get_viewers: bool = get_object(kwargs.get('can_get_viewers'))
        # True, if media timestamp links can be generated for media timestamp entities in the message text, caption or web page description through getMessageLink.
        self.can_get_media_timestamp_links: bool = get_object(kwargs.get('can_get_media_timestamp_links'))
        # True, if reactions on the message can be reported through reportMessageReactions.
        self.can_report_reactions: bool = get_object(kwargs.get('can_report_reactions'))
        # True, if media timestamp entities refers to a media in this message as opposed to a media in the replied message.
        self.has_timestamped_media: bool = get_object(kwargs.get('has_timestamped_media'))
        # True, if the message is a channel post. All messages to channels are channel posts, all other messages are not channel posts.
        self.is_channel_post: bool = get_object(kwargs.get('is_channel_post'))
        # True, if the message is a forum topic message.
        self.is_topic_message: bool = get_object(kwargs.get('is_topic_message'))
        # True, if the message contains an unread mention for the current user.
        self.contains_unread_mention: bool = get_object(kwargs.get('contains_unread_mention'))
        # Point in time (Unix timestamp) when the message was sent.
        self.date: int = get_object(kwargs.get('date'))
        # Point in time (Unix timestamp) when the message was last edited.
        self.edit_date: int = get_object(kwargs.get('edit_date'))
        # Information about the initial message sender; may be null if none or unknown.
        self.forward_info: MessageForwardInfo = get_object(kwargs.get('forward_info'))
        # Information about interactions with the message; may be null if none.
        self.interaction_info: MessageInteractionInfo = get_object(kwargs.get('interaction_info'))
        # Information about unread reactions added to the message.
        self.unread_reactions: list[UnreadReaction] = get_object(kwargs.get('unread_reactions'))
        # Information about the message or the story this message is replying to; may be null if none.
        self.reply_to: MessageReplyTo = get_object(kwargs.get('reply_to'))
        # If non-zero, the identifier of the message thread the message belongs to; unique within the chat to which the message belongs.
        self.message_thread_id: int = get_object(kwargs.get('message_thread_id'))
        # The message's self-destruct type; may be null if none.
        self.self_destruct_type: MessageSelfDestructType = get_object(kwargs.get('self_destruct_type'))
        # Time left before the message self-destruct timer expires, in seconds; 0 if self-desctruction isn't scheduled yet.
        self.self_destruct_in: float = get_object(kwargs.get('self_destruct_in'))
        # Time left before the message will be automatically deleted by message_auto_delete_time setting of the chat, in seconds; 0 if never.
        self.auto_delete_in: float = get_object(kwargs.get('auto_delete_in'))
        # If non-zero, the user identifier of the bot through which this message was sent.
        self.via_bot_user_id: int = get_object(kwargs.get('via_bot_user_id'))
        # For channel posts and anonymous group messages, optional author signature.
        self.author_signature: str = get_object(kwargs.get('author_signature'))
        # Unique identifier of an album this message belongs to. Only audios, documents, photos and videos can be grouped together in albums.
        self.media_album_id: int = get_object(kwargs.get('media_album_id'))
        # If non-empty, contains a human-readable description of the reason why access to this message must be restricted.
        self.restriction_reason: str = get_object(kwargs.get('restriction_reason'))
        # Content of the message.
        self.content: MessageContent = get_object(kwargs.get('content'))
        # Reply markup for the message; may be null if none.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))


class VideoChat(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Group call identifier of an active video chat; 0 if none. Full information about the video chat can be received through the method getGroupCall.
        self.group_call_id: int = get_object(kwargs.get('group_call_id'))
        # True, if the video chat has participants.
        self.has_participants: bool = get_object(kwargs.get('has_participants'))
        # Default group call participant identifier to join the video chat; may be null.
        self.default_participant_id: MessageSender = get_object(kwargs.get('default_participant_id'))


class Chat(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat unique identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Type of the chat.
        self.type: ChatType = get_object(kwargs.get('type'))
        # Chat title.
        self.title: str = get_object(kwargs.get('title'))
        # Chat photo; may be null.
        self.photo: ChatPhotoInfo = get_object(kwargs.get('photo'))
        # Actions that non-administrator chat members are allowed to take in the chat.
        self.permissions: ChatPermissions = get_object(kwargs.get('permissions'))
        # Last message in the chat; may be null if none or unknown.
        self.last_message: Message = get_object(kwargs.get('last_message'))
        # Positions of the chat in chat lists.
        self.positions: list[ChatPosition] = get_object(kwargs.get('positions'))
        # Identifier of a user or chat that is selected to send messages in the chat; may be null if the user can't change message sender.
        self.message_sender_id: MessageSender = get_object(kwargs.get('message_sender_id'))
        # Block list to which the chat is added; may be null if none.
        self.block_list: BlockList = get_object(kwargs.get('block_list'))
        # True, if chat content can't be saved locally, forwarded, or copied.
        self.has_protected_content: bool = get_object(kwargs.get('has_protected_content'))
        # True, if translation of all messages in the chat must be suggested to the user.
        self.is_translatable: bool = get_object(kwargs.get('is_translatable'))
        # True, if the chat is marked as unread.
        self.is_marked_as_unread: bool = get_object(kwargs.get('is_marked_as_unread'))
        # True, if the chat has scheduled messages.
        self.has_scheduled_messages: bool = get_object(kwargs.get('has_scheduled_messages'))
        # True, if the chat messages can be deleted only for the current user while other users will continue to see the messages.
        self.can_be_deleted_only_for_self: bool = get_object(kwargs.get('can_be_deleted_only_for_self'))
        # True, if the chat messages can be deleted for all users.
        self.can_be_deleted_for_all_users: bool = get_object(kwargs.get('can_be_deleted_for_all_users'))
        # True, if the chat can be reported to Telegram moderators through reportChat or reportChatPhoto.
        self.can_be_reported: bool = get_object(kwargs.get('can_be_reported'))
        # Default value of the disable_notification parameter, used when a message is sent to the chat.
        self.default_disable_notification: bool = get_object(kwargs.get('default_disable_notification'))
        # Number of unread messages in the chat.
        self.unread_count: int = get_object(kwargs.get('unread_count'))
        # Identifier of the last read incoming message.
        self.last_read_inbox_message_id: int = get_object(kwargs.get('last_read_inbox_message_id'))
        # Identifier of the last read outgoing message.
        self.last_read_outbox_message_id: int = get_object(kwargs.get('last_read_outbox_message_id'))
        # Number of unread messages with a mention/reply in the chat.
        self.unread_mention_count: int = get_object(kwargs.get('unread_mention_count'))
        # Number of messages with unread reactions in the chat.
        self.unread_reaction_count: int = get_object(kwargs.get('unread_reaction_count'))
        # Notification settings for the chat.
        self.notification_settings: ChatNotificationSettings = get_object(kwargs.get('notification_settings'))
        # Types of reaction, available in the chat.
        self.available_reactions: ChatAvailableReactions = get_object(kwargs.get('available_reactions'))
        # Current message auto-delete or self-destruct timer setting for the chat, in seconds; 0 if disabled. Self-destruct timer in secret chats starts after the message or its content is viewed. Auto-delete timer in other chats starts from the send date.
        self.message_auto_delete_time: int = get_object(kwargs.get('message_auto_delete_time'))
        # Background set for the chat; may be null if none.
        self.background: ChatBackground = get_object(kwargs.get('background'))
        # If non-empty, name of a theme, set for the chat.
        self.theme_name: str = get_object(kwargs.get('theme_name'))
        # Information about actions which must be possible to do through the chat action bar; may be null if none.
        self.action_bar: ChatActionBar = get_object(kwargs.get('action_bar'))
        # Information about video chat of the chat.
        self.video_chat: VideoChat = get_object(kwargs.get('video_chat'))
        # Information about pending join requests; may be null if none.
        self.pending_join_requests: ChatJoinRequestsInfo = get_object(kwargs.get('pending_join_requests'))
        # Identifier of the message from which reply markup needs to be used; 0 if there is no default custom reply markup in the chat.
        self.reply_markup_message_id: int = get_object(kwargs.get('reply_markup_message_id'))
        # A draft of a message in the chat; may be null if none.
        self.draft_message: DraftMessage = get_object(kwargs.get('draft_message'))
        # Application-specific data associated with the chat. (For example, the chat scroll position or local chat notification settings can be stored here.) Persistent if the message database is used.
        self.client_data: str = get_object(kwargs.get('client_data'))


class ChatAction(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionTyping(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionRecordingVideo(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionUploadingVideo(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Upload progress, as a percentage.
        self.progress: int = get_object(kwargs.get('progress'))


class ChatActionRecordingVoiceNote(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionUploadingVoiceNote(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Upload progress, as a percentage.
        self.progress: int = get_object(kwargs.get('progress'))


class ChatActionUploadingPhoto(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Upload progress, as a percentage.
        self.progress: int = get_object(kwargs.get('progress'))


class ChatActionUploadingDocument(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Upload progress, as a percentage.
        self.progress: int = get_object(kwargs.get('progress'))


class ChatActionChoosingSticker(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionChoosingLocation(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionChoosingContact(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionStartPlayingGame(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionRecordingVideoNote(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionUploadingVideoNote(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Upload progress, as a percentage.
        self.progress: int = get_object(kwargs.get('progress'))


class ChatActionWatchingAnimations(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The animated emoji.
        self.emoji: str = get_object(kwargs.get('emoji'))


class ChatActionCancel(ChatAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionBarReportSpam(ChatActionBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # If true, the chat was automatically archived and can be moved back to the main chat list using addChatToList simultaneously with setting chat notification settings to default using setChatNotificationSettings.
        self.can_unarchive: bool = get_object(kwargs.get('can_unarchive'))


class ChatActionBarReportUnrelatedLocation(ChatActionBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionBarInviteMembers(ChatActionBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionBarReportAddBlock(ChatActionBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # If true, the chat was automatically archived and can be moved back to the main chat list using addChatToList simultaneously with setting chat notification settings to default using setChatNotificationSettings.
        self.can_unarchive: bool = get_object(kwargs.get('can_unarchive'))
        # If non-negative, the current user was found by the peer through searchChatsNearby and this is the distance between the users.
        self.distance: int = get_object(kwargs.get('distance'))


class ChatActionBarAddContact(ChatActionBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionBarSharePhoneNumber(ChatActionBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatActionBarJoinRequest(ChatActionBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title of the chat to which the join request was sent.
        self.title: str = get_object(kwargs.get('title'))
        # True, if the join request was sent to a channel chat.
        self.is_channel: bool = get_object(kwargs.get('is_channel'))
        # Point in time (Unix timestamp) when the join request was sent.
        self.request_date: int = get_object(kwargs.get('request_date'))


class StoryList(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique story identifier among stories of the given sender.
        self.story_id: int = get_object(kwargs.get('story_id'))
        # Point in time (Unix timestamp) when the story was published.
        self.date: int = get_object(kwargs.get('date'))
        # True, if the story is available only to close friends.
        self.is_for_close_friends: bool = get_object(kwargs.get('is_for_close_friends'))


class ChatActiveStories(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat that posted the stories.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifier of the story list in which the stories are shown; may be null if the stories aren't shown in a story list.
        self.list: StoryList = get_object(kwargs.get('list'))
        # A parameter used to determine order of the stories in the story list; 0 if the stories doesn't need to be shown in the story list. Stories must be sorted by the pair (order, story_sender_chat_id) in descending order.
        self.order: int = get_object(kwargs.get('order'))
        # Identifier of the last read active story.
        self.max_read_story_id: int = get_object(kwargs.get('max_read_story_id'))
        # Basic information about the stories; use getStory to get full information about the stories. The stories are in a chronological order (i.e., in order of increasing story identifiers).
        self.stories: list[StoryInfo] = get_object(kwargs.get('stories'))


class ChatAdministrator(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the administrator.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Custom title of the administrator.
        self.custom_title: str = get_object(kwargs.get('custom_title'))
        # True, if the user is the owner of the chat.
        self.is_owner: bool = get_object(kwargs.get('is_owner'))


class ChatAdministrators(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of chat administrators.
        self.administrators: list[ChatAdministrator] = get_object(kwargs.get('administrators'))


class ChatAvailableReactionsAll(ChatAvailableReactions):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatAvailableReactionsSome(ChatAvailableReactions):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The list of reactions.
        self.reactions: list[ReactionType] = get_object(kwargs.get('reactions'))


class ChatEventAction(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatEvent(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat event identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Point in time (Unix timestamp) when the event happened.
        self.date: int = get_object(kwargs.get('date'))
        # Identifier of the user or chat who performed the action.
        self.member_id: MessageSender = get_object(kwargs.get('member_id'))
        # The action.
        self.action: ChatEventAction = get_object(kwargs.get('action'))


class ChatLocation(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The location.
        self.location: Location = get_object(kwargs.get('location'))
        # Location address; 1-64 characters, as defined by the chat owner.
        self.address: str = get_object(kwargs.get('address'))


class ForumTopicInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message thread identifier of the topic.
        self.message_thread_id: int = get_object(kwargs.get('message_thread_id'))
        # Name of the topic.
        self.name: str = get_object(kwargs.get('name'))
        # Icon of the topic.
        self.icon: ForumTopicIcon = get_object(kwargs.get('icon'))
        # Point in time (Unix timestamp) when the topic was created.
        self.creation_date: int = get_object(kwargs.get('creation_date'))
        # Identifier of the creator of the topic.
        self.creator_id: MessageSender = get_object(kwargs.get('creator_id'))
        # True, if the topic is the General topic list.
        self.is_general: bool = get_object(kwargs.get('is_general'))
        # True, if the topic was created by the current user.
        self.is_outgoing: bool = get_object(kwargs.get('is_outgoing'))
        # True, if the topic is closed.
        self.is_closed: bool = get_object(kwargs.get('is_closed'))
        # True, if the topic is hidden above the topic list and closed; for General topic only.
        self.is_hidden: bool = get_object(kwargs.get('is_hidden'))


class ChatEventMessageEdited(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The original message before the edit.
        self.old_message: Message = get_object(kwargs.get('old_message'))
        # The message after it was edited.
        self.new_message: Message = get_object(kwargs.get('new_message'))


class ChatEventMessageDeleted(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Deleted message.
        self.message: Message = get_object(kwargs.get('message'))
        # True, if the message deletion can be reported via reportSupergroupAntiSpamFalsePositive.
        self.can_report_anti_spam_false_positive: bool = get_object(kwargs.get('can_report_anti_spam_false_positive'))


class ChatEventMessagePinned(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Pinned message.
        self.message: Message = get_object(kwargs.get('message'))


class ChatEventMessageUnpinned(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unpinned message.
        self.message: Message = get_object(kwargs.get('message'))


class ChatEventPollStopped(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The message with the poll.
        self.message: Message = get_object(kwargs.get('message'))


class ChatEventMemberJoined(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatEventMemberJoinedByInviteLink(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Invite link used to join the chat.
        self.invite_link: ChatInviteLink = get_object(kwargs.get('invite_link'))
        # True, if the user has joined the chat using an invite link for a chat filter.
        self.via_chat_filter_invite_link: bool = get_object(kwargs.get('via_chat_filter_invite_link'))


class ChatEventMemberJoinedByRequest(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the chat administrator, approved user join request.
        self.approver_user_id: int = get_object(kwargs.get('approver_user_id'))
        # Invite link used to join the chat; may be null.
        self.invite_link: ChatInviteLink = get_object(kwargs.get('invite_link'))


class ChatEventMemberInvited(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New member user identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # New member status.
        self.status: ChatMemberStatus = get_object(kwargs.get('status'))


class ChatEventMemberLeft(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatEventMemberPromoted(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Affected chat member user identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Previous status of the chat member.
        self.old_status: ChatMemberStatus = get_object(kwargs.get('old_status'))
        # New status of the chat member.
        self.new_status: ChatMemberStatus = get_object(kwargs.get('new_status'))


class ChatEventMemberRestricted(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Affected chat member identifier.
        self.member_id: MessageSender = get_object(kwargs.get('member_id'))
        # Previous status of the chat member.
        self.old_status: ChatMemberStatus = get_object(kwargs.get('old_status'))
        # New status of the chat member.
        self.new_status: ChatMemberStatus = get_object(kwargs.get('new_status'))


class ChatEventAvailableReactionsChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous chat available reactions.
        self.old_available_reactions: ChatAvailableReactions = get_object(kwargs.get('old_available_reactions'))
        # New chat available reactions.
        self.new_available_reactions: ChatAvailableReactions = get_object(kwargs.get('new_available_reactions'))


class ChatEventDescriptionChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous chat description.
        self.old_description: str = get_object(kwargs.get('old_description'))
        # New chat description.
        self.new_description: str = get_object(kwargs.get('new_description'))


class ChatEventLinkedChatChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous supergroup linked chat identifier.
        self.old_linked_chat_id: int = get_object(kwargs.get('old_linked_chat_id'))
        # New supergroup linked chat identifier.
        self.new_linked_chat_id: int = get_object(kwargs.get('new_linked_chat_id'))


class ChatEventLocationChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous location; may be null.
        self.old_location: ChatLocation = get_object(kwargs.get('old_location'))
        # New location; may be null.
        self.new_location: ChatLocation = get_object(kwargs.get('new_location'))


class ChatEventMessageAutoDeleteTimeChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous value of message_auto_delete_time.
        self.old_message_auto_delete_time: int = get_object(kwargs.get('old_message_auto_delete_time'))
        # New value of message_auto_delete_time.
        self.new_message_auto_delete_time: int = get_object(kwargs.get('new_message_auto_delete_time'))


class ChatEventPermissionsChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous chat permissions.
        self.old_permissions: ChatPermissions = get_object(kwargs.get('old_permissions'))
        # New chat permissions.
        self.new_permissions: ChatPermissions = get_object(kwargs.get('new_permissions'))


class ChatEventPhotoChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous chat photo value; may be null.
        self.old_photo: ChatPhoto = get_object(kwargs.get('old_photo'))
        # New chat photo value; may be null.
        self.new_photo: ChatPhoto = get_object(kwargs.get('new_photo'))


class ChatEventSlowModeDelayChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous value of slow_mode_delay, in seconds.
        self.old_slow_mode_delay: int = get_object(kwargs.get('old_slow_mode_delay'))
        # New value of slow_mode_delay, in seconds.
        self.new_slow_mode_delay: int = get_object(kwargs.get('new_slow_mode_delay'))


class ChatEventStickerSetChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous identifier of the chat sticker set; 0 if none.
        self.old_sticker_set_id: int = get_object(kwargs.get('old_sticker_set_id'))
        # New identifier of the chat sticker set; 0 if none.
        self.new_sticker_set_id: int = get_object(kwargs.get('new_sticker_set_id'))


class ChatEventTitleChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous chat title.
        self.old_title: str = get_object(kwargs.get('old_title'))
        # New chat title.
        self.new_title: str = get_object(kwargs.get('new_title'))


class ChatEventUsernameChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous chat username.
        self.old_username: str = get_object(kwargs.get('old_username'))
        # New chat username.
        self.new_username: str = get_object(kwargs.get('new_username'))


class ChatEventActiveUsernamesChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous list of active usernames.
        self.old_usernames: list[str] = get_object(kwargs.get('old_usernames'))
        # New list of active usernames.
        self.new_usernames: list[str] = get_object(kwargs.get('new_usernames'))


class ChatEventHasProtectedContentToggled(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New value of has_protected_content.
        self.has_protected_content: bool = get_object(kwargs.get('has_protected_content'))


class ChatEventInvitesToggled(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New value of can_invite_users permission.
        self.can_invite_users: bool = get_object(kwargs.get('can_invite_users'))


class ChatEventIsAllHistoryAvailableToggled(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New value of is_all_history_available.
        self.is_all_history_available: bool = get_object(kwargs.get('is_all_history_available'))


class ChatEventHasAggressiveAntiSpamEnabledToggled(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New value of has_aggressive_anti_spam_enabled.
        self.has_aggressive_anti_spam_enabled: bool = get_object(kwargs.get('has_aggressive_anti_spam_enabled'))


class ChatEventSignMessagesToggled(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New value of sign_messages.
        self.sign_messages: bool = get_object(kwargs.get('sign_messages'))


class ChatEventInviteLinkEdited(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Previous information about the invite link.
        self.old_invite_link: ChatInviteLink = get_object(kwargs.get('old_invite_link'))
        # New information about the invite link.
        self.new_invite_link: ChatInviteLink = get_object(kwargs.get('new_invite_link'))


class ChatEventInviteLinkRevoked(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The invite link.
        self.invite_link: ChatInviteLink = get_object(kwargs.get('invite_link'))


class ChatEventInviteLinkDeleted(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The invite link.
        self.invite_link: ChatInviteLink = get_object(kwargs.get('invite_link'))


class ChatEventVideoChatCreated(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the video chat. The video chat can be received through the method getGroupCall.
        self.group_call_id: int = get_object(kwargs.get('group_call_id'))


class ChatEventVideoChatEnded(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the video chat. The video chat can be received through the method getGroupCall.
        self.group_call_id: int = get_object(kwargs.get('group_call_id'))


class ChatEventVideoChatMuteNewParticipantsToggled(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New value of the mute_new_participants setting.
        self.mute_new_participants: bool = get_object(kwargs.get('mute_new_participants'))


class ChatEventVideoChatParticipantIsMutedToggled(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the affected group call participant.
        self.participant_id: MessageSender = get_object(kwargs.get('participant_id'))
        # New value of is_muted.
        self.is_muted: bool = get_object(kwargs.get('is_muted'))


class ChatEventVideoChatParticipantVolumeLevelChanged(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the affected group call participant.
        self.participant_id: MessageSender = get_object(kwargs.get('participant_id'))
        # New value of volume_level; 1-20000 in hundreds of percents.
        self.volume_level: int = get_object(kwargs.get('volume_level'))


class ChatEventIsForumToggled(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New value of is_forum.
        self.is_forum: bool = get_object(kwargs.get('is_forum'))


class ChatEventForumTopicCreated(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the topic.
        self.topic_info: ForumTopicInfo = get_object(kwargs.get('topic_info'))


class ChatEventForumTopicEdited(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Old information about the topic.
        self.old_topic_info: ForumTopicInfo = get_object(kwargs.get('old_topic_info'))
        # New information about the topic.
        self.new_topic_info: ForumTopicInfo = get_object(kwargs.get('new_topic_info'))


class ChatEventForumTopicToggleIsClosed(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New information about the topic.
        self.topic_info: ForumTopicInfo = get_object(kwargs.get('topic_info'))


class ChatEventForumTopicToggleIsHidden(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New information about the topic.
        self.topic_info: ForumTopicInfo = get_object(kwargs.get('topic_info'))


class ChatEventForumTopicDeleted(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the topic.
        self.topic_info: ForumTopicInfo = get_object(kwargs.get('topic_info'))


class ChatEventForumTopicPinned(ChatEventAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the old pinned topic; may be null.
        self.old_topic_info: ForumTopicInfo = get_object(kwargs.get('old_topic_info'))
        # Information about the new pinned topic; may be null.
        self.new_topic_info: ForumTopicInfo = get_object(kwargs.get('new_topic_info'))


class ChatEventLogFilters(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if message edits need to be returned.
        self.message_edits: bool = get_object(kwargs.get('message_edits'))
        # True, if message deletions need to be returned.
        self.message_deletions: bool = get_object(kwargs.get('message_deletions'))
        # True, if pin/unpin events need to be returned.
        self.message_pins: bool = get_object(kwargs.get('message_pins'))
        # True, if members joining events need to be returned.
        self.member_joins: bool = get_object(kwargs.get('member_joins'))
        # True, if members leaving events need to be returned.
        self.member_leaves: bool = get_object(kwargs.get('member_leaves'))
        # True, if invited member events need to be returned.
        self.member_invites: bool = get_object(kwargs.get('member_invites'))
        # True, if member promotion/demotion events need to be returned.
        self.member_promotions: bool = get_object(kwargs.get('member_promotions'))
        # True, if member restricted/unrestricted/banned/unbanned events need to be returned.
        self.member_restrictions: bool = get_object(kwargs.get('member_restrictions'))
        # True, if changes in chat information need to be returned.
        self.info_changes: bool = get_object(kwargs.get('info_changes'))
        # True, if changes in chat settings need to be returned.
        self.setting_changes: bool = get_object(kwargs.get('setting_changes'))
        # True, if changes to invite links need to be returned.
        self.invite_link_changes: bool = get_object(kwargs.get('invite_link_changes'))
        # True, if video chat actions need to be returned.
        self.video_chat_changes: bool = get_object(kwargs.get('video_chat_changes'))
        # True, if forum-related actions need to be returned.
        self.forum_changes: bool = get_object(kwargs.get('forum_changes'))


class ChatEvents(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of events.
        self.events: list[ChatEvent] = get_object(kwargs.get('events'))


class ChatFilterIcon(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chosen icon name for short filter representation; one of &quot;All&quot;, &quot;Unread&quot;, &quot;Unmuted&quot;, &quot;Bots&quot;, &quot;Channels&quot;, &quot;Groups&quot;, &quot;Private&quot;, &quot;Custom&quot;, &quot;Setup&quot;, &quot;Cat&quot;, &quot;Crown&quot;, &quot;Favorite&quot;, &quot;Flower&quot;, &quot;Game&quot;, &quot;Home&quot;, &quot;Love&quot;, &quot;Mask&quot;, &quot;Party&quot;, &quot;Sport&quot;, &quot;Study&quot;, &quot;Trade&quot;, &quot;Travel&quot;, &quot;Work&quot;, &quot;Airplane&quot;, &quot;Book&quot;, &quot;Light&quot;, &quot;Like&quot;, &quot;Money&quot;, &quot;Note&quot;, &quot;Palette&quot;.
        self.name: str = get_object(kwargs.get('name'))


class ChatFilter(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The title of the filter; 1-12 characters without line feeds.
        self.title: str = get_object(kwargs.get('title'))
        # The chosen icon for the chat filter; may be null. If null, use getChatFilterDefaultIconName to get default icon name for the filter.
        self.icon: ChatFilterIcon = get_object(kwargs.get('icon'))
        # True, if at least one link has been created for the filter.
        self.is_shareable: bool = get_object(kwargs.get('is_shareable'))
        # The chat identifiers of pinned chats in the filter. There can be up to getOption(&quot;chat_filter_chosen_chat_count_max&quot;) pinned and always included non-secret chats and the same number of secret chats, but the limit can be increased with Telegram Premium.
        self.pinned_chat_ids: list[int] = get_object(kwargs.get('pinned_chat_ids'))
        # The chat identifiers of always included chats in the filter. There can be up to getOption(&quot;chat_filter_chosen_chat_count_max&quot;) pinned and always included non-secret chats and the same number of secret chats, but the limit can be increased with Telegram Premium.
        self.included_chat_ids: list[int] = get_object(kwargs.get('included_chat_ids'))
        # The chat identifiers of always excluded chats in the filter. There can be up to getOption(&quot;chat_filter_chosen_chat_count_max&quot;) always excluded non-secret chats and the same number of secret chats, but the limit can be increased with Telegram Premium.
        self.excluded_chat_ids: list[int] = get_object(kwargs.get('excluded_chat_ids'))
        # True, if muted chats need to be excluded.
        self.exclude_muted: bool = get_object(kwargs.get('exclude_muted'))
        # True, if read chats need to be excluded.
        self.exclude_read: bool = get_object(kwargs.get('exclude_read'))
        # True, if archived chats need to be excluded.
        self.exclude_archived: bool = get_object(kwargs.get('exclude_archived'))
        # True, if contacts need to be included.
        self.include_contacts: bool = get_object(kwargs.get('include_contacts'))
        # True, if non-contact users need to be included.
        self.include_non_contacts: bool = get_object(kwargs.get('include_non_contacts'))
        # True, if bots need to be included.
        self.include_bots: bool = get_object(kwargs.get('include_bots'))
        # True, if basic groups and supergroups need to be included.
        self.include_groups: bool = get_object(kwargs.get('include_groups'))
        # True, if channels need to be included.
        self.include_channels: bool = get_object(kwargs.get('include_channels'))


class ChatFilterInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique chat filter identifier.
        self.id: int = get_object(kwargs.get('id'))
        # The title of the filter; 1-12 characters without line feeds.
        self.title: str = get_object(kwargs.get('title'))
        # The chosen or default icon for the chat filter.
        self.icon: ChatFilterIcon = get_object(kwargs.get('icon'))
        # True, if at least one link has been created for the filter.
        self.is_shareable: bool = get_object(kwargs.get('is_shareable'))
        # True, if the chat filter has invite links created by the current user.
        self.has_my_invite_links: bool = get_object(kwargs.get('has_my_invite_links'))


class ChatFilterInviteLink(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat filter invite link.
        self.invite_link: str = get_object(kwargs.get('invite_link'))
        # Name of the link.
        self.name: str = get_object(kwargs.get('name'))
        # Identifiers of chats, included in the link.
        self.chat_ids: list[int] = get_object(kwargs.get('chat_ids'))


class ChatFilterInviteLinkInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Basic information about the chat filter; chat filter identifier will be 0 if the user didn't have the chat filter yet.
        self.chat_filter_info: ChatFilterInfo = get_object(kwargs.get('chat_filter_info'))
        # Identifiers of the chats from the link, which aren't added to the filter yet.
        self.missing_chat_ids: list[int] = get_object(kwargs.get('missing_chat_ids'))
        # Identifiers of the chats from the link, which are added to the filter already.
        self.added_chat_ids: list[int] = get_object(kwargs.get('added_chat_ids'))


class ChatFilterInviteLinks(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of the invite links.
        self.invite_links: list[ChatFilterInviteLink] = get_object(kwargs.get('invite_links'))


class ChatInviteLinkCount(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Administrator's user identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Number of active invite links.
        self.invite_link_count: int = get_object(kwargs.get('invite_link_count'))
        # Number of revoked invite links.
        self.revoked_invite_link_count: int = get_object(kwargs.get('revoked_invite_link_count'))


class ChatInviteLinkCounts(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of invite link counts.
        self.invite_link_counts: list[ChatInviteLinkCount] = get_object(kwargs.get('invite_link_counts'))


class InviteLinkChatType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatInviteLinkInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier of the invite link; 0 if the user has no access to the chat before joining.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # If non-zero, the amount of time for which read access to the chat will remain available, in seconds.
        self.accessible_for: int = get_object(kwargs.get('accessible_for'))
        # Type of the chat.
        self.type: InviteLinkChatType = get_object(kwargs.get('type'))
        # Title of the chat.
        self.title: str = get_object(kwargs.get('title'))
        # Chat photo; may be null.
        self.photo: ChatPhotoInfo = get_object(kwargs.get('photo'))
        # Chat description.
        self.description: str = get_object(kwargs.get('description'))
        # Number of members in the chat.
        self.member_count: int = get_object(kwargs.get('member_count'))
        # User identifiers of some chat members that may be known to the current user.
        self.member_user_ids: list[int] = get_object(kwargs.get('member_user_ids'))
        # True, if the link only creates join request.
        self.creates_join_request: bool = get_object(kwargs.get('creates_join_request'))
        # True, if the chat is a public supergroup or channel, i.e. it has a username or it is a location-based supergroup.
        self.is_public: bool = get_object(kwargs.get('is_public'))
        # True, if the chat is verified.
        self.is_verified: bool = get_object(kwargs.get('is_verified'))
        # True, if many users reported this chat as a scam.
        self.is_scam: bool = get_object(kwargs.get('is_scam'))
        # True, if many users reported this chat as a fake account.
        self.is_fake: bool = get_object(kwargs.get('is_fake'))


class ChatInviteLinkMember(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Point in time (Unix timestamp) when the user joined the chat.
        self.joined_chat_date: int = get_object(kwargs.get('joined_chat_date'))
        # True, if the user has joined the chat using an invite link for a chat filter.
        self.via_chat_filter_invite_link: bool = get_object(kwargs.get('via_chat_filter_invite_link'))
        # User identifier of the chat administrator, approved user join request.
        self.approver_user_id: int = get_object(kwargs.get('approver_user_id'))


class ChatInviteLinkMembers(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of chat members found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of chat members, joined a chat via an invite link.
        self.members: list[ChatInviteLinkMember] = get_object(kwargs.get('members'))


class ChatInviteLinks(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of chat invite links found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of invite links.
        self.invite_links: list[ChatInviteLink] = get_object(kwargs.get('invite_links'))


class ChatJoinRequest(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Point in time (Unix timestamp) when the user sent the join request.
        self.date: int = get_object(kwargs.get('date'))
        # A short bio of the user.
        self.bio: str = get_object(kwargs.get('bio'))


class ChatJoinRequests(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of requests found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of the requests.
        self.requests: list[ChatJoinRequest] = get_object(kwargs.get('requests'))


class ChatList(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatListMain(ChatList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatListArchive(ChatList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatListFilter(ChatList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat filter identifier.
        self.chat_filter_id: int = get_object(kwargs.get('chat_filter_id'))


class ChatLists(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of chat lists.
        self.chat_lists: list[ChatList] = get_object(kwargs.get('chat_lists'))


class Location(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Latitude of the location in degrees; as defined by the sender.
        self.latitude: float = get_object(kwargs.get('latitude'))
        # Longitude of the location, in degrees; as defined by the sender.
        self.longitude: float = get_object(kwargs.get('longitude'))
        # The estimated horizontal accuracy of the location, in meters; as defined by the sender. 0 if unknown.
        self.horizontal_accuracy: float = get_object(kwargs.get('horizontal_accuracy'))


class ChatMemberStatusCreator(ChatMemberStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A custom title of the owner; 0-16 characters without emojis; applicable to supergroups only.
        self.custom_title: str = get_object(kwargs.get('custom_title'))
        # True, if the creator isn't shown in the chat member list and sends messages anonymously; applicable to supergroups only.
        self.is_anonymous: bool = get_object(kwargs.get('is_anonymous'))
        # True, if the user is a member of the chat.
        self.is_member: bool = get_object(kwargs.get('is_member'))


class ChatMemberStatusAdministrator(ChatMemberStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A custom title of the administrator; 0-16 characters without emojis; applicable to supergroups only.
        self.custom_title: str = get_object(kwargs.get('custom_title'))
        # True, if the current user can edit the administrator privileges for the called user.
        self.can_be_edited: bool = get_object(kwargs.get('can_be_edited'))
        # Rights of the administrator.
        self.rights: ChatAdministratorRights = get_object(kwargs.get('rights'))


class ChatMemberStatusMember(ChatMemberStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMemberStatusRestricted(ChatMemberStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the user is a member of the chat.
        self.is_member: bool = get_object(kwargs.get('is_member'))
        # Point in time (Unix timestamp) when restrictions will be lifted from the user; 0 if never. If the user is restricted for more than 366 days or for less than 30 seconds from the current time, the user is considered to be restricted forever.
        self.restricted_until_date: int = get_object(kwargs.get('restricted_until_date'))
        # User permissions in the chat.
        self.permissions: ChatPermissions = get_object(kwargs.get('permissions'))


class ChatMemberStatusLeft(ChatMemberStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMemberStatusBanned(ChatMemberStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) when the user will be unbanned; 0 if never. If the user is banned for more than 366 days or for less than 30 seconds from the current time, the user is considered to be banned forever. Always 0 in basic groups.
        self.banned_until_date: int = get_object(kwargs.get('banned_until_date'))


class ChatMembers(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of chat members found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # A list of chat members.
        self.members: list[ChatMember] = get_object(kwargs.get('members'))


class ChatMembersFilter(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMembersFilterContacts(ChatMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMembersFilterAdministrators(ChatMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMembersFilterMembers(ChatMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMembersFilterMention(ChatMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # If non-zero, the identifier of the current message thread.
        self.message_thread_id: int = get_object(kwargs.get('message_thread_id'))


class ChatMembersFilterRestricted(ChatMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMembersFilterBanned(ChatMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMembersFilterBots(ChatMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatMessageSender(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Available message senders.
        self.sender: MessageSender = get_object(kwargs.get('sender'))
        # True, if Telegram Premium is needed to use the message sender.
        self.needs_premium: bool = get_object(kwargs.get('needs_premium'))


class ChatMessageSenders(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of available message senders.
        self.senders: list[ChatMessageSender] = get_object(kwargs.get('senders'))


class ChatNearby(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Distance to the chat location, in meters.
        self.distance: int = get_object(kwargs.get('distance'))


class ChatPhotoSticker(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the sticker.
        self.type: ChatPhotoStickerType = get_object(kwargs.get('type'))
        # The fill to be used as background for the sticker; rotation angle in backgroundFillGradient isn't supported.
        self.background_fill: BackgroundFill = get_object(kwargs.get('background_fill'))


class PhotoSize(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Image type (see https://core.telegram.org/constructor/photoSize).
        self.type: str = get_object(kwargs.get('type'))
        # Information about the image file.
        self.photo: File = get_object(kwargs.get('photo'))
        # Image width.
        self.width: int = get_object(kwargs.get('width'))
        # Image height.
        self.height: int = get_object(kwargs.get('height'))
        # Sizes of progressive JPEG file prefixes, which can be used to preliminarily show the image; in bytes.
        self.progressive_sizes: list[int] = get_object(kwargs.get('progressive_sizes'))


class ChatPhotoStickerType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatPhotoStickerTypeRegularOrMask(ChatPhotoStickerType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Sticker set identifier.
        self.sticker_set_id: int = get_object(kwargs.get('sticker_set_id'))
        # Identifier of the sticker in the set.
        self.sticker_id: int = get_object(kwargs.get('sticker_id'))


class ChatPhotoStickerTypeCustomEmoji(ChatPhotoStickerType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the custom emoji.
        self.custom_emoji_id: int = get_object(kwargs.get('custom_emoji_id'))


class ChatPhotos(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total number of photos.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of photos.
        self.photos: list[ChatPhoto] = get_object(kwargs.get('photos'))


class ChatSource(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatSourceMtprotoProxy(ChatSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatSourcePublicServiceAnnouncement(ChatSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The type of the announcement.
        self.type: str = get_object(kwargs.get('type'))
        # The text of the announcement.
        self.text: str = get_object(kwargs.get('text'))


class StatisticalGraph(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatStatisticsAdministratorActionsInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Administrator user identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Number of messages deleted by the administrator.
        self.deleted_message_count: int = get_object(kwargs.get('deleted_message_count'))
        # Number of users banned by the administrator.
        self.banned_user_count: int = get_object(kwargs.get('banned_user_count'))
        # Number of users restricted by the administrator.
        self.restricted_user_count: int = get_object(kwargs.get('restricted_user_count'))


class ChatStatisticsInviterInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Number of new members invited by the user.
        self.added_member_count: int = get_object(kwargs.get('added_member_count'))


class ChatStatisticsMessageInteractionInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # Number of times the message was viewed.
        self.view_count: int = get_object(kwargs.get('view_count'))
        # Number of times the message was forwarded.
        self.forward_count: int = get_object(kwargs.get('forward_count'))


class ChatStatisticsMessageSenderInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Number of sent messages.
        self.sent_message_count: int = get_object(kwargs.get('sent_message_count'))
        # Average number of characters in sent messages; 0 if unknown.
        self.average_character_count: int = get_object(kwargs.get('average_character_count'))


class DateRange(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) at which the date range begins.
        self.start_date: int = get_object(kwargs.get('start_date'))
        # Point in time (Unix timestamp) at which the date range ends.
        self.end_date: int = get_object(kwargs.get('end_date'))


class StatisticalValue(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The current value.
        self.value: float = get_object(kwargs.get('value'))
        # The value for the previous day.
        self.previous_value: float = get_object(kwargs.get('previous_value'))
        # The growth rate of the value, as a percentage.
        self.growth_rate_percentage: float = get_object(kwargs.get('growth_rate_percentage'))


class ChatStatistics(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ChatStatisticsSupergroup(ChatStatistics):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A period to which the statistics applies.
        self.period: DateRange = get_object(kwargs.get('period'))
        # Number of members in the chat.
        self.member_count: StatisticalValue = get_object(kwargs.get('member_count'))
        # Number of messages sent to the chat.
        self.message_count: StatisticalValue = get_object(kwargs.get('message_count'))
        # Number of users who viewed messages in the chat.
        self.viewer_count: StatisticalValue = get_object(kwargs.get('viewer_count'))
        # Number of users who sent messages to the chat.
        self.sender_count: StatisticalValue = get_object(kwargs.get('sender_count'))
        # A graph containing number of members in the chat.
        self.member_count_graph: StatisticalGraph = get_object(kwargs.get('member_count_graph'))
        # A graph containing number of members joined and left the chat.
        self.join_graph: StatisticalGraph = get_object(kwargs.get('join_graph'))
        # A graph containing number of new member joins per source.
        self.join_by_source_graph: StatisticalGraph = get_object(kwargs.get('join_by_source_graph'))
        # A graph containing distribution of active users per language.
        self.language_graph: StatisticalGraph = get_object(kwargs.get('language_graph'))
        # A graph containing distribution of sent messages by content type.
        self.message_content_graph: StatisticalGraph = get_object(kwargs.get('message_content_graph'))
        # A graph containing number of different actions in the chat.
        self.action_graph: StatisticalGraph = get_object(kwargs.get('action_graph'))
        # A graph containing distribution of message views per hour.
        self.day_graph: StatisticalGraph = get_object(kwargs.get('day_graph'))
        # A graph containing distribution of message views per day of week.
        self.week_graph: StatisticalGraph = get_object(kwargs.get('week_graph'))
        # List of users sent most messages in the last week.
        self.top_senders: list[ChatStatisticsMessageSenderInfo] = get_object(kwargs.get('top_senders'))
        # List of most active administrators in the last week.
        self.top_administrators: list[ChatStatisticsAdministratorActionsInfo] = get_object(kwargs.get('top_administrators'))
        # List of most active inviters of new members in the last week.
        self.top_inviters: list[ChatStatisticsInviterInfo] = get_object(kwargs.get('top_inviters'))


class ChatStatisticsChannel(ChatStatistics):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A period to which the statistics applies.
        self.period: DateRange = get_object(kwargs.get('period'))
        # Number of members in the chat.
        self.member_count: StatisticalValue = get_object(kwargs.get('member_count'))
        # Mean number of times the recently sent messages was viewed.
        self.mean_view_count: StatisticalValue = get_object(kwargs.get('mean_view_count'))
        # Mean number of times the recently sent messages was shared.
        self.mean_share_count: StatisticalValue = get_object(kwargs.get('mean_share_count'))
        # A percentage of users with enabled notifications for the chat.
        self.enabled_notifications_percentage: float = get_object(kwargs.get('enabled_notifications_percentage'))
        # A graph containing number of members in the chat.
        self.member_count_graph: StatisticalGraph = get_object(kwargs.get('member_count_graph'))
        # A graph containing number of members joined and left the chat.
        self.join_graph: StatisticalGraph = get_object(kwargs.get('join_graph'))
        # A graph containing number of members muted and unmuted the chat.
        self.mute_graph: StatisticalGraph = get_object(kwargs.get('mute_graph'))
        # A graph containing number of message views in a given hour in the last two weeks.
        self.view_count_by_hour_graph: StatisticalGraph = get_object(kwargs.get('view_count_by_hour_graph'))
        # A graph containing number of message views per source.
        self.view_count_by_source_graph: StatisticalGraph = get_object(kwargs.get('view_count_by_source_graph'))
        # A graph containing number of new member joins per source.
        self.join_by_source_graph: StatisticalGraph = get_object(kwargs.get('join_by_source_graph'))
        # A graph containing number of users viewed chat messages per language.
        self.language_graph: StatisticalGraph = get_object(kwargs.get('language_graph'))
        # A graph containing number of chat message views and shares.
        self.message_interaction_graph: StatisticalGraph = get_object(kwargs.get('message_interaction_graph'))
        # A graph containing number of views of associated with the chat instant views.
        self.instant_view_interaction_graph: StatisticalGraph = get_object(kwargs.get('instant_view_interaction_graph'))
        # Detailed statistics about number of views and shares of recently sent messages.
        self.recent_message_interactions: list[ChatStatisticsMessageInteractionInfo] = get_object(kwargs.get('recent_message_interactions'))


class ThemeSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Theme accent color in ARGB format.
        self.accent_color: int = get_object(kwargs.get('accent_color'))
        # The background to be used in chats; may be null.
        self.background: Background = get_object(kwargs.get('background'))
        # The fill to be used as a background for outgoing messages.
        self.outgoing_message_fill: BackgroundFill = get_object(kwargs.get('outgoing_message_fill'))
        # If true, the freeform gradient fill needs to be animated on every sent message.
        self.animate_outgoing_message_fill: bool = get_object(kwargs.get('animate_outgoing_message_fill'))
        # Accent color of outgoing messages in ARGB format.
        self.outgoing_message_accent_color: int = get_object(kwargs.get('outgoing_message_accent_color'))


class ChatTheme(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Theme name.
        self.name: str = get_object(kwargs.get('name'))
        # Theme settings for a light chat theme.
        self.light_settings: ThemeSettings = get_object(kwargs.get('light_settings'))
        # Theme settings for a dark chat theme.
        self.dark_settings: ThemeSettings = get_object(kwargs.get('dark_settings'))


class ChatTypePrivate(ChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))


class ChatTypeBasicGroup(ChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Basic group identifier.
        self.basic_group_id: int = get_object(kwargs.get('basic_group_id'))


class ChatTypeSupergroup(ChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Supergroup or channel identifier.
        self.supergroup_id: int = get_object(kwargs.get('supergroup_id'))
        # True, if the supergroup is a channel.
        self.is_channel: bool = get_object(kwargs.get('is_channel'))


class ChatTypeSecret(ChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Secret chat identifier.
        self.secret_chat_id: int = get_object(kwargs.get('secret_chat_id'))
        # User identifier of the secret chat peer.
        self.user_id: int = get_object(kwargs.get('user_id'))


class Chats(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of chats found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of chat identifiers.
        self.chat_ids: list[int] = get_object(kwargs.get('chat_ids'))


class ChatsNearby(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of users nearby.
        self.users_nearby: list[ChatNearby] = get_object(kwargs.get('users_nearby'))
        # List of location-based supergroups nearby.
        self.supergroups_nearby: list[ChatNearby] = get_object(kwargs.get('supergroups_nearby'))


class CheckChatUsernameResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckChatUsernameResultOk(CheckChatUsernameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckChatUsernameResultUsernameInvalid(CheckChatUsernameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckChatUsernameResultUsernameOccupied(CheckChatUsernameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckChatUsernameResultUsernamePurchasable(CheckChatUsernameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckChatUsernameResultPublicChatsTooMany(CheckChatUsernameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckChatUsernameResultPublicGroupsUnavailable(CheckChatUsernameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckStickerSetNameResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckStickerSetNameResultOk(CheckStickerSetNameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckStickerSetNameResultNameInvalid(CheckStickerSetNameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class CheckStickerSetNameResultNameOccupied(CheckStickerSetNameResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class VectorPathCommand(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ClosedVectorPath(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of vector path commands.
        self.commands: list[VectorPathCommand] = get_object(kwargs.get('commands'))


class ConnectedWebsite(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Website identifier.
        self.id: int = get_object(kwargs.get('id'))
        # The domain name of the website.
        self.domain_name: str = get_object(kwargs.get('domain_name'))
        # User identifier of a bot linked with the website.
        self.bot_user_id: int = get_object(kwargs.get('bot_user_id'))
        # The version of a browser used to log in.
        self.browser: str = get_object(kwargs.get('browser'))
        # Operating system the browser is running on.
        self.platform: str = get_object(kwargs.get('platform'))
        # Point in time (Unix timestamp) when the user was logged in.
        self.log_in_date: int = get_object(kwargs.get('log_in_date'))
        # Point in time (Unix timestamp) when obtained authorization was last used.
        self.last_active_date: int = get_object(kwargs.get('last_active_date'))
        # IP address from which the user was logged in, in human-readable format.
        self.ip_address: str = get_object(kwargs.get('ip_address'))
        # Human-readable description of a country and a region from which the user was logged in, based on the IP address.
        self.location: str = get_object(kwargs.get('location'))


class ConnectedWebsites(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of connected websites.
        self.websites: list[ConnectedWebsite] = get_object(kwargs.get('websites'))


class ConnectionState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ConnectionStateWaitingForNetwork(ConnectionState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ConnectionStateConnectingToProxy(ConnectionState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ConnectionStateConnecting(ConnectionState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ConnectionStateUpdating(ConnectionState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ConnectionStateReady(ConnectionState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Contact(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Phone number of the user.
        self.phone_number: str = get_object(kwargs.get('phone_number'))
        # First name of the user; 1-255 characters in length.
        self.first_name: str = get_object(kwargs.get('first_name'))
        # Last name of the user.
        self.last_name: str = get_object(kwargs.get('last_name'))
        # Additional data about the user in a form of vCard; 0-2048 bytes in length.
        self.vcard: str = get_object(kwargs.get('vcard'))
        # Identifier of the user, if known; 0 otherwise.
        self.user_id: int = get_object(kwargs.get('user_id'))


class Count(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Count.
        self.count: int = get_object(kwargs.get('count'))


class CountryInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A two-letter ISO 3166-1 alpha-2 country code.
        self.country_code: str = get_object(kwargs.get('country_code'))
        # Native name of the country.
        self.name: str = get_object(kwargs.get('name'))
        # English name of the country.
        self.english_name: str = get_object(kwargs.get('english_name'))
        # True, if the country must be hidden from the list of all countries.
        self.is_hidden: bool = get_object(kwargs.get('is_hidden'))
        # List of country calling codes.
        self.calling_codes: list[str] = get_object(kwargs.get('calling_codes'))


class Countries(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The list of countries.
        self.countries: list[CountryInfo] = get_object(kwargs.get('countries'))


class CustomRequestResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A JSON-serialized result.
        self.result: str = get_object(kwargs.get('result'))


class DatabaseStatistics(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Database statistics in an unspecified human-readable format.
        self.statistics: str = get_object(kwargs.get('statistics'))


class Date(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Day of the month; 1-31.
        self.day: int = get_object(kwargs.get('day'))
        # Month; 1-12.
        self.month: int = get_object(kwargs.get('month'))
        # Year; 1-9999.
        self.year: int = get_object(kwargs.get('year'))


class DatedFile(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The file.
        self.file: File = get_object(kwargs.get('file'))
        # Point in time (Unix timestamp) when the file was uploaded.
        self.date: int = get_object(kwargs.get('date'))


class FormattedText(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The text.
        self.text: str = get_object(kwargs.get('text'))
        # Entities contained in the text. Entities can be nested, but must not mutually intersect with each other. Pre, Code and PreCode entities can't contain other entities. Bold, Italic, Underline, Strikethrough, and Spoiler entities can contain and can be part of any other entities. All other entities can't contain each other.
        self.entities: list[TextEntity] = get_object(kwargs.get('entities'))


class DeepLinkInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text to be shown to the user.
        self.text: FormattedText = get_object(kwargs.get('text'))
        # True, if the user must be asked to update the application.
        self.need_update_application: bool = get_object(kwargs.get('need_update_application'))


class DeviceToken(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class DeviceTokenFirebaseCloudMessaging(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Device registration token; may be empty to deregister a device.
        self.token: str = get_object(kwargs.get('token'))
        # True, if push notifications must be additionally encrypted.
        self.encrypt: bool = get_object(kwargs.get('encrypt'))


class DeviceTokenApplePush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Device token; may be empty to deregister a device.
        self.device_token: str = get_object(kwargs.get('device_token'))
        # True, if App Sandbox is enabled.
        self.is_app_sandbox: bool = get_object(kwargs.get('is_app_sandbox'))


class DeviceTokenApplePushVoIP(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Device token; may be empty to deregister a device.
        self.device_token: str = get_object(kwargs.get('device_token'))
        # True, if App Sandbox is enabled.
        self.is_app_sandbox: bool = get_object(kwargs.get('is_app_sandbox'))
        # True, if push notifications must be additionally encrypted.
        self.encrypt: bool = get_object(kwargs.get('encrypt'))


class DeviceTokenWindowsPush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The access token that will be used to send notifications; may be empty to deregister a device.
        self.access_token: str = get_object(kwargs.get('access_token'))


class DeviceTokenMicrosoftPush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Push notification channel URI; may be empty to deregister a device.
        self.channel_uri: str = get_object(kwargs.get('channel_uri'))


class DeviceTokenMicrosoftPushVoIP(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Push notification channel URI; may be empty to deregister a device.
        self.channel_uri: str = get_object(kwargs.get('channel_uri'))


class DeviceTokenWebPush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Absolute URL exposed by the push service where the application server can send push messages; may be empty to deregister a device.
        self.endpoint: str = get_object(kwargs.get('endpoint'))
        # Base64url-encoded P-256 elliptic curve Diffie-Hellman public key.
        self.p256dh_base64url: str = get_object(kwargs.get('p256dh_base64url'))
        # Base64url-encoded authentication secret.
        self.auth_base64url: str = get_object(kwargs.get('auth_base64url'))


class DeviceTokenSimplePush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Absolute URL exposed by the push service where the application server can send push messages; may be empty to deregister a device.
        self.endpoint: str = get_object(kwargs.get('endpoint'))


class DeviceTokenUbuntuPush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Token; may be empty to deregister a device.
        self.token: str = get_object(kwargs.get('token'))


class DeviceTokenBlackBerryPush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Token; may be empty to deregister a device.
        self.token: str = get_object(kwargs.get('token'))


class DeviceTokenTizenPush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Push service registration identifier; may be empty to deregister a device.
        self.reg_id: str = get_object(kwargs.get('reg_id'))


class DeviceTokenHuaweiPush(DeviceToken):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Device registration token; may be empty to deregister a device.
        self.token: str = get_object(kwargs.get('token'))
        # True, if push notifications must be additionally encrypted.
        self.encrypt: bool = get_object(kwargs.get('encrypt'))


class DiceStickers(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class DiceStickersRegular(DiceStickers):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The animated sticker with the dice animation.
        self.sticker: Sticker = get_object(kwargs.get('sticker'))


class DiceStickersSlotMachine(DiceStickers):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The animated sticker with the slot machine background. The background animation must start playing after all reel animations finish.
        self.background: Sticker = get_object(kwargs.get('background'))
        # The animated sticker with the lever animation. The lever animation must play once in the initial dice state.
        self.lever: Sticker = get_object(kwargs.get('lever'))
        # The animated sticker with the left reel.
        self.left_reel: Sticker = get_object(kwargs.get('left_reel'))
        # The animated sticker with the center reel.
        self.center_reel: Sticker = get_object(kwargs.get('center_reel'))
        # The animated sticker with the right reel.
        self.right_reel: Sticker = get_object(kwargs.get('right_reel'))


class DownloadedFileCounts(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number of active file downloads found, including paused.
        self.active_count: int = get_object(kwargs.get('active_count'))
        # Number of paused file downloads found.
        self.paused_count: int = get_object(kwargs.get('paused_count'))
        # Number of completed file downloads found.
        self.completed_count: int = get_object(kwargs.get('completed_count'))


class InputMessageContent(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class EmailAddressAuthentication(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class EmailAddressAuthenticationCode(EmailAddressAuthentication):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The code.
        self.code: str = get_object(kwargs.get('code'))


class EmailAddressAuthenticationAppleId(EmailAddressAuthentication):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The token.
        self.token: str = get_object(kwargs.get('token'))


class EmailAddressAuthenticationGoogleId(EmailAddressAuthentication):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The token.
        self.token: str = get_object(kwargs.get('token'))


class EmailAddressResetStateAvailable(EmailAddressResetState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Time required to wait before the email address can be reset; 0 if the user is subscribed to Telegram Premium.
        self.wait_period: int = get_object(kwargs.get('wait_period'))


class EmailAddressResetStatePending(EmailAddressResetState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Left time before the email address will be reset, in seconds. updateAuthorizationState is not sent when this field changes.
        self.reset_in: int = get_object(kwargs.get('reset_in'))


class EmojiCategory(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the category.
        self.name: str = get_object(kwargs.get('name'))
        # Custom emoji sticker, which represents icon of the category.
        self.icon: Sticker = get_object(kwargs.get('icon'))
        # List of emojis in the category.
        self.emojis: list[str] = get_object(kwargs.get('emojis'))


class EmojiCategories(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of categories.
        self.categories: list[EmojiCategory] = get_object(kwargs.get('categories'))


class EmojiCategoryType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class EmojiCategoryTypeDefault(EmojiCategoryType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class EmojiCategoryTypeEmojiStatus(EmojiCategoryType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class EmojiCategoryTypeChatPhoto(EmojiCategoryType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class EmojiReaction(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text representation of the reaction.
        self.emoji: str = get_object(kwargs.get('emoji'))
        # Reaction title.
        self.title: str = get_object(kwargs.get('title'))
        # True, if the reaction can be added to new messages and enabled in chats.
        self.is_active: bool = get_object(kwargs.get('is_active'))
        # Static icon for the reaction.
        self.static_icon: Sticker = get_object(kwargs.get('static_icon'))
        # Appear animation for the reaction.
        self.appear_animation: Sticker = get_object(kwargs.get('appear_animation'))
        # Select animation for the reaction.
        self.select_animation: Sticker = get_object(kwargs.get('select_animation'))
        # Activate animation for the reaction.
        self.activate_animation: Sticker = get_object(kwargs.get('activate_animation'))
        # Effect animation for the reaction.
        self.effect_animation: Sticker = get_object(kwargs.get('effect_animation'))
        # Around animation for the reaction; may be null.
        self.around_animation: Sticker = get_object(kwargs.get('around_animation'))
        # Center animation for the reaction; may be null.
        self.center_animation: Sticker = get_object(kwargs.get('center_animation'))


class EmojiStatus(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the custom emoji in stickerFormatTgs format.
        self.custom_emoji_id: int = get_object(kwargs.get('custom_emoji_id'))
        # Point in time (Unix timestamp) when the status will expire; 0 if never.
        self.expiration_date: int = get_object(kwargs.get('expiration_date'))


class EmojiStatuses(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The list of custom emoji identifiers.
        self.custom_emoji_ids: list[int] = get_object(kwargs.get('custom_emoji_ids'))


class Emojis(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of emojis.
        self.emojis: list[str] = get_object(kwargs.get('emojis'))


class EncryptedCredentials(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The encrypted credentials.
        self.data: bytes = get_object(kwargs.get('data'))
        # The decrypted data hash.
        self.hash: bytes = get_object(kwargs.get('hash'))
        # Secret for data decryption, encrypted with the service's public key.
        self.secret: bytes = get_object(kwargs.get('secret'))


class PassportElementType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class EncryptedPassportElement(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of Telegram Passport element.
        self.type: PassportElementType = get_object(kwargs.get('type'))
        # Encrypted JSON-encoded data about the user.
        self.data: bytes = get_object(kwargs.get('data'))
        # The front side of an identity document.
        self.front_side: DatedFile = get_object(kwargs.get('front_side'))
        # The reverse side of an identity document; may be null.
        self.reverse_side: DatedFile = get_object(kwargs.get('reverse_side'))
        # Selfie with the document; may be null.
        self.selfie: DatedFile = get_object(kwargs.get('selfie'))
        # List of files containing a certified English translation of the document.
        self.translation: list[DatedFile] = get_object(kwargs.get('translation'))
        # List of attached files.
        self.files: list[DatedFile] = get_object(kwargs.get('files'))
        # Unencrypted data, phone number or email address.
        self.value: str = get_object(kwargs.get('value'))
        # Hash of the entire element.
        self.hash: str = get_object(kwargs.get('hash'))


class LocalFile(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Local path to the locally available file part; may be empty.
        self.path: str = get_object(kwargs.get('path'))
        # True, if it is possible to download or generate the file.
        self.can_be_downloaded: bool = get_object(kwargs.get('can_be_downloaded'))
        # True, if the file can be deleted.
        self.can_be_deleted: bool = get_object(kwargs.get('can_be_deleted'))
        # True, if the file is currently being downloaded (or a local copy is being generated by some other means).
        self.is_downloading_active: bool = get_object(kwargs.get('is_downloading_active'))
        # True, if the local copy is fully available.
        self.is_downloading_completed: bool = get_object(kwargs.get('is_downloading_completed'))
        # Download will be started from this offset. downloaded_prefix_size is calculated from this offset.
        self.download_offset: int = get_object(kwargs.get('download_offset'))
        # If is_downloading_completed is false, then only some prefix of the file starting from download_offset is ready to be read. downloaded_prefix_size is the size of that prefix in bytes.
        self.downloaded_prefix_size: int = get_object(kwargs.get('downloaded_prefix_size'))
        # Total downloaded file size, in bytes. Can be used only for calculating download progress. The actual file size may be bigger, and some parts of it may contain garbage.
        self.downloaded_size: int = get_object(kwargs.get('downloaded_size'))


class RemoteFile(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Remote file identifier; may be empty. Can be used by the current user across application restarts or even from other devices. Uniquely identifies a file, but a file can have a lot of different valid identifiers. If the identifier starts with &quot;<a href="http://">http://</a>&quot; or &quot;<a href="https://">https://</a>&quot;, it represents the HTTP URL of the file. TDLib is currently unable to download files if only their URL is known. If downloadFile/addFileToDownloads is called on such a file or if it is sent to a secret chat, TDLib starts a file generation process by sending updateFileGenerationStart to the application with the HTTP URL in the original_path and &quot;\#url\#&quot; as the conversion string. Application must generate the file by downloading it to the specified location.
        self.id: str = get_object(kwargs.get('id'))
        # Unique file identifier; may be empty if unknown. The unique file identifier which is the same for the same file even for different users and is persistent over time.
        self.unique_id: str = get_object(kwargs.get('unique_id'))
        # True, if the file is currently being uploaded (or a remote copy is being generated by some other means).
        self.is_uploading_active: bool = get_object(kwargs.get('is_uploading_active'))
        # True, if a remote copy is fully available.
        self.is_uploading_completed: bool = get_object(kwargs.get('is_uploading_completed'))
        # Size of the remote available part of the file, in bytes; 0 if unknown.
        self.uploaded_size: int = get_object(kwargs.get('uploaded_size'))


class FileDownload(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # File identifier.
        self.file_id: int = get_object(kwargs.get('file_id'))
        # The message with the file.
        self.message: Message = get_object(kwargs.get('message'))
        # Point in time (Unix timestamp) when the file was added to the download list.
        self.add_date: int = get_object(kwargs.get('add_date'))
        # Point in time (Unix timestamp) when the file downloading was completed; 0 if the file downloading isn't completed.
        self.complete_date: int = get_object(kwargs.get('complete_date'))
        # True, if downloading of the file is paused.
        self.is_paused: bool = get_object(kwargs.get('is_paused'))


class FileDownloadedPrefixSize(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The prefix size, in bytes.
        self.size: int = get_object(kwargs.get('size'))


class FilePart(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # File bytes.
        self.data: bytes = get_object(kwargs.get('data'))


class FileType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeNone(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeAnimation(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeAudio(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeDocument(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeNotificationSound(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypePhoto(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypePhotoStory(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeProfilePhoto(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeSecret(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeSecretThumbnail(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeSecure(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeSticker(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeThumbnail(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeUnknown(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeVideo(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeVideoNote(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeVideoStory(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeVoiceNote(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FileTypeWallpaper(FileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FirebaseAuthenticationSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FirebaseAuthenticationSettingsAndroid(FirebaseAuthenticationSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class FirebaseAuthenticationSettingsIos(FirebaseAuthenticationSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Device token from Apple Push Notification service.
        self.device_token: str = get_object(kwargs.get('device_token'))
        # True, if App Sandbox is enabled.
        self.is_app_sandbox: bool = get_object(kwargs.get('is_app_sandbox'))


class TextEntity(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Offset of the entity, in UTF-16 code units.
        self.offset: int = get_object(kwargs.get('offset'))
        # Length of the entity, in UTF-16 code units.
        self.length: int = get_object(kwargs.get('length'))
        # Type of the entity.
        self.type: TextEntityType = get_object(kwargs.get('type'))


class ForumTopic(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Basic information about the topic.
        self.info: ForumTopicInfo = get_object(kwargs.get('info'))
        # Last message in the topic; may be null if unknown.
        self.last_message: Message = get_object(kwargs.get('last_message'))
        # True, if the topic is pinned in the topic list.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))
        # Number of unread messages in the topic.
        self.unread_count: int = get_object(kwargs.get('unread_count'))
        # Identifier of the last read incoming message.
        self.last_read_inbox_message_id: int = get_object(kwargs.get('last_read_inbox_message_id'))
        # Identifier of the last read outgoing message.
        self.last_read_outbox_message_id: int = get_object(kwargs.get('last_read_outbox_message_id'))
        # Number of unread messages with a mention/reply in the topic.
        self.unread_mention_count: int = get_object(kwargs.get('unread_mention_count'))
        # Number of messages with unread reactions in the topic.
        self.unread_reaction_count: int = get_object(kwargs.get('unread_reaction_count'))
        # Notification settings for the topic.
        self.notification_settings: ChatNotificationSettings = get_object(kwargs.get('notification_settings'))
        # A draft of a message in the topic; may be null if none.
        self.draft_message: DraftMessage = get_object(kwargs.get('draft_message'))


class ForumTopicIcon(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Color of the topic icon in RGB format.
        self.color: int = get_object(kwargs.get('color'))
        # Unique identifier of the custom emoji shown on the topic icon; 0 if none.
        self.custom_emoji_id: int = get_object(kwargs.get('custom_emoji_id'))


class ForumTopics(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of forum topics found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of forum topics.
        self.topics: list[ForumTopic] = get_object(kwargs.get('topics'))
        # Offset date for the next getForumTopics request.
        self.next_offset_date: int = get_object(kwargs.get('next_offset_date'))
        # Offset message identifier for the next getForumTopics request.
        self.next_offset_message_id: int = get_object(kwargs.get('next_offset_message_id'))
        # Offset message thread identifier for the next getForumTopics request.
        self.next_offset_message_thread_id: int = get_object(kwargs.get('next_offset_message_thread_id'))


class FoundChatMessages(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of messages found; -1 if unknown.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of messages.
        self.messages: list[Message] = get_object(kwargs.get('messages'))
        # The offset for the next request. If 0, there are no more results.
        self.next_from_message_id: int = get_object(kwargs.get('next_from_message_id'))


class FoundFileDownloads(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total number of suitable files, ignoring offset.
        self.total_counts: DownloadedFileCounts = get_object(kwargs.get('total_counts'))
        # The list of files.
        self.files: list[FileDownload] = get_object(kwargs.get('files'))
        # The offset for the next request. If empty, there are no more results.
        self.next_offset: str = get_object(kwargs.get('next_offset'))


class FoundMessages(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of messages found; -1 if unknown.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of messages.
        self.messages: list[Message] = get_object(kwargs.get('messages'))
        # The offset for the next request. If empty, there are no more results.
        self.next_offset: str = get_object(kwargs.get('next_offset'))


class FoundPositions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total number of matched objects.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # The positions of the matched objects.
        self.positions: list[int] = get_object(kwargs.get('positions'))


class WebApp(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Web App short name.
        self.short_name: str = get_object(kwargs.get('short_name'))
        # Web App title.
        self.title: str = get_object(kwargs.get('title'))
        # Web App description.
        self.description: str = get_object(kwargs.get('description'))
        # Web App photo.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Web App animation; may be null.
        self.animation: Animation = get_object(kwargs.get('animation'))


class FoundWebApp(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The Web App.
        self.web_app: WebApp = get_object(kwargs.get('web_app'))
        # True, if the app supports &quot;settings_button_pressed&quot; event.
        self.supports_settings: bool = get_object(kwargs.get('supports_settings'))
        # True, if the user must be asked for the permission to the bot to send them messages.
        self.request_write_access: bool = get_object(kwargs.get('request_write_access'))
        # True, if there is no need to show an ordinary open URL confirmation before opening the Web App. The field must be ignored and confirmation must be shown anyway if the Web App link was hidden.
        self.skip_confirmation: bool = get_object(kwargs.get('skip_confirmation'))


class Game(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique game identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Game short name.
        self.short_name: str = get_object(kwargs.get('short_name'))
        # Game title.
        self.title: str = get_object(kwargs.get('title'))
        # Game text, usually containing scoreboards for a game.
        self.text: FormattedText = get_object(kwargs.get('text'))
        # Game description.
        self.description: str = get_object(kwargs.get('description'))
        # Game photo.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Game animation; may be null.
        self.animation: Animation = get_object(kwargs.get('animation'))


class GameHighScore(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Position in the high score table.
        self.position: int = get_object(kwargs.get('position'))
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # User score.
        self.score: int = get_object(kwargs.get('score'))


class GameHighScores(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of game high scores.
        self.scores: list[GameHighScore] = get_object(kwargs.get('scores'))


class GroupCallRecentSpeaker(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Group call participant identifier.
        self.participant_id: MessageSender = get_object(kwargs.get('participant_id'))
        # True, is the user has spoken recently.
        self.is_speaking: bool = get_object(kwargs.get('is_speaking'))


class GroupCall(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Group call identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Group call title.
        self.title: str = get_object(kwargs.get('title'))
        # Point in time (Unix timestamp) when the group call is supposed to be started by an administrator; 0 if it is already active or was ended.
        self.scheduled_start_date: int = get_object(kwargs.get('scheduled_start_date'))
        # True, if the group call is scheduled and the current user will receive a notification when the group call will start.
        self.enabled_start_notification: bool = get_object(kwargs.get('enabled_start_notification'))
        # True, if the call is active.
        self.is_active: bool = get_object(kwargs.get('is_active'))
        # True, if the chat is an RTMP stream instead of an ordinary video chat.
        self.is_rtmp_stream: bool = get_object(kwargs.get('is_rtmp_stream'))
        # True, if the call is joined.
        self.is_joined: bool = get_object(kwargs.get('is_joined'))
        # True, if user was kicked from the call because of network loss and the call needs to be rejoined.
        self.need_rejoin: bool = get_object(kwargs.get('need_rejoin'))
        # True, if the current user can manage the group call.
        self.can_be_managed: bool = get_object(kwargs.get('can_be_managed'))
        # Number of participants in the group call.
        self.participant_count: int = get_object(kwargs.get('participant_count'))
        # True, if group call participants, which are muted, aren't returned in participant list.
        self.has_hidden_listeners: bool = get_object(kwargs.get('has_hidden_listeners'))
        # True, if all group call participants are loaded.
        self.loaded_all_participants: bool = get_object(kwargs.get('loaded_all_participants'))
        # At most 3 recently speaking users in the group call.
        self.recent_speakers: list[GroupCallRecentSpeaker] = get_object(kwargs.get('recent_speakers'))
        # True, if the current user's video is enabled.
        self.is_my_video_enabled: bool = get_object(kwargs.get('is_my_video_enabled'))
        # True, if the current user's video is paused.
        self.is_my_video_paused: bool = get_object(kwargs.get('is_my_video_paused'))
        # True, if the current user can broadcast video or share screen.
        self.can_enable_video: bool = get_object(kwargs.get('can_enable_video'))
        # True, if only group call administrators can unmute new participants.
        self.mute_new_participants: bool = get_object(kwargs.get('mute_new_participants'))
        # True, if the current user can enable or disable mute_new_participants setting.
        self.can_toggle_mute_new_participants: bool = get_object(kwargs.get('can_toggle_mute_new_participants'))
        # Duration of the ongoing group call recording, in seconds; 0 if none. An updateGroupCall update is not triggered when value of this field changes, but the same recording goes on.
        self.record_duration: int = get_object(kwargs.get('record_duration'))
        # True, if a video file is being recorded for the call.
        self.is_video_recorded: bool = get_object(kwargs.get('is_video_recorded'))
        # Call duration, in seconds; for ended calls only.
        self.duration: int = get_object(kwargs.get('duration'))


class GroupCallId(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Group call identifier.
        self.id: int = get_object(kwargs.get('id'))


class GroupCallParticipantVideoInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of synchronization source groups of the video.
        self.source_groups: list[GroupCallVideoSourceGroup] = get_object(kwargs.get('source_groups'))
        # Video channel endpoint identifier.
        self.endpoint_id: str = get_object(kwargs.get('endpoint_id'))
        # True, if the video is paused. This flag needs to be ignored, if new video frames are received.
        self.is_paused: bool = get_object(kwargs.get('is_paused'))


class GroupCallParticipant(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the group call participant.
        self.participant_id: MessageSender = get_object(kwargs.get('participant_id'))
        # User's audio channel synchronization source identifier.
        self.audio_source_id: int = get_object(kwargs.get('audio_source_id'))
        # User's screen sharing audio channel synchronization source identifier.
        self.screen_sharing_audio_source_id: int = get_object(kwargs.get('screen_sharing_audio_source_id'))
        # Information about user's video channel; may be null if there is no active video.
        self.video_info: GroupCallParticipantVideoInfo = get_object(kwargs.get('video_info'))
        # Information about user's screen sharing video channel; may be null if there is no active screen sharing video.
        self.screen_sharing_video_info: GroupCallParticipantVideoInfo = get_object(kwargs.get('screen_sharing_video_info'))
        # The participant user's bio or the participant chat's description.
        self.bio: str = get_object(kwargs.get('bio'))
        # True, if the participant is the current user.
        self.is_current_user: bool = get_object(kwargs.get('is_current_user'))
        # True, if the participant is speaking as set by setGroupCallParticipantIsSpeaking.
        self.is_speaking: bool = get_object(kwargs.get('is_speaking'))
        # True, if the participant hand is raised.
        self.is_hand_raised: bool = get_object(kwargs.get('is_hand_raised'))
        # True, if the current user can mute the participant for all other group call participants.
        self.can_be_muted_for_all_users: bool = get_object(kwargs.get('can_be_muted_for_all_users'))
        # True, if the current user can allow the participant to unmute themselves or unmute the participant (if the participant is the current user).
        self.can_be_unmuted_for_all_users: bool = get_object(kwargs.get('can_be_unmuted_for_all_users'))
        # True, if the current user can mute the participant only for self.
        self.can_be_muted_for_current_user: bool = get_object(kwargs.get('can_be_muted_for_current_user'))
        # True, if the current user can unmute the participant for self.
        self.can_be_unmuted_for_current_user: bool = get_object(kwargs.get('can_be_unmuted_for_current_user'))
        # True, if the participant is muted for all users.
        self.is_muted_for_all_users: bool = get_object(kwargs.get('is_muted_for_all_users'))
        # True, if the participant is muted for the current user.
        self.is_muted_for_current_user: bool = get_object(kwargs.get('is_muted_for_current_user'))
        # True, if the participant is muted for all users, but can unmute themselves.
        self.can_unmute_self: bool = get_object(kwargs.get('can_unmute_self'))
        # Participant's volume level; 1-20000 in hundreds of percents.
        self.volume_level: int = get_object(kwargs.get('volume_level'))
        # User's order in the group call participant list. Orders must be compared lexicographically. The bigger is order, the higher is user in the list. If order is empty, the user must be removed from the participant list.
        self.order: str = get_object(kwargs.get('order'))


class GroupCallVideoSourceGroup(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The semantics of sources, one of &quot;SIM&quot; or &quot;FID&quot;.
        self.semantics: str = get_object(kwargs.get('semantics'))
        # The list of synchronization source identifiers.
        self.source_ids: list[int] = get_object(kwargs.get('source_ids'))


class GroupCallStream(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of an audio/video channel.
        self.channel_id: int = get_object(kwargs.get('channel_id'))
        # Scale of segment durations in the stream. The duration is 1000/(2**scale) milliseconds.
        self.scale: int = get_object(kwargs.get('scale'))
        # Point in time when the stream currently ends; Unix timestamp in milliseconds.
        self.time_offset: int = get_object(kwargs.get('time_offset'))


class GroupCallStreams(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of group call streams.
        self.streams: list[GroupCallStream] = get_object(kwargs.get('streams'))


class GroupCallVideoQuality(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class GroupCallVideoQualityThumbnail(GroupCallVideoQuality):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class GroupCallVideoQualityMedium(GroupCallVideoQuality):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class GroupCallVideoQualityFull(GroupCallVideoQuality):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Hashtags(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of hashtags.
        self.hashtags: list[str] = get_object(kwargs.get('hashtags'))


class HttpUrl(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The URL.
        self.url: str = get_object(kwargs.get('url'))


class IdentityDocument(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Document number; 1-24 characters.
        self.number: str = get_object(kwargs.get('number'))
        # Document expiration date; may be null if not applicable.
        self.expiration_date: Date = get_object(kwargs.get('expiration_date'))
        # Front side of the document.
        self.front_side: DatedFile = get_object(kwargs.get('front_side'))
        # Reverse side of the document; only for driver license and identity card; may be null.
        self.reverse_side: DatedFile = get_object(kwargs.get('reverse_side'))
        # Selfie with the document; may be null.
        self.selfie: DatedFile = get_object(kwargs.get('selfie'))
        # List of files containing a certified English translation of the document.
        self.translation: list[DatedFile] = get_object(kwargs.get('translation'))


class ImportedContacts(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifiers of the imported contacts in the same order as they were specified in the request; 0 if the contact is not yet a registered user.
        self.user_ids: list[int] = get_object(kwargs.get('user_ids'))
        # The number of users that imported the corresponding contact; 0 for already registered users or if unavailable.
        self.importer_count: list[int] = get_object(kwargs.get('importer_count'))


class InlineKeyboardButtonType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InlineKeyboardButton(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the button.
        self.text: str = get_object(kwargs.get('text'))
        # Type of the button.
        self.type: InlineKeyboardButtonType = get_object(kwargs.get('type'))


class TargetChat(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InlineKeyboardButtonTypeUrl(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # HTTP or tg:// URL to open.
        self.url: str = get_object(kwargs.get('url'))


class InlineKeyboardButtonTypeLoginUrl(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # An HTTP URL to pass to getLoginUrlInfo.
        self.url: str = get_object(kwargs.get('url'))
        # Unique button identifier.
        self.id: int = get_object(kwargs.get('id'))
        # If non-empty, new text of the button in forwarded messages.
        self.forward_text: str = get_object(kwargs.get('forward_text'))


class InlineKeyboardButtonTypeWebApp(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # An HTTP URL to pass to openWebApp.
        self.url: str = get_object(kwargs.get('url'))


class InlineKeyboardButtonTypeCallback(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Data to be sent to the bot via a callback query.
        self.data: bytes = get_object(kwargs.get('data'))


class InlineKeyboardButtonTypeCallbackWithPassword(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Data to be sent to the bot via a callback query.
        self.data: bytes = get_object(kwargs.get('data'))


class InlineKeyboardButtonTypeCallbackGame(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InlineKeyboardButtonTypeSwitchInline(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Inline query to be sent to the bot.
        self.query: str = get_object(kwargs.get('query'))
        # Target chat from which to send the inline query.
        self.target_chat: TargetChat = get_object(kwargs.get('target_chat'))


class InlineKeyboardButtonTypeBuy(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InlineKeyboardButtonTypeUser(InlineKeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))


class Venue(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Venue location; as defined by the sender.
        self.location: Location = get_object(kwargs.get('location'))
        # Venue name; as defined by the sender.
        self.title: str = get_object(kwargs.get('title'))
        # Venue address; as defined by the sender.
        self.address: str = get_object(kwargs.get('address'))
        # Provider of the venue database; as defined by the sender. Currently, only &quot;foursquare&quot; and &quot;gplaces&quot; (Google Places) need to be supported.
        self.provider: str = get_object(kwargs.get('provider'))
        # Identifier of the venue in the provider database; as defined by the sender.
        self.id: str = get_object(kwargs.get('id'))
        # Type of the venue in the provider database; as defined by the sender.
        self.type: str = get_object(kwargs.get('type'))


class Video(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Duration of the video, in seconds; as defined by the sender.
        self.duration: int = get_object(kwargs.get('duration'))
        # Video width; as defined by the sender.
        self.width: int = get_object(kwargs.get('width'))
        # Video height; as defined by the sender.
        self.height: int = get_object(kwargs.get('height'))
        # Original name of the file; as defined by the sender.
        self.file_name: str = get_object(kwargs.get('file_name'))
        # MIME type of the file; as defined by the sender.
        self.mime_type: str = get_object(kwargs.get('mime_type'))
        # True, if stickers were added to the video. The list of corresponding sticker sets can be received using getAttachedStickerSets.
        self.has_stickers: bool = get_object(kwargs.get('has_stickers'))
        # True, if the video is supposed to be streamed.
        self.supports_streaming: bool = get_object(kwargs.get('supports_streaming'))
        # Video minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # Video thumbnail in JPEG or MPEG4 format; as defined by the sender; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))
        # File containing the video.
        self.video: File = get_object(kwargs.get('video'))


class VoiceNote(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Duration of the voice note, in seconds; as defined by the sender.
        self.duration: int = get_object(kwargs.get('duration'))
        # A waveform representation of the voice note in 5-bit format.
        self.waveform: bytes = get_object(kwargs.get('waveform'))
        # MIME type of the file; as defined by the sender.
        self.mime_type: str = get_object(kwargs.get('mime_type'))
        # Result of speech recognition in the voice note; may be null.
        self.speech_recognition_result: SpeechRecognitionResult = get_object(kwargs.get('speech_recognition_result'))
        # File containing the voice note.
        self.voice: File = get_object(kwargs.get('voice'))


class InlineQueryResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InlineQueryResultArticle(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # URL of the result, if it exists.
        self.url: str = get_object(kwargs.get('url'))
        # True, if the URL must be not shown.
        self.hide_url: bool = get_object(kwargs.get('hide_url'))
        # Title of the result.
        self.title: str = get_object(kwargs.get('title'))
        # A short description of the result.
        self.description: str = get_object(kwargs.get('description'))
        # Result thumbnail in JPEG format; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))


class InlineQueryResultContact(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # A user contact.
        self.contact: Contact = get_object(kwargs.get('contact'))
        # Result thumbnail in JPEG format; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))


class InlineQueryResultLocation(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Location result.
        self.location: Location = get_object(kwargs.get('location'))
        # Title of the result.
        self.title: str = get_object(kwargs.get('title'))
        # Result thumbnail in JPEG format; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))


class InlineQueryResultVenue(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Venue result.
        self.venue: Venue = get_object(kwargs.get('venue'))
        # Result thumbnail in JPEG format; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))


class InlineQueryResultGame(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Game result.
        self.game: Game = get_object(kwargs.get('game'))


class InlineQueryResultAnimation(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Animation file.
        self.animation: Animation = get_object(kwargs.get('animation'))
        # Animation title.
        self.title: str = get_object(kwargs.get('title'))


class InlineQueryResultAudio(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Audio file.
        self.audio: Audio = get_object(kwargs.get('audio'))


class InlineQueryResultDocument(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Document.
        self.document: Document = get_object(kwargs.get('document'))
        # Document title.
        self.title: str = get_object(kwargs.get('title'))
        # Document description.
        self.description: str = get_object(kwargs.get('description'))


class InlineQueryResultPhoto(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Photo.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Title of the result, if known.
        self.title: str = get_object(kwargs.get('title'))
        # A short description of the result, if known.
        self.description: str = get_object(kwargs.get('description'))


class InlineQueryResultSticker(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Sticker.
        self.sticker: Sticker = get_object(kwargs.get('sticker'))


class InlineQueryResultVideo(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Video.
        self.video: Video = get_object(kwargs.get('video'))
        # Title of the video.
        self.title: str = get_object(kwargs.get('title'))
        # Description of the video.
        self.description: str = get_object(kwargs.get('description'))


class InlineQueryResultVoiceNote(InlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Voice note.
        self.voice_note: VoiceNote = get_object(kwargs.get('voice_note'))
        # Title of the voice note.
        self.title: str = get_object(kwargs.get('title'))


class InlineQueryResultsButton(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The text of the button.
        self.text: str = get_object(kwargs.get('text'))
        # Type of the button.
        self.type: InlineQueryResultsButtonType = get_object(kwargs.get('type'))


class InlineQueryResults(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the inline query.
        self.inline_query_id: int = get_object(kwargs.get('inline_query_id'))
        # Button to be shown above inline query results; may be null.
        self.button: InlineQueryResultsButton = get_object(kwargs.get('button'))
        # Results of the query.
        self.results: list[InlineQueryResult] = get_object(kwargs.get('results'))
        # The offset for the next request. If empty, there are no more results.
        self.next_offset: str = get_object(kwargs.get('next_offset'))


class InlineQueryResultsButtonType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InlineQueryResultsButtonTypeStartBot(InlineQueryResultsButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The parameter for the bot start message.
        self.parameter: str = get_object(kwargs.get('parameter'))


class InlineQueryResultsButtonTypeWebApp(InlineQueryResultsButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # An HTTP URL to pass to getWebAppUrl.
        self.url: str = get_object(kwargs.get('url'))


class InputFile(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputBackground(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputBackgroundLocal(InputBackground):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Background file to use. Only inputFileLocal and inputFileGenerated are supported. The file must be in JPEG format for wallpapers and in PNG format for patterns.
        self.background: InputFile = get_object(kwargs.get('background'))


class InputBackgroundRemote(InputBackground):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The background identifier.
        self.background_id: int = get_object(kwargs.get('background_id'))


class InputBackgroundPrevious(InputBackground):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the message with the background.
        self.message_id: int = get_object(kwargs.get('message_id'))


class InputChatPhoto(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputChatPhotoPrevious(InputChatPhoto):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the current user's profile photo to reuse.
        self.chat_photo_id: int = get_object(kwargs.get('chat_photo_id'))


class InputChatPhotoStatic(InputChatPhoto):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Photo to be set as profile photo. Only inputFileLocal and inputFileGenerated are allowed.
        self.photo: InputFile = get_object(kwargs.get('photo'))


class InputChatPhotoAnimation(InputChatPhoto):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Animation to be set as profile photo. Only inputFileLocal and inputFileGenerated are allowed.
        self.animation: InputFile = get_object(kwargs.get('animation'))
        # Timestamp of the frame, which will be used as static chat photo.
        self.main_frame_timestamp: float = get_object(kwargs.get('main_frame_timestamp'))


class InputChatPhotoSticker(InputChatPhoto):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the sticker.
        self.sticker: ChatPhotoSticker = get_object(kwargs.get('sticker'))


class InputCredentials(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputCredentialsSaved(InputCredentials):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the saved credentials.
        self.saved_credentials_id: str = get_object(kwargs.get('saved_credentials_id'))


class InputCredentialsNew(InputCredentials):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # JSON-encoded data with the credential identifier from the payment provider.
        self.data: str = get_object(kwargs.get('data'))
        # True, if the credential identifier can be saved on the server side.
        self.allow_save: bool = get_object(kwargs.get('allow_save'))


class InputCredentialsApplePay(InputCredentials):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # JSON-encoded data with the credential identifier.
        self.data: str = get_object(kwargs.get('data'))


class InputCredentialsGooglePay(InputCredentials):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # JSON-encoded data with the credential identifier.
        self.data: str = get_object(kwargs.get('data'))


class InputFileId(InputFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique file identifier.
        self.id: int = get_object(kwargs.get('id'))


class InputFileRemote(InputFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Remote file identifier.
        self.id: str = get_object(kwargs.get('id'))


class InputFileLocal(InputFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Local path to the file.
        self.path: str = get_object(kwargs.get('path'))


class InputFileGenerated(InputFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Local path to a file from which the file is generated; may be empty if there is no such file.
        self.original_path: str = get_object(kwargs.get('original_path'))
        # String specifying the conversion applied to the original file; must be persistent across application restarts. Conversions beginning with '\#' are reserved for internal TDLib usage.
        self.conversion: str = get_object(kwargs.get('conversion'))
        # Expected size of the generated file, in bytes; 0 if unknown.
        self.expected_size: int = get_object(kwargs.get('expected_size'))


class InputIdentityDocument(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Document number; 1-24 characters.
        self.number: str = get_object(kwargs.get('number'))
        # Document expiration date; pass null if not applicable.
        self.expiration_date: Date = get_object(kwargs.get('expiration_date'))
        # Front side of the document.
        self.front_side: InputFile = get_object(kwargs.get('front_side'))
        # Reverse side of the document; only for driver license and identity card; pass null otherwise.
        self.reverse_side: InputFile = get_object(kwargs.get('reverse_side'))
        # Selfie with the document; pass null if unavailable.
        self.selfie: InputFile = get_object(kwargs.get('selfie'))
        # List of files containing a certified English translation of the document.
        self.translation: list[InputFile] = get_object(kwargs.get('translation'))


class ReplyMarkup(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputInlineQueryResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputInlineQueryResultAnimation(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Title of the query result.
        self.title: str = get_object(kwargs.get('title'))
        # URL of the result thumbnail (JPEG, GIF, or MPEG4), if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # MIME type of the video thumbnail. If non-empty, must be one of &quot;image/jpeg&quot;, &quot;image/gif&quot; and &quot;video/mp4&quot;.
        self.thumbnail_mime_type: str = get_object(kwargs.get('thumbnail_mime_type'))
        # The URL of the video file (file size must not exceed 1MB).
        self.video_url: str = get_object(kwargs.get('video_url'))
        # MIME type of the video file. Must be one of &quot;image/gif&quot; and &quot;video/mp4&quot;.
        self.video_mime_type: str = get_object(kwargs.get('video_mime_type'))
        # Duration of the video, in seconds.
        self.video_duration: int = get_object(kwargs.get('video_duration'))
        # Width of the video.
        self.video_width: int = get_object(kwargs.get('video_width'))
        # Height of the video.
        self.video_height: int = get_object(kwargs.get('video_height'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageAnimation, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultArticle(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # URL of the result, if it exists.
        self.url: str = get_object(kwargs.get('url'))
        # True, if the URL must be not shown.
        self.hide_url: bool = get_object(kwargs.get('hide_url'))
        # Title of the result.
        self.title: str = get_object(kwargs.get('title'))
        # A short description of the result.
        self.description: str = get_object(kwargs.get('description'))
        # URL of the result thumbnail, if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # Thumbnail width, if known.
        self.thumbnail_width: int = get_object(kwargs.get('thumbnail_width'))
        # Thumbnail height, if known.
        self.thumbnail_height: int = get_object(kwargs.get('thumbnail_height'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultAudio(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Title of the audio file.
        self.title: str = get_object(kwargs.get('title'))
        # Performer of the audio file.
        self.performer: str = get_object(kwargs.get('performer'))
        # The URL of the audio file.
        self.audio_url: str = get_object(kwargs.get('audio_url'))
        # Audio file duration, in seconds.
        self.audio_duration: int = get_object(kwargs.get('audio_duration'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageAudio, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultContact(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # User contact.
        self.contact: Contact = get_object(kwargs.get('contact'))
        # URL of the result thumbnail, if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # Thumbnail width, if known.
        self.thumbnail_width: int = get_object(kwargs.get('thumbnail_width'))
        # Thumbnail height, if known.
        self.thumbnail_height: int = get_object(kwargs.get('thumbnail_height'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultDocument(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Title of the resulting file.
        self.title: str = get_object(kwargs.get('title'))
        # Short description of the result, if known.
        self.description: str = get_object(kwargs.get('description'))
        # URL of the file.
        self.document_url: str = get_object(kwargs.get('document_url'))
        # MIME type of the file content; only &quot;application/pdf&quot; and &quot;application/zip&quot; are currently allowed.
        self.mime_type: str = get_object(kwargs.get('mime_type'))
        # The URL of the file thumbnail, if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # Width of the thumbnail.
        self.thumbnail_width: int = get_object(kwargs.get('thumbnail_width'))
        # Height of the thumbnail.
        self.thumbnail_height: int = get_object(kwargs.get('thumbnail_height'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageDocument, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultGame(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Short name of the game.
        self.game_short_name: str = get_object(kwargs.get('game_short_name'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))


class InputInlineQueryResultLocation(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Location result.
        self.location: Location = get_object(kwargs.get('location'))
        # Amount of time relative to the message sent time until the location can be updated, in seconds.
        self.live_period: int = get_object(kwargs.get('live_period'))
        # Title of the result.
        self.title: str = get_object(kwargs.get('title'))
        # URL of the result thumbnail, if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # Thumbnail width, if known.
        self.thumbnail_width: int = get_object(kwargs.get('thumbnail_width'))
        # Thumbnail height, if known.
        self.thumbnail_height: int = get_object(kwargs.get('thumbnail_height'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultPhoto(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Title of the result, if known.
        self.title: str = get_object(kwargs.get('title'))
        # A short description of the result, if known.
        self.description: str = get_object(kwargs.get('description'))
        # URL of the photo thumbnail, if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # The URL of the JPEG photo (photo size must not exceed 5MB).
        self.photo_url: str = get_object(kwargs.get('photo_url'))
        # Width of the photo.
        self.photo_width: int = get_object(kwargs.get('photo_width'))
        # Height of the photo.
        self.photo_height: int = get_object(kwargs.get('photo_height'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessagePhoto, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultSticker(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # URL of the sticker thumbnail, if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # The URL of the WEBP, TGS, or WEBM sticker (sticker file size must not exceed 5MB).
        self.sticker_url: str = get_object(kwargs.get('sticker_url'))
        # Width of the sticker.
        self.sticker_width: int = get_object(kwargs.get('sticker_width'))
        # Height of the sticker.
        self.sticker_height: int = get_object(kwargs.get('sticker_height'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageSticker, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultVenue(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Venue result.
        self.venue: Venue = get_object(kwargs.get('venue'))
        # URL of the result thumbnail, if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # Thumbnail width, if known.
        self.thumbnail_width: int = get_object(kwargs.get('thumbnail_width'))
        # Thumbnail height, if known.
        self.thumbnail_height: int = get_object(kwargs.get('thumbnail_height'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultVideo(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Title of the result.
        self.title: str = get_object(kwargs.get('title'))
        # A short description of the result, if known.
        self.description: str = get_object(kwargs.get('description'))
        # The URL of the video thumbnail (JPEG), if it exists.
        self.thumbnail_url: str = get_object(kwargs.get('thumbnail_url'))
        # URL of the embedded video player or video file.
        self.video_url: str = get_object(kwargs.get('video_url'))
        # MIME type of the content of the video URL, only &quot;text/html&quot; or &quot;video/mp4&quot; are currently supported.
        self.mime_type: str = get_object(kwargs.get('mime_type'))
        # Width of the video.
        self.video_width: int = get_object(kwargs.get('video_width'))
        # Height of the video.
        self.video_height: int = get_object(kwargs.get('video_height'))
        # Video duration, in seconds.
        self.video_duration: int = get_object(kwargs.get('video_duration'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageVideo, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInlineQueryResultVoiceNote(InputInlineQueryResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the query result.
        self.id: str = get_object(kwargs.get('id'))
        # Title of the voice note.
        self.title: str = get_object(kwargs.get('title'))
        # The URL of the voice note file.
        self.voice_note_url: str = get_object(kwargs.get('voice_note_url'))
        # Duration of the voice note, in seconds.
        self.voice_note_duration: int = get_object(kwargs.get('voice_note_duration'))
        # The message reply markup; pass null if none. Must be of type replyMarkupInlineKeyboard or null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))
        # The content of the message to be sent. Must be one of the following types: inputMessageText, inputMessageVoiceNote, inputMessageInvoice, inputMessageLocation, inputMessageVenue or inputMessageContact.
        self.input_message_content: InputMessageContent = get_object(kwargs.get('input_message_content'))


class InputInvoice(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputInvoiceMessage(InputInvoice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier of the message.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))


class InputInvoiceName(InputInvoice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the invoice.
        self.name: str = get_object(kwargs.get('name'))


class MessageSelfDestructType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PollType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputThumbnail(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Thumbnail file to send. Sending thumbnails by file_id is currently not supported.
        self.thumbnail: InputFile = get_object(kwargs.get('thumbnail'))
        # Thumbnail width, usually shouldn't exceed 320. Use 0 if unknown.
        self.width: int = get_object(kwargs.get('width'))
        # Thumbnail height, usually shouldn't exceed 320. Use 0 if unknown.
        self.height: int = get_object(kwargs.get('height'))


class Invoice(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # ISO 4217 currency code.
        self.currency: str = get_object(kwargs.get('currency'))
        # A list of objects used to calculate the total price of the product.
        self.price_parts: list[LabeledPricePart] = get_object(kwargs.get('price_parts'))
        # The maximum allowed amount of tip in the smallest units of the currency.
        self.max_tip_amount: int = get_object(kwargs.get('max_tip_amount'))
        # Suggested amounts of tip in the smallest units of the currency.
        self.suggested_tip_amounts: list[int] = get_object(kwargs.get('suggested_tip_amounts'))
        # An HTTP URL with terms of service for recurring payments. If non-empty, the invoice payment will result in recurring payments and the user must accept the terms of service before allowed to pay.
        self.recurring_payment_terms_of_service_url: str = get_object(kwargs.get('recurring_payment_terms_of_service_url'))
        # True, if the payment is a test payment.
        self.is_test: bool = get_object(kwargs.get('is_test'))
        # True, if the user's name is needed for payment.
        self.need_name: bool = get_object(kwargs.get('need_name'))
        # True, if the user's phone number is needed for payment.
        self.need_phone_number: bool = get_object(kwargs.get('need_phone_number'))
        # True, if the user's email address is needed for payment.
        self.need_email_address: bool = get_object(kwargs.get('need_email_address'))
        # True, if the user's shipping address is needed for payment.
        self.need_shipping_address: bool = get_object(kwargs.get('need_shipping_address'))
        # True, if the user's phone number will be sent to the provider.
        self.send_phone_number_to_provider: bool = get_object(kwargs.get('send_phone_number_to_provider'))
        # True, if the user's email address will be sent to the provider.
        self.send_email_address_to_provider: bool = get_object(kwargs.get('send_email_address_to_provider'))
        # True, if the total price depends on the shipping method.
        self.is_flexible: bool = get_object(kwargs.get('is_flexible'))


class MessageCopyOptions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if content of the message needs to be copied without reference to the original sender. Always true if the message is forwarded to a secret chat or is local.
        self.send_copy: bool = get_object(kwargs.get('send_copy'))
        # True, if media caption of the message copy needs to be replaced. Ignored if send_copy is false.
        self.replace_caption: bool = get_object(kwargs.get('replace_caption'))
        # New message caption; pass null to copy message without caption. Ignored if replace_caption is false.
        self.new_caption: FormattedText = get_object(kwargs.get('new_caption'))


class InputMessageText(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Formatted text to be sent; 1-getOption(&quot;message_text_length_max&quot;) characters. Only Bold, Italic, Underline, Strikethrough, Spoiler, CustomEmoji, Code, Pre, PreCode, TextUrl and MentionName entities are allowed to be specified manually.
        self.text: FormattedText = get_object(kwargs.get('text'))
        # True, if rich web page previews for URLs in the message text must be disabled.
        self.disable_web_page_preview: bool = get_object(kwargs.get('disable_web_page_preview'))
        # True, if a chat message draft must be deleted.
        self.clear_draft: bool = get_object(kwargs.get('clear_draft'))


class InputMessageAnimation(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Animation file to be sent.
        self.animation: InputFile = get_object(kwargs.get('animation'))
        # Animation thumbnail; pass null to skip thumbnail uploading.
        self.thumbnail: InputThumbnail = get_object(kwargs.get('thumbnail'))
        # File identifiers of the stickers added to the animation, if applicable.
        self.added_sticker_file_ids: list[int] = get_object(kwargs.get('added_sticker_file_ids'))
        # Duration of the animation, in seconds.
        self.duration: int = get_object(kwargs.get('duration'))
        # Width of the animation; may be replaced by the server.
        self.width: int = get_object(kwargs.get('width'))
        # Height of the animation; may be replaced by the server.
        self.height: int = get_object(kwargs.get('height'))
        # Animation caption; pass null to use an empty caption; 0-getOption(&quot;message_caption_length_max&quot;) characters.
        self.caption: FormattedText = get_object(kwargs.get('caption'))
        # True, if the animation preview must be covered by a spoiler animation; not supported in secret chats.
        self.has_spoiler: bool = get_object(kwargs.get('has_spoiler'))


class InputMessageAudio(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Audio file to be sent.
        self.audio: InputFile = get_object(kwargs.get('audio'))
        # Thumbnail of the cover for the album; pass null to skip thumbnail uploading.
        self.album_cover_thumbnail: InputThumbnail = get_object(kwargs.get('album_cover_thumbnail'))
        # Duration of the audio, in seconds; may be replaced by the server.
        self.duration: int = get_object(kwargs.get('duration'))
        # Title of the audio; 0-64 characters; may be replaced by the server.
        self.title: str = get_object(kwargs.get('title'))
        # Performer of the audio; 0-64 characters, may be replaced by the server.
        self.performer: str = get_object(kwargs.get('performer'))
        # Audio caption; pass null to use an empty caption; 0-getOption(&quot;message_caption_length_max&quot;) characters.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class InputMessageDocument(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Document to be sent.
        self.document: InputFile = get_object(kwargs.get('document'))
        # Document thumbnail; pass null to skip thumbnail uploading.
        self.thumbnail: InputThumbnail = get_object(kwargs.get('thumbnail'))
        # If true, automatic file type detection will be disabled and the document will always be sent as file. Always true for files sent to secret chats.
        self.disable_content_type_detection: bool = get_object(kwargs.get('disable_content_type_detection'))
        # Document caption; pass null to use an empty caption; 0-getOption(&quot;message_caption_length_max&quot;) characters.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class InputMessagePhoto(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Photo to send. The photo must be at most 10 MB in size. The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20.
        self.photo: InputFile = get_object(kwargs.get('photo'))
        # Photo thumbnail to be sent; pass null to skip thumbnail uploading. The thumbnail is sent to the other party only in secret chats.
        self.thumbnail: InputThumbnail = get_object(kwargs.get('thumbnail'))
        # File identifiers of the stickers added to the photo, if applicable.
        self.added_sticker_file_ids: list[int] = get_object(kwargs.get('added_sticker_file_ids'))
        # Photo width.
        self.width: int = get_object(kwargs.get('width'))
        # Photo height.
        self.height: int = get_object(kwargs.get('height'))
        # Photo caption; pass null to use an empty caption; 0-getOption(&quot;message_caption_length_max&quot;) characters.
        self.caption: FormattedText = get_object(kwargs.get('caption'))
        # Photo self-destruct type; pass null if none; private chats only.
        self.self_destruct_type: MessageSelfDestructType = get_object(kwargs.get('self_destruct_type'))
        # True, if the photo preview must be covered by a spoiler animation; not supported in secret chats.
        self.has_spoiler: bool = get_object(kwargs.get('has_spoiler'))


class InputMessageSticker(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Sticker to be sent.
        self.sticker: InputFile = get_object(kwargs.get('sticker'))
        # Sticker thumbnail; pass null to skip thumbnail uploading.
        self.thumbnail: InputThumbnail = get_object(kwargs.get('thumbnail'))
        # Sticker width.
        self.width: int = get_object(kwargs.get('width'))
        # Sticker height.
        self.height: int = get_object(kwargs.get('height'))
        # Emoji used to choose the sticker.
        self.emoji: str = get_object(kwargs.get('emoji'))


class InputMessageVideo(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Video to be sent.
        self.video: InputFile = get_object(kwargs.get('video'))
        # Video thumbnail; pass null to skip thumbnail uploading.
        self.thumbnail: InputThumbnail = get_object(kwargs.get('thumbnail'))
        # File identifiers of the stickers added to the video, if applicable.
        self.added_sticker_file_ids: list[int] = get_object(kwargs.get('added_sticker_file_ids'))
        # Duration of the video, in seconds.
        self.duration: int = get_object(kwargs.get('duration'))
        # Video width.
        self.width: int = get_object(kwargs.get('width'))
        # Video height.
        self.height: int = get_object(kwargs.get('height'))
        # True, if the video is supposed to be streamed.
        self.supports_streaming: bool = get_object(kwargs.get('supports_streaming'))
        # Video caption; pass null to use an empty caption; 0-getOption(&quot;message_caption_length_max&quot;) characters.
        self.caption: FormattedText = get_object(kwargs.get('caption'))
        # Video self-destruct type; pass null if none; private chats only.
        self.self_destruct_type: MessageSelfDestructType = get_object(kwargs.get('self_destruct_type'))
        # True, if the video preview must be covered by a spoiler animation; not supported in secret chats.
        self.has_spoiler: bool = get_object(kwargs.get('has_spoiler'))


class InputMessageVideoNote(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Video note to be sent.
        self.video_note: InputFile = get_object(kwargs.get('video_note'))
        # Video thumbnail; pass null to skip thumbnail uploading.
        self.thumbnail: InputThumbnail = get_object(kwargs.get('thumbnail'))
        # Duration of the video, in seconds.
        self.duration: int = get_object(kwargs.get('duration'))
        # Video width and height; must be positive and not greater than 640.
        self.length: int = get_object(kwargs.get('length'))


class InputMessageVoiceNote(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Voice note to be sent.
        self.voice_note: InputFile = get_object(kwargs.get('voice_note'))
        # Duration of the voice note, in seconds.
        self.duration: int = get_object(kwargs.get('duration'))
        # Waveform representation of the voice note in 5-bit format.
        self.waveform: bytes = get_object(kwargs.get('waveform'))
        # Voice note caption; pass null to use an empty caption; 0-getOption(&quot;message_caption_length_max&quot;) characters.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class InputMessageLocation(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Location to be sent.
        self.location: Location = get_object(kwargs.get('location'))
        # Period for which the location can be updated, in seconds; must be between 60 and 86400 for a live location and 0 otherwise.
        self.live_period: int = get_object(kwargs.get('live_period'))
        # For live locations, a direction in which the location moves, in degrees; 1-360. Pass 0 if unknown.
        self.heading: int = get_object(kwargs.get('heading'))
        # For live locations, a maximum distance to another chat member for proximity alerts, in meters (0-100000). Pass 0 if the notification is disabled. Can't be enabled in channels and Saved Messages.
        self.proximity_alert_radius: int = get_object(kwargs.get('proximity_alert_radius'))


class InputMessageVenue(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Venue to send.
        self.venue: Venue = get_object(kwargs.get('venue'))


class InputMessageContact(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Contact to send.
        self.contact: Contact = get_object(kwargs.get('contact'))


class InputMessageDice(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Emoji on which the dice throw animation is based.
        self.emoji: str = get_object(kwargs.get('emoji'))
        # True, if the chat message draft must be deleted.
        self.clear_draft: bool = get_object(kwargs.get('clear_draft'))


class InputMessageGame(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the bot that owns the game.
        self.bot_user_id: int = get_object(kwargs.get('bot_user_id'))
        # Short name of the game.
        self.game_short_name: str = get_object(kwargs.get('game_short_name'))


class InputMessageInvoice(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Invoice.
        self.invoice: Invoice = get_object(kwargs.get('invoice'))
        # Product title; 1-32 characters.
        self.title: str = get_object(kwargs.get('title'))
        # Product description; 0-255 characters.
        self.description: str = get_object(kwargs.get('description'))
        # Product photo URL; optional.
        self.photo_url: str = get_object(kwargs.get('photo_url'))
        # Product photo size.
        self.photo_size: int = get_object(kwargs.get('photo_size'))
        # Product photo width.
        self.photo_width: int = get_object(kwargs.get('photo_width'))
        # Product photo height.
        self.photo_height: int = get_object(kwargs.get('photo_height'))
        # The invoice payload.
        self.payload: bytes = get_object(kwargs.get('payload'))
        # Payment provider token.
        self.provider_token: str = get_object(kwargs.get('provider_token'))
        # JSON-encoded data about the invoice, which will be shared with the payment provider.
        self.provider_data: str = get_object(kwargs.get('provider_data'))
        # Unique invoice bot deep link parameter for the generation of this invoice. If empty, it would be possible to pay directly from forwards of the invoice message.
        self.start_parameter: str = get_object(kwargs.get('start_parameter'))
        # The content of extended media attached to the invoice. The content of the message to be sent. Must be one of the following types: inputMessagePhoto, inputMessageVideo.
        self.extended_media_content: InputMessageContent = get_object(kwargs.get('extended_media_content'))


class InputMessagePoll(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Poll question; 1-255 characters (up to 300 characters for bots).
        self.question: str = get_object(kwargs.get('question'))
        # List of poll answer options, 2-10 strings 1-100 characters each.
        self.options: list[str] = get_object(kwargs.get('options'))
        # True, if the poll voters are anonymous. Non-anonymous polls can't be sent or forwarded to channels.
        self.is_anonymous: bool = get_object(kwargs.get('is_anonymous'))
        # Type of the poll.
        self.type: PollType = get_object(kwargs.get('type'))
        # Amount of time the poll will be active after creation, in seconds; for bots only.
        self.open_period: int = get_object(kwargs.get('open_period'))
        # Point in time (Unix timestamp) when the poll will automatically be closed; for bots only.
        self.close_date: int = get_object(kwargs.get('close_date'))
        # True, if the poll needs to be sent already closed; for bots only.
        self.is_closed: bool = get_object(kwargs.get('is_closed'))


class InputMessageStory(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat that posted the story.
        self.story_sender_chat_id: int = get_object(kwargs.get('story_sender_chat_id'))
        # Story identifier.
        self.story_id: int = get_object(kwargs.get('story_id'))


class InputMessageForwarded(InputMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier for the chat this forwarded message came from.
        self.from_chat_id: int = get_object(kwargs.get('from_chat_id'))
        # Identifier of the message to forward.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # True, if a game message is being shared from a launched game; applies only to game messages.
        self.in_game_share: bool = get_object(kwargs.get('in_game_share'))
        # Options to be used to copy content of the message without reference to the original sender; pass null to forward the message as usual.
        self.copy_options: MessageCopyOptions = get_object(kwargs.get('copy_options'))


class InputPersonalDocument(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of files containing the pages of the document.
        self.files: list[InputFile] = get_object(kwargs.get('files'))
        # List of files containing a certified English translation of the document.
        self.translation: list[InputFile] = get_object(kwargs.get('translation'))


class PersonalDetails(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # First name of the user written in English; 1-255 characters.
        self.first_name: str = get_object(kwargs.get('first_name'))
        # Middle name of the user written in English; 0-255 characters.
        self.middle_name: str = get_object(kwargs.get('middle_name'))
        # Last name of the user written in English; 1-255 characters.
        self.last_name: str = get_object(kwargs.get('last_name'))
        # Native first name of the user; 1-255 characters.
        self.native_first_name: str = get_object(kwargs.get('native_first_name'))
        # Native middle name of the user; 0-255 characters.
        self.native_middle_name: str = get_object(kwargs.get('native_middle_name'))
        # Native last name of the user; 1-255 characters.
        self.native_last_name: str = get_object(kwargs.get('native_last_name'))
        # Birthdate of the user.
        self.birthdate: Date = get_object(kwargs.get('birthdate'))
        # Gender of the user, &quot;male&quot; or &quot;female&quot;.
        self.gender: str = get_object(kwargs.get('gender'))
        # A two-letter ISO 3166-1 alpha-2 country code of the user's country.
        self.country_code: str = get_object(kwargs.get('country_code'))
        # A two-letter ISO 3166-1 alpha-2 country code of the user's residence country.
        self.residence_country_code: str = get_object(kwargs.get('residence_country_code'))


class InputPassportElement(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputPassportElementPersonalDetails(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Personal details of the user.
        self.personal_details: PersonalDetails = get_object(kwargs.get('personal_details'))


class InputPassportElementPassport(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The passport to be saved.
        self.passport: InputIdentityDocument = get_object(kwargs.get('passport'))


class InputPassportElementDriverLicense(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The driver license to be saved.
        self.driver_license: InputIdentityDocument = get_object(kwargs.get('driver_license'))


class InputPassportElementIdentityCard(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The identity card to be saved.
        self.identity_card: InputIdentityDocument = get_object(kwargs.get('identity_card'))


class InputPassportElementInternalPassport(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The internal passport to be saved.
        self.internal_passport: InputIdentityDocument = get_object(kwargs.get('internal_passport'))


class InputPassportElementAddress(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The address to be saved.
        self.address: Address = get_object(kwargs.get('address'))


class InputPassportElementUtilityBill(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The utility bill to be saved.
        self.utility_bill: InputPersonalDocument = get_object(kwargs.get('utility_bill'))


class InputPassportElementBankStatement(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The bank statement to be saved.
        self.bank_statement: InputPersonalDocument = get_object(kwargs.get('bank_statement'))


class InputPassportElementRentalAgreement(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The rental agreement to be saved.
        self.rental_agreement: InputPersonalDocument = get_object(kwargs.get('rental_agreement'))


class InputPassportElementPassportRegistration(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The passport registration page to be saved.
        self.passport_registration: InputPersonalDocument = get_object(kwargs.get('passport_registration'))


class InputPassportElementTemporaryRegistration(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The temporary registration document to be saved.
        self.temporary_registration: InputPersonalDocument = get_object(kwargs.get('temporary_registration'))


class InputPassportElementPhoneNumber(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The phone number to be saved.
        self.phone_number: str = get_object(kwargs.get('phone_number'))


class InputPassportElementEmailAddress(InputPassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The email address to be saved.
        self.email_address: str = get_object(kwargs.get('email_address'))


class InputPassportElementErrorSource(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputPassportElementError(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of Telegram Passport element that has the error.
        self.type: PassportElementType = get_object(kwargs.get('type'))
        # Error message.
        self.message: str = get_object(kwargs.get('message'))
        # Error source.
        self.source: InputPassportElementErrorSource = get_object(kwargs.get('source'))


class InputPassportElementErrorSourceUnspecified(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Current hash of the entire element.
        self.element_hash: bytes = get_object(kwargs.get('element_hash'))


class InputPassportElementErrorSourceDataField(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Field name.
        self.field_name: str = get_object(kwargs.get('field_name'))
        # Current data hash.
        self.data_hash: bytes = get_object(kwargs.get('data_hash'))


class InputPassportElementErrorSourceFrontSide(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Current hash of the file containing the front side.
        self.file_hash: bytes = get_object(kwargs.get('file_hash'))


class InputPassportElementErrorSourceReverseSide(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Current hash of the file containing the reverse side.
        self.file_hash: bytes = get_object(kwargs.get('file_hash'))


class InputPassportElementErrorSourceSelfie(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Current hash of the file containing the selfie.
        self.file_hash: bytes = get_object(kwargs.get('file_hash'))


class InputPassportElementErrorSourceTranslationFile(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Current hash of the file containing the translation.
        self.file_hash: bytes = get_object(kwargs.get('file_hash'))


class InputPassportElementErrorSourceTranslationFiles(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Current hashes of all files with the translation.
        self.file_hashes: list[bytes] = get_object(kwargs.get('file_hashes'))


class InputPassportElementErrorSourceFile(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Current hash of the file which has the error.
        self.file_hash: bytes = get_object(kwargs.get('file_hash'))


class InputPassportElementErrorSourceFiles(InputPassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Current hashes of all attached files.
        self.file_hashes: list[bytes] = get_object(kwargs.get('file_hashes'))


class MaskPosition(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Part of the face, relative to which the mask is placed.
        self.point: MaskPoint = get_object(kwargs.get('point'))
        # Shift by X-axis measured in widths of the mask scaled to the face size, from left to right. (For example, -1.0 will place the mask just to the left of the default mask position.)
        self.x_shift: float = get_object(kwargs.get('x_shift'))
        # Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom. (For example, 1.0 will place the mask just below the default mask position.)
        self.y_shift: float = get_object(kwargs.get('y_shift'))
        # Mask scaling coefficient. (For example, 2.0 means a doubled size.)
        self.scale: float = get_object(kwargs.get('scale'))


class InputSticker(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # File with the sticker; must fit in a 512x512 square. For WEBP stickers the file must be in WEBP or PNG format, which will be converted to WEBP server-side. See https://core.telegram.org/animated_stickers\#technical-requirements for technical requirements.
        self.sticker: InputFile = get_object(kwargs.get('sticker'))
        # String with 1-20 emoji corresponding to the sticker.
        self.emojis: str = get_object(kwargs.get('emojis'))
        # Position where the mask is placed; pass null if not specified.
        self.mask_position: MaskPosition = get_object(kwargs.get('mask_position'))
        # List of up to 20 keywords with total length up to 64 characters, which can be used to find the sticker.
        self.keywords: list[str] = get_object(kwargs.get('keywords'))


class InputStoryAreaType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryAreaPosition(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The abscissa of the rectangle's center, as a percentage of the media width.
        self.x_percentage: float = get_object(kwargs.get('x_percentage'))
        # The ordinate of the rectangle's center, as a percentage of the media height.
        self.y_percentage: float = get_object(kwargs.get('y_percentage'))
        # The width of the rectangle, as a percentage of the media width.
        self.width_percentage: float = get_object(kwargs.get('width_percentage'))
        # The ordinate of the rectangle's center, as a percentage of the media height.
        self.height_percentage: float = get_object(kwargs.get('height_percentage'))
        # Clockwise rotation angle of the rectangle, in degrees; 0-360.
        self.rotation_angle: float = get_object(kwargs.get('rotation_angle'))


class InputStoryArea(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Position of the area.
        self.position: StoryAreaPosition = get_object(kwargs.get('position'))
        # Type of the area.
        self.type: InputStoryAreaType = get_object(kwargs.get('type'))


class InputStoryAreaTypeLocation(InputStoryAreaType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The location.
        self.location: Location = get_object(kwargs.get('location'))


class InputStoryAreaTypeFoundVenue(InputStoryAreaType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the inline query, used to found the venue.
        self.query_id: int = get_object(kwargs.get('query_id'))
        # Identifier of the inline query result.
        self.result_id: str = get_object(kwargs.get('result_id'))


class InputStoryAreaTypePreviousVenue(InputStoryAreaType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Provider of the venue.
        self.venue_provider: str = get_object(kwargs.get('venue_provider'))
        # Identifier of the venue in the provider database.
        self.venue_id: str = get_object(kwargs.get('venue_id'))


class InputStoryAreas(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of 0-10 input story areas.
        self.areas: list[InputStoryArea] = get_object(kwargs.get('areas'))


class InputStoryContent(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InputStoryContentPhoto(InputStoryContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Photo to send. The photo must be at most 10 MB in size. The photo size must be 1080x1920.
        self.photo: InputFile = get_object(kwargs.get('photo'))
        # File identifiers of the stickers added to the photo, if applicable.
        self.added_sticker_file_ids: list[int] = get_object(kwargs.get('added_sticker_file_ids'))


class InputStoryContentVideo(InputStoryContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Video to be sent. The video size must be 720x1280. The video must be streamable and stored in MPEG4 format, after encoding with x265 codec and key frames added each second.
        self.video: InputFile = get_object(kwargs.get('video'))
        # File identifiers of the stickers added to the video, if applicable.
        self.added_sticker_file_ids: list[int] = get_object(kwargs.get('added_sticker_file_ids'))
        # Precise duration of the video, in seconds; 0-60.
        self.duration: float = get_object(kwargs.get('duration'))
        # True, if the video has no sound.
        self.is_animation: bool = get_object(kwargs.get('is_animation'))


class ProxyType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeActiveSessions(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeAttachmentMenuBot(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Target chat to be opened.
        self.target_chat: TargetChat = get_object(kwargs.get('target_chat'))
        # Username of the bot.
        self.bot_username: str = get_object(kwargs.get('bot_username'))
        # URL to be passed to openWebApp.
        self.url: str = get_object(kwargs.get('url'))


class InternalLinkTypeAuthenticationCode(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The authentication code.
        self.code: str = get_object(kwargs.get('code'))


class InternalLinkTypeBackground(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the background.
        self.background_name: str = get_object(kwargs.get('background_name'))


class InternalLinkTypeBotAddToChannel(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the bot.
        self.bot_username: str = get_object(kwargs.get('bot_username'))
        # Expected administrator rights for the bot.
        self.administrator_rights: ChatAdministratorRights = get_object(kwargs.get('administrator_rights'))


class InternalLinkTypeBotStart(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the bot.
        self.bot_username: str = get_object(kwargs.get('bot_username'))
        # The parameter to be passed to sendBotStartMessage.
        self.start_parameter: str = get_object(kwargs.get('start_parameter'))
        # True, if sendBotStartMessage must be called automatically without showing the START button.
        self.autostart: bool = get_object(kwargs.get('autostart'))


class InternalLinkTypeBotStartInGroup(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the bot.
        self.bot_username: str = get_object(kwargs.get('bot_username'))
        # The parameter to be passed to sendBotStartMessage.
        self.start_parameter: str = get_object(kwargs.get('start_parameter'))
        # Expected administrator rights for the bot; may be null.
        self.administrator_rights: ChatAdministratorRights = get_object(kwargs.get('administrator_rights'))


class InternalLinkTypeChangePhoneNumber(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeChatFilterInvite(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Internal representation of the invite link.
        self.invite_link: str = get_object(kwargs.get('invite_link'))


class InternalLinkTypeChatFilterSettings(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeChatInvite(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Internal representation of the invite link.
        self.invite_link: str = get_object(kwargs.get('invite_link'))


class InternalLinkTypeDefaultMessageAutoDeleteTimerSettings(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeEditProfileSettings(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeGame(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the bot that owns the game.
        self.bot_username: str = get_object(kwargs.get('bot_username'))
        # Short name of the game.
        self.game_short_name: str = get_object(kwargs.get('game_short_name'))


class InternalLinkTypeInstantView(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # URL to be passed to getWebPageInstantView.
        self.url: str = get_object(kwargs.get('url'))
        # An URL to open if getWebPageInstantView fails.
        self.fallback_url: str = get_object(kwargs.get('fallback_url'))


class InternalLinkTypeInvoice(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the invoice.
        self.invoice_name: str = get_object(kwargs.get('invoice_name'))


class InternalLinkTypeLanguagePack(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Language pack identifier.
        self.language_pack_id: str = get_object(kwargs.get('language_pack_id'))


class InternalLinkTypeLanguageSettings(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeMessage(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # URL to be passed to getMessageLinkInfo.
        self.url: str = get_object(kwargs.get('url'))


class InternalLinkTypeMessageDraft(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message draft text.
        self.text: FormattedText = get_object(kwargs.get('text'))
        # True, if the first line of the text contains a link. If true, the input field needs to be focused and the text after the link must be selected.
        self.contains_link: bool = get_object(kwargs.get('contains_link'))


class InternalLinkTypePassportDataRequest(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the service's bot.
        self.bot_user_id: int = get_object(kwargs.get('bot_user_id'))
        # Telegram Passport element types requested by the service.
        self.scope: str = get_object(kwargs.get('scope'))
        # Service's public key.
        self.public_key: str = get_object(kwargs.get('public_key'))
        # Unique request identifier provided by the service.
        self.nonce: str = get_object(kwargs.get('nonce'))
        # An HTTP URL to open once the request is finished, canceled, or failed with the parameters tg_passport=success, tg_passport=cancel, or tg_passport=error&amp;error=... respectively. If empty, then onActivityResult method must be used to return response on Android, or the link tgbot{bot_user_id}://passport/success or tgbot{bot_user_id}://passport/cancel must be opened otherwise.
        self.callback_url: str = get_object(kwargs.get('callback_url'))


class InternalLinkTypePhoneNumberConfirmation(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Hash value from the link.
        self.hash: str = get_object(kwargs.get('hash'))
        # Phone number value from the link.
        self.phone_number: str = get_object(kwargs.get('phone_number'))


class InternalLinkTypePremiumFeatures(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Referrer specified in the link.
        self.referrer: str = get_object(kwargs.get('referrer'))


class InternalLinkTypePrivacyAndSecuritySettings(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeProxy(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Proxy server domain or IP address.
        self.server: str = get_object(kwargs.get('server'))
        # Proxy server port.
        self.port: int = get_object(kwargs.get('port'))
        # Type of the proxy.
        self.type: ProxyType = get_object(kwargs.get('type'))


class InternalLinkTypePublicChat(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the chat.
        self.chat_username: str = get_object(kwargs.get('chat_username'))


class InternalLinkTypeQrCodeAuthentication(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeRestorePurchases(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeSettings(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeSideMenuBot(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the bot.
        self.bot_username: str = get_object(kwargs.get('bot_username'))
        # URL to be passed to getWebAppUrl.
        self.url: str = get_object(kwargs.get('url'))


class InternalLinkTypeStickerSet(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the sticker set.
        self.sticker_set_name: str = get_object(kwargs.get('sticker_set_name'))
        # True, if the sticker set is expected to contain custom emoji.
        self.expect_custom_emoji: bool = get_object(kwargs.get('expect_custom_emoji'))


class InternalLinkTypeStory(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the sender of the story.
        self.story_sender_username: str = get_object(kwargs.get('story_sender_username'))
        # Story identifier.
        self.story_id: int = get_object(kwargs.get('story_id'))


class InternalLinkTypeTheme(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the theme.
        self.theme_name: str = get_object(kwargs.get('theme_name'))


class InternalLinkTypeThemeSettings(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeUnknownDeepLink(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Link to be passed to getDeepLinkInfo.
        self.link: str = get_object(kwargs.get('link'))


class InternalLinkTypeUnsupportedProxy(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InternalLinkTypeUserPhoneNumber(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Phone number of the user.
        self.phone_number: str = get_object(kwargs.get('phone_number'))


class InternalLinkTypeUserToken(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The token.
        self.token: str = get_object(kwargs.get('token'))


class InternalLinkTypeVideoChat(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the chat with the video chat.
        self.chat_username: str = get_object(kwargs.get('chat_username'))
        # If non-empty, invite hash to be used to join the video chat without being muted by administrators.
        self.invite_hash: str = get_object(kwargs.get('invite_hash'))
        # True, if the video chat is expected to be a live stream in a channel or a broadcast group.
        self.is_live_stream: bool = get_object(kwargs.get('is_live_stream'))


class InternalLinkTypeWebApp(InternalLinkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username of the bot that owns the Web App.
        self.bot_username: str = get_object(kwargs.get('bot_username'))
        # Short name of the Web App.
        self.web_app_short_name: str = get_object(kwargs.get('web_app_short_name'))
        # Start parameter to be passed to getWebAppLinkUrl.
        self.start_parameter: str = get_object(kwargs.get('start_parameter'))


class InviteLinkChatTypeBasicGroup(InviteLinkChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InviteLinkChatTypeSupergroup(InviteLinkChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class InviteLinkChatTypeChannel(InviteLinkChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class LabeledPricePart(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Label for this portion of the product price.
        self.label: str = get_object(kwargs.get('label'))
        # Currency amount in the smallest units of the currency.
        self.amount: int = get_object(kwargs.get('amount'))


class JsonValue(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class JsonObjectMember(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Member's key.
        self.key: str = get_object(kwargs.get('key'))
        # Member's value.
        self.value: JsonValue = get_object(kwargs.get('value'))


class JsonValueNull(JsonValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class JsonValueBoolean(JsonValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The value.
        self.value: bool = get_object(kwargs.get('value'))


class JsonValueNumber(JsonValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The value.
        self.value: float = get_object(kwargs.get('value'))


class JsonValueString(JsonValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The value.
        self.value: str = get_object(kwargs.get('value'))


class JsonValueArray(JsonValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The list of array elements.
        self.values: list[JsonValue] = get_object(kwargs.get('values'))


class JsonValueObject(JsonValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The list of object members.
        self.members: list[JsonObjectMember] = get_object(kwargs.get('members'))


class KeyboardButtonType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class KeyboardButton(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the button.
        self.text: str = get_object(kwargs.get('text'))
        # Type of the button.
        self.type: KeyboardButtonType = get_object(kwargs.get('type'))


class KeyboardButtonTypeText(KeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class KeyboardButtonTypeRequestPhoneNumber(KeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class KeyboardButtonTypeRequestLocation(KeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class KeyboardButtonTypeRequestPoll(KeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # If true, only regular polls must be allowed to create.
        self.force_regular: bool = get_object(kwargs.get('force_regular'))
        # If true, only polls in quiz mode must be allowed to create.
        self.force_quiz: bool = get_object(kwargs.get('force_quiz'))


class KeyboardButtonTypeRequestUser(KeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique button identifier.
        self.id: int = get_object(kwargs.get('id'))
        # True, if the shared user must or must not be a bot.
        self.restrict_user_is_bot: bool = get_object(kwargs.get('restrict_user_is_bot'))
        # True, if the shared user must be a bot; otherwise, the shared user must no be a bot. Ignored if restrict_user_is_bot is false.
        self.user_is_bot: bool = get_object(kwargs.get('user_is_bot'))
        # True, if the shared user must or must not be a Telegram Premium user.
        self.restrict_user_is_premium: bool = get_object(kwargs.get('restrict_user_is_premium'))
        # True, if the shared user must be a Telegram Premium user; otherwise, the shared user must no be a Telegram Premium user. Ignored if restrict_user_is_premium is false.
        self.user_is_premium: bool = get_object(kwargs.get('user_is_premium'))


class KeyboardButtonTypeRequestChat(KeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique button identifier.
        self.id: int = get_object(kwargs.get('id'))
        # True, if the chat must be a channel; otherwise, a basic group or a supergroup chat is shared.
        self.chat_is_channel: bool = get_object(kwargs.get('chat_is_channel'))
        # True, if the chat must or must not be a forum supergroup.
        self.restrict_chat_is_forum: bool = get_object(kwargs.get('restrict_chat_is_forum'))
        # True, if the chat must be a forum supergroup; otherwise, the chat must not be a forum supergroup. Ignored if restrict_chat_is_forum is false.
        self.chat_is_forum: bool = get_object(kwargs.get('chat_is_forum'))
        # True, if the chat must or must not have a username.
        self.restrict_chat_has_username: bool = get_object(kwargs.get('restrict_chat_has_username'))
        # True, if the chat must have a username; otherwise, the chat must not have a username. Ignored if restrict_chat_has_username is false.
        self.chat_has_username: bool = get_object(kwargs.get('chat_has_username'))
        # True, if the chat must be created by the current user.
        self.chat_is_created: bool = get_object(kwargs.get('chat_is_created'))
        # Expected user administrator rights in the chat; may be null if they aren't restricted.
        self.user_administrator_rights: ChatAdministratorRights = get_object(kwargs.get('user_administrator_rights'))
        # Expected bot administrator rights in the chat; may be null if they aren't restricted.
        self.bot_administrator_rights: ChatAdministratorRights = get_object(kwargs.get('bot_administrator_rights'))
        # True, if the bot must be a member of the chat; for basic group and supergroup chats only.
        self.bot_is_member: bool = get_object(kwargs.get('bot_is_member'))


class KeyboardButtonTypeWebApp(KeyboardButtonType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # An HTTP URL to pass to getWebAppUrl.
        self.url: str = get_object(kwargs.get('url'))


class LanguagePackInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique language pack identifier.
        self.id: str = get_object(kwargs.get('id'))
        # Identifier of a base language pack; may be empty. If a string is missed in the language pack, then it must be fetched from base language pack. Unsupported in custom language packs.
        self.base_language_pack_id: str = get_object(kwargs.get('base_language_pack_id'))
        # Language name.
        self.name: str = get_object(kwargs.get('name'))
        # Name of the language in that language.
        self.native_name: str = get_object(kwargs.get('native_name'))
        # A language code to be used to apply plural forms. See https://www.unicode.org/cldr/charts/latest/supplemental/language_plural_rules.html for more information.
        self.plural_code: str = get_object(kwargs.get('plural_code'))
        # True, if the language pack is official.
        self.is_official: bool = get_object(kwargs.get('is_official'))
        # True, if the language pack strings are RTL.
        self.is_rtl: bool = get_object(kwargs.get('is_rtl'))
        # True, if the language pack is a beta language pack.
        self.is_beta: bool = get_object(kwargs.get('is_beta'))
        # True, if the language pack is installed by the current user.
        self.is_installed: bool = get_object(kwargs.get('is_installed'))
        # Total number of non-deleted strings from the language pack.
        self.total_string_count: int = get_object(kwargs.get('total_string_count'))
        # Total number of translated strings from the language pack.
        self.translated_string_count: int = get_object(kwargs.get('translated_string_count'))
        # Total number of non-deleted strings from the language pack available locally.
        self.local_string_count: int = get_object(kwargs.get('local_string_count'))
        # Link to language translation interface; empty for custom local language packs.
        self.translation_url: str = get_object(kwargs.get('translation_url'))


class LanguagePackStringValue(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class LanguagePackString(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # String key.
        self.key: str = get_object(kwargs.get('key'))
        # String value; pass null if the string needs to be taken from the built-in English language pack.
        self.value: LanguagePackStringValue = get_object(kwargs.get('value'))


class LanguagePackStringValueOrdinary(LanguagePackStringValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # String value.
        self.value: str = get_object(kwargs.get('value'))


class LanguagePackStringValuePluralized(LanguagePackStringValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Value for zero objects.
        self.zero_value: str = get_object(kwargs.get('zero_value'))
        # Value for one object.
        self.one_value: str = get_object(kwargs.get('one_value'))
        # Value for two objects.
        self.two_value: str = get_object(kwargs.get('two_value'))
        # Value for few objects.
        self.few_value: str = get_object(kwargs.get('few_value'))
        # Value for many objects.
        self.many_value: str = get_object(kwargs.get('many_value'))
        # Default value.
        self.other_value: str = get_object(kwargs.get('other_value'))


class LanguagePackStringValueDeleted(LanguagePackStringValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class LanguagePackStrings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of language pack strings.
        self.strings: list[LanguagePackString] = get_object(kwargs.get('strings'))


class LocalizationTargetInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of available language packs for this application.
        self.language_packs: list[LanguagePackInfo] = get_object(kwargs.get('language_packs'))


class LogStream(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class LogStreamDefault(LogStream):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class LogStreamFile(LogStream):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Path to the file to where the internal TDLib log will be written.
        self.path: str = get_object(kwargs.get('path'))
        # The maximum size of the file to where the internal TDLib log is written before the file will automatically be rotated, in bytes.
        self.max_file_size: int = get_object(kwargs.get('max_file_size'))
        # Pass true to additionally redirect stderr to the log file. Ignored on Windows.
        self.redirect_stderr: bool = get_object(kwargs.get('redirect_stderr'))


class LogStreamEmpty(LogStream):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class LogTags(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of log tags.
        self.tags: list[str] = get_object(kwargs.get('tags'))


class LogVerbosityLevel(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Log verbosity level.
        self.verbosity_level: int = get_object(kwargs.get('verbosity_level'))


class LoginUrlInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class LoginUrlInfoOpen(LoginUrlInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The URL to open.
        self.url: str = get_object(kwargs.get('url'))
        # True, if there is no need to show an ordinary open URL confirmation.
        self.skip_confirmation: bool = get_object(kwargs.get('skip_confirmation'))


class LoginUrlInfoRequestConfirmation(LoginUrlInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # An HTTP URL to be opened.
        self.url: str = get_object(kwargs.get('url'))
        # A domain of the URL.
        self.domain: str = get_object(kwargs.get('domain'))
        # User identifier of a bot linked with the website.
        self.bot_user_id: int = get_object(kwargs.get('bot_user_id'))
        # True, if the user must be asked for the permission to the bot to send them messages.
        self.request_write_access: bool = get_object(kwargs.get('request_write_access'))


class MaskPoint(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MaskPointForehead(MaskPoint):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MaskPointEyes(MaskPoint):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MaskPointMouth(MaskPoint):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MaskPointChin(MaskPoint):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageContent(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageReplyTo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSchedulingState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSendingState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageForwardInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Origin of a forwarded message.
        self.origin: MessageForwardOrigin = get_object(kwargs.get('origin'))
        # Point in time (Unix timestamp) when the message was originally sent.
        self.date: int = get_object(kwargs.get('date'))
        # The type of a public service announcement for the forwarded message.
        self.public_service_announcement_type: str = get_object(kwargs.get('public_service_announcement_type'))
        # For messages forwarded to the chat with the current user (Saved Messages), to the Replies bot chat, or to the channel's discussion group, the identifier of the chat from which the message was forwarded last time; 0 if unknown.
        self.from_chat_id: int = get_object(kwargs.get('from_chat_id'))
        # For messages forwarded to the chat with the current user (Saved Messages), to the Replies bot chat, or to the channel's discussion group, the identifier of the original message from which the new message was forwarded last time; 0 if unknown.
        self.from_message_id: int = get_object(kwargs.get('from_message_id'))


class MessageInteractionInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number of times the message was viewed.
        self.view_count: int = get_object(kwargs.get('view_count'))
        # Number of times the message was forwarded.
        self.forward_count: int = get_object(kwargs.get('forward_count'))
        # Information about direct or indirect replies to the message; may be null. Currently, available only in channels with a discussion supergroup and discussion supergroups for messages, which are not replies itself.
        self.reply_info: MessageReplyInfo = get_object(kwargs.get('reply_info'))
        # The list of reactions added to the message.
        self.reactions: list[MessageReaction] = get_object(kwargs.get('reactions'))


class UnreadReaction(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the reaction.
        self.type: ReactionType = get_object(kwargs.get('type'))
        # Identifier of the sender, added the reaction.
        self.sender_id: MessageSender = get_object(kwargs.get('sender_id'))
        # True, if the reaction was added with a big animation.
        self.is_big: bool = get_object(kwargs.get('is_big'))


class MessageAutoDeleteTime(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message auto-delete time, in seconds. If 0, then messages aren't deleted automatically.
        self.time: int = get_object(kwargs.get('time'))


class MessageCalendarDay(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total number of found messages sent on the day.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # First message sent on the day.
        self.message: Message = get_object(kwargs.get('message'))


class MessageCalendar(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total number of found messages.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # Information about messages sent.
        self.days: list[MessageCalendarDay] = get_object(kwargs.get('days'))


class MessageExtendedMedia(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class OrderInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the user.
        self.name: str = get_object(kwargs.get('name'))
        # Phone number of the user.
        self.phone_number: str = get_object(kwargs.get('phone_number'))
        # Email address of the user.
        self.email_address: str = get_object(kwargs.get('email_address'))
        # Shipping address for this order; may be null.
        self.shipping_address: Address = get_object(kwargs.get('shipping_address'))


class Poll(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique poll identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Poll question; 1-300 characters.
        self.question: str = get_object(kwargs.get('question'))
        # List of poll answer options.
        self.options: list[PollOption] = get_object(kwargs.get('options'))
        # Total number of voters, participating in the poll.
        self.total_voter_count: int = get_object(kwargs.get('total_voter_count'))
        # Identifiers of recent voters, if the poll is non-anonymous.
        self.recent_voter_ids: list[MessageSender] = get_object(kwargs.get('recent_voter_ids'))
        # True, if the poll is anonymous.
        self.is_anonymous: bool = get_object(kwargs.get('is_anonymous'))
        # Type of the poll.
        self.type: PollType = get_object(kwargs.get('type'))
        # Amount of time the poll will be active after creation, in seconds.
        self.open_period: int = get_object(kwargs.get('open_period'))
        # Point in time (Unix timestamp) when the poll will automatically be closed.
        self.close_date: int = get_object(kwargs.get('close_date'))
        # True, if the poll is closed.
        self.is_closed: bool = get_object(kwargs.get('is_closed'))


class VideoNote(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Duration of the video, in seconds; as defined by the sender.
        self.duration: int = get_object(kwargs.get('duration'))
        # A waveform representation of the video note's audio in 5-bit format; may be empty if unknown.
        self.waveform: bytes = get_object(kwargs.get('waveform'))
        # Video width and height; as defined by the sender.
        self.length: int = get_object(kwargs.get('length'))
        # Video minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # Video thumbnail in JPEG format; as defined by the sender; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))
        # Result of speech recognition in the video note; may be null.
        self.speech_recognition_result: SpeechRecognitionResult = get_object(kwargs.get('speech_recognition_result'))
        # File containing the video.
        self.video: File = get_object(kwargs.get('video'))


class WebPage(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Original URL of the link.
        self.url: str = get_object(kwargs.get('url'))
        # URL to display.
        self.display_url: str = get_object(kwargs.get('display_url'))
        # Type of the web page. Can be: article, photo, audio, video, document, profile, app, or something else.
        self.type: str = get_object(kwargs.get('type'))
        # Short name of the site (e.g., Google Docs, App Store).
        self.site_name: str = get_object(kwargs.get('site_name'))
        # Title of the content.
        self.title: str = get_object(kwargs.get('title'))
        # Description of the content.
        self.description: FormattedText = get_object(kwargs.get('description'))
        # Image representing the content; may be null.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # URL to show in the embedded preview.
        self.embed_url: str = get_object(kwargs.get('embed_url'))
        # MIME type of the embedded preview, (e.g., text/html or video/mp4).
        self.embed_type: str = get_object(kwargs.get('embed_type'))
        # Width of the embedded preview.
        self.embed_width: int = get_object(kwargs.get('embed_width'))
        # Height of the embedded preview.
        self.embed_height: int = get_object(kwargs.get('embed_height'))
        # Duration of the content, in seconds.
        self.duration: int = get_object(kwargs.get('duration'))
        # Author of the content.
        self.author: str = get_object(kwargs.get('author'))
        # Preview of the content as an animation, if available; may be null.
        self.animation: Animation = get_object(kwargs.get('animation'))
        # Preview of the content as an audio file, if available; may be null.
        self.audio: Audio = get_object(kwargs.get('audio'))
        # Preview of the content as a document, if available; may be null.
        self.document: Document = get_object(kwargs.get('document'))
        # Preview of the content as a sticker for small WEBP files, if available; may be null.
        self.sticker: Sticker = get_object(kwargs.get('sticker'))
        # Preview of the content as a video, if available; may be null.
        self.video: Video = get_object(kwargs.get('video'))
        # Preview of the content as a video note, if available; may be null.
        self.video_note: VideoNote = get_object(kwargs.get('video_note'))
        # Preview of the content as a voice note, if available; may be null.
        self.voice_note: VoiceNote = get_object(kwargs.get('voice_note'))
        # The identifier of the sender of the previewed story; 0 if none.
        self.story_sender_chat_id: int = get_object(kwargs.get('story_sender_chat_id'))
        # The identifier of the previewed story; 0 if none.
        self.story_id: int = get_object(kwargs.get('story_id'))
        # Version of web page instant view (currently, can be 1 or 2); 0 if none.
        self.instant_view_version: int = get_object(kwargs.get('instant_view_version'))


class MessageText(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the message.
        self.text: FormattedText = get_object(kwargs.get('text'))
        # A preview of the web page that's mentioned in the text; may be null.
        self.web_page: WebPage = get_object(kwargs.get('web_page'))


class MessageAnimation(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The animation description.
        self.animation: Animation = get_object(kwargs.get('animation'))
        # Animation caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))
        # True, if the animation preview must be covered by a spoiler animation.
        self.has_spoiler: bool = get_object(kwargs.get('has_spoiler'))
        # True, if the animation thumbnail must be blurred and the animation must be shown only while tapped.
        self.is_secret: bool = get_object(kwargs.get('is_secret'))


class MessageAudio(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The audio description.
        self.audio: Audio = get_object(kwargs.get('audio'))
        # Audio caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class MessageDocument(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The document description.
        self.document: Document = get_object(kwargs.get('document'))
        # Document caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class MessagePhoto(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The photo.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Photo caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))
        # True, if the photo preview must be covered by a spoiler animation.
        self.has_spoiler: bool = get_object(kwargs.get('has_spoiler'))
        # True, if the photo must be blurred and must be shown only while tapped.
        self.is_secret: bool = get_object(kwargs.get('is_secret'))


class MessageExpiredPhoto(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSticker(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The sticker description.
        self.sticker: Sticker = get_object(kwargs.get('sticker'))
        # True, if premium animation of the sticker must be played.
        self.is_premium: bool = get_object(kwargs.get('is_premium'))


class MessageVideo(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The video description.
        self.video: Video = get_object(kwargs.get('video'))
        # Video caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))
        # True, if the video preview must be covered by a spoiler animation.
        self.has_spoiler: bool = get_object(kwargs.get('has_spoiler'))
        # True, if the video thumbnail must be blurred and the video must be shown only while tapped.
        self.is_secret: bool = get_object(kwargs.get('is_secret'))


class MessageExpiredVideo(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageVideoNote(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The video note description.
        self.video_note: VideoNote = get_object(kwargs.get('video_note'))
        # True, if at least one of the recipients has viewed the video note.
        self.is_viewed: bool = get_object(kwargs.get('is_viewed'))
        # True, if the video note thumbnail must be blurred and the video note must be shown only while tapped.
        self.is_secret: bool = get_object(kwargs.get('is_secret'))


class MessageVoiceNote(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The voice note description.
        self.voice_note: VoiceNote = get_object(kwargs.get('voice_note'))
        # Voice note caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))
        # True, if at least one of the recipients has listened to the voice note.
        self.is_listened: bool = get_object(kwargs.get('is_listened'))


class MessageLocation(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The location description.
        self.location: Location = get_object(kwargs.get('location'))
        # Time relative to the message send date, for which the location can be updated, in seconds.
        self.live_period: int = get_object(kwargs.get('live_period'))
        # Left time for which the location can be updated, in seconds. updateMessageContent is not sent when this field changes.
        self.expires_in: int = get_object(kwargs.get('expires_in'))
        # For live locations, a direction in which the location moves, in degrees; 1-360. If 0 the direction is unknown.
        self.heading: int = get_object(kwargs.get('heading'))
        # For live locations, a maximum distance to another chat member for proximity alerts, in meters (0-100000). 0 if the notification is disabled. Available only to the message sender.
        self.proximity_alert_radius: int = get_object(kwargs.get('proximity_alert_radius'))


class MessageVenue(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The venue description.
        self.venue: Venue = get_object(kwargs.get('venue'))


class MessageContact(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The contact description.
        self.contact: Contact = get_object(kwargs.get('contact'))


class MessageAnimatedEmoji(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The animated emoji.
        self.animated_emoji: AnimatedEmoji = get_object(kwargs.get('animated_emoji'))
        # The corresponding emoji.
        self.emoji: str = get_object(kwargs.get('emoji'))


class MessageDice(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The animated stickers with the initial dice animation; may be null if unknown. updateMessageContent will be sent when the sticker became known.
        self.initial_state: DiceStickers = get_object(kwargs.get('initial_state'))
        # The animated stickers with the final dice animation; may be null if unknown. updateMessageContent will be sent when the sticker became known.
        self.final_state: DiceStickers = get_object(kwargs.get('final_state'))
        # Emoji on which the dice throw animation is based.
        self.emoji: str = get_object(kwargs.get('emoji'))
        # The dice value. If the value is 0, the dice don't have final state yet.
        self.value: int = get_object(kwargs.get('value'))
        # Number of frame after which a success animation like a shower of confetti needs to be shown on updateMessageSendSucceeded.
        self.success_animation_frame_number: int = get_object(kwargs.get('success_animation_frame_number'))


class MessageGame(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The game description.
        self.game: Game = get_object(kwargs.get('game'))


class MessagePoll(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The poll description.
        self.poll: Poll = get_object(kwargs.get('poll'))


class MessageStory(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat that posted the story.
        self.story_sender_chat_id: int = get_object(kwargs.get('story_sender_chat_id'))
        # Story identifier.
        self.story_id: int = get_object(kwargs.get('story_id'))
        # True, if the story was automatically forwarded because of a mention of the user.
        self.via_mention: bool = get_object(kwargs.get('via_mention'))


class MessageInvoice(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Product title.
        self.title: str = get_object(kwargs.get('title'))
        # Product description.
        self.description: FormattedText = get_object(kwargs.get('description'))
        # Product photo; may be null.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Currency for the product price.
        self.currency: str = get_object(kwargs.get('currency'))
        # Product total price in the smallest units of the currency.
        self.total_amount: int = get_object(kwargs.get('total_amount'))
        # Unique invoice bot start_parameter to be passed to getInternalLink.
        self.start_parameter: str = get_object(kwargs.get('start_parameter'))
        # True, if the invoice is a test invoice.
        self.is_test: bool = get_object(kwargs.get('is_test'))
        # True, if the shipping address must be specified.
        self.need_shipping_address: bool = get_object(kwargs.get('need_shipping_address'))
        # The identifier of the message with the receipt, after the product has been purchased.
        self.receipt_message_id: int = get_object(kwargs.get('receipt_message_id'))
        # Extended media attached to the invoice; may be null.
        self.extended_media: MessageExtendedMedia = get_object(kwargs.get('extended_media'))


class MessageCall(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the call was a video call.
        self.is_video: bool = get_object(kwargs.get('is_video'))
        # Reason why the call was discarded.
        self.discard_reason: CallDiscardReason = get_object(kwargs.get('discard_reason'))
        # Call duration, in seconds.
        self.duration: int = get_object(kwargs.get('duration'))


class MessageVideoChatScheduled(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the video chat. The video chat can be received through the method getGroupCall.
        self.group_call_id: int = get_object(kwargs.get('group_call_id'))
        # Point in time (Unix timestamp) when the group call is supposed to be started by an administrator.
        self.start_date: int = get_object(kwargs.get('start_date'))


class MessageVideoChatStarted(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the video chat. The video chat can be received through the method getGroupCall.
        self.group_call_id: int = get_object(kwargs.get('group_call_id'))


class MessageVideoChatEnded(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Call duration, in seconds.
        self.duration: int = get_object(kwargs.get('duration'))


class MessageInviteVideoChatParticipants(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the video chat. The video chat can be received through the method getGroupCall.
        self.group_call_id: int = get_object(kwargs.get('group_call_id'))
        # Invited user identifiers.
        self.user_ids: list[int] = get_object(kwargs.get('user_ids'))


class MessageBasicGroupChatCreate(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title of the basic group.
        self.title: str = get_object(kwargs.get('title'))
        # User identifiers of members in the basic group.
        self.member_user_ids: list[int] = get_object(kwargs.get('member_user_ids'))


class MessageSupergroupChatCreate(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title of the supergroup or channel.
        self.title: str = get_object(kwargs.get('title'))


class MessageChatChangeTitle(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New chat title.
        self.title: str = get_object(kwargs.get('title'))


class MessageChatChangePhoto(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New chat photo.
        self.photo: ChatPhoto = get_object(kwargs.get('photo'))


class MessageChatDeletePhoto(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageChatAddMembers(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifiers of the new members.
        self.member_user_ids: list[int] = get_object(kwargs.get('member_user_ids'))


class MessageChatJoinByLink(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageChatJoinByRequest(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageChatDeleteMember(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the deleted chat member.
        self.user_id: int = get_object(kwargs.get('user_id'))


class MessageChatUpgradeTo(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the supergroup to which the basic group was upgraded.
        self.supergroup_id: int = get_object(kwargs.get('supergroup_id'))


class MessageChatUpgradeFrom(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title of the newly created supergroup.
        self.title: str = get_object(kwargs.get('title'))
        # The identifier of the original basic group.
        self.basic_group_id: int = get_object(kwargs.get('basic_group_id'))


class MessagePinMessage(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the pinned message, can be an identifier of a deleted message or 0.
        self.message_id: int = get_object(kwargs.get('message_id'))


class MessageScreenshotTaken(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageChatSetBackground(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the message with a previously set same background; 0 if none. Can be an identifier of a deleted message.
        self.old_background_message_id: int = get_object(kwargs.get('old_background_message_id'))
        # The new background.
        self.background: ChatBackground = get_object(kwargs.get('background'))


class MessageChatSetTheme(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # If non-empty, name of a new theme, set for the chat. Otherwise, chat theme was reset to the default one.
        self.theme_name: str = get_object(kwargs.get('theme_name'))


class MessageChatSetMessageAutoDeleteTime(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New value auto-delete or self-destruct time, in seconds; 0 if disabled.
        self.message_auto_delete_time: int = get_object(kwargs.get('message_auto_delete_time'))
        # If not 0, a user identifier, which default setting was automatically applied.
        self.from_user_id: int = get_object(kwargs.get('from_user_id'))


class MessageForumTopicCreated(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the topic.
        self.name: str = get_object(kwargs.get('name'))
        # Icon of the topic.
        self.icon: ForumTopicIcon = get_object(kwargs.get('icon'))


class MessageForumTopicEdited(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # If non-empty, the new name of the topic.
        self.name: str = get_object(kwargs.get('name'))
        # True, if icon's custom_emoji_id is changed.
        self.edit_icon_custom_emoji_id: bool = get_object(kwargs.get('edit_icon_custom_emoji_id'))
        # New unique identifier of the custom emoji shown on the topic icon; 0 if none. Must be ignored if edit_icon_custom_emoji_id is false.
        self.icon_custom_emoji_id: int = get_object(kwargs.get('icon_custom_emoji_id'))


class MessageForumTopicIsClosedToggled(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the topic was closed; otherwise, the topic was reopened.
        self.is_closed: bool = get_object(kwargs.get('is_closed'))


class MessageForumTopicIsHiddenToggled(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the topic was hidden; otherwise, the topic was unhidden.
        self.is_hidden: bool = get_object(kwargs.get('is_hidden'))


class MessageSuggestProfilePhoto(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The suggested chat photo. Use the method setProfilePhoto with inputChatPhotoPrevious to apply the photo.
        self.photo: ChatPhoto = get_object(kwargs.get('photo'))


class MessageCustomServiceAction(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message text to be shown in the chat.
        self.text: str = get_object(kwargs.get('text'))


class MessageGameScore(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the message with the game, can be an identifier of a deleted message.
        self.game_message_id: int = get_object(kwargs.get('game_message_id'))
        # Identifier of the game; may be different from the games presented in the message with the game.
        self.game_id: int = get_object(kwargs.get('game_id'))
        # New score.
        self.score: int = get_object(kwargs.get('score'))


class MessagePaymentSuccessful(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat, containing the corresponding invoice message.
        self.invoice_chat_id: int = get_object(kwargs.get('invoice_chat_id'))
        # Identifier of the message with the corresponding invoice; can be 0 or an identifier of a deleted message.
        self.invoice_message_id: int = get_object(kwargs.get('invoice_message_id'))
        # Currency for the price of the product.
        self.currency: str = get_object(kwargs.get('currency'))
        # Total price for the product, in the smallest units of the currency.
        self.total_amount: int = get_object(kwargs.get('total_amount'))
        # True, if this is a recurring payment.
        self.is_recurring: bool = get_object(kwargs.get('is_recurring'))
        # True, if this is the first recurring payment.
        self.is_first_recurring: bool = get_object(kwargs.get('is_first_recurring'))
        # Name of the invoice; may be empty if unknown.
        self.invoice_name: str = get_object(kwargs.get('invoice_name'))


class MessagePaymentSuccessfulBot(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Currency for price of the product.
        self.currency: str = get_object(kwargs.get('currency'))
        # Total price for the product, in the smallest units of the currency.
        self.total_amount: int = get_object(kwargs.get('total_amount'))
        # True, if this is a recurring payment.
        self.is_recurring: bool = get_object(kwargs.get('is_recurring'))
        # True, if this is the first recurring payment.
        self.is_first_recurring: bool = get_object(kwargs.get('is_first_recurring'))
        # Invoice payload.
        self.invoice_payload: bytes = get_object(kwargs.get('invoice_payload'))
        # Identifier of the shipping option chosen by the user; may be empty if not applicable.
        self.shipping_option_id: str = get_object(kwargs.get('shipping_option_id'))
        # Information about the order; may be null.
        self.order_info: OrderInfo = get_object(kwargs.get('order_info'))
        # Telegram payment identifier.
        self.telegram_payment_charge_id: str = get_object(kwargs.get('telegram_payment_charge_id'))
        # Provider payment identifier.
        self.provider_payment_charge_id: str = get_object(kwargs.get('provider_payment_charge_id'))


class MessageGiftedPremium(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The identifier of a user that gifted Telegram Premium; 0 if the gift was anonymous.
        self.gifter_user_id: int = get_object(kwargs.get('gifter_user_id'))
        # Currency for the paid amount.
        self.currency: str = get_object(kwargs.get('currency'))
        # The paid amount, in the smallest units of the currency.
        self.amount: int = get_object(kwargs.get('amount'))
        # Cryptocurrency used to pay for the gift; may be empty if none.
        self.cryptocurrency: str = get_object(kwargs.get('cryptocurrency'))
        # The paid amount, in the smallest units of the cryptocurrency.
        self.cryptocurrency_amount: int = get_object(kwargs.get('cryptocurrency_amount'))
        # Number of month the Telegram Premium subscription will be active.
        self.month_count: int = get_object(kwargs.get('month_count'))
        # A sticker to be shown in the message; may be null if unknown.
        self.sticker: Sticker = get_object(kwargs.get('sticker'))


class MessageContactRegistered(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageUserShared(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the shared user.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Identifier of the keyboard button with the request.
        self.button_id: int = get_object(kwargs.get('button_id'))


class MessageChatShared(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the shared chat.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifier of the keyboard button with the request.
        self.button_id: int = get_object(kwargs.get('button_id'))


class MessageWebsiteConnected(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Domain name of the connected website.
        self.domain_name: str = get_object(kwargs.get('domain_name'))


class MessageBotWriteAccessAllowed(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the Web App, which requested the access; may be null if none or the Web App was opened from the attachment menu.
        self.web_app: WebApp = get_object(kwargs.get('web_app'))
        # True, if user allowed the bot to send messages by an explicit call to allowBotToSendMessages.
        self.by_request: bool = get_object(kwargs.get('by_request'))


class MessageWebAppDataSent(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the keyboardButtonTypeWebApp button, which opened the Web App.
        self.button_text: str = get_object(kwargs.get('button_text'))


class MessageWebAppDataReceived(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text of the keyboardButtonTypeWebApp button, which opened the Web App.
        self.button_text: str = get_object(kwargs.get('button_text'))
        # The data.
        self.data: str = get_object(kwargs.get('data'))


class MessagePassportDataSent(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of Telegram Passport element types sent.
        self.types: list[PassportElementType] = get_object(kwargs.get('types'))


class MessagePassportDataReceived(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of received Telegram Passport elements.
        self.elements: list[EncryptedPassportElement] = get_object(kwargs.get('elements'))
        # Encrypted data credentials.
        self.credentials: EncryptedCredentials = get_object(kwargs.get('credentials'))


class MessageProximityAlertTriggered(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The identifier of a user or chat that triggered the proximity alert.
        self.traveler_id: MessageSender = get_object(kwargs.get('traveler_id'))
        # The identifier of a user or chat that subscribed for the proximity alert.
        self.watcher_id: MessageSender = get_object(kwargs.get('watcher_id'))
        # The distance between the users.
        self.distance: int = get_object(kwargs.get('distance'))


class MessageUnsupported(MessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageExtendedMediaPreview(MessageExtendedMedia):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Media width; 0 if unknown.
        self.width: int = get_object(kwargs.get('width'))
        # Media height; 0 if unknown.
        self.height: int = get_object(kwargs.get('height'))
        # Media duration; 0 if unknown.
        self.duration: int = get_object(kwargs.get('duration'))
        # Media minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # Media caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class MessageExtendedMediaPhoto(MessageExtendedMedia):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The photo.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Photo caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class MessageExtendedMediaVideo(MessageExtendedMedia):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The video.
        self.video: Video = get_object(kwargs.get('video'))
        # Photo caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class MessageExtendedMediaUnsupported(MessageExtendedMedia):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Media caption.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class MessageFileType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageFileTypePrivate(MessageFileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the other party; may be empty if unrecognized.
        self.name: str = get_object(kwargs.get('name'))


class MessageFileTypeGroup(MessageFileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title of the group chat; may be empty if unrecognized.
        self.title: str = get_object(kwargs.get('title'))


class MessageFileTypeUnknown(MessageFileType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageForwardOrigin(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageForwardOriginUser(MessageForwardOrigin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the user that originally sent the message.
        self.sender_user_id: int = get_object(kwargs.get('sender_user_id'))


class MessageForwardOriginChat(MessageForwardOrigin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat that originally sent the message.
        self.sender_chat_id: int = get_object(kwargs.get('sender_chat_id'))
        # For messages originally sent by an anonymous chat administrator, original message author signature.
        self.author_signature: str = get_object(kwargs.get('author_signature'))


class MessageForwardOriginHiddenUser(MessageForwardOrigin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the sender.
        self.sender_name: str = get_object(kwargs.get('sender_name'))


class MessageForwardOriginChannel(MessageForwardOrigin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat from which the message was originally forwarded.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier of the original message.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # Original post author signature.
        self.author_signature: str = get_object(kwargs.get('author_signature'))


class MessageForwardOriginMessageImport(MessageForwardOrigin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the sender.
        self.sender_name: str = get_object(kwargs.get('sender_name'))


class MessageReaction(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the reaction.
        self.type: ReactionType = get_object(kwargs.get('type'))
        # Number of times the reaction was added.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # True, if the reaction is chosen by the current user.
        self.is_chosen: bool = get_object(kwargs.get('is_chosen'))
        # Identifiers of at most 3 recent message senders, added the reaction; available in private, basic group and supergroup chats.
        self.recent_sender_ids: list[MessageSender] = get_object(kwargs.get('recent_sender_ids'))


class MessageReplyInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number of times the message was directly or indirectly replied.
        self.reply_count: int = get_object(kwargs.get('reply_count'))
        # Identifiers of at most 3 recent repliers to the message; available in channels with a discussion supergroup. The users and chats are expected to be inaccessible: only their photo and name will be available.
        self.recent_replier_ids: list[MessageSender] = get_object(kwargs.get('recent_replier_ids'))
        # Identifier of the last read incoming reply to the message.
        self.last_read_inbox_message_id: int = get_object(kwargs.get('last_read_inbox_message_id'))
        # Identifier of the last read outgoing reply to the message.
        self.last_read_outbox_message_id: int = get_object(kwargs.get('last_read_outbox_message_id'))
        # Identifier of the last reply to the message.
        self.last_message_id: int = get_object(kwargs.get('last_message_id'))


class MessageLink(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The link.
        self.link: str = get_object(kwargs.get('link'))
        # True, if the link will work for non-members of the chat.
        self.is_public: bool = get_object(kwargs.get('is_public'))


class MessageLinkInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the link is a public link for a message or a forum topic in a chat.
        self.is_public: bool = get_object(kwargs.get('is_public'))
        # If found, identifier of the chat to which the link points, 0 otherwise.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # If found, identifier of the message thread in which to open the message, or a forum topic to open if the message is missing.
        self.message_thread_id: int = get_object(kwargs.get('message_thread_id'))
        # If found, the linked message; may be null.
        self.message: Message = get_object(kwargs.get('message'))
        # Timestamp from which the video/audio/video note/voice note playing must start, in seconds; 0 if not specified. The media can be in the message content or in its web page preview.
        self.media_timestamp: int = get_object(kwargs.get('media_timestamp'))
        # True, if the whole media album to which the message belongs is linked.
        self.for_album: bool = get_object(kwargs.get('for_album'))


class MessagePosition(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # 0-based message position in the full list of suitable messages.
        self.position: int = get_object(kwargs.get('position'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # Point in time (Unix timestamp) when the message was sent.
        self.date: int = get_object(kwargs.get('date'))


class MessagePositions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total number of messages found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of message positions.
        self.positions: list[MessagePosition] = get_object(kwargs.get('positions'))


class MessageReplyToMessage(MessageReplyTo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The identifier of the chat to which the replied message belongs; ignored for outgoing replies. For example, messages in the Replies chat are replies to messages in different chats.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The identifier of the replied message.
        self.message_id: int = get_object(kwargs.get('message_id'))


class MessageReplyToStory(MessageReplyTo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The identifier of the sender of the replied story. Currently, stories can be replied only in the sender's chat.
        self.story_sender_chat_id: int = get_object(kwargs.get('story_sender_chat_id'))
        # The identifier of the replied story.
        self.story_id: int = get_object(kwargs.get('story_id'))


class MessageSchedulingStateSendAtDate(MessageSchedulingState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) when the message will be sent. The date must be within 367 days in the future.
        self.send_date: int = get_object(kwargs.get('send_date'))


class MessageSchedulingStateSendWhenOnline(MessageSchedulingState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSelfDestructTypeTimer(MessageSelfDestructType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The message's self-destruct time, in seconds; must be between 0 and 60 in private chats.
        self.self_destruct_time: int = get_object(kwargs.get('self_destruct_time'))


class MessageSelfDestructTypeImmediately(MessageSelfDestructType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSendOptions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Pass true to disable notification for the message.
        self.disable_notification: bool = get_object(kwargs.get('disable_notification'))
        # Pass true if the message is sent from the background.
        self.from_background: bool = get_object(kwargs.get('from_background'))
        # Pass true if the content of the message must be protected from forwarding and saving; for bots only.
        self.protect_content: bool = get_object(kwargs.get('protect_content'))
        # Pass true if the user explicitly chosen a sticker or a custom emoji from an installed sticker set; applicable only to sendMessage and sendMessageAlbum.
        self.update_order_of_installed_sticker_sets: bool = get_object(kwargs.get('update_order_of_installed_sticker_sets'))
        # Message scheduling state; pass null to send message immediately. Messages sent to a secret chat, live location messages and self-destructing messages can't be scheduled.
        self.scheduling_state: MessageSchedulingState = get_object(kwargs.get('scheduling_state'))
        # Non-persistent identifier, which will be returned back in messageSendingStatePending object and can be used to match sent messages and corresponding updateNewMessage updates.
        self.sending_id: int = get_object(kwargs.get('sending_id'))


class MessageSenderUser(MessageSender):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the user that sent the message.
        self.user_id: int = get_object(kwargs.get('user_id'))


class MessageSenderChat(MessageSender):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat that sent the message.
        self.chat_id: int = get_object(kwargs.get('chat_id'))


class MessageSenders(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of messages senders found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of message senders.
        self.senders: list[MessageSender] = get_object(kwargs.get('senders'))


class MessageSendingStatePending(MessageSendingState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Non-persistent message sending identifier, specified by the application.
        self.sending_id: int = get_object(kwargs.get('sending_id'))


class MessageSendingStateFailed(MessageSendingState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # An error code; 0 if unknown.
        self.error_code: int = get_object(kwargs.get('error_code'))
        # Error message.
        self.error_message: str = get_object(kwargs.get('error_message'))
        # True, if the message can be re-sent.
        self.can_retry: bool = get_object(kwargs.get('can_retry'))
        # True, if the message can be re-sent only on behalf of a different sender.
        self.need_another_sender: bool = get_object(kwargs.get('need_another_sender'))
        # Time left before the message can be re-sent, in seconds. No update is sent when this field changes.
        self.retry_after: float = get_object(kwargs.get('retry_after'))


class MessageSource(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceChatHistory(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceMessageThreadHistory(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceForumTopicHistory(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceHistoryPreview(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceChatList(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceSearch(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceChatEventLog(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceNotification(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceScreenshot(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSourceOther(MessageSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSponsorType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class MessageSponsor(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the sponsor.
        self.type: MessageSponsorType = get_object(kwargs.get('type'))
        # Photo of the sponsor; may be null if must not be shown.
        self.photo: ChatPhotoInfo = get_object(kwargs.get('photo'))
        # Additional optional information about the sponsor to be shown along with the message.
        self.info: str = get_object(kwargs.get('info'))


class MessageSponsorTypeBot(MessageSponsorType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the bot.
        self.bot_user_id: int = get_object(kwargs.get('bot_user_id'))
        # An internal link to be opened when the sponsored message is clicked.
        self.link: InternalLinkType = get_object(kwargs.get('link'))


class MessageSponsorTypePublicChannel(MessageSponsorType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Sponsor chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # An internal link to be opened when the sponsored message is clicked; may be null if the sponsor chat needs to be opened instead.
        self.link: InternalLinkType = get_object(kwargs.get('link'))


class MessageSponsorTypePrivateChannel(MessageSponsorType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title of the chat.
        self.title: str = get_object(kwargs.get('title'))
        # Invite link for the channel.
        self.invite_link: str = get_object(kwargs.get('invite_link'))


class MessageSponsorTypeWebsite(MessageSponsorType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # URL of the website.
        self.url: str = get_object(kwargs.get('url'))
        # Name of the website.
        self.name: str = get_object(kwargs.get('name'))


class MessageStatistics(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A graph containing number of message views and shares.
        self.message_interaction_graph: StatisticalGraph = get_object(kwargs.get('message_interaction_graph'))


class MessageThreadInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat to which the message thread belongs.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message thread identifier, unique within the chat.
        self.message_thread_id: int = get_object(kwargs.get('message_thread_id'))
        # Information about the message thread; may be null for forum topic threads.
        self.reply_info: MessageReplyInfo = get_object(kwargs.get('reply_info'))
        # Approximate number of unread messages in the message thread.
        self.unread_message_count: int = get_object(kwargs.get('unread_message_count'))
        # The messages from which the thread starts. The messages are returned in a reverse chronological order (i.e., in order of decreasing message_id).
        self.messages: list[Message] = get_object(kwargs.get('messages'))
        # A draft of a message in the message thread; may be null if none.
        self.draft_message: DraftMessage = get_object(kwargs.get('draft_message'))


class MessageViewer(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the viewer.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Approximate point in time (Unix timestamp) when the message was viewed.
        self.view_date: int = get_object(kwargs.get('view_date'))


class MessageViewers(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of message viewers.
        self.viewers: list[MessageViewer] = get_object(kwargs.get('viewers'))


class Messages(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of messages found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of messages; messages may be null.
        self.messages: list[Message] = get_object(kwargs.get('messages'))


class NetworkStatisticsEntry(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NetworkStatistics(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) from which the statistics are collected.
        self.since_date: int = get_object(kwargs.get('since_date'))
        # Network statistics entries.
        self.entries: list[NetworkStatisticsEntry] = get_object(kwargs.get('entries'))


class NetworkType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NetworkStatisticsEntryFile(NetworkStatisticsEntry):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the file the data is part of; pass null if the data isn't related to files.
        self.file_type: FileType = get_object(kwargs.get('file_type'))
        # Type of the network the data was sent through. Call setNetworkType to maintain the actual network type.
        self.network_type: NetworkType = get_object(kwargs.get('network_type'))
        # Total number of bytes sent.
        self.sent_bytes: int = get_object(kwargs.get('sent_bytes'))
        # Total number of bytes received.
        self.received_bytes: int = get_object(kwargs.get('received_bytes'))


class NetworkStatisticsEntryCall(NetworkStatisticsEntry):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the network the data was sent through. Call setNetworkType to maintain the actual network type.
        self.network_type: NetworkType = get_object(kwargs.get('network_type'))
        # Total number of bytes sent.
        self.sent_bytes: int = get_object(kwargs.get('sent_bytes'))
        # Total number of bytes received.
        self.received_bytes: int = get_object(kwargs.get('received_bytes'))
        # Total call duration, in seconds.
        self.duration: float = get_object(kwargs.get('duration'))


class NetworkTypeNone(NetworkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NetworkTypeMobile(NetworkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NetworkTypeMobileRoaming(NetworkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NetworkTypeWiFi(NetworkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NetworkTypeOther(NetworkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Notification(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique persistent identifier of this notification.
        self.id: int = get_object(kwargs.get('id'))
        # Notification date.
        self.date: int = get_object(kwargs.get('date'))
        # True, if the notification was explicitly sent without sound.
        self.is_silent: bool = get_object(kwargs.get('is_silent'))
        # Notification type.
        self.type: NotificationType = get_object(kwargs.get('type'))


class NotificationGroupType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationGroup(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique persistent auto-incremented from 1 identifier of the notification group.
        self.id: int = get_object(kwargs.get('id'))
        # Type of the group.
        self.type: NotificationGroupType = get_object(kwargs.get('type'))
        # Identifier of a chat to which all notifications in the group belong.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Total number of active notifications in the group.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # The list of active notifications.
        self.notifications: list[Notification] = get_object(kwargs.get('notifications'))


class NotificationGroupTypeMessages(NotificationGroupType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationGroupTypeMentions(NotificationGroupType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationGroupTypeSecretChat(NotificationGroupType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationGroupTypeCalls(NotificationGroupType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationSettingsScope(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationSettingsScopePrivateChats(NotificationSettingsScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationSettingsScopeGroupChats(NotificationSettingsScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationSettingsScopeChannelChats(NotificationSettingsScope):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationSound(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the notification sound.
        self.id: int = get_object(kwargs.get('id'))
        # Duration of the sound, in seconds.
        self.duration: int = get_object(kwargs.get('duration'))
        # Point in time (Unix timestamp) when the sound was created.
        self.date: int = get_object(kwargs.get('date'))
        # Title of the notification sound.
        self.title: str = get_object(kwargs.get('title'))
        # Arbitrary data, defined while the sound was uploaded.
        self.data: str = get_object(kwargs.get('data'))
        # File containing the sound.
        self.sound: File = get_object(kwargs.get('sound'))


class NotificationSounds(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of notification sounds.
        self.notification_sounds: list[NotificationSound] = get_object(kwargs.get('notification_sounds'))


class PushMessageContent(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationTypeNewMessage(NotificationType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The message.
        self.message: Message = get_object(kwargs.get('message'))
        # True, if message content must be displayed in notifications.
        self.show_preview: bool = get_object(kwargs.get('show_preview'))


class NotificationTypeNewSecretChat(NotificationType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class NotificationTypeNewCall(NotificationType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Call identifier.
        self.call_id: int = get_object(kwargs.get('call_id'))


class NotificationTypeNewPushMessage(NotificationType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The message identifier. The message will not be available in the chat history, but the identifier can be used in viewMessages, or as a message to reply.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # Identifier of the sender of the message. Corresponding user or chat may be inaccessible.
        self.sender_id: MessageSender = get_object(kwargs.get('sender_id'))
        # Name of the sender.
        self.sender_name: str = get_object(kwargs.get('sender_name'))
        # True, if the message is outgoing.
        self.is_outgoing: bool = get_object(kwargs.get('is_outgoing'))
        # Push message content.
        self.content: PushMessageContent = get_object(kwargs.get('content'))


class Ok(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class OptionValue(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class OptionValueBoolean(OptionValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The value of the option.
        self.value: bool = get_object(kwargs.get('value'))


class OptionValueEmpty(OptionValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class OptionValueInteger(OptionValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The value of the option.
        self.value: int = get_object(kwargs.get('value'))


class OptionValueString(OptionValue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The value of the option.
        self.value: str = get_object(kwargs.get('value'))


class PageBlock(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class RichText(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockCaption(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Content of the caption.
        self.text: RichText = get_object(kwargs.get('text'))
        # Block credit (like HTML tag &lt;cite&gt;).
        self.credit: RichText = get_object(kwargs.get('credit'))


class PageBlockListItem(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Item label.
        self.label: str = get_object(kwargs.get('label'))
        # Item blocks.
        self.page_blocks: list[PageBlock] = get_object(kwargs.get('page_blocks'))


class PageBlockRelatedArticle(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Related article URL.
        self.url: str = get_object(kwargs.get('url'))
        # Article title; may be empty.
        self.title: str = get_object(kwargs.get('title'))
        # Article description; may be empty.
        self.description: str = get_object(kwargs.get('description'))
        # Article photo; may be null.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Article author; may be empty.
        self.author: str = get_object(kwargs.get('author'))
        # Point in time (Unix timestamp) when the article was published; 0 if unknown.
        self.publish_date: int = get_object(kwargs.get('publish_date'))


class PageBlockTableCell(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Cell text; may be null. If the text is null, then the cell must be invisible.
        self.text: RichText = get_object(kwargs.get('text'))
        # True, if it is a header cell.
        self.is_header: bool = get_object(kwargs.get('is_header'))
        # The number of columns the cell spans.
        self.colspan: int = get_object(kwargs.get('colspan'))
        # The number of rows the cell spans.
        self.rowspan: int = get_object(kwargs.get('rowspan'))
        # Horizontal cell content alignment.
        self.align: PageBlockHorizontalAlignment = get_object(kwargs.get('align'))
        # Vertical cell content alignment.
        self.valign: PageBlockVerticalAlignment = get_object(kwargs.get('valign'))


class PageBlockTitle(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title.
        self.title: RichText = get_object(kwargs.get('title'))


class PageBlockSubtitle(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Subtitle.
        self.subtitle: RichText = get_object(kwargs.get('subtitle'))


class PageBlockAuthorDate(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Author.
        self.author: RichText = get_object(kwargs.get('author'))
        # Point in time (Unix timestamp) when the article was published; 0 if unknown.
        self.publish_date: int = get_object(kwargs.get('publish_date'))


class PageBlockHeader(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Header.
        self.header: RichText = get_object(kwargs.get('header'))


class PageBlockSubheader(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Subheader.
        self.subheader: RichText = get_object(kwargs.get('subheader'))


class PageBlockKicker(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Kicker.
        self.kicker: RichText = get_object(kwargs.get('kicker'))


class PageBlockParagraph(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Paragraph text.
        self.text: RichText = get_object(kwargs.get('text'))


class PageBlockPreformatted(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Paragraph text.
        self.text: RichText = get_object(kwargs.get('text'))
        # Programming language for which the text needs to be formatted.
        self.language: str = get_object(kwargs.get('language'))


class PageBlockFooter(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Footer.
        self.footer: RichText = get_object(kwargs.get('footer'))


class PageBlockDivider(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockAnchor(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the anchor.
        self.name: str = get_object(kwargs.get('name'))


class PageBlockList(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The items of the list.
        self.items: list[PageBlockListItem] = get_object(kwargs.get('items'))


class PageBlockBlockQuote(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Quote text.
        self.text: RichText = get_object(kwargs.get('text'))
        # Quote credit.
        self.credit: RichText = get_object(kwargs.get('credit'))


class PageBlockPullQuote(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Quote text.
        self.text: RichText = get_object(kwargs.get('text'))
        # Quote credit.
        self.credit: RichText = get_object(kwargs.get('credit'))


class PageBlockAnimation(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Animation file; may be null.
        self.animation: Animation = get_object(kwargs.get('animation'))
        # Animation caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))
        # True, if the animation must be played automatically.
        self.need_autoplay: bool = get_object(kwargs.get('need_autoplay'))


class PageBlockAudio(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Audio file; may be null.
        self.audio: Audio = get_object(kwargs.get('audio'))
        # Audio file caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))


class PageBlockPhoto(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Photo file; may be null.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Photo caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))
        # URL that needs to be opened when the photo is clicked.
        self.url: str = get_object(kwargs.get('url'))


class PageBlockVideo(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Video file; may be null.
        self.video: Video = get_object(kwargs.get('video'))
        # Video caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))
        # True, if the video must be played automatically.
        self.need_autoplay: bool = get_object(kwargs.get('need_autoplay'))
        # True, if the video must be looped.
        self.is_looped: bool = get_object(kwargs.get('is_looped'))


class PageBlockVoiceNote(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Voice note; may be null.
        self.voice_note: VoiceNote = get_object(kwargs.get('voice_note'))
        # Voice note caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))


class PageBlockCover(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Cover.
        self.cover: PageBlock = get_object(kwargs.get('cover'))


class PageBlockEmbedded(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Web page URL, if available.
        self.url: str = get_object(kwargs.get('url'))
        # HTML-markup of the embedded page.
        self.html: str = get_object(kwargs.get('html'))
        # Poster photo, if available; may be null.
        self.poster_photo: Photo = get_object(kwargs.get('poster_photo'))
        # Block width; 0 if unknown.
        self.width: int = get_object(kwargs.get('width'))
        # Block height; 0 if unknown.
        self.height: int = get_object(kwargs.get('height'))
        # Block caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))
        # True, if the block must be full width.
        self.is_full_width: bool = get_object(kwargs.get('is_full_width'))
        # True, if scrolling needs to be allowed.
        self.allow_scrolling: bool = get_object(kwargs.get('allow_scrolling'))


class PageBlockEmbeddedPost(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Web page URL.
        self.url: str = get_object(kwargs.get('url'))
        # Post author.
        self.author: str = get_object(kwargs.get('author'))
        # Post author photo; may be null.
        self.author_photo: Photo = get_object(kwargs.get('author_photo'))
        # Point in time (Unix timestamp) when the post was created; 0 if unknown.
        self.date: int = get_object(kwargs.get('date'))
        # Post content.
        self.page_blocks: list[PageBlock] = get_object(kwargs.get('page_blocks'))
        # Post caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))


class PageBlockCollage(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Collage item contents.
        self.page_blocks: list[PageBlock] = get_object(kwargs.get('page_blocks'))
        # Block caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))


class PageBlockSlideshow(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Slideshow item contents.
        self.page_blocks: list[PageBlock] = get_object(kwargs.get('page_blocks'))
        # Block caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))


class PageBlockChatLink(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat title.
        self.title: str = get_object(kwargs.get('title'))
        # Chat photo; may be null.
        self.photo: ChatPhotoInfo = get_object(kwargs.get('photo'))
        # Chat username by which all other information about the chat can be resolved.
        self.username: str = get_object(kwargs.get('username'))


class PageBlockTable(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Table caption.
        self.caption: RichText = get_object(kwargs.get('caption'))
        # Table cells.
        self.cells: list[list[PageBlockTableCell]] = get_object(kwargs.get('cells'))
        # True, if the table is bordered.
        self.is_bordered: bool = get_object(kwargs.get('is_bordered'))
        # True, if the table is striped.
        self.is_striped: bool = get_object(kwargs.get('is_striped'))


class PageBlockDetails(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Always visible heading for the block.
        self.header: RichText = get_object(kwargs.get('header'))
        # Block contents.
        self.page_blocks: list[PageBlock] = get_object(kwargs.get('page_blocks'))
        # True, if the block is open by default.
        self.is_open: bool = get_object(kwargs.get('is_open'))


class PageBlockRelatedArticles(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Block header.
        self.header: RichText = get_object(kwargs.get('header'))
        # List of related articles.
        self.articles: list[PageBlockRelatedArticle] = get_object(kwargs.get('articles'))


class PageBlockMap(PageBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Location of the map center.
        self.location: Location = get_object(kwargs.get('location'))
        # Map zoom level.
        self.zoom: int = get_object(kwargs.get('zoom'))
        # Map width.
        self.width: int = get_object(kwargs.get('width'))
        # Map height.
        self.height: int = get_object(kwargs.get('height'))
        # Block caption.
        self.caption: PageBlockCaption = get_object(kwargs.get('caption'))


class PageBlockHorizontalAlignment(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockHorizontalAlignmentLeft(PageBlockHorizontalAlignment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockHorizontalAlignmentCenter(PageBlockHorizontalAlignment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockHorizontalAlignmentRight(PageBlockHorizontalAlignment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockVerticalAlignment(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockVerticalAlignmentTop(PageBlockVerticalAlignment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockVerticalAlignmentMiddle(PageBlockVerticalAlignment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PageBlockVerticalAlignmentBottom(PageBlockVerticalAlignment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportRequiredElement(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of Telegram Passport elements any of which is enough to provide.
        self.suitable_elements: list[PassportSuitableElement] = get_object(kwargs.get('suitable_elements'))


class PassportAuthorizationForm(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the authorization form.
        self.id: int = get_object(kwargs.get('id'))
        # Telegram Passport elements that must be provided to complete the form.
        self.required_elements: list[PassportRequiredElement] = get_object(kwargs.get('required_elements'))
        # URL for the privacy policy of the service; may be empty.
        self.privacy_policy_url: str = get_object(kwargs.get('privacy_policy_url'))


class PersonalDocument(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of files containing the pages of the document.
        self.files: list[DatedFile] = get_object(kwargs.get('files'))
        # List of files containing a certified English translation of the document.
        self.translation: list[DatedFile] = get_object(kwargs.get('translation'))


class PassportElement(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementPersonalDetails(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Personal details of the user.
        self.personal_details: PersonalDetails = get_object(kwargs.get('personal_details'))


class PassportElementPassport(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Passport.
        self.passport: IdentityDocument = get_object(kwargs.get('passport'))


class PassportElementDriverLicense(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Driver license.
        self.driver_license: IdentityDocument = get_object(kwargs.get('driver_license'))


class PassportElementIdentityCard(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identity card.
        self.identity_card: IdentityDocument = get_object(kwargs.get('identity_card'))


class PassportElementInternalPassport(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Internal passport.
        self.internal_passport: IdentityDocument = get_object(kwargs.get('internal_passport'))


class PassportElementAddress(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Address.
        self.address: Address = get_object(kwargs.get('address'))


class PassportElementUtilityBill(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Utility bill.
        self.utility_bill: PersonalDocument = get_object(kwargs.get('utility_bill'))


class PassportElementBankStatement(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Bank statement.
        self.bank_statement: PersonalDocument = get_object(kwargs.get('bank_statement'))


class PassportElementRentalAgreement(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Rental agreement.
        self.rental_agreement: PersonalDocument = get_object(kwargs.get('rental_agreement'))


class PassportElementPassportRegistration(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Passport registration pages.
        self.passport_registration: PersonalDocument = get_object(kwargs.get('passport_registration'))


class PassportElementTemporaryRegistration(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Temporary registration.
        self.temporary_registration: PersonalDocument = get_object(kwargs.get('temporary_registration'))


class PassportElementPhoneNumber(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Phone number.
        self.phone_number: str = get_object(kwargs.get('phone_number'))


class PassportElementEmailAddress(PassportElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Email address.
        self.email_address: str = get_object(kwargs.get('email_address'))


class PassportElementErrorSource(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementError(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the Telegram Passport element which has the error.
        self.type: PassportElementType = get_object(kwargs.get('type'))
        # Error message.
        self.message: str = get_object(kwargs.get('message'))
        # Error source.
        self.source: PassportElementErrorSource = get_object(kwargs.get('source'))


class PassportElementErrorSourceUnspecified(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementErrorSourceDataField(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Field name.
        self.field_name: str = get_object(kwargs.get('field_name'))


class PassportElementErrorSourceFrontSide(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementErrorSourceReverseSide(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementErrorSourceSelfie(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementErrorSourceTranslationFile(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Index of a file with the error.
        self.file_index: int = get_object(kwargs.get('file_index'))


class PassportElementErrorSourceTranslationFiles(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementErrorSourceFile(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Index of a file with the error.
        self.file_index: int = get_object(kwargs.get('file_index'))


class PassportElementErrorSourceFiles(PassportElementErrorSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypePersonalDetails(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypePassport(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeDriverLicense(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeIdentityCard(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeInternalPassport(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeAddress(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeUtilityBill(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeBankStatement(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeRentalAgreement(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypePassportRegistration(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeTemporaryRegistration(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypePhoneNumber(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElementTypeEmailAddress(PassportElementType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PassportElements(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Telegram Passport elements.
        self.elements: list[PassportElement] = get_object(kwargs.get('elements'))


class PassportElementsWithErrors(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Telegram Passport elements.
        self.elements: list[PassportElement] = get_object(kwargs.get('elements'))
        # Errors in the elements that are already available.
        self.errors: list[PassportElementError] = get_object(kwargs.get('errors'))


class PassportSuitableElement(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the element.
        self.type: PassportElementType = get_object(kwargs.get('type'))
        # True, if a selfie is required with the identity document.
        self.is_selfie_required: bool = get_object(kwargs.get('is_selfie_required'))
        # True, if a certified English translation is required with the document.
        self.is_translation_required: bool = get_object(kwargs.get('is_translation_required'))
        # True, if personal details must include the user's name in the language of their country of residence.
        self.is_native_name_required: bool = get_object(kwargs.get('is_native_name_required'))


class PasswordState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if a 2-step verification password is set.
        self.has_password: bool = get_object(kwargs.get('has_password'))
        # Hint for the password; may be empty.
        self.password_hint: str = get_object(kwargs.get('password_hint'))
        # True, if a recovery email is set.
        self.has_recovery_email_address: bool = get_object(kwargs.get('has_recovery_email_address'))
        # True, if some Telegram Passport elements were saved.
        self.has_passport_data: bool = get_object(kwargs.get('has_passport_data'))
        # Information about the recovery email address to which the confirmation email was sent; may be null.
        self.recovery_email_address_code_info: EmailAddressAuthenticationCodeInfo = get_object(kwargs.get('recovery_email_address_code_info'))
        # Pattern of the email address set up for logging in.
        self.login_email_address_pattern: str = get_object(kwargs.get('login_email_address_pattern'))
        # If not 0, point in time (Unix timestamp) after which the 2-step verification password can be reset immediately using resetPassword.
        self.pending_reset_date: int = get_object(kwargs.get('pending_reset_date'))


class PaymentProvider(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PaymentOption(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Title for the payment option.
        self.title: str = get_object(kwargs.get('title'))
        # Payment form URL to be opened in a web view.
        self.url: str = get_object(kwargs.get('url'))


class SavedCredentials(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the saved credentials.
        self.id: str = get_object(kwargs.get('id'))
        # Title of the saved credentials.
        self.title: str = get_object(kwargs.get('title'))


class PaymentForm(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The payment form identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Full information about the invoice.
        self.invoice: Invoice = get_object(kwargs.get('invoice'))
        # User identifier of the seller bot.
        self.seller_bot_user_id: int = get_object(kwargs.get('seller_bot_user_id'))
        # User identifier of the payment provider bot.
        self.payment_provider_user_id: int = get_object(kwargs.get('payment_provider_user_id'))
        # Information about the payment provider.
        self.payment_provider: PaymentProvider = get_object(kwargs.get('payment_provider'))
        # The list of additional payment options.
        self.additional_payment_options: list[PaymentOption] = get_object(kwargs.get('additional_payment_options'))
        # Saved server-side order information; may be null.
        self.saved_order_info: OrderInfo = get_object(kwargs.get('saved_order_info'))
        # The list of saved payment credentials.
        self.saved_credentials: list[SavedCredentials] = get_object(kwargs.get('saved_credentials'))
        # True, if the user can choose to save credentials.
        self.can_save_credentials: bool = get_object(kwargs.get('can_save_credentials'))
        # True, if the user will be able to save credentials, if sets up a 2-step verification password.
        self.need_password: bool = get_object(kwargs.get('need_password'))
        # Product title.
        self.product_title: str = get_object(kwargs.get('product_title'))
        # Product description.
        self.product_description: FormattedText = get_object(kwargs.get('product_description'))
        # Product photo; may be null.
        self.product_photo: Photo = get_object(kwargs.get('product_photo'))


class PaymentProviderSmartGlocal(PaymentProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Public payment token.
        self.public_token: str = get_object(kwargs.get('public_token'))


class PaymentProviderStripe(PaymentProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Stripe API publishable key.
        self.publishable_key: str = get_object(kwargs.get('publishable_key'))
        # True, if the user country must be provided.
        self.need_country: bool = get_object(kwargs.get('need_country'))
        # True, if the user ZIP/postal code must be provided.
        self.need_postal_code: bool = get_object(kwargs.get('need_postal_code'))
        # True, if the cardholder name must be provided.
        self.need_cardholder_name: bool = get_object(kwargs.get('need_cardholder_name'))


class PaymentProviderOther(PaymentProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Payment form URL.
        self.url: str = get_object(kwargs.get('url'))


class ShippingOption(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Shipping option identifier.
        self.id: str = get_object(kwargs.get('id'))
        # Option title.
        self.title: str = get_object(kwargs.get('title'))
        # A list of objects used to calculate the total shipping costs.
        self.price_parts: list[LabeledPricePart] = get_object(kwargs.get('price_parts'))


class PaymentReceipt(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Product title.
        self.title: str = get_object(kwargs.get('title'))
        # Product description.
        self.description: FormattedText = get_object(kwargs.get('description'))
        # Product photo; may be null.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Point in time (Unix timestamp) when the payment was made.
        self.date: int = get_object(kwargs.get('date'))
        # User identifier of the seller bot.
        self.seller_bot_user_id: int = get_object(kwargs.get('seller_bot_user_id'))
        # User identifier of the payment provider bot.
        self.payment_provider_user_id: int = get_object(kwargs.get('payment_provider_user_id'))
        # Information about the invoice.
        self.invoice: Invoice = get_object(kwargs.get('invoice'))
        # Order information; may be null.
        self.order_info: OrderInfo = get_object(kwargs.get('order_info'))
        # Chosen shipping option; may be null.
        self.shipping_option: ShippingOption = get_object(kwargs.get('shipping_option'))
        # Title of the saved credentials chosen by the buyer.
        self.credentials_title: str = get_object(kwargs.get('credentials_title'))
        # The amount of tip chosen by the buyer in the smallest units of the currency.
        self.tip_amount: int = get_object(kwargs.get('tip_amount'))


class PaymentResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the payment request was successful; otherwise, the verification_url will be non-empty.
        self.success: bool = get_object(kwargs.get('success'))
        # URL for additional payment credentials verification.
        self.verification_url: str = get_object(kwargs.get('verification_url'))


class PhoneNumberAuthenticationSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Pass true if the authentication code may be sent via a flash call to the specified phone number.
        self.allow_flash_call: bool = get_object(kwargs.get('allow_flash_call'))
        # Pass true if the authentication code may be sent via a missed call to the specified phone number.
        self.allow_missed_call: bool = get_object(kwargs.get('allow_missed_call'))
        # Pass true if the authenticated phone number is used on the current device.
        self.is_current_phone_number: bool = get_object(kwargs.get('is_current_phone_number'))
        # For official applications only. True, if the application can use Android SMS Retriever API (requires Google Play Services &gt;= 10.2) to automatically receive the authentication code from the SMS. See https://developers.google.com/identity/sms-retriever/ for more details.
        self.allow_sms_retriever_api: bool = get_object(kwargs.get('allow_sms_retriever_api'))
        # For official Android and iOS applications only; pass null otherwise. Settings for Firebase Authentication.
        self.firebase_authentication_settings: FirebaseAuthenticationSettings = get_object(kwargs.get('firebase_authentication_settings'))
        # List of up to 20 authentication tokens, recently received in updateOption(&quot;authentication_token&quot;) in previously logged out sessions.
        self.authentication_tokens: list[str] = get_object(kwargs.get('authentication_tokens'))


class PhoneNumberInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the country to which the phone number belongs; may be null.
        self.country: CountryInfo = get_object(kwargs.get('country'))
        # The part of the phone number denoting country calling code or its part.
        self.country_calling_code: str = get_object(kwargs.get('country_calling_code'))
        # The phone number without country calling code formatted accordingly to local rules. Expected digits are returned as '-', but even more digits might be entered by the user.
        self.formatted_phone_number: str = get_object(kwargs.get('formatted_phone_number'))
        # True, if the phone number was bought on Fragment and isn't tied to a SIM card.
        self.is_anonymous: bool = get_object(kwargs.get('is_anonymous'))


class Point(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The point's first coordinate.
        self.x: float = get_object(kwargs.get('x'))
        # The point's second coordinate.
        self.y: float = get_object(kwargs.get('y'))


class PollOption(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Option text; 1-100 characters.
        self.text: str = get_object(kwargs.get('text'))
        # Number of voters for this option, available only for closed or voted polls.
        self.voter_count: int = get_object(kwargs.get('voter_count'))
        # The percentage of votes for this option; 0-100.
        self.vote_percentage: int = get_object(kwargs.get('vote_percentage'))
        # True, if the option was chosen by the user.
        self.is_chosen: bool = get_object(kwargs.get('is_chosen'))
        # True, if the option is being chosen by a pending setPollAnswer request.
        self.is_being_chosen: bool = get_object(kwargs.get('is_being_chosen'))


class PollTypeRegular(PollType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if multiple answer options can be chosen simultaneously.
        self.allow_multiple_answers: bool = get_object(kwargs.get('allow_multiple_answers'))


class PollTypeQuiz(PollType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # 0-based identifier of the correct answer option; -1 for a yet unanswered poll.
        self.correct_option_id: int = get_object(kwargs.get('correct_option_id'))
        # Text that is shown when the user chooses an incorrect answer or taps on the lamp icon; 0-200 characters with at most 2 line feeds; empty for a yet unanswered poll.
        self.explanation: FormattedText = get_object(kwargs.get('explanation'))


class PremiumFeature(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureIncreasedLimits(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureIncreasedUploadFileSize(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureImprovedDownloadSpeed(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureVoiceRecognition(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureDisabledAds(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureUniqueReactions(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureUniqueStickers(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureCustomEmoji(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureAdvancedChatManagement(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureProfileBadge(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureEmojiStatus(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureAnimatedProfilePhoto(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureForumTopicIcon(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureAppIcons(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureRealTimeChatTranslation(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeatureUpgradedStories(PremiumFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumFeaturePromotionAnimation(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Premium feature.
        self.feature: PremiumFeature = get_object(kwargs.get('feature'))
        # Promotion animation for the feature.
        self.animation: Animation = get_object(kwargs.get('animation'))


class PremiumLimit(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The type of the limit.
        self.type: PremiumLimitType = get_object(kwargs.get('type'))
        # Default value of the limit.
        self.default_value: int = get_object(kwargs.get('default_value'))
        # Value of the limit for Premium users.
        self.premium_value: int = get_object(kwargs.get('premium_value'))


class PremiumFeatures(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The list of available features.
        self.features: list[PremiumFeature] = get_object(kwargs.get('features'))
        # The list of limits, increased for Premium users.
        self.limits: list[PremiumLimit] = get_object(kwargs.get('limits'))
        # An internal link to be opened to pay for Telegram Premium if store payment isn't possible; may be null if direct payment isn't available.
        self.payment_link: InternalLinkType = get_object(kwargs.get('payment_link'))


class PremiumLimitType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeSupergroupCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypePinnedChatCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeCreatedPublicChatCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeSavedAnimationCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeFavoriteStickerCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeChatFilterCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeChatFilterChosenChatCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypePinnedArchivedChatCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeCaptionLength(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeBioLength(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeChatFilterInviteLinkCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeShareableChatFilterCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeActiveStoryCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeWeeklySentStoryCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeMonthlySentStoryCount(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumLimitTypeStoryCaptionLength(PremiumLimitType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumPaymentOption(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # ISO 4217 currency code for Telegram Premium subscription payment.
        self.currency: str = get_object(kwargs.get('currency'))
        # The amount to pay, in the smallest units of the currency.
        self.amount: int = get_object(kwargs.get('amount'))
        # The discount associated with this option, as a percentage.
        self.discount_percentage: int = get_object(kwargs.get('discount_percentage'))
        # Number of month the Telegram Premium subscription will be active.
        self.month_count: int = get_object(kwargs.get('month_count'))
        # Identifier of the store product associated with the option.
        self.store_product_id: str = get_object(kwargs.get('store_product_id'))
        # An internal link to be opened for buying Telegram Premium to the user if store payment isn't possible; may be null if direct payment isn't available.
        self.payment_link: InternalLinkType = get_object(kwargs.get('payment_link'))


class PremiumStoryFeature(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumSource(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumSourceLimitExceeded(PremiumSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the exceeded limit.
        self.limit_type: PremiumLimitType = get_object(kwargs.get('limit_type'))


class PremiumSourceFeature(PremiumSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The used feature.
        self.feature: PremiumFeature = get_object(kwargs.get('feature'))


class PremiumSourceStoryFeature(PremiumSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The used feature.
        self.feature: PremiumStoryFeature = get_object(kwargs.get('feature'))


class PremiumSourceLink(PremiumSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The referrer from the link.
        self.referrer: str = get_object(kwargs.get('referrer'))


class PremiumSourceSettings(PremiumSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumStatePaymentOption(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the payment option.
        self.payment_option: PremiumPaymentOption = get_object(kwargs.get('payment_option'))
        # True, if this is the currently used Telegram Premium subscription option.
        self.is_current: bool = get_object(kwargs.get('is_current'))
        # True, if the payment option can be used to upgrade the existing Telegram Premium subscription.
        self.is_upgrade: bool = get_object(kwargs.get('is_upgrade'))
        # Identifier of the last in-store transaction for the currently used option.
        self.last_transaction_id: str = get_object(kwargs.get('last_transaction_id'))


class PremiumState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text description of the state of the current Premium subscription; may be empty if the current user has no Telegram Premium subscription.
        self.state: FormattedText = get_object(kwargs.get('state'))
        # The list of available options for buying Telegram Premium.
        self.payment_options: list[PremiumStatePaymentOption] = get_object(kwargs.get('payment_options'))
        # The list of available promotion animations for Premium features.
        self.animations: list[PremiumFeaturePromotionAnimation] = get_object(kwargs.get('animations'))


class PremiumStoryFeaturePriorityOrder(PremiumStoryFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumStoryFeatureStealthMode(PremiumStoryFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumStoryFeaturePermanentViewsHistory(PremiumStoryFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumStoryFeatureCustomExpirationDuration(PremiumStoryFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumStoryFeatureSaveStories(PremiumStoryFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PremiumStoryFeatureLinksAndFormatting(PremiumStoryFeature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ProfilePhoto(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Photo identifier; 0 for an empty photo. Can be used to find a photo in a list of user profile photos.
        self.id: int = get_object(kwargs.get('id'))
        # A small (160x160) user profile photo. The file can be downloaded only before the photo is changed.
        self.small: File = get_object(kwargs.get('small'))
        # A big (640x640) user profile photo. The file can be downloaded only before the photo is changed.
        self.big: File = get_object(kwargs.get('big'))
        # User profile photo minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # True, if the photo has animated variant.
        self.has_animation: bool = get_object(kwargs.get('has_animation'))
        # True, if the photo is visible only for the current user.
        self.is_personal: bool = get_object(kwargs.get('is_personal'))


class Proxy(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the proxy.
        self.id: int = get_object(kwargs.get('id'))
        # Proxy server domain or IP address.
        self.server: str = get_object(kwargs.get('server'))
        # Proxy server port.
        self.port: int = get_object(kwargs.get('port'))
        # Point in time (Unix timestamp) when the proxy was last used; 0 if never.
        self.last_used_date: int = get_object(kwargs.get('last_used_date'))
        # True, if the proxy is enabled now.
        self.is_enabled: bool = get_object(kwargs.get('is_enabled'))
        # Type of the proxy.
        self.type: ProxyType = get_object(kwargs.get('type'))


class Proxies(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of proxy servers.
        self.proxies: list[Proxy] = get_object(kwargs.get('proxies'))


class ProxyTypeSocks5(ProxyType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username for logging in; may be empty.
        self.username: str = get_object(kwargs.get('username'))
        # Password for logging in; may be empty.
        self.password: str = get_object(kwargs.get('password'))


class ProxyTypeHttp(ProxyType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Username for logging in; may be empty.
        self.username: str = get_object(kwargs.get('username'))
        # Password for logging in; may be empty.
        self.password: str = get_object(kwargs.get('password'))
        # Pass true if the proxy supports only HTTP requests and doesn't support transparent TCP connections via HTTP CONNECT method.
        self.http_only: bool = get_object(kwargs.get('http_only'))


class ProxyTypeMtproto(ProxyType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The proxy's secret in hexadecimal encoding.
        self.secret: str = get_object(kwargs.get('secret'))


class PublicChatType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PublicChatTypeHasUsername(PublicChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PublicChatTypeIsLocationBased(PublicChatType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PushMessageContentHidden(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentAnimation(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message content; may be null.
        self.animation: Animation = get_object(kwargs.get('animation'))
        # Animation caption.
        self.caption: str = get_object(kwargs.get('caption'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentAudio(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message content; may be null.
        self.audio: Audio = get_object(kwargs.get('audio'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentContact(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Contact's name.
        self.name: str = get_object(kwargs.get('name'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentContactRegistered(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PushMessageContentDocument(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message content; may be null.
        self.document: Document = get_object(kwargs.get('document'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentGame(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Game title, empty for pinned game message.
        self.title: str = get_object(kwargs.get('title'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentGameScore(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Game title, empty for pinned message.
        self.title: str = get_object(kwargs.get('title'))
        # New score, 0 for pinned message.
        self.score: int = get_object(kwargs.get('score'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentInvoice(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Product price.
        self.price: str = get_object(kwargs.get('price'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentLocation(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the location is live.
        self.is_live: bool = get_object(kwargs.get('is_live'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentPhoto(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message content; may be null.
        self.photo: Photo = get_object(kwargs.get('photo'))
        # Photo caption.
        self.caption: str = get_object(kwargs.get('caption'))
        # True, if the photo is secret.
        self.is_secret: bool = get_object(kwargs.get('is_secret'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentPoll(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Poll question.
        self.question: str = get_object(kwargs.get('question'))
        # True, if the poll is regular and not in quiz mode.
        self.is_regular: bool = get_object(kwargs.get('is_regular'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentScreenshotTaken(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PushMessageContentSticker(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message content; may be null.
        self.sticker: Sticker = get_object(kwargs.get('sticker'))
        # Emoji corresponding to the sticker; may be empty.
        self.emoji: str = get_object(kwargs.get('emoji'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentStory(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentText(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message text.
        self.text: str = get_object(kwargs.get('text'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentVideo(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message content; may be null.
        self.video: Video = get_object(kwargs.get('video'))
        # Video caption.
        self.caption: str = get_object(kwargs.get('caption'))
        # True, if the video is secret.
        self.is_secret: bool = get_object(kwargs.get('is_secret'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentVideoNote(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message content; may be null.
        self.video_note: VideoNote = get_object(kwargs.get('video_note'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentVoiceNote(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message content; may be null.
        self.voice_note: VoiceNote = get_object(kwargs.get('voice_note'))
        # True, if the message is a pinned message with the specified content.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class PushMessageContentBasicGroupChatCreate(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PushMessageContentChatAddMembers(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the added member.
        self.member_name: str = get_object(kwargs.get('member_name'))
        # True, if the current user was added to the group.
        self.is_current_user: bool = get_object(kwargs.get('is_current_user'))
        # True, if the user has returned to the group themselves.
        self.is_returned: bool = get_object(kwargs.get('is_returned'))


class PushMessageContentChatChangePhoto(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PushMessageContentChatChangeTitle(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New chat title.
        self.title: str = get_object(kwargs.get('title'))


class PushMessageContentChatSetBackground(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the set background is the same as the background of the current user.
        self.is_same: bool = get_object(kwargs.get('is_same'))


class PushMessageContentChatSetTheme(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # If non-empty, name of a new theme, set for the chat. Otherwise, the chat theme was reset to the default one.
        self.theme_name: str = get_object(kwargs.get('theme_name'))


class PushMessageContentChatDeleteMember(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the deleted member.
        self.member_name: str = get_object(kwargs.get('member_name'))
        # True, if the current user was deleted from the group.
        self.is_current_user: bool = get_object(kwargs.get('is_current_user'))
        # True, if the user has left the group themselves.
        self.is_left: bool = get_object(kwargs.get('is_left'))


class PushMessageContentChatJoinByLink(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PushMessageContentChatJoinByRequest(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PushMessageContentRecurringPayment(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The paid amount.
        self.amount: str = get_object(kwargs.get('amount'))


class PushMessageContentSuggestProfilePhoto(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class PushMessageContentMessageForwards(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number of forwarded messages.
        self.total_count: int = get_object(kwargs.get('total_count'))


class PushMessageContentMediaAlbum(PushMessageContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number of messages in the album.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # True, if the album has at least one photo.
        self.has_photos: bool = get_object(kwargs.get('has_photos'))
        # True, if the album has at least one video file.
        self.has_videos: bool = get_object(kwargs.get('has_videos'))
        # True, if the album has at least one audio file.
        self.has_audios: bool = get_object(kwargs.get('has_audios'))
        # True, if the album has at least one document.
        self.has_documents: bool = get_object(kwargs.get('has_documents'))


class PushReceiverId(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The globally unique identifier of push notification subscription.
        self.id: int = get_object(kwargs.get('id'))


class ReactionTypeEmoji(ReactionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text representation of the reaction.
        self.emoji: str = get_object(kwargs.get('emoji'))


class ReactionTypeCustomEmoji(ReactionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the custom emoji.
        self.custom_emoji_id: int = get_object(kwargs.get('custom_emoji_id'))


class RecommendedChatFilter(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat filter.
        self.filter: ChatFilter = get_object(kwargs.get('filter'))
        # Chat filter description.
        self.description: str = get_object(kwargs.get('description'))


class RecommendedChatFilters(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of recommended chat filters.
        self.chat_filters: list[RecommendedChatFilter] = get_object(kwargs.get('chat_filters'))


class RecoveryEmailAddress(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Recovery email address.
        self.recovery_email_address: str = get_object(kwargs.get('recovery_email_address'))


class ReplyMarkupRemoveKeyboard(ReplyMarkup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the keyboard is removed only for the mentioned users or the target user of a reply.
        self.is_personal: bool = get_object(kwargs.get('is_personal'))


class ReplyMarkupForceReply(ReplyMarkup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if a forced reply must automatically be shown to the current user. For outgoing messages, specify true to show the forced reply only for the mentioned users and for the target user of a reply.
        self.is_personal: bool = get_object(kwargs.get('is_personal'))
        # If non-empty, the placeholder to be shown in the input field when the reply is active; 0-64 characters.
        self.input_field_placeholder: str = get_object(kwargs.get('input_field_placeholder'))


class ReplyMarkupShowKeyboard(ReplyMarkup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of rows of bot keyboard buttons.
        self.rows: list[list[KeyboardButton]] = get_object(kwargs.get('rows'))
        # True, if the keyboard is supposed to always be shown when the ordinary keyboard is hidden.
        self.is_persistent: bool = get_object(kwargs.get('is_persistent'))
        # True, if the application needs to resize the keyboard vertically.
        self.resize_keyboard: bool = get_object(kwargs.get('resize_keyboard'))
        # True, if the application needs to hide the keyboard after use.
        self.one_time: bool = get_object(kwargs.get('one_time'))
        # True, if the keyboard must automatically be shown to the current user. For outgoing messages, specify true to show the keyboard only for the mentioned users and for the target user of a reply.
        self.is_personal: bool = get_object(kwargs.get('is_personal'))
        # If non-empty, the placeholder to be shown in the input field when the keyboard is active; 0-64 characters.
        self.input_field_placeholder: str = get_object(kwargs.get('input_field_placeholder'))


class ReplyMarkupInlineKeyboard(ReplyMarkup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of rows of inline keyboard buttons.
        self.rows: list[list[InlineKeyboardButton]] = get_object(kwargs.get('rows'))


class ReportReason(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonSpam(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonViolence(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonPornography(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonChildAbuse(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonCopyright(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonUnrelatedLocation(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonFake(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonIllegalDrugs(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonPersonalDetails(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ReportReasonCustom(ReportReason):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ResetPasswordResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ResetPasswordResultOk(ResetPasswordResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ResetPasswordResultPending(ResetPasswordResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) after which the password can be reset immediately using resetPassword.
        self.pending_reset_date: int = get_object(kwargs.get('pending_reset_date'))


class ResetPasswordResultDeclined(ResetPasswordResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) when the password reset can be retried.
        self.retry_date: int = get_object(kwargs.get('retry_date'))


class RichTextPlain(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: str = get_object(kwargs.get('text'))


class RichTextBold(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))


class RichTextItalic(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))


class RichTextUnderline(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))


class RichTextStrikethrough(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))


class RichTextFixed(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))


class RichTextUrl(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))
        # URL.
        self.url: str = get_object(kwargs.get('url'))
        # True, if the URL has cached instant view server-side.
        self.is_cached: bool = get_object(kwargs.get('is_cached'))


class RichTextEmailAddress(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))
        # Email address.
        self.email_address: str = get_object(kwargs.get('email_address'))


class RichTextSubscript(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))


class RichTextSuperscript(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))


class RichTextMarked(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))


class RichTextPhoneNumber(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: RichText = get_object(kwargs.get('text'))
        # Phone number.
        self.phone_number: str = get_object(kwargs.get('phone_number'))


class RichTextIcon(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The image represented as a document. The image can be in GIF, JPEG or PNG format.
        self.document: Document = get_object(kwargs.get('document'))
        # Width of a bounding box in which the image must be shown; 0 if unknown.
        self.width: int = get_object(kwargs.get('width'))
        # Height of a bounding box in which the image must be shown; 0 if unknown.
        self.height: int = get_object(kwargs.get('height'))


class RichTextReference(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The text.
        self.text: RichText = get_object(kwargs.get('text'))
        # The name of a richTextAnchor object, which is the first element of the target richTexts object.
        self.anchor_name: str = get_object(kwargs.get('anchor_name'))
        # An HTTP URL, opening the reference.
        self.url: str = get_object(kwargs.get('url'))


class RichTextAnchor(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Anchor name.
        self.name: str = get_object(kwargs.get('name'))


class RichTextAnchorLink(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The link text.
        self.text: RichText = get_object(kwargs.get('text'))
        # The anchor name. If the name is empty, the link must bring back to top.
        self.anchor_name: str = get_object(kwargs.get('anchor_name'))
        # An HTTP URL, opening the anchor.
        self.url: str = get_object(kwargs.get('url'))


class RichTexts(RichText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Texts.
        self.texts: list[RichText] = get_object(kwargs.get('texts'))


class RtmpUrl(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The URL.
        self.url: str = get_object(kwargs.get('url'))
        # Stream key.
        self.stream_key: str = get_object(kwargs.get('stream_key'))


class ScopeNotificationSettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Time left before notifications will be unmuted, in seconds.
        self.mute_for: int = get_object(kwargs.get('mute_for'))
        # Identifier of the notification sound to be played; 0 if sound is disabled.
        self.sound_id: int = get_object(kwargs.get('sound_id'))
        # True, if message content must be displayed in notifications.
        self.show_preview: bool = get_object(kwargs.get('show_preview'))
        # If true, mute_stories is ignored and story notifications are received only for the first 5 chats from topChatCategoryUsers.
        self.use_default_mute_stories: bool = get_object(kwargs.get('use_default_mute_stories'))
        # True, if story notifications are disabled for the chat.
        self.mute_stories: bool = get_object(kwargs.get('mute_stories'))
        # Identifier of the notification sound to be played for stories; 0 if sound is disabled.
        self.story_sound_id: int = get_object(kwargs.get('story_sound_id'))
        # True, if the sender of stories must be displayed in notifications.
        self.show_story_sender: bool = get_object(kwargs.get('show_story_sender'))
        # True, if notifications for incoming pinned messages will be created as for an ordinary unread message.
        self.disable_pinned_message_notifications: bool = get_object(kwargs.get('disable_pinned_message_notifications'))
        # True, if notifications for messages with mentions will be created as for an ordinary unread message.
        self.disable_mention_notifications: bool = get_object(kwargs.get('disable_mention_notifications'))


class SearchMessagesFilter(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterEmpty(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterAnimation(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterAudio(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterDocument(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterPhoto(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterVideo(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterVoiceNote(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterPhotoAndVideo(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterUrl(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterChatPhoto(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterVideoNote(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterVoiceAndVideoNote(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterMention(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterUnreadMention(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterUnreadReaction(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterFailedToSend(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SearchMessagesFilterPinned(SearchMessagesFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Seconds(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number of seconds.
        self.seconds: float = get_object(kwargs.get('seconds'))


class SecretChatState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SecretChat(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Secret chat identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the chat partner.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # State of the secret chat.
        self.state: SecretChatState = get_object(kwargs.get('state'))
        # True, if the chat was created by the current user; false otherwise.
        self.is_outbound: bool = get_object(kwargs.get('is_outbound'))
        # Hash of the currently used key for comparison with the hash of the chat partner's key. This is a string of 36 little-endian bytes, which must be split into groups of 2 bits, each denoting a pixel of one of 4 colors FFFFFF, D5E6F3, 2D5775, and 2F99C9. The pixels must be used to make a 12x12 square image filled from left to right, top to bottom. Alternatively, the first 32 bytes of the hash can be converted to the hexadecimal format and printed as 32 2-digit hex numbers.
        self.key_hash: bytes = get_object(kwargs.get('key_hash'))
        # Secret chat layer; determines features supported by the chat partner's application. Nested text entities and underline and strikethrough entities are supported if the layer &gt;= 101, files bigger than 2000MB are supported if the layer &gt;= 143, spoiler and custom emoji text entities are supported if the layer &gt;= 144.
        self.layer: int = get_object(kwargs.get('layer'))


class SecretChatStatePending(SecretChatState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SecretChatStateReady(SecretChatState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SecretChatStateClosed(SecretChatState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SentWebAppMessage(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the sent inline message, if known.
        self.inline_message_id: str = get_object(kwargs.get('inline_message_id'))


class SessionType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Session(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Session identifier.
        self.id: int = get_object(kwargs.get('id'))
        # True, if this session is the current session.
        self.is_current: bool = get_object(kwargs.get('is_current'))
        # True, if a 2-step verification password is needed to complete authorization of the session.
        self.is_password_pending: bool = get_object(kwargs.get('is_password_pending'))
        # True, if the session wasn't confirmed from another session.
        self.is_unconfirmed: bool = get_object(kwargs.get('is_unconfirmed'))
        # True, if incoming secret chats can be accepted by the session.
        self.can_accept_secret_chats: bool = get_object(kwargs.get('can_accept_secret_chats'))
        # True, if incoming calls can be accepted by the session.
        self.can_accept_calls: bool = get_object(kwargs.get('can_accept_calls'))
        # Session type based on the system and application version, which can be used to display a corresponding icon.
        self.type: SessionType = get_object(kwargs.get('type'))
        # Telegram API identifier, as provided by the application.
        self.api_id: int = get_object(kwargs.get('api_id'))
        # Name of the application, as provided by the application.
        self.application_name: str = get_object(kwargs.get('application_name'))
        # The version of the application, as provided by the application.
        self.application_version: str = get_object(kwargs.get('application_version'))
        # True, if the application is an official application or uses the api_id of an official application.
        self.is_official_application: bool = get_object(kwargs.get('is_official_application'))
        # Model of the device the application has been run or is running on, as provided by the application.
        self.device_model: str = get_object(kwargs.get('device_model'))
        # Operating system the application has been run or is running on, as provided by the application.
        self.platform: str = get_object(kwargs.get('platform'))
        # Version of the operating system the application has been run or is running on, as provided by the application.
        self.system_version: str = get_object(kwargs.get('system_version'))
        # Point in time (Unix timestamp) when the user has logged in.
        self.log_in_date: int = get_object(kwargs.get('log_in_date'))
        # Point in time (Unix timestamp) when the session was last used.
        self.last_active_date: int = get_object(kwargs.get('last_active_date'))
        # IP address from which the session was created, in human-readable format.
        self.ip_address: str = get_object(kwargs.get('ip_address'))
        # A human-readable description of the location from which the session was created, based on the IP address.
        self.location: str = get_object(kwargs.get('location'))


class SessionTypeAndroid(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeApple(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeBrave(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeChrome(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeEdge(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeFirefox(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeIpad(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeIphone(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeLinux(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeMac(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeOpera(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeSafari(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeUbuntu(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeUnknown(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeVivaldi(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeWindows(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SessionTypeXbox(SessionType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Sessions(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of sessions.
        self.sessions: list[Session] = get_object(kwargs.get('sessions'))
        # Number of days of inactivity before sessions will automatically be terminated; 1-366 days.
        self.inactive_session_ttl_days: int = get_object(kwargs.get('inactive_session_ttl_days'))


class SpeechRecognitionResult(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SpeechRecognitionResultPending(SpeechRecognitionResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Partially recognized text.
        self.partial_text: str = get_object(kwargs.get('partial_text'))


class SpeechRecognitionResultText(SpeechRecognitionResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Recognized text.
        self.text: str = get_object(kwargs.get('text'))


class SpeechRecognitionResultError(SpeechRecognitionResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Recognition error.
        self.error: Error = get_object(kwargs.get('error'))


class SponsoredMessage(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Message identifier; unique for the chat to which the sponsored message belongs among both ordinary and sponsored messages.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # True, if the message needs to be labeled as &quot;recommended&quot; instead of &quot;sponsored&quot;.
        self.is_recommended: bool = get_object(kwargs.get('is_recommended'))
        # Content of the message. Currently, can be only of the type messageText.
        self.content: MessageContent = get_object(kwargs.get('content'))
        # Information about the sponsor of the message.
        self.sponsor: MessageSponsor = get_object(kwargs.get('sponsor'))
        # If non-empty, additional information about the sponsored message to be shown along with the message.
        self.additional_info: str = get_object(kwargs.get('additional_info'))


class SponsoredMessages(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of sponsored messages.
        self.messages: list[SponsoredMessage] = get_object(kwargs.get('messages'))
        # The minimum number of messages between shown sponsored messages, or 0 if only one sponsored message must be shown after all ordinary messages.
        self.messages_between: int = get_object(kwargs.get('messages_between'))


class StatisticalGraphData(StatisticalGraph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Graph data in JSON format.
        self.json_data: str = get_object(kwargs.get('json_data'))
        # If non-empty, a token which can be used to receive a zoomed in graph.
        self.zoom_token: str = get_object(kwargs.get('zoom_token'))


class StatisticalGraphAsync(StatisticalGraph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The token to use for data loading.
        self.token: str = get_object(kwargs.get('token'))


class StatisticalGraphError(StatisticalGraph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The error message.
        self.error_message: str = get_object(kwargs.get('error_message'))


class StickerFormat(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StickerFullType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StickerFormatWebp(StickerFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StickerFormatTgs(StickerFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StickerFormatWebm(StickerFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StickerFullTypeRegular(StickerFullType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Premium animation of the sticker; may be null. If present, only Telegram Premium users can use the sticker.
        self.premium_animation: File = get_object(kwargs.get('premium_animation'))


class StickerFullTypeMask(StickerFullType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Position where the mask is placed; may be null.
        self.mask_position: MaskPosition = get_object(kwargs.get('mask_position'))


class StickerFullTypeCustomEmoji(StickerFullType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the custom emoji.
        self.custom_emoji_id: int = get_object(kwargs.get('custom_emoji_id'))
        # True, if the sticker must be repainted to a text color in messages, the color of the Telegram Premium badge in emoji status, white color on chat photos, or another appropriate color in other places.
        self.needs_repainting: bool = get_object(kwargs.get('needs_repainting'))


class StickerType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StickerSet(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the sticker set.
        self.id: int = get_object(kwargs.get('id'))
        # Title of the sticker set.
        self.title: str = get_object(kwargs.get('title'))
        # Name of the sticker set.
        self.name: str = get_object(kwargs.get('name'))
        # Sticker set thumbnail in WEBP, TGS, or WEBM format with width and height 100; may be null. The file can be downloaded only before the thumbnail is changed.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))
        # Sticker set thumbnail's outline represented as a list of closed vector paths; may be empty. The coordinate system origin is in the upper-left corner.
        self.thumbnail_outline: list[ClosedVectorPath] = get_object(kwargs.get('thumbnail_outline'))
        # True, if the sticker set has been installed by the current user.
        self.is_installed: bool = get_object(kwargs.get('is_installed'))
        # True, if the sticker set has been archived. A sticker set can't be installed and archived simultaneously.
        self.is_archived: bool = get_object(kwargs.get('is_archived'))
        # True, if the sticker set is official.
        self.is_official: bool = get_object(kwargs.get('is_official'))
        # Format of the stickers in the set.
        self.sticker_format: StickerFormat = get_object(kwargs.get('sticker_format'))
        # Type of the stickers in the set.
        self.sticker_type: StickerType = get_object(kwargs.get('sticker_type'))
        # True for already viewed trending sticker sets.
        self.is_viewed: bool = get_object(kwargs.get('is_viewed'))
        # List of stickers in this set.
        self.stickers: list[Sticker] = get_object(kwargs.get('stickers'))
        # A list of emoji corresponding to the stickers in the same order. The list is only for informational purposes, because a sticker is always sent with a fixed emoji from the corresponding Sticker object.
        self.emojis: list[Emojis] = get_object(kwargs.get('emojis'))


class StickerSetInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the sticker set.
        self.id: int = get_object(kwargs.get('id'))
        # Title of the sticker set.
        self.title: str = get_object(kwargs.get('title'))
        # Name of the sticker set.
        self.name: str = get_object(kwargs.get('name'))
        # Sticker set thumbnail in WEBP, TGS, or WEBM format with width and height 100; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))
        # Sticker set thumbnail's outline represented as a list of closed vector paths; may be empty. The coordinate system origin is in the upper-left corner.
        self.thumbnail_outline: list[ClosedVectorPath] = get_object(kwargs.get('thumbnail_outline'))
        # True, if the sticker set has been installed by the current user.
        self.is_installed: bool = get_object(kwargs.get('is_installed'))
        # True, if the sticker set has been archived. A sticker set can't be installed and archived simultaneously.
        self.is_archived: bool = get_object(kwargs.get('is_archived'))
        # True, if the sticker set is official.
        self.is_official: bool = get_object(kwargs.get('is_official'))
        # Format of the stickers in the set.
        self.sticker_format: StickerFormat = get_object(kwargs.get('sticker_format'))
        # Type of the stickers in the set.
        self.sticker_type: StickerType = get_object(kwargs.get('sticker_type'))
        # True for already viewed trending sticker sets.
        self.is_viewed: bool = get_object(kwargs.get('is_viewed'))
        # Total number of stickers in the set.
        self.size: int = get_object(kwargs.get('size'))
        # Up to the first 5 stickers from the set, depending on the context. If the application needs more stickers the full sticker set needs to be requested.
        self.covers: list[Sticker] = get_object(kwargs.get('covers'))


class StickerSets(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of sticker sets found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of sticker sets.
        self.sets: list[StickerSetInfo] = get_object(kwargs.get('sets'))


class StickerTypeRegular(StickerType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StickerTypeMask(StickerType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StickerTypeCustomEmoji(StickerType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Stickers(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of stickers.
        self.stickers: list[Sticker] = get_object(kwargs.get('stickers'))


class StorageStatisticsByChat(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier; 0 if none.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Total size of the files in the chat, in bytes.
        self.size: int = get_object(kwargs.get('size'))
        # Total number of files in the chat.
        self.count: int = get_object(kwargs.get('count'))
        # Statistics split by file types.
        self.by_file_type: list[StorageStatisticsByFileType] = get_object(kwargs.get('by_file_type'))


class StorageStatistics(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total size of files, in bytes.
        self.size: int = get_object(kwargs.get('size'))
        # Total number of files.
        self.count: int = get_object(kwargs.get('count'))
        # Statistics split by chats.
        self.by_chat: list[StorageStatisticsByChat] = get_object(kwargs.get('by_chat'))


class StorageStatisticsByFileType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # File type.
        self.file_type: FileType = get_object(kwargs.get('file_type'))
        # Total size of the files, in bytes.
        self.size: int = get_object(kwargs.get('size'))
        # Total number of files.
        self.count: int = get_object(kwargs.get('count'))


class StorageStatisticsFast(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total size of files, in bytes.
        self.files_size: int = get_object(kwargs.get('files_size'))
        # Approximate number of files.
        self.file_count: int = get_object(kwargs.get('file_count'))
        # Size of the database.
        self.database_size: int = get_object(kwargs.get('database_size'))
        # Size of the language pack database.
        self.language_pack_database_size: int = get_object(kwargs.get('language_pack_database_size'))
        # Size of the TDLib internal log.
        self.log_size: int = get_object(kwargs.get('log_size'))


class StorePaymentPurpose(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StorePaymentPurposePremiumSubscription(StorePaymentPurpose):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Pass true if this is a restore of a Telegram Premium purchase; only for App Store.
        self.is_restore: bool = get_object(kwargs.get('is_restore'))
        # Pass true if this is an upgrade from a monthly subscription to early subscription; only for App Store.
        self.is_upgrade: bool = get_object(kwargs.get('is_upgrade'))


class StorePaymentPurposeGiftedPremium(StorePaymentPurpose):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the user for which Premium was gifted.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # ISO 4217 currency code of the payment currency.
        self.currency: str = get_object(kwargs.get('currency'))
        # Paid amount, in the smallest units of the currency.
        self.amount: int = get_object(kwargs.get('amount'))


class Story(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique story identifier among stories of the given sender.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the chat that posted the story.
        self.sender_chat_id: int = get_object(kwargs.get('sender_chat_id'))
        # Point in time (Unix timestamp) when the story was published.
        self.date: int = get_object(kwargs.get('date'))
        # True, if the story is being sent by the current user.
        self.is_being_sent: bool = get_object(kwargs.get('is_being_sent'))
        # True, if the story is being edited by the current user.
        self.is_being_edited: bool = get_object(kwargs.get('is_being_edited'))
        # True, if the story was edited.
        self.is_edited: bool = get_object(kwargs.get('is_edited'))
        # True, if the story is saved in the sender's profile and will be available there after expiration.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))
        # True, if the story is visible only for the current user.
        self.is_visible_only_for_self: bool = get_object(kwargs.get('is_visible_only_for_self'))
        # True, if the story can be forwarded as a message. Otherwise, screenshots and saving of the story content must be also forbidden.
        self.can_be_forwarded: bool = get_object(kwargs.get('can_be_forwarded'))
        # True, if the story can be replied in the chat with the story sender.
        self.can_be_replied: bool = get_object(kwargs.get('can_be_replied'))
        # True, if users viewed the story can be received through getStoryViewers.
        self.can_get_viewers: bool = get_object(kwargs.get('can_get_viewers'))
        # True, if users viewed the story can't be received, because the story has expired more than getOption(&quot;story_viewers_expiration_delay&quot;) seconds ago.
        self.has_expired_viewers: bool = get_object(kwargs.get('has_expired_viewers'))
        # Information about interactions with the story; may be null if the story isn't owned or there were no interactions.
        self.interaction_info: StoryInteractionInfo = get_object(kwargs.get('interaction_info'))
        # Type of the chosen reaction; may be null if none.
        self.chosen_reaction_type: ReactionType = get_object(kwargs.get('chosen_reaction_type'))
        # Privacy rules affecting story visibility; may be approximate for non-owned stories.
        self.privacy_settings: StoryPrivacySettings = get_object(kwargs.get('privacy_settings'))
        # Content of the story.
        self.content: StoryContent = get_object(kwargs.get('content'))
        # Clickable areas to be shown on the story content.
        self.areas: list[StoryArea] = get_object(kwargs.get('areas'))
        # Caption of the story.
        self.caption: FormattedText = get_object(kwargs.get('caption'))


class Stories(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of stories found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # The list of stories.
        self.stories: list[Story] = get_object(kwargs.get('stories'))


class StoryContent(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryPrivacySettings(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryArea(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Position of the area.
        self.position: StoryAreaPosition = get_object(kwargs.get('position'))
        # Type of the area.
        self.type: StoryAreaType = get_object(kwargs.get('type'))


class StoryInteractionInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number of times the story was viewed.
        self.view_count: int = get_object(kwargs.get('view_count'))
        # Number of reactions added to the story.
        self.reaction_count: int = get_object(kwargs.get('reaction_count'))
        # Identifiers of at most 3 recent viewers of the story.
        self.recent_viewer_user_ids: list[int] = get_object(kwargs.get('recent_viewer_user_ids'))


class StoryAreaType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryAreaTypeLocation(StoryAreaType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The location.
        self.location: Location = get_object(kwargs.get('location'))


class StoryAreaTypeVenue(StoryAreaType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the venue.
        self.venue: Venue = get_object(kwargs.get('venue'))


class StoryVideo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Duration of the video, in seconds.
        self.duration: float = get_object(kwargs.get('duration'))
        # Video width.
        self.width: int = get_object(kwargs.get('width'))
        # Video height.
        self.height: int = get_object(kwargs.get('height'))
        # True, if stickers were added to the video. The list of corresponding sticker sets can be received using getAttachedStickerSets.
        self.has_stickers: bool = get_object(kwargs.get('has_stickers'))
        # True, if the video has no sound.
        self.is_animation: bool = get_object(kwargs.get('is_animation'))
        # Video minithumbnail; may be null.
        self.minithumbnail: Minithumbnail = get_object(kwargs.get('minithumbnail'))
        # Video thumbnail in JPEG or MPEG4 format; may be null.
        self.thumbnail: Thumbnail = get_object(kwargs.get('thumbnail'))
        # Size of file prefix, which is supposed to be preloaded, in bytes.
        self.preload_prefix_size: int = get_object(kwargs.get('preload_prefix_size'))
        # File containing the video.
        self.video: File = get_object(kwargs.get('video'))


class StoryContentPhoto(StoryContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The photo.
        self.photo: Photo = get_object(kwargs.get('photo'))


class StoryContentVideo(StoryContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The video in MPEG4 format.
        self.video: StoryVideo = get_object(kwargs.get('video'))
        # Alternative version of the video in MPEG4 format, encoded by x264 codec; may be null.
        self.alternative_video: StoryVideo = get_object(kwargs.get('alternative_video'))


class StoryContentUnsupported(StoryContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryListMain(StoryList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryListArchive(StoryList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryPrivacySettingsEveryone(StoryPrivacySettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifiers of the users that can't see the story; always unknown and empty for non-owned stories.
        self.except_user_ids: list[int] = get_object(kwargs.get('except_user_ids'))


class StoryPrivacySettingsContacts(StoryPrivacySettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifiers of the contacts that can't see the story; always unknown and empty for non-owned stories.
        self.except_user_ids: list[int] = get_object(kwargs.get('except_user_ids'))


class StoryPrivacySettingsCloseFriends(StoryPrivacySettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class StoryPrivacySettingsSelectedUsers(StoryPrivacySettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifiers of the users; always unknown and empty for non-owned stories.
        self.user_ids: list[int] = get_object(kwargs.get('user_ids'))


class StoryViewer(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier of the viewer.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # Approximate point in time (Unix timestamp) when the story was viewed.
        self.view_date: int = get_object(kwargs.get('view_date'))
        # Block list to which the user is added; may be null if none.
        self.block_list: BlockList = get_object(kwargs.get('block_list'))
        # Type of the reaction that was chosen by the user; may be null if none.
        self.chosen_reaction_type: ReactionType = get_object(kwargs.get('chosen_reaction_type'))


class StoryViewers(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of story viewers found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # Approximate total number of reactions set by found story viewers.
        self.total_reaction_count: int = get_object(kwargs.get('total_reaction_count'))
        # List of story viewers.
        self.viewers: list[StoryViewer] = get_object(kwargs.get('viewers'))
        # The offset for the next request. If empty, there are no more results.
        self.next_offset: str = get_object(kwargs.get('next_offset'))


class SuggestedAction(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SuggestedActionEnableArchiveAndMuteNewChats(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SuggestedActionCheckPassword(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SuggestedActionCheckPhoneNumber(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SuggestedActionViewChecksHint(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SuggestedActionConvertToBroadcastGroup(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Supergroup identifier.
        self.supergroup_id: int = get_object(kwargs.get('supergroup_id'))


class SuggestedActionSetPassword(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The number of days to pass between consecutive authorizations if the user declines to set password; if 0, then the user is advised to set the password for security reasons.
        self.authorization_delay: int = get_object(kwargs.get('authorization_delay'))


class SuggestedActionUpgradePremium(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SuggestedActionRestorePremium(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SuggestedActionSubscribeToAnnualPremium(SuggestedAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Usernames(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of active usernames; the first one must be shown as the primary username. The order of active usernames can be changed with reorderActiveUsernames, reorderBotActiveUsernames or reorderSupergroupActiveUsernames.
        self.active_usernames: list[str] = get_object(kwargs.get('active_usernames'))
        # List of currently disabled usernames; the username can be activated with toggleUsernameIsActive, toggleBotUsernameIsActive, or toggleSupergroupUsernameIsActive.
        self.disabled_usernames: list[str] = get_object(kwargs.get('disabled_usernames'))
        # The active username, which can be changed with setUsername or setSupergroupUsername.
        self.editable_username: str = get_object(kwargs.get('editable_username'))


class Supergroup(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Supergroup or channel identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Usernames of the supergroup or channel; may be null.
        self.usernames: Usernames = get_object(kwargs.get('usernames'))
        # Point in time (Unix timestamp) when the current user joined, or the point in time when the supergroup or channel was created, in case the user is not a member.
        self.date: int = get_object(kwargs.get('date'))
        # Status of the current user in the supergroup or channel; custom title will always be empty.
        self.status: ChatMemberStatus = get_object(kwargs.get('status'))
        # Number of members in the supergroup or channel; 0 if unknown. Currently, it is guaranteed to be known only if the supergroup or channel was received through searchPublicChats, searchChatsNearby, getInactiveSupergroupChats, getSuitableDiscussionChats, getGroupsInCommon, getUserPrivacySettingRules, or in chatFilterInviteLinkInfo.missing_chat_ids.
        self.member_count: int = get_object(kwargs.get('member_count'))
        # True, if the channel has a discussion group, or the supergroup is the designated discussion group for a channel.
        self.has_linked_chat: bool = get_object(kwargs.get('has_linked_chat'))
        # True, if the supergroup is connected to a location, i.e. the supergroup is a location-based supergroup.
        self.has_location: bool = get_object(kwargs.get('has_location'))
        # True, if messages sent to the channel need to contain information about the sender. This field is only applicable to channels.
        self.sign_messages: bool = get_object(kwargs.get('sign_messages'))
        # True, if users need to join the supergroup before they can send messages. Always true for channels and non-discussion supergroups.
        self.join_to_send_messages: bool = get_object(kwargs.get('join_to_send_messages'))
        # True, if all users directly joining the supergroup need to be approved by supergroup administrators. Always false for channels and supergroups without username, location, or a linked chat.
        self.join_by_request: bool = get_object(kwargs.get('join_by_request'))
        # True, if the slow mode is enabled in the supergroup.
        self.is_slow_mode_enabled: bool = get_object(kwargs.get('is_slow_mode_enabled'))
        # True, if the supergroup is a channel.
        self.is_channel: bool = get_object(kwargs.get('is_channel'))
        # True, if the supergroup is a broadcast group, i.e. only administrators can send messages and there is no limit on the number of members.
        self.is_broadcast_group: bool = get_object(kwargs.get('is_broadcast_group'))
        # True, if the supergroup must be shown as a forum by default.
        self.is_forum: bool = get_object(kwargs.get('is_forum'))
        # True, if the supergroup or channel is verified.
        self.is_verified: bool = get_object(kwargs.get('is_verified'))
        # If non-empty, contains a human-readable description of the reason why access to this supergroup or channel must be restricted.
        self.restriction_reason: str = get_object(kwargs.get('restriction_reason'))
        # True, if many users reported this supergroup or channel as a scam.
        self.is_scam: bool = get_object(kwargs.get('is_scam'))
        # True, if many users reported this supergroup or channel as a fake account.
        self.is_fake: bool = get_object(kwargs.get('is_fake'))


class SupergroupFullInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat photo; may be null if empty or unknown. If non-null, then it is the same photo as in chat.photo.
        self.photo: ChatPhoto = get_object(kwargs.get('photo'))
        # Supergroup or channel description.
        self.description: str = get_object(kwargs.get('description'))
        # Number of members in the supergroup or channel; 0 if unknown.
        self.member_count: int = get_object(kwargs.get('member_count'))
        # Number of privileged users in the supergroup or channel; 0 if unknown.
        self.administrator_count: int = get_object(kwargs.get('administrator_count'))
        # Number of restricted users in the supergroup; 0 if unknown.
        self.restricted_count: int = get_object(kwargs.get('restricted_count'))
        # Number of users banned from chat; 0 if unknown.
        self.banned_count: int = get_object(kwargs.get('banned_count'))
        # Chat identifier of a discussion group for the channel, or a channel, for which the supergroup is the designated discussion group; 0 if none or unknown.
        self.linked_chat_id: int = get_object(kwargs.get('linked_chat_id'))
        # Delay between consecutive sent messages for non-administrator supergroup members, in seconds.
        self.slow_mode_delay: int = get_object(kwargs.get('slow_mode_delay'))
        # Time left before next message can be sent in the supergroup, in seconds. An updateSupergroupFullInfo update is not triggered when value of this field changes, but both new and old values are non-zero.
        self.slow_mode_delay_expires_in: float = get_object(kwargs.get('slow_mode_delay_expires_in'))
        # True, if members of the chat can be retrieved via getSupergroupMembers or searchChatMembers.
        self.can_get_members: bool = get_object(kwargs.get('can_get_members'))
        # True, if non-administrators can receive only administrators and bots using getSupergroupMembers or searchChatMembers.
        self.has_hidden_members: bool = get_object(kwargs.get('has_hidden_members'))
        # True, if non-administrators and non-bots can be hidden in responses to getSupergroupMembers and searchChatMembers for non-administrators.
        self.can_hide_members: bool = get_object(kwargs.get('can_hide_members'))
        # True, if the supergroup sticker set can be changed.
        self.can_set_sticker_set: bool = get_object(kwargs.get('can_set_sticker_set'))
        # True, if the supergroup location can be changed.
        self.can_set_location: bool = get_object(kwargs.get('can_set_location'))
        # True, if the supergroup or channel statistics are available.
        self.can_get_statistics: bool = get_object(kwargs.get('can_get_statistics'))
        # True, if aggressive anti-spam checks can be enabled or disabled in the supergroup.
        self.can_toggle_aggressive_anti_spam: bool = get_object(kwargs.get('can_toggle_aggressive_anti_spam'))
        # True, if new chat members will have access to old messages. In public, discussion, of forum groups and all channels, old messages are always available, so this option affects only private non-forum supergroups without a linked chat. The value of this field is only available to chat administrators.
        self.is_all_history_available: bool = get_object(kwargs.get('is_all_history_available'))
        # True, if aggressive anti-spam checks are enabled in the supergroup. The value of this field is only available to chat administrators.
        self.has_aggressive_anti_spam_enabled: bool = get_object(kwargs.get('has_aggressive_anti_spam_enabled'))
        # Identifier of the supergroup sticker set; 0 if none.
        self.sticker_set_id: int = get_object(kwargs.get('sticker_set_id'))
        # Location to which the supergroup is connected; may be null if none.
        self.location: ChatLocation = get_object(kwargs.get('location'))
        # Primary invite link for the chat; may be null. For chat administrators with can_invite_users right only.
        self.invite_link: ChatInviteLink = get_object(kwargs.get('invite_link'))
        # List of commands of bots in the group.
        self.bot_commands: list[BotCommands] = get_object(kwargs.get('bot_commands'))
        # Identifier of the basic group from which supergroup was upgraded; 0 if none.
        self.upgraded_from_basic_group_id: int = get_object(kwargs.get('upgraded_from_basic_group_id'))
        # Identifier of the last message in the basic group from which supergroup was upgraded; 0 if none.
        self.upgraded_from_max_message_id: int = get_object(kwargs.get('upgraded_from_max_message_id'))


class SupergroupMembersFilter(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SupergroupMembersFilterRecent(SupergroupMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SupergroupMembersFilterContacts(SupergroupMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Query to search for.
        self.query: str = get_object(kwargs.get('query'))


class SupergroupMembersFilterAdministrators(SupergroupMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class SupergroupMembersFilterSearch(SupergroupMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Query to search for.
        self.query: str = get_object(kwargs.get('query'))


class SupergroupMembersFilterRestricted(SupergroupMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Query to search for.
        self.query: str = get_object(kwargs.get('query'))


class SupergroupMembersFilterBanned(SupergroupMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Query to search for.
        self.query: str = get_object(kwargs.get('query'))


class SupergroupMembersFilterMention(SupergroupMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Query to search for.
        self.query: str = get_object(kwargs.get('query'))
        # If non-zero, the identifier of the current message thread.
        self.message_thread_id: int = get_object(kwargs.get('message_thread_id'))


class SupergroupMembersFilterBots(SupergroupMembersFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TMeUrlType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TMeUrl(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # URL.
        self.url: str = get_object(kwargs.get('url'))
        # Type of the URL.
        self.type: TMeUrlType = get_object(kwargs.get('type'))


class TMeUrlTypeUser(TMeUrlType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the user.
        self.user_id: int = get_object(kwargs.get('user_id'))


class TMeUrlTypeSupergroup(TMeUrlType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the supergroup or channel.
        self.supergroup_id: int = get_object(kwargs.get('supergroup_id'))


class TMeUrlTypeChatInvite(TMeUrlType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information about the chat invite link.
        self.info: ChatInviteLinkInfo = get_object(kwargs.get('info'))


class TMeUrlTypeStickerSet(TMeUrlType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the sticker set.
        self.sticker_set_id: int = get_object(kwargs.get('sticker_set_id'))


class TMeUrls(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of URLs.
        self.urls: list[TMeUrl] = get_object(kwargs.get('urls'))


class TargetChatCurrent(TargetChat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TargetChatChosen(TargetChat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if private chats with ordinary users are allowed.
        self.allow_user_chats: bool = get_object(kwargs.get('allow_user_chats'))
        # True, if private chats with other bots are allowed.
        self.allow_bot_chats: bool = get_object(kwargs.get('allow_bot_chats'))
        # True, if basic group and supergroup chats are allowed.
        self.allow_group_chats: bool = get_object(kwargs.get('allow_group_chats'))
        # True, if channel chats are allowed.
        self.allow_channel_chats: bool = get_object(kwargs.get('allow_channel_chats'))


class TargetChatInternalLink(TargetChat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # An internal link pointing to the chat.
        self.link: InternalLinkType = get_object(kwargs.get('link'))


class TemporaryPasswordState(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if a temporary password is available.
        self.has_password: bool = get_object(kwargs.get('has_password'))
        # Time left before the temporary password expires, in seconds.
        self.valid_for: int = get_object(kwargs.get('valid_for'))


class TestBytes(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Bytes.
        self.value: bytes = get_object(kwargs.get('value'))


class TestInt(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Number.
        self.value: int = get_object(kwargs.get('value'))


class TestString(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # String.
        self.value: str = get_object(kwargs.get('value'))


class TestVectorInt(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Vector of numbers.
        self.value: list[int] = get_object(kwargs.get('value'))


class TestVectorIntObject(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Vector of objects.
        self.value: list[TestInt] = get_object(kwargs.get('value'))


class TestVectorString(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Vector of strings.
        self.value: list[str] = get_object(kwargs.get('value'))


class TestVectorStringObject(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Vector of objects.
        self.value: list[TestString] = get_object(kwargs.get('value'))


class Text(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Text.
        self.text: str = get_object(kwargs.get('text'))


class TextEntities(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of text entities.
        self.entities: list[TextEntity] = get_object(kwargs.get('entities'))


class TextEntityType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeMention(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeHashtag(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeCashtag(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeBotCommand(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeUrl(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeEmailAddress(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypePhoneNumber(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeBankCardNumber(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeBold(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeItalic(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeUnderline(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeStrikethrough(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeSpoiler(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypeCode(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypePre(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextEntityTypePreCode(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Programming language of the code; as defined by the sender.
        self.language: str = get_object(kwargs.get('language'))


class TextEntityTypeTextUrl(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # HTTP or tg:// URL to be opened when the link is clicked.
        self.url: str = get_object(kwargs.get('url'))


class TextEntityTypeMentionName(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the mentioned user.
        self.user_id: int = get_object(kwargs.get('user_id'))


class TextEntityTypeCustomEmoji(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier of the custom emoji.
        self.custom_emoji_id: int = get_object(kwargs.get('custom_emoji_id'))


class TextEntityTypeMediaTimestamp(TextEntityType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Timestamp from which a video/audio/video note/voice note playing must start, in seconds. The media can be in the content or the web page preview of the current message, or in the same places in the replied message.
        self.media_timestamp: int = get_object(kwargs.get('media_timestamp'))


class TextParseMode(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TextParseModeMarkdown(TextParseMode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Version of the parser: 0 or 1 - Telegram Bot API &quot;Markdown&quot; parse mode, 2 - Telegram Bot API &quot;MarkdownV2&quot; parse mode.
        self.version: int = get_object(kwargs.get('version'))


class TextParseModeHTML(TextParseMode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ThemeParameters(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A color of the background in the RGB24 format.
        self.background_color: int = get_object(kwargs.get('background_color'))
        # A secondary color for the background in the RGB24 format.
        self.secondary_background_color: int = get_object(kwargs.get('secondary_background_color'))
        # A color of text in the RGB24 format.
        self.text_color: int = get_object(kwargs.get('text_color'))
        # A color of hints in the RGB24 format.
        self.hint_color: int = get_object(kwargs.get('hint_color'))
        # A color of links in the RGB24 format.
        self.link_color: int = get_object(kwargs.get('link_color'))
        # A color of the buttons in the RGB24 format.
        self.button_color: int = get_object(kwargs.get('button_color'))
        # A color of text on the buttons in the RGB24 format.
        self.button_text_color: int = get_object(kwargs.get('button_text_color'))


class ThumbnailFormat(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ThumbnailFormatJpeg(ThumbnailFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ThumbnailFormatGif(ThumbnailFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ThumbnailFormatMpeg4(ThumbnailFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ThumbnailFormatPng(ThumbnailFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ThumbnailFormatTgs(ThumbnailFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ThumbnailFormatWebm(ThumbnailFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class ThumbnailFormatWebp(ThumbnailFormat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TopChatCategory(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TopChatCategoryUsers(TopChatCategory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TopChatCategoryBots(TopChatCategory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TopChatCategoryGroups(TopChatCategory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TopChatCategoryChannels(TopChatCategory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TopChatCategoryInlineBots(TopChatCategory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TopChatCategoryCalls(TopChatCategory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TopChatCategoryForwardChats(TopChatCategory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class TrendingStickerSets(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of trending sticker sets.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of trending sticker sets.
        self.sets: list[StickerSetInfo] = get_object(kwargs.get('sets'))
        # True, if the list contains sticker sets with premium stickers.
        self.is_premium: bool = get_object(kwargs.get('is_premium'))


class UnconfirmedSession(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Session identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Point in time (Unix timestamp) when the user has logged in.
        self.log_in_date: int = get_object(kwargs.get('log_in_date'))
        # Model of the device that was used for the session creation, as provided by the application.
        self.device_model: str = get_object(kwargs.get('device_model'))
        # A human-readable description of the location from which the session was created, based on the IP address.
        self.location: str = get_object(kwargs.get('location'))


class UserPrivacySetting(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserStatus(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class User(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.id: int = get_object(kwargs.get('id'))
        # First name of the user.
        self.first_name: str = get_object(kwargs.get('first_name'))
        # Last name of the user.
        self.last_name: str = get_object(kwargs.get('last_name'))
        # Usernames of the user; may be null.
        self.usernames: Usernames = get_object(kwargs.get('usernames'))
        # Phone number of the user.
        self.phone_number: str = get_object(kwargs.get('phone_number'))
        # Current online status of the user.
        self.status: UserStatus = get_object(kwargs.get('status'))
        # Profile photo of the user; may be null.
        self.profile_photo: ProfilePhoto = get_object(kwargs.get('profile_photo'))
        # Emoji status to be shown instead of the default Telegram Premium badge; may be null. For Telegram Premium users only.
        self.emoji_status: EmojiStatus = get_object(kwargs.get('emoji_status'))
        # The user is a contact of the current user.
        self.is_contact: bool = get_object(kwargs.get('is_contact'))
        # The user is a contact of the current user and the current user is a contact of the user.
        self.is_mutual_contact: bool = get_object(kwargs.get('is_mutual_contact'))
        # The user is a close friend of the current user; implies that the user is a contact.
        self.is_close_friend: bool = get_object(kwargs.get('is_close_friend'))
        # True, if the user is verified.
        self.is_verified: bool = get_object(kwargs.get('is_verified'))
        # True, if the user is a Telegram Premium user.
        self.is_premium: bool = get_object(kwargs.get('is_premium'))
        # True, if the user is Telegram support account.
        self.is_support: bool = get_object(kwargs.get('is_support'))
        # If non-empty, it contains a human-readable description of the reason why access to this user must be restricted.
        self.restriction_reason: str = get_object(kwargs.get('restriction_reason'))
        # True, if many users reported this user as a scam.
        self.is_scam: bool = get_object(kwargs.get('is_scam'))
        # True, if many users reported this user as a fake account.
        self.is_fake: bool = get_object(kwargs.get('is_fake'))
        # True, if the user has non-expired stories available to the current user.
        self.has_active_stories: bool = get_object(kwargs.get('has_active_stories'))
        # True, if the user has unread non-expired stories available to the current user.
        self.has_unread_active_stories: bool = get_object(kwargs.get('has_unread_active_stories'))
        # If false, the user is inaccessible, and the only information known about the user is inside this class. Identifier of the user can't be passed to any method.
        self.have_access: bool = get_object(kwargs.get('have_access'))
        # Type of the user.
        self.type: UserType = get_object(kwargs.get('type'))
        # IETF language tag of the user's language; only available to bots.
        self.language_code: str = get_object(kwargs.get('language_code'))
        # True, if the user added the current bot to attachment menu; only available to bots.
        self.added_to_attachment_menu: bool = get_object(kwargs.get('added_to_attachment_menu'))


class UserFullInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User profile photo set by the current user for the contact; may be null. If null and user.profile_photo is null, then the photo is empty; otherwise, it is unknown. If non-null, then it is the same photo as in user.profile_photo and chat.photo. This photo isn't returned in the list of user photos.
        self.personal_photo: ChatPhoto = get_object(kwargs.get('personal_photo'))
        # User profile photo; may be null. If null and user.profile_photo is null, then the photo is empty; otherwise, it is unknown. If non-null and personal_photo is null, then it is the same photo as in user.profile_photo and chat.photo.
        self.photo: ChatPhoto = get_object(kwargs.get('photo'))
        # User profile photo visible if the main photo is hidden by privacy settings; may be null. If null and user.profile_photo is null, then the photo is empty; otherwise, it is unknown. If non-null and both photo and personal_photo are null, then it is the same photo as in user.profile_photo and chat.photo. This photo isn't returned in the list of user photos.
        self.public_photo: ChatPhoto = get_object(kwargs.get('public_photo'))
        # Block list to which the user is added; may be null if none.
        self.block_list: BlockList = get_object(kwargs.get('block_list'))
        # True, if the user can be called.
        self.can_be_called: bool = get_object(kwargs.get('can_be_called'))
        # True, if a video call can be created with the user.
        self.supports_video_calls: bool = get_object(kwargs.get('supports_video_calls'))
        # True, if the user can't be called due to their privacy settings.
        self.has_private_calls: bool = get_object(kwargs.get('has_private_calls'))
        # True, if the user can't be linked in forwarded messages due to their privacy settings.
        self.has_private_forwards: bool = get_object(kwargs.get('has_private_forwards'))
        # True, if voice and video notes can't be sent or forwarded to the user.
        self.has_restricted_voice_and_video_note_messages: bool = get_object(kwargs.get('has_restricted_voice_and_video_note_messages'))
        # True, if the user has pinned stories.
        self.has_pinned_stories: bool = get_object(kwargs.get('has_pinned_stories'))
        # True, if the current user needs to explicitly allow to share their phone number with the user when the method addContact is used.
        self.need_phone_number_privacy_exception: bool = get_object(kwargs.get('need_phone_number_privacy_exception'))
        # A short user bio; may be null for bots.
        self.bio: FormattedText = get_object(kwargs.get('bio'))
        # The list of available options for gifting Telegram Premium to the user.
        self.premium_gift_options: list[PremiumPaymentOption] = get_object(kwargs.get('premium_gift_options'))
        # Number of group chats where both the other user and the current user are a member; 0 for the current user.
        self.group_in_common_count: int = get_object(kwargs.get('group_in_common_count'))
        # For bots, information about the bot; may be null if the user isn't a bot.
        self.bot_info: BotInfo = get_object(kwargs.get('bot_info'))


class UserPrivacySettingRules(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A list of rules.
        self.rules: list[UserPrivacySettingRule] = get_object(kwargs.get('rules'))


class Update(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UpdateAuthorizationState(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New authorization state.
        self.authorization_state: AuthorizationState = get_object(kwargs.get('authorization_state'))


class UpdateNewMessage(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new message.
        self.message: Message = get_object(kwargs.get('message'))


class UpdateMessageSendAcknowledged(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat identifier of the sent message.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # A temporary message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))


class UpdateMessageSendSucceeded(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The sent message. Usually only the message identifier, date, and content are changed, but almost all other fields can also change.
        self.message: Message = get_object(kwargs.get('message'))
        # The previous temporary message identifier.
        self.old_message_id: int = get_object(kwargs.get('old_message_id'))


class UpdateMessageSendFailed(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The failed to send message.
        self.message: Message = get_object(kwargs.get('message'))
        # The previous temporary message identifier.
        self.old_message_id: int = get_object(kwargs.get('old_message_id'))
        # An error code.
        self.error_code: int = get_object(kwargs.get('error_code'))
        # Error message.
        self.error_message: str = get_object(kwargs.get('error_message'))


class UpdateMessageContent(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # New message content.
        self.new_content: MessageContent = get_object(kwargs.get('new_content'))


class UpdateMessageEdited(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # Point in time (Unix timestamp) when the message was edited.
        self.edit_date: int = get_object(kwargs.get('edit_date'))
        # New message reply markup; may be null.
        self.reply_markup: ReplyMarkup = get_object(kwargs.get('reply_markup'))


class UpdateMessageIsPinned(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # True, if the message is pinned.
        self.is_pinned: bool = get_object(kwargs.get('is_pinned'))


class UpdateMessageInteractionInfo(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # New information about interactions with the message; may be null.
        self.interaction_info: MessageInteractionInfo = get_object(kwargs.get('interaction_info'))


class UpdateMessageContentOpened(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))


class UpdateMessageMentionRead(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # The new number of unread mention messages left in the chat.
        self.unread_mention_count: int = get_object(kwargs.get('unread_mention_count'))


class UpdateMessageUnreadReactions(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # The new list of unread reactions.
        self.unread_reactions: list[UnreadReaction] = get_object(kwargs.get('unread_reactions'))
        # The new number of messages with unread reactions left in the chat.
        self.unread_reaction_count: int = get_object(kwargs.get('unread_reaction_count'))


class UpdateMessageLiveLocationViewed(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat with the live location message.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifier of the message with live location.
        self.message_id: int = get_object(kwargs.get('message_id'))


class UpdateNewChat(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat.
        self.chat: Chat = get_object(kwargs.get('chat'))


class UpdateChatTitle(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new chat title.
        self.title: str = get_object(kwargs.get('title'))


class UpdateChatPhoto(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new chat photo; may be null.
        self.photo: ChatPhotoInfo = get_object(kwargs.get('photo'))


class UpdateChatPermissions(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new chat permissions.
        self.permissions: ChatPermissions = get_object(kwargs.get('permissions'))


class UpdateChatLastMessage(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new last message in the chat; may be null.
        self.last_message: Message = get_object(kwargs.get('last_message'))
        # The new chat positions in the chat lists.
        self.positions: list[ChatPosition] = get_object(kwargs.get('positions'))


class UpdateChatPosition(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New chat position. If new order is 0, then the chat needs to be removed from the list.
        self.position: ChatPosition = get_object(kwargs.get('position'))


class UpdateChatReadInbox(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifier of the last read incoming message.
        self.last_read_inbox_message_id: int = get_object(kwargs.get('last_read_inbox_message_id'))
        # The number of unread messages left in the chat.
        self.unread_count: int = get_object(kwargs.get('unread_count'))


class UpdateChatReadOutbox(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifier of last read outgoing message.
        self.last_read_outbox_message_id: int = get_object(kwargs.get('last_read_outbox_message_id'))


class UpdateChatActionBar(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new value of the action bar; may be null.
        self.action_bar: ChatActionBar = get_object(kwargs.get('action_bar'))


class UpdateChatAvailableReactions(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new reactions, available in the chat.
        self.available_reactions: ChatAvailableReactions = get_object(kwargs.get('available_reactions'))


class UpdateChatDraftMessage(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new draft message; may be null.
        self.draft_message: DraftMessage = get_object(kwargs.get('draft_message'))
        # The new chat positions in the chat lists.
        self.positions: list[ChatPosition] = get_object(kwargs.get('positions'))


class UpdateChatMessageSender(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New value of message_sender_id; may be null if the user can't change message sender.
        self.message_sender_id: MessageSender = get_object(kwargs.get('message_sender_id'))


class UpdateChatMessageAutoDeleteTime(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New value of message_auto_delete_time.
        self.message_auto_delete_time: int = get_object(kwargs.get('message_auto_delete_time'))


class UpdateChatNotificationSettings(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new notification settings.
        self.notification_settings: ChatNotificationSettings = get_object(kwargs.get('notification_settings'))


class UpdateChatPendingJoinRequests(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new data about pending join requests; may be null.
        self.pending_join_requests: ChatJoinRequestsInfo = get_object(kwargs.get('pending_join_requests'))


class UpdateChatReplyMarkup(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifier of the message from which reply markup needs to be used; 0 if there is no default custom reply markup in the chat.
        self.reply_markup_message_id: int = get_object(kwargs.get('reply_markup_message_id'))


class UpdateChatBackground(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new chat background; may be null if background was reset to default.
        self.background: ChatBackground = get_object(kwargs.get('background'))


class UpdateChatTheme(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new name of the chat theme; may be empty if theme was reset to default.
        self.theme_name: str = get_object(kwargs.get('theme_name'))


class UpdateChatUnreadMentionCount(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The number of unread mention messages left in the chat.
        self.unread_mention_count: int = get_object(kwargs.get('unread_mention_count'))


class UpdateChatUnreadReactionCount(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The number of messages with unread reactions left in the chat.
        self.unread_reaction_count: int = get_object(kwargs.get('unread_reaction_count'))


class UpdateChatVideoChat(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New value of video_chat.
        self.video_chat: VideoChat = get_object(kwargs.get('video_chat'))


class UpdateChatDefaultDisableNotification(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # The new default_disable_notification value.
        self.default_disable_notification: bool = get_object(kwargs.get('default_disable_notification'))


class UpdateChatHasProtectedContent(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New value of has_protected_content.
        self.has_protected_content: bool = get_object(kwargs.get('has_protected_content'))


class UpdateChatIsTranslatable(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New value of is_translatable.
        self.is_translatable: bool = get_object(kwargs.get('is_translatable'))


class UpdateChatIsMarkedAsUnread(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New value of is_marked_as_unread.
        self.is_marked_as_unread: bool = get_object(kwargs.get('is_marked_as_unread'))


class UpdateChatBlockList(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Block list to which the chat is added; may be null if none.
        self.block_list: BlockList = get_object(kwargs.get('block_list'))


class UpdateChatHasScheduledMessages(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New value of has_scheduled_messages.
        self.has_scheduled_messages: bool = get_object(kwargs.get('has_scheduled_messages'))


class UpdateChatFilters(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of chat filters.
        self.chat_filters: list[ChatFilterInfo] = get_object(kwargs.get('chat_filters'))
        # Position of the main chat list among chat filters, 0-based.
        self.main_chat_list_position: int = get_object(kwargs.get('main_chat_list_position'))


class UpdateChatOnlineMemberCount(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New number of online members in the chat, or 0 if unknown.
        self.online_member_count: int = get_object(kwargs.get('online_member_count'))


class UpdateForumTopicInfo(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # New information about the topic.
        self.info: ForumTopicInfo = get_object(kwargs.get('info'))


class UpdateScopeNotificationSettings(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Types of chats for which notification settings were updated.
        self.scope: NotificationSettingsScope = get_object(kwargs.get('scope'))
        # The new notification settings.
        self.notification_settings: ScopeNotificationSettings = get_object(kwargs.get('notification_settings'))


class UpdateNotification(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique notification group identifier.
        self.notification_group_id: int = get_object(kwargs.get('notification_group_id'))
        # Changed notification.
        self.notification: Notification = get_object(kwargs.get('notification'))


class UpdateNotificationGroup(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique notification group identifier.
        self.notification_group_id: int = get_object(kwargs.get('notification_group_id'))
        # New type of the notification group.
        self.type: NotificationGroupType = get_object(kwargs.get('type'))
        # Identifier of a chat to which all notifications in the group belong.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Chat identifier, which notification settings must be applied to the added notifications.
        self.notification_settings_chat_id: int = get_object(kwargs.get('notification_settings_chat_id'))
        # Identifier of the notification sound to be played; 0 if sound is disabled.
        self.notification_sound_id: int = get_object(kwargs.get('notification_sound_id'))
        # Total number of unread notifications in the group, can be bigger than number of active notifications.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # List of added group notifications, sorted by notification identifier.
        self.added_notifications: list[Notification] = get_object(kwargs.get('added_notifications'))
        # Identifiers of removed group notifications, sorted by notification identifier.
        self.removed_notification_ids: list[int] = get_object(kwargs.get('removed_notification_ids'))


class UpdateActiveNotifications(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Lists of active notification groups.
        self.groups: list[NotificationGroup] = get_object(kwargs.get('groups'))


class UpdateHavePendingNotifications(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if there are some delayed notification updates, which will be sent soon.
        self.have_delayed_notifications: bool = get_object(kwargs.get('have_delayed_notifications'))
        # True, if there can be some yet unreceived notifications, which are being fetched from the server.
        self.have_unreceived_notifications: bool = get_object(kwargs.get('have_unreceived_notifications'))


class UpdateDeleteMessages(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifiers of the deleted messages.
        self.message_ids: list[int] = get_object(kwargs.get('message_ids'))
        # True, if the messages are permanently deleted by a user (as opposed to just becoming inaccessible).
        self.is_permanent: bool = get_object(kwargs.get('is_permanent'))
        # True, if the messages are deleted only from the cache and can possibly be retrieved again in the future.
        self.from_cache: bool = get_object(kwargs.get('from_cache'))


class UpdateChatAction(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # If not 0, a message thread identifier in which the action was performed.
        self.message_thread_id: int = get_object(kwargs.get('message_thread_id'))
        # Identifier of a message sender performing the action.
        self.sender_id: MessageSender = get_object(kwargs.get('sender_id'))
        # The action.
        self.action: ChatAction = get_object(kwargs.get('action'))


class UpdateUserStatus(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # New status of the user.
        self.status: UserStatus = get_object(kwargs.get('status'))


class UpdateUser(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New data about the user.
        self.user: User = get_object(kwargs.get('user'))


class UpdateBasicGroup(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New data about the group.
        self.basic_group: BasicGroup = get_object(kwargs.get('basic_group'))


class UpdateSupergroup(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New data about the supergroup.
        self.supergroup: Supergroup = get_object(kwargs.get('supergroup'))


class UpdateSecretChat(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New data about the secret chat.
        self.secret_chat: SecretChat = get_object(kwargs.get('secret_chat'))


class UpdateUserFullInfo(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # User identifier.
        self.user_id: int = get_object(kwargs.get('user_id'))
        # New full information about the user.
        self.user_full_info: UserFullInfo = get_object(kwargs.get('user_full_info'))


class UpdateBasicGroupFullInfo(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of a basic group.
        self.basic_group_id: int = get_object(kwargs.get('basic_group_id'))
        # New full information about the group.
        self.basic_group_full_info: BasicGroupFullInfo = get_object(kwargs.get('basic_group_full_info'))


class UpdateSupergroupFullInfo(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the supergroup or channel.
        self.supergroup_id: int = get_object(kwargs.get('supergroup_id'))
        # New full information about the supergroup.
        self.supergroup_full_info: SupergroupFullInfo = get_object(kwargs.get('supergroup_full_info'))


class UpdateServiceNotification(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Notification type. If type begins with &quot;AUTH_KEY_DROP_&quot;, then two buttons &quot;Cancel&quot; and &quot;Log out&quot; must be shown under notification; if user presses the second, all local data must be destroyed using Destroy method.
        self.type: str = get_object(kwargs.get('type'))
        # Notification content.
        self.content: MessageContent = get_object(kwargs.get('content'))


class UpdateFile(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New data about the file.
        self.file: File = get_object(kwargs.get('file'))


class UpdateFileGenerationStart(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier for the generation process.
        self.generation_id: int = get_object(kwargs.get('generation_id'))
        # The path to a file from which a new file is generated; may be empty.
        self.original_path: str = get_object(kwargs.get('original_path'))
        # The path to a file that must be created and where the new file is generated.
        self.destination_path: str = get_object(kwargs.get('destination_path'))
        # String specifying the conversion applied to the original file. If conversion is &quot;\#url\#&quot; than original_path contains an HTTP/HTTPS URL of a file, which must be downloaded by the application.
        self.conversion: str = get_object(kwargs.get('conversion'))


class UpdateFileGenerationStop(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier for the generation process.
        self.generation_id: int = get_object(kwargs.get('generation_id'))


class UpdateFileDownloads(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Total size of files in the file download list, in bytes.
        self.total_size: int = get_object(kwargs.get('total_size'))
        # Total number of files in the file download list.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # Total downloaded size of files in the file download list, in bytes.
        self.downloaded_size: int = get_object(kwargs.get('downloaded_size'))


class UpdateFileAddedToDownloads(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The added file download.
        self.file_download: FileDownload = get_object(kwargs.get('file_download'))
        # New number of being downloaded and recently downloaded files found.
        self.counts: DownloadedFileCounts = get_object(kwargs.get('counts'))


class UpdateFileDownload(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # File identifier.
        self.file_id: int = get_object(kwargs.get('file_id'))
        # Point in time (Unix timestamp) when the file downloading was completed; 0 if the file downloading isn't completed.
        self.complete_date: int = get_object(kwargs.get('complete_date'))
        # True, if downloading of the file is paused.
        self.is_paused: bool = get_object(kwargs.get('is_paused'))
        # New number of being downloaded and recently downloaded files found.
        self.counts: DownloadedFileCounts = get_object(kwargs.get('counts'))


class UpdateFileRemovedFromDownloads(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # File identifier.
        self.file_id: int = get_object(kwargs.get('file_id'))
        # New number of being downloaded and recently downloaded files found.
        self.counts: DownloadedFileCounts = get_object(kwargs.get('counts'))


class UpdateCall(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New data about a call.
        self.call: Call = get_object(kwargs.get('call'))


class UpdateGroupCall(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New data about a group call.
        self.group_call: GroupCall = get_object(kwargs.get('group_call'))


class UpdateGroupCallParticipant(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of group call.
        self.group_call_id: int = get_object(kwargs.get('group_call_id'))
        # New data about a participant.
        self.participant: GroupCallParticipant = get_object(kwargs.get('participant'))


class UpdateNewCallSignalingData(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The call identifier.
        self.call_id: int = get_object(kwargs.get('call_id'))
        # The data.
        self.data: bytes = get_object(kwargs.get('data'))


class UpdateUserPrivacySettingRules(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The privacy setting.
        self.setting: UserPrivacySetting = get_object(kwargs.get('setting'))
        # New privacy rules.
        self.rules: UserPrivacySettingRules = get_object(kwargs.get('rules'))


class UpdateUnreadMessageCount(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat list with changed number of unread messages.
        self.chat_list: ChatList = get_object(kwargs.get('chat_list'))
        # Total number of unread messages.
        self.unread_count: int = get_object(kwargs.get('unread_count'))
        # Total number of unread messages in unmuted chats.
        self.unread_unmuted_count: int = get_object(kwargs.get('unread_unmuted_count'))


class UpdateUnreadChatCount(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat list with changed number of unread messages.
        self.chat_list: ChatList = get_object(kwargs.get('chat_list'))
        # Approximate total number of chats in the chat list.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # Total number of unread chats.
        self.unread_count: int = get_object(kwargs.get('unread_count'))
        # Total number of unread unmuted chats.
        self.unread_unmuted_count: int = get_object(kwargs.get('unread_unmuted_count'))
        # Total number of chats marked as unread.
        self.marked_as_unread_count: int = get_object(kwargs.get('marked_as_unread_count'))
        # Total number of unmuted chats marked as unread.
        self.marked_as_unread_unmuted_count: int = get_object(kwargs.get('marked_as_unread_unmuted_count'))


class UpdateStory(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new information about the story.
        self.story: Story = get_object(kwargs.get('story'))


class UpdateStoryDeleted(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the chat that posted the story.
        self.story_sender_chat_id: int = get_object(kwargs.get('story_sender_chat_id'))
        # Story identifier.
        self.story_id: int = get_object(kwargs.get('story_id'))


class UpdateStorySendSucceeded(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The sent story.
        self.story: Story = get_object(kwargs.get('story'))
        # The previous temporary story identifier.
        self.old_story_id: int = get_object(kwargs.get('old_story_id'))


class UpdateStorySendFailed(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The failed to send story.
        self.story: Story = get_object(kwargs.get('story'))
        # The cause of the failure; may be null if unknown.
        self.error: CanSendStoryResult = get_object(kwargs.get('error'))
        # An error code.
        self.error_code: int = get_object(kwargs.get('error_code'))
        # Error message.
        self.error_message: str = get_object(kwargs.get('error_message'))


class UpdateChatActiveStories(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of active stories.
        self.active_stories: ChatActiveStories = get_object(kwargs.get('active_stories'))


class UpdateStoryListChatCount(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The story list.
        self.story_list: StoryList = get_object(kwargs.get('story_list'))
        # Approximate total number of chats with active stories in the list.
        self.chat_count: int = get_object(kwargs.get('chat_count'))


class UpdateStoryStealthMode(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) until stealth mode is active; 0 if it is disabled.
        self.active_until_date: int = get_object(kwargs.get('active_until_date'))
        # Point in time (Unix timestamp) when stealth mode can be enabled again; 0 if there is no active cooldown.
        self.cooldown_until_date: int = get_object(kwargs.get('cooldown_until_date'))


class UpdateOption(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The option name.
        self.name: str = get_object(kwargs.get('name'))
        # The new option value.
        self.value: OptionValue = get_object(kwargs.get('value'))


class UpdateStickerSet(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The sticker set.
        self.sticker_set: StickerSet = get_object(kwargs.get('sticker_set'))


class UpdateInstalledStickerSets(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the affected stickers.
        self.sticker_type: StickerType = get_object(kwargs.get('sticker_type'))
        # The new list of installed ordinary sticker sets.
        self.sticker_set_ids: list[int] = get_object(kwargs.get('sticker_set_ids'))


class UpdateTrendingStickerSets(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of the affected stickers.
        self.sticker_type: StickerType = get_object(kwargs.get('sticker_type'))
        # The prefix of the list of trending sticker sets with the newest trending sticker sets.
        self.sticker_sets: TrendingStickerSets = get_object(kwargs.get('sticker_sets'))


class UpdateRecentStickers(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the list of stickers attached to photo or video files was updated; otherwise, the list of sent stickers is updated.
        self.is_attached: bool = get_object(kwargs.get('is_attached'))
        # The new list of file identifiers of recently used stickers.
        self.sticker_ids: list[int] = get_object(kwargs.get('sticker_ids'))


class UpdateFavoriteStickers(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of file identifiers of favorite stickers.
        self.sticker_ids: list[int] = get_object(kwargs.get('sticker_ids'))


class UpdateSavedAnimations(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of file identifiers of saved animations.
        self.animation_ids: list[int] = get_object(kwargs.get('animation_ids'))


class UpdateSavedNotificationSounds(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of identifiers of saved notification sounds.
        self.notification_sound_ids: list[int] = get_object(kwargs.get('notification_sound_ids'))


class UpdateSelectedBackground(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if background for dark theme has changed.
        self.for_dark_theme: bool = get_object(kwargs.get('for_dark_theme'))
        # The new selected background; may be null.
        self.background: Background = get_object(kwargs.get('background'))


class UpdateChatThemes(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of chat themes.
        self.chat_themes: list[ChatTheme] = get_object(kwargs.get('chat_themes'))


class UpdateLanguagePackStrings(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Localization target to which the language pack belongs.
        self.localization_target: str = get_object(kwargs.get('localization_target'))
        # Identifier of the updated language pack.
        self.language_pack_id: str = get_object(kwargs.get('language_pack_id'))
        # List of changed language pack strings; empty if all strings have changed.
        self.strings: list[LanguagePackString] = get_object(kwargs.get('strings'))


class UpdateConnectionState(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new connection state.
        self.state: ConnectionState = get_object(kwargs.get('state'))


class UpdateTermsOfService(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the terms of service.
        self.terms_of_service_id: str = get_object(kwargs.get('terms_of_service_id'))
        # The new terms of service.
        self.terms_of_service: TermsOfService = get_object(kwargs.get('terms_of_service'))


class UpdateUsersNearby(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of users nearby.
        self.users_nearby: list[ChatNearby] = get_object(kwargs.get('users_nearby'))


class UpdateUnconfirmedSession(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The unconfirmed session; may be null if none.
        self.session: UnconfirmedSession = get_object(kwargs.get('session'))


class UpdateAttachmentMenuBots(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of bots. The bots must not be shown on scheduled messages screen.
        self.bots: list[AttachmentMenuBot] = get_object(kwargs.get('bots'))


class UpdateWebAppMessageSent(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of Web App launch.
        self.web_app_launch_id: int = get_object(kwargs.get('web_app_launch_id'))


class UpdateActiveEmojiReactions(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of active emoji reactions.
        self.emojis: list[str] = get_object(kwargs.get('emojis'))


class UpdateDefaultReactionType(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new type of the default reaction.
        self.reaction_type: ReactionType = get_object(kwargs.get('reaction_type'))


class UpdateDiceEmojis(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The new list of supported dice emojis.
        self.emojis: list[str] = get_object(kwargs.get('emojis'))


class UpdateAnimatedEmojiMessageClicked(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Message identifier.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # The animated sticker to be played.
        self.sticker: Sticker = get_object(kwargs.get('sticker'))


class UpdateAnimationSearchParameters(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Name of the animation search provider.
        self.provider: str = get_object(kwargs.get('provider'))
        # The new list of emojis suggested for searching.
        self.emojis: list[str] = get_object(kwargs.get('emojis'))


class UpdateSuggestedActions(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Added suggested actions.
        self.added_actions: list[SuggestedAction] = get_object(kwargs.get('added_actions'))
        # Removed suggested actions.
        self.removed_actions: list[SuggestedAction] = get_object(kwargs.get('removed_actions'))


class UpdateAddChatMembersPrivacyForbidden(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifiers of users, which weren't added because of their privacy settings.
        self.user_ids: list[int] = get_object(kwargs.get('user_ids'))


class UpdateAutosaveSettings(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Type of chats for which autosave settings were updated.
        self.scope: AutosaveSettingsScope = get_object(kwargs.get('scope'))
        # The new autosave settings; may be null if the settings are reset to default.
        self.settings: ScopeAutosaveSettings = get_object(kwargs.get('settings'))


class UpdateNewInlineQuery(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique query identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the user who sent the query.
        self.sender_user_id: int = get_object(kwargs.get('sender_user_id'))
        # User location; may be null.
        self.user_location: Location = get_object(kwargs.get('user_location'))
        # The type of the chat from which the query originated; may be null if unknown.
        self.chat_type: ChatType = get_object(kwargs.get('chat_type'))
        # Text of the query.
        self.query: str = get_object(kwargs.get('query'))
        # Offset of the first entry to return.
        self.offset: str = get_object(kwargs.get('offset'))


class UpdateNewChosenInlineResult(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Identifier of the user who sent the query.
        self.sender_user_id: int = get_object(kwargs.get('sender_user_id'))
        # User location; may be null.
        self.user_location: Location = get_object(kwargs.get('user_location'))
        # Text of the query.
        self.query: str = get_object(kwargs.get('query'))
        # Identifier of the chosen result.
        self.result_id: str = get_object(kwargs.get('result_id'))
        # Identifier of the sent inline message, if known.
        self.inline_message_id: str = get_object(kwargs.get('inline_message_id'))


class UpdateNewCallbackQuery(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique query identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the user who sent the query.
        self.sender_user_id: int = get_object(kwargs.get('sender_user_id'))
        # Identifier of the chat where the query was sent.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifier of the message from which the query originated.
        self.message_id: int = get_object(kwargs.get('message_id'))
        # Identifier that uniquely corresponds to the chat to which the message was sent.
        self.chat_instance: int = get_object(kwargs.get('chat_instance'))
        # Query payload.
        self.payload: CallbackQueryPayload = get_object(kwargs.get('payload'))


class UpdateNewInlineCallbackQuery(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique query identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the user who sent the query.
        self.sender_user_id: int = get_object(kwargs.get('sender_user_id'))
        # Identifier of the inline message from which the query originated.
        self.inline_message_id: str = get_object(kwargs.get('inline_message_id'))
        # An identifier uniquely corresponding to the chat a message was sent to.
        self.chat_instance: int = get_object(kwargs.get('chat_instance'))
        # Query payload.
        self.payload: CallbackQueryPayload = get_object(kwargs.get('payload'))


class UpdateNewShippingQuery(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique query identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the user who sent the query.
        self.sender_user_id: int = get_object(kwargs.get('sender_user_id'))
        # Invoice payload.
        self.invoice_payload: str = get_object(kwargs.get('invoice_payload'))
        # User shipping address.
        self.shipping_address: Address = get_object(kwargs.get('shipping_address'))


class UpdateNewPreCheckoutQuery(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique query identifier.
        self.id: int = get_object(kwargs.get('id'))
        # Identifier of the user who sent the query.
        self.sender_user_id: int = get_object(kwargs.get('sender_user_id'))
        # Currency for the product price.
        self.currency: str = get_object(kwargs.get('currency'))
        # Total price for the product, in the smallest units of the currency.
        self.total_amount: int = get_object(kwargs.get('total_amount'))
        # Invoice payload.
        self.invoice_payload: bytes = get_object(kwargs.get('invoice_payload'))
        # Identifier of a shipping option chosen by the user; may be empty if not applicable.
        self.shipping_option_id: str = get_object(kwargs.get('shipping_option_id'))
        # Information about the order; may be null.
        self.order_info: OrderInfo = get_object(kwargs.get('order_info'))


class UpdateNewCustomEvent(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # A JSON-serialized event.
        self.event: str = get_object(kwargs.get('event'))


class UpdateNewCustomQuery(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The query identifier.
        self.id: int = get_object(kwargs.get('id'))
        # JSON-serialized query data.
        self.data: str = get_object(kwargs.get('data'))
        # Query timeout.
        self.timeout: int = get_object(kwargs.get('timeout'))


class UpdatePoll(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # New data about the poll.
        self.poll: Poll = get_object(kwargs.get('poll'))


class UpdatePollAnswer(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique poll identifier.
        self.poll_id: int = get_object(kwargs.get('poll_id'))
        # Identifier of the message sender that changed the answer to the poll.
        self.voter_id: MessageSender = get_object(kwargs.get('voter_id'))
        # 0-based identifiers of answer options, chosen by the user.
        self.option_ids: list[int] = get_object(kwargs.get('option_ids'))


class UpdateChatMember(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Identifier of the user, changing the rights.
        self.actor_user_id: int = get_object(kwargs.get('actor_user_id'))
        # Point in time (Unix timestamp) when the user rights was changed.
        self.date: int = get_object(kwargs.get('date'))
        # If user has joined the chat using an invite link, the invite link; may be null.
        self.invite_link: ChatInviteLink = get_object(kwargs.get('invite_link'))
        # True, if the user has joined the chat using an invite link for a chat filter.
        self.via_chat_filter_invite_link: bool = get_object(kwargs.get('via_chat_filter_invite_link'))
        # Previous chat member.
        self.old_chat_member: ChatMember = get_object(kwargs.get('old_chat_member'))
        # New chat member.
        self.new_chat_member: ChatMember = get_object(kwargs.get('new_chat_member'))


class UpdateNewChatJoinRequest(Update):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Chat identifier.
        self.chat_id: int = get_object(kwargs.get('chat_id'))
        # Join request.
        self.request: ChatJoinRequest = get_object(kwargs.get('request'))
        # Chat identifier of the private chat with the user.
        self.user_chat_id: int = get_object(kwargs.get('user_chat_id'))
        # The invite link, which was used to send join request; may be null.
        self.invite_link: ChatInviteLink = get_object(kwargs.get('invite_link'))


class Updates(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # List of updates.
        self.updates: list[Update] = get_object(kwargs.get('updates'))


class UserType(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserLink(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The URL.
        self.url: str = get_object(kwargs.get('url'))
        # Left time for which the link is valid, in seconds; 0 if the link is a public username link.
        self.expires_in: int = get_object(kwargs.get('expires_in'))


class UserPrivacySettingShowStatus(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingShowProfilePhoto(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingShowLinkInForwardedMessages(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingShowPhoneNumber(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingShowBio(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingAllowChatInvites(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingAllowCalls(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingAllowPeerToPeerCalls(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingAllowFindingByPhoneNumber(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingAllowPrivateVoiceAndVideoNoteMessages(UserPrivacySetting):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingRule(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingRuleAllowAll(UserPrivacySettingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingRuleAllowContacts(UserPrivacySettingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingRuleAllowUsers(UserPrivacySettingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The user identifiers, total number of users in all rules must not exceed 1000.
        self.user_ids: list[int] = get_object(kwargs.get('user_ids'))


class UserPrivacySettingRuleAllowChatMembers(UserPrivacySettingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat identifiers, total number of chats in all rules must not exceed 20.
        self.chat_ids: list[int] = get_object(kwargs.get('chat_ids'))


class UserPrivacySettingRuleRestrictAll(UserPrivacySettingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingRuleRestrictContacts(UserPrivacySettingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserPrivacySettingRuleRestrictUsers(UserPrivacySettingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The user identifiers, total number of users in all rules must not exceed 1000.
        self.user_ids: list[int] = get_object(kwargs.get('user_ids'))


class UserPrivacySettingRuleRestrictChatMembers(UserPrivacySettingRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The chat identifiers, total number of chats in all rules must not exceed 20.
        self.chat_ids: list[int] = get_object(kwargs.get('chat_ids'))


class UserStatusEmpty(UserStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserStatusOnline(UserStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) when the user's online status will expire.
        self.expires: int = get_object(kwargs.get('expires'))


class UserStatusOffline(UserStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Point in time (Unix timestamp) when the user was last online.
        self.was_online: int = get_object(kwargs.get('was_online'))


class UserStatusRecently(UserStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserStatusLastWeek(UserStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserStatusLastMonth(UserStatus):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserSupportInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Information message.
        self.message: FormattedText = get_object(kwargs.get('message'))
        # Information author.
        self.author: str = get_object(kwargs.get('author'))
        # Information change date.
        self.date: int = get_object(kwargs.get('date'))


class UserTypeRegular(UserType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserTypeDeleted(UserType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class UserTypeBot(UserType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # True, if the bot is owned by the current user and can be edited using the methods toggleBotUsernameIsActive, reorderBotActiveUsernames, setBotProfilePhoto, setBotName, setBotInfoDescription, and setBotInfoShortDescription.
        self.can_be_edited: bool = get_object(kwargs.get('can_be_edited'))
        # True, if the bot can be invited to basic group and supergroup chats.
        self.can_join_groups: bool = get_object(kwargs.get('can_join_groups'))
        # True, if the bot can read all messages in basic group or supergroup chats and not just those addressed to the bot. In private and channel chats a bot can always read all messages.
        self.can_read_all_group_messages: bool = get_object(kwargs.get('can_read_all_group_messages'))
        # True, if the bot supports inline queries.
        self.is_inline: bool = get_object(kwargs.get('is_inline'))
        # Placeholder for inline queries (displayed on the application input field).
        self.inline_query_placeholder: str = get_object(kwargs.get('inline_query_placeholder'))
        # True, if the location of the user is expected to be sent with every inline query to this bot.
        self.need_location: bool = get_object(kwargs.get('need_location'))
        # True, if the bot can be added to attachment or side menu.
        self.can_be_added_to_attachment_menu: bool = get_object(kwargs.get('can_be_added_to_attachment_menu'))


class UserTypeUnknown(UserType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs


class Users(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Approximate total number of users found.
        self.total_count: int = get_object(kwargs.get('total_count'))
        # A list of user identifiers.
        self.user_ids: list[int] = get_object(kwargs.get('user_ids'))


class ValidatedOrderInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Temporary identifier of the order information.
        self.order_info_id: str = get_object(kwargs.get('order_info_id'))
        # Available shipping options.
        self.shipping_options: list[ShippingOption] = get_object(kwargs.get('shipping_options'))


class VectorPathCommandLine(VectorPathCommand):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The end point of the straight line.
        self.end_point: Point = get_object(kwargs.get('end_point'))


class VectorPathCommandCubicBezierCurve(VectorPathCommand):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # The start control point of the curve.
        self.start_control_point: Point = get_object(kwargs.get('start_control_point'))
        # The end control point of the curve.
        self.end_control_point: Point = get_object(kwargs.get('end_control_point'))
        # The end point of the curve.
        self.end_point: Point = get_object(kwargs.get('end_point'))


class WebAppInfo(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Unique identifier for the Web App launch.
        self.launch_id: int = get_object(kwargs.get('launch_id'))
        # A Web App URL to open in a web view.
        self.url: str = get_object(kwargs.get('url'))


class WebPageInstantView(Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        # Content of the web page.
        self.page_blocks: list[PageBlock] = get_object(kwargs.get('page_blocks'))
        # Number of the instant view views; 0 if unknown.
        self.view_count: int = get_object(kwargs.get('view_count'))
        # Version of the instant view; currently, can be 1 or 2.
        self.version: int = get_object(kwargs.get('version'))
        # True, if the instant view must be shown from right to left.
        self.is_rtl: bool = get_object(kwargs.get('is_rtl'))
        # True, if the instant view contains the full page. A network request might be needed to get the full web page instant view.
        self.is_full: bool = get_object(kwargs.get('is_full'))
        # An internal link to be opened to leave feedback about the instant view.
        self.feedback_link: InternalLinkType = get_object(kwargs.get('feedback_link'))


types = {
    'TlObject': TlObject,
    'TlStorerToString': TlStorerToString,
    'Object': Object,
    'Function': Function,
    'accountTtl': AccountTtl,
    'MessageSender': MessageSender,
    'ReactionType': ReactionType,
    'addedReaction': AddedReaction,
    'addedReactions': AddedReactions,
    'address': Address,
    'file': File,
    'animatedChatPhoto': AnimatedChatPhoto,
    'sticker': Sticker,
    'animatedEmoji': AnimatedEmoji,
    'minithumbnail': Minithumbnail,
    'thumbnail': Thumbnail,
    'animation': Animation,
    'animations': Animations,
    'archiveChatListSettings': ArchiveChatListSettings,
    'attachmentMenuBotColor': AttachmentMenuBotColor,
    'attachmentMenuBot': AttachmentMenuBot,
    'audio': Audio,
    'AuthenticationCodeType': AuthenticationCodeType,
    'authenticationCodeInfo': AuthenticationCodeInfo,
    'authenticationCodeTypeTelegramMessage': AuthenticationCodeTypeTelegramMessage,
    'authenticationCodeTypeSms': AuthenticationCodeTypeSms,
    'authenticationCodeTypeCall': AuthenticationCodeTypeCall,
    'authenticationCodeTypeFlashCall': AuthenticationCodeTypeFlashCall,
    'authenticationCodeTypeMissedCall': AuthenticationCodeTypeMissedCall,
    'authenticationCodeTypeFragment': AuthenticationCodeTypeFragment,
    'authenticationCodeTypeFirebaseAndroid': AuthenticationCodeTypeFirebaseAndroid,
    'authenticationCodeTypeFirebaseIos': AuthenticationCodeTypeFirebaseIos,
    'EmailAddressResetState': EmailAddressResetState,
    'emailAddressAuthenticationCodeInfo': EmailAddressAuthenticationCodeInfo,
    'termsOfService': TermsOfService,
    'AuthorizationState': AuthorizationState,
    'authorizationStateWaitTdlibParameters': AuthorizationStateWaitTdlibParameters,
    'authorizationStateWaitPhoneNumber': AuthorizationStateWaitPhoneNumber,
    'authorizationStateWaitEmailAddress': AuthorizationStateWaitEmailAddress,
    'authorizationStateWaitEmailCode': AuthorizationStateWaitEmailCode,
    'authorizationStateWaitCode': AuthorizationStateWaitCode,
    'authorizationStateWaitOtherDeviceConfirmation': AuthorizationStateWaitOtherDeviceConfirmation,
    'authorizationStateWaitRegistration': AuthorizationStateWaitRegistration,
    'authorizationStateWaitPassword': AuthorizationStateWaitPassword,
    'authorizationStateReady': AuthorizationStateReady,
    'authorizationStateLoggingOut': AuthorizationStateLoggingOut,
    'authorizationStateClosing': AuthorizationStateClosing,
    'authorizationStateClosed': AuthorizationStateClosed,
    'autoDownloadSettings': AutoDownloadSettings,
    'autoDownloadSettingsPresets': AutoDownloadSettingsPresets,
    'autosaveSettingsException': AutosaveSettingsException,
    'scopeAutosaveSettings': ScopeAutosaveSettings,
    'autosaveSettings': AutosaveSettings,
    'AutosaveSettingsScope': AutosaveSettingsScope,
    'autosaveSettingsScopePrivateChats': AutosaveSettingsScopePrivateChats,
    'autosaveSettingsScopeGroupChats': AutosaveSettingsScopeGroupChats,
    'autosaveSettingsScopeChannelChats': AutosaveSettingsScopeChannelChats,
    'autosaveSettingsScopeChat': AutosaveSettingsScopeChat,
    'availableReaction': AvailableReaction,
    'availableReactions': AvailableReactions,
    'BackgroundType': BackgroundType,
    'document': Document,
    'background': Background,
    'BackgroundFill': BackgroundFill,
    'backgroundFillSolid': BackgroundFillSolid,
    'backgroundFillGradient': BackgroundFillGradient,
    'backgroundFillFreeformGradient': BackgroundFillFreeformGradient,
    'backgroundTypeWallpaper': BackgroundTypeWallpaper,
    'backgroundTypePattern': BackgroundTypePattern,
    'backgroundTypeFill': BackgroundTypeFill,
    'backgrounds': Backgrounds,
    'bankCardActionOpenUrl': BankCardActionOpenUrl,
    'bankCardInfo': BankCardInfo,
    'ChatMemberStatus': ChatMemberStatus,
    'basicGroup': BasicGroup,
    'botCommands': BotCommands,
    'chatInviteLink': ChatInviteLink,
    'chatMember': ChatMember,
    'chatPhoto': ChatPhoto,
    'basicGroupFullInfo': BasicGroupFullInfo,
    'BlockList': BlockList,
    'blockListMain': BlockListMain,
    'blockListStories': BlockListStories,
    'botCommand': BotCommand,
    'BotCommandScope': BotCommandScope,
    'botCommandScopeDefault': BotCommandScopeDefault,
    'botCommandScopeAllPrivateChats': BotCommandScopeAllPrivateChats,
    'botCommandScopeAllGroupChats': BotCommandScopeAllGroupChats,
    'botCommandScopeAllChatAdministrators': BotCommandScopeAllChatAdministrators,
    'botCommandScopeChat': BotCommandScopeChat,
    'botCommandScopeChatAdministrators': BotCommandScopeChatAdministrators,
    'botCommandScopeChatMember': BotCommandScopeChatMember,
    'InternalLinkType': InternalLinkType,
    'botMenuButton': BotMenuButton,
    'chatAdministratorRights': ChatAdministratorRights,
    'photo': Photo,
    'botInfo': BotInfo,
    'CallState': CallState,
    'call': Call,
    'CallDiscardReason': CallDiscardReason,
    'callDiscardReasonEmpty': CallDiscardReasonEmpty,
    'callDiscardReasonMissed': CallDiscardReasonMissed,
    'callDiscardReasonDeclined': CallDiscardReasonDeclined,
    'callDiscardReasonDisconnected': CallDiscardReasonDisconnected,
    'callDiscardReasonHungUp': CallDiscardReasonHungUp,
    'callId': CallId,
    'CallProblem': CallProblem,
    'callProblemEcho': CallProblemEcho,
    'callProblemNoise': CallProblemNoise,
    'callProblemInterruptions': CallProblemInterruptions,
    'callProblemDistortedSpeech': CallProblemDistortedSpeech,
    'callProblemSilentLocal': CallProblemSilentLocal,
    'callProblemSilentRemote': CallProblemSilentRemote,
    'callProblemDropped': CallProblemDropped,
    'callProblemDistortedVideo': CallProblemDistortedVideo,
    'callProblemPixelatedVideo': CallProblemPixelatedVideo,
    'callProtocol': CallProtocol,
    'CallServerType': CallServerType,
    'callServer': CallServer,
    'callServerTypeTelegramReflector': CallServerTypeTelegramReflector,
    'callServerTypeWebrtc': CallServerTypeWebrtc,
    'error': Error,
    'callStatePending': CallStatePending,
    'callStateExchangingKeys': CallStateExchangingKeys,
    'callStateReady': CallStateReady,
    'callStateHangingUp': CallStateHangingUp,
    'callStateDiscarded': CallStateDiscarded,
    'callStateError': CallStateError,
    'callbackQueryAnswer': CallbackQueryAnswer,
    'CallbackQueryPayload': CallbackQueryPayload,
    'callbackQueryPayloadData': CallbackQueryPayloadData,
    'callbackQueryPayloadDataWithPassword': CallbackQueryPayloadDataWithPassword,
    'callbackQueryPayloadGame': CallbackQueryPayloadGame,
    'CanSendStoryResult': CanSendStoryResult,
    'canSendStoryResultOk': CanSendStoryResultOk,
    'canSendStoryResultPremiumNeeded': CanSendStoryResultPremiumNeeded,
    'canSendStoryResultActiveStoryLimitExceeded': CanSendStoryResultActiveStoryLimitExceeded,
    'canSendStoryResultWeeklyLimitExceeded': CanSendStoryResultWeeklyLimitExceeded,
    'canSendStoryResultMonthlyLimitExceeded': CanSendStoryResultMonthlyLimitExceeded,
    'CanTransferOwnershipResult': CanTransferOwnershipResult,
    'canTransferOwnershipResultOk': CanTransferOwnershipResultOk,
    'canTransferOwnershipResultPasswordNeeded': CanTransferOwnershipResultPasswordNeeded,
    'canTransferOwnershipResultPasswordTooFresh': CanTransferOwnershipResultPasswordTooFresh,
    'canTransferOwnershipResultSessionTooFresh': CanTransferOwnershipResultSessionTooFresh,
    'ChatActionBar': ChatActionBar,
    'ChatAvailableReactions': ChatAvailableReactions,
    'ChatType': ChatType,
    'chatBackground': ChatBackground,
    'chatJoinRequestsInfo': ChatJoinRequestsInfo,
    'chatNotificationSettings': ChatNotificationSettings,
    'chatPermissions': ChatPermissions,
    'chatPhotoInfo': ChatPhotoInfo,
    'chatPosition': ChatPosition,
    'draftMessage': DraftMessage,
    'message': Message,
    'videoChat': VideoChat,
    'chat': Chat,
    'ChatAction': ChatAction,
    'chatActionTyping': ChatActionTyping,
    'chatActionRecordingVideo': ChatActionRecordingVideo,
    'chatActionUploadingVideo': ChatActionUploadingVideo,
    'chatActionRecordingVoiceNote': ChatActionRecordingVoiceNote,
    'chatActionUploadingVoiceNote': ChatActionUploadingVoiceNote,
    'chatActionUploadingPhoto': ChatActionUploadingPhoto,
    'chatActionUploadingDocument': ChatActionUploadingDocument,
    'chatActionChoosingSticker': ChatActionChoosingSticker,
    'chatActionChoosingLocation': ChatActionChoosingLocation,
    'chatActionChoosingContact': ChatActionChoosingContact,
    'chatActionStartPlayingGame': ChatActionStartPlayingGame,
    'chatActionRecordingVideoNote': ChatActionRecordingVideoNote,
    'chatActionUploadingVideoNote': ChatActionUploadingVideoNote,
    'chatActionWatchingAnimations': ChatActionWatchingAnimations,
    'chatActionCancel': ChatActionCancel,
    'chatActionBarReportSpam': ChatActionBarReportSpam,
    'chatActionBarReportUnrelatedLocation': ChatActionBarReportUnrelatedLocation,
    'chatActionBarInviteMembers': ChatActionBarInviteMembers,
    'chatActionBarReportAddBlock': ChatActionBarReportAddBlock,
    'chatActionBarAddContact': ChatActionBarAddContact,
    'chatActionBarSharePhoneNumber': ChatActionBarSharePhoneNumber,
    'chatActionBarJoinRequest': ChatActionBarJoinRequest,
    'StoryList': StoryList,
    'storyInfo': StoryInfo,
    'chatActiveStories': ChatActiveStories,
    'chatAdministrator': ChatAdministrator,
    'chatAdministrators': ChatAdministrators,
    'chatAvailableReactionsAll': ChatAvailableReactionsAll,
    'chatAvailableReactionsSome': ChatAvailableReactionsSome,
    'ChatEventAction': ChatEventAction,
    'chatEvent': ChatEvent,
    'chatLocation': ChatLocation,
    'forumTopicInfo': ForumTopicInfo,
    'chatEventMessageEdited': ChatEventMessageEdited,
    'chatEventMessageDeleted': ChatEventMessageDeleted,
    'chatEventMessagePinned': ChatEventMessagePinned,
    'chatEventMessageUnpinned': ChatEventMessageUnpinned,
    'chatEventPollStopped': ChatEventPollStopped,
    'chatEventMemberJoined': ChatEventMemberJoined,
    'chatEventMemberJoinedByInviteLink': ChatEventMemberJoinedByInviteLink,
    'chatEventMemberJoinedByRequest': ChatEventMemberJoinedByRequest,
    'chatEventMemberInvited': ChatEventMemberInvited,
    'chatEventMemberLeft': ChatEventMemberLeft,
    'chatEventMemberPromoted': ChatEventMemberPromoted,
    'chatEventMemberRestricted': ChatEventMemberRestricted,
    'chatEventAvailableReactionsChanged': ChatEventAvailableReactionsChanged,
    'chatEventDescriptionChanged': ChatEventDescriptionChanged,
    'chatEventLinkedChatChanged': ChatEventLinkedChatChanged,
    'chatEventLocationChanged': ChatEventLocationChanged,
    'chatEventMessageAutoDeleteTimeChanged': ChatEventMessageAutoDeleteTimeChanged,
    'chatEventPermissionsChanged': ChatEventPermissionsChanged,
    'chatEventPhotoChanged': ChatEventPhotoChanged,
    'chatEventSlowModeDelayChanged': ChatEventSlowModeDelayChanged,
    'chatEventStickerSetChanged': ChatEventStickerSetChanged,
    'chatEventTitleChanged': ChatEventTitleChanged,
    'chatEventUsernameChanged': ChatEventUsernameChanged,
    'chatEventActiveUsernamesChanged': ChatEventActiveUsernamesChanged,
    'chatEventHasProtectedContentToggled': ChatEventHasProtectedContentToggled,
    'chatEventInvitesToggled': ChatEventInvitesToggled,
    'chatEventIsAllHistoryAvailableToggled': ChatEventIsAllHistoryAvailableToggled,
    'chatEventHasAggressiveAntiSpamEnabledToggled': ChatEventHasAggressiveAntiSpamEnabledToggled,
    'chatEventSignMessagesToggled': ChatEventSignMessagesToggled,
    'chatEventInviteLinkEdited': ChatEventInviteLinkEdited,
    'chatEventInviteLinkRevoked': ChatEventInviteLinkRevoked,
    'chatEventInviteLinkDeleted': ChatEventInviteLinkDeleted,
    'chatEventVideoChatCreated': ChatEventVideoChatCreated,
    'chatEventVideoChatEnded': ChatEventVideoChatEnded,
    'chatEventVideoChatMuteNewParticipantsToggled': ChatEventVideoChatMuteNewParticipantsToggled,
    'chatEventVideoChatParticipantIsMutedToggled': ChatEventVideoChatParticipantIsMutedToggled,
    'chatEventVideoChatParticipantVolumeLevelChanged': ChatEventVideoChatParticipantVolumeLevelChanged,
    'chatEventIsForumToggled': ChatEventIsForumToggled,
    'chatEventForumTopicCreated': ChatEventForumTopicCreated,
    'chatEventForumTopicEdited': ChatEventForumTopicEdited,
    'chatEventForumTopicToggleIsClosed': ChatEventForumTopicToggleIsClosed,
    'chatEventForumTopicToggleIsHidden': ChatEventForumTopicToggleIsHidden,
    'chatEventForumTopicDeleted': ChatEventForumTopicDeleted,
    'chatEventForumTopicPinned': ChatEventForumTopicPinned,
    'chatEventLogFilters': ChatEventLogFilters,
    'chatEvents': ChatEvents,
    'chatFilterIcon': ChatFilterIcon,
    'chatFilter': ChatFilter,
    'chatFilterInfo': ChatFilterInfo,
    'chatFilterInviteLink': ChatFilterInviteLink,
    'chatFilterInviteLinkInfo': ChatFilterInviteLinkInfo,
    'chatFilterInviteLinks': ChatFilterInviteLinks,
    'chatInviteLinkCount': ChatInviteLinkCount,
    'chatInviteLinkCounts': ChatInviteLinkCounts,
    'InviteLinkChatType': InviteLinkChatType,
    'chatInviteLinkInfo': ChatInviteLinkInfo,
    'chatInviteLinkMember': ChatInviteLinkMember,
    'chatInviteLinkMembers': ChatInviteLinkMembers,
    'chatInviteLinks': ChatInviteLinks,
    'chatJoinRequest': ChatJoinRequest,
    'chatJoinRequests': ChatJoinRequests,
    'ChatList': ChatList,
    'chatListMain': ChatListMain,
    'chatListArchive': ChatListArchive,
    'chatListFilter': ChatListFilter,
    'chatLists': ChatLists,
    'location': Location,
    'chatMemberStatusCreator': ChatMemberStatusCreator,
    'chatMemberStatusAdministrator': ChatMemberStatusAdministrator,
    'chatMemberStatusMember': ChatMemberStatusMember,
    'chatMemberStatusRestricted': ChatMemberStatusRestricted,
    'chatMemberStatusLeft': ChatMemberStatusLeft,
    'chatMemberStatusBanned': ChatMemberStatusBanned,
    'chatMembers': ChatMembers,
    'ChatMembersFilter': ChatMembersFilter,
    'chatMembersFilterContacts': ChatMembersFilterContacts,
    'chatMembersFilterAdministrators': ChatMembersFilterAdministrators,
    'chatMembersFilterMembers': ChatMembersFilterMembers,
    'chatMembersFilterMention': ChatMembersFilterMention,
    'chatMembersFilterRestricted': ChatMembersFilterRestricted,
    'chatMembersFilterBanned': ChatMembersFilterBanned,
    'chatMembersFilterBots': ChatMembersFilterBots,
    'chatMessageSender': ChatMessageSender,
    'chatMessageSenders': ChatMessageSenders,
    'chatNearby': ChatNearby,
    'chatPhotoSticker': ChatPhotoSticker,
    'photoSize': PhotoSize,
    'ChatPhotoStickerType': ChatPhotoStickerType,
    'chatPhotoStickerTypeRegularOrMask': ChatPhotoStickerTypeRegularOrMask,
    'chatPhotoStickerTypeCustomEmoji': ChatPhotoStickerTypeCustomEmoji,
    'chatPhotos': ChatPhotos,
    'ChatSource': ChatSource,
    'chatSourceMtprotoProxy': ChatSourceMtprotoProxy,
    'chatSourcePublicServiceAnnouncement': ChatSourcePublicServiceAnnouncement,
    'StatisticalGraph': StatisticalGraph,
    'chatStatisticsAdministratorActionsInfo': ChatStatisticsAdministratorActionsInfo,
    'chatStatisticsInviterInfo': ChatStatisticsInviterInfo,
    'chatStatisticsMessageInteractionInfo': ChatStatisticsMessageInteractionInfo,
    'chatStatisticsMessageSenderInfo': ChatStatisticsMessageSenderInfo,
    'dateRange': DateRange,
    'statisticalValue': StatisticalValue,
    'ChatStatistics': ChatStatistics,
    'chatStatisticsSupergroup': ChatStatisticsSupergroup,
    'chatStatisticsChannel': ChatStatisticsChannel,
    'themeSettings': ThemeSettings,
    'chatTheme': ChatTheme,
    'chatTypePrivate': ChatTypePrivate,
    'chatTypeBasicGroup': ChatTypeBasicGroup,
    'chatTypeSupergroup': ChatTypeSupergroup,
    'chatTypeSecret': ChatTypeSecret,
    'chats': Chats,
    'chatsNearby': ChatsNearby,
    'CheckChatUsernameResult': CheckChatUsernameResult,
    'checkChatUsernameResultOk': CheckChatUsernameResultOk,
    'checkChatUsernameResultUsernameInvalid': CheckChatUsernameResultUsernameInvalid,
    'checkChatUsernameResultUsernameOccupied': CheckChatUsernameResultUsernameOccupied,
    'checkChatUsernameResultUsernamePurchasable': CheckChatUsernameResultUsernamePurchasable,
    'checkChatUsernameResultPublicChatsTooMany': CheckChatUsernameResultPublicChatsTooMany,
    'checkChatUsernameResultPublicGroupsUnavailable': CheckChatUsernameResultPublicGroupsUnavailable,
    'CheckStickerSetNameResult': CheckStickerSetNameResult,
    'checkStickerSetNameResultOk': CheckStickerSetNameResultOk,
    'checkStickerSetNameResultNameInvalid': CheckStickerSetNameResultNameInvalid,
    'checkStickerSetNameResultNameOccupied': CheckStickerSetNameResultNameOccupied,
    'VectorPathCommand': VectorPathCommand,
    'closedVectorPath': ClosedVectorPath,
    'connectedWebsite': ConnectedWebsite,
    'connectedWebsites': ConnectedWebsites,
    'ConnectionState': ConnectionState,
    'connectionStateWaitingForNetwork': ConnectionStateWaitingForNetwork,
    'connectionStateConnectingToProxy': ConnectionStateConnectingToProxy,
    'connectionStateConnecting': ConnectionStateConnecting,
    'connectionStateUpdating': ConnectionStateUpdating,
    'connectionStateReady': ConnectionStateReady,
    'contact': Contact,
    'count': Count,
    'countryInfo': CountryInfo,
    'countries': Countries,
    'customRequestResult': CustomRequestResult,
    'databaseStatistics': DatabaseStatistics,
    'date': Date,
    'datedFile': DatedFile,
    'formattedText': FormattedText,
    'deepLinkInfo': DeepLinkInfo,
    'DeviceToken': DeviceToken,
    'deviceTokenFirebaseCloudMessaging': DeviceTokenFirebaseCloudMessaging,
    'deviceTokenApplePush': DeviceTokenApplePush,
    'deviceTokenApplePushVoIP': DeviceTokenApplePushVoIP,
    'deviceTokenWindowsPush': DeviceTokenWindowsPush,
    'deviceTokenMicrosoftPush': DeviceTokenMicrosoftPush,
    'deviceTokenMicrosoftPushVoIP': DeviceTokenMicrosoftPushVoIP,
    'deviceTokenWebPush': DeviceTokenWebPush,
    'deviceTokenSimplePush': DeviceTokenSimplePush,
    'deviceTokenUbuntuPush': DeviceTokenUbuntuPush,
    'deviceTokenBlackBerryPush': DeviceTokenBlackBerryPush,
    'deviceTokenTizenPush': DeviceTokenTizenPush,
    'deviceTokenHuaweiPush': DeviceTokenHuaweiPush,
    'DiceStickers': DiceStickers,
    'diceStickersRegular': DiceStickersRegular,
    'diceStickersSlotMachine': DiceStickersSlotMachine,
    'downloadedFileCounts': DownloadedFileCounts,
    'InputMessageContent': InputMessageContent,
    'EmailAddressAuthentication': EmailAddressAuthentication,
    'emailAddressAuthenticationCode': EmailAddressAuthenticationCode,
    'emailAddressAuthenticationAppleId': EmailAddressAuthenticationAppleId,
    'emailAddressAuthenticationGoogleId': EmailAddressAuthenticationGoogleId,
    'emailAddressResetStateAvailable': EmailAddressResetStateAvailable,
    'emailAddressResetStatePending': EmailAddressResetStatePending,
    'emojiCategory': EmojiCategory,
    'emojiCategories': EmojiCategories,
    'EmojiCategoryType': EmojiCategoryType,
    'emojiCategoryTypeDefault': EmojiCategoryTypeDefault,
    'emojiCategoryTypeEmojiStatus': EmojiCategoryTypeEmojiStatus,
    'emojiCategoryTypeChatPhoto': EmojiCategoryTypeChatPhoto,
    'emojiReaction': EmojiReaction,
    'emojiStatus': EmojiStatus,
    'emojiStatuses': EmojiStatuses,
    'emojis': Emojis,
    'encryptedCredentials': EncryptedCredentials,
    'PassportElementType': PassportElementType,
    'encryptedPassportElement': EncryptedPassportElement,
    'localFile': LocalFile,
    'remoteFile': RemoteFile,
    'fileDownload': FileDownload,
    'fileDownloadedPrefixSize': FileDownloadedPrefixSize,
    'filePart': FilePart,
    'FileType': FileType,
    'fileTypeNone': FileTypeNone,
    'fileTypeAnimation': FileTypeAnimation,
    'fileTypeAudio': FileTypeAudio,
    'fileTypeDocument': FileTypeDocument,
    'fileTypeNotificationSound': FileTypeNotificationSound,
    'fileTypePhoto': FileTypePhoto,
    'fileTypePhotoStory': FileTypePhotoStory,
    'fileTypeProfilePhoto': FileTypeProfilePhoto,
    'fileTypeSecret': FileTypeSecret,
    'fileTypeSecretThumbnail': FileTypeSecretThumbnail,
    'fileTypeSecure': FileTypeSecure,
    'fileTypeSticker': FileTypeSticker,
    'fileTypeThumbnail': FileTypeThumbnail,
    'fileTypeUnknown': FileTypeUnknown,
    'fileTypeVideo': FileTypeVideo,
    'fileTypeVideoNote': FileTypeVideoNote,
    'fileTypeVideoStory': FileTypeVideoStory,
    'fileTypeVoiceNote': FileTypeVoiceNote,
    'fileTypeWallpaper': FileTypeWallpaper,
    'FirebaseAuthenticationSettings': FirebaseAuthenticationSettings,
    'firebaseAuthenticationSettingsAndroid': FirebaseAuthenticationSettingsAndroid,
    'firebaseAuthenticationSettingsIos': FirebaseAuthenticationSettingsIos,
    'textEntity': TextEntity,
    'forumTopic': ForumTopic,
    'forumTopicIcon': ForumTopicIcon,
    'forumTopics': ForumTopics,
    'foundChatMessages': FoundChatMessages,
    'foundFileDownloads': FoundFileDownloads,
    'foundMessages': FoundMessages,
    'foundPositions': FoundPositions,
    'webApp': WebApp,
    'foundWebApp': FoundWebApp,
    'game': Game,
    'gameHighScore': GameHighScore,
    'gameHighScores': GameHighScores,
    'groupCallRecentSpeaker': GroupCallRecentSpeaker,
    'groupCall': GroupCall,
    'groupCallId': GroupCallId,
    'groupCallParticipantVideoInfo': GroupCallParticipantVideoInfo,
    'groupCallParticipant': GroupCallParticipant,
    'groupCallVideoSourceGroup': GroupCallVideoSourceGroup,
    'groupCallStream': GroupCallStream,
    'groupCallStreams': GroupCallStreams,
    'GroupCallVideoQuality': GroupCallVideoQuality,
    'groupCallVideoQualityThumbnail': GroupCallVideoQualityThumbnail,
    'groupCallVideoQualityMedium': GroupCallVideoQualityMedium,
    'groupCallVideoQualityFull': GroupCallVideoQualityFull,
    'hashtags': Hashtags,
    'httpUrl': HttpUrl,
    'identityDocument': IdentityDocument,
    'importedContacts': ImportedContacts,
    'InlineKeyboardButtonType': InlineKeyboardButtonType,
    'inlineKeyboardButton': InlineKeyboardButton,
    'TargetChat': TargetChat,
    'inlineKeyboardButtonTypeUrl': InlineKeyboardButtonTypeUrl,
    'inlineKeyboardButtonTypeLoginUrl': InlineKeyboardButtonTypeLoginUrl,
    'inlineKeyboardButtonTypeWebApp': InlineKeyboardButtonTypeWebApp,
    'inlineKeyboardButtonTypeCallback': InlineKeyboardButtonTypeCallback,
    'inlineKeyboardButtonTypeCallbackWithPassword': InlineKeyboardButtonTypeCallbackWithPassword,
    'inlineKeyboardButtonTypeCallbackGame': InlineKeyboardButtonTypeCallbackGame,
    'inlineKeyboardButtonTypeSwitchInline': InlineKeyboardButtonTypeSwitchInline,
    'inlineKeyboardButtonTypeBuy': InlineKeyboardButtonTypeBuy,
    'inlineKeyboardButtonTypeUser': InlineKeyboardButtonTypeUser,
    'venue': Venue,
    'video': Video,
    'voiceNote': VoiceNote,
    'InlineQueryResult': InlineQueryResult,
    'inlineQueryResultArticle': InlineQueryResultArticle,
    'inlineQueryResultContact': InlineQueryResultContact,
    'inlineQueryResultLocation': InlineQueryResultLocation,
    'inlineQueryResultVenue': InlineQueryResultVenue,
    'inlineQueryResultGame': InlineQueryResultGame,
    'inlineQueryResultAnimation': InlineQueryResultAnimation,
    'inlineQueryResultAudio': InlineQueryResultAudio,
    'inlineQueryResultDocument': InlineQueryResultDocument,
    'inlineQueryResultPhoto': InlineQueryResultPhoto,
    'inlineQueryResultSticker': InlineQueryResultSticker,
    'inlineQueryResultVideo': InlineQueryResultVideo,
    'inlineQueryResultVoiceNote': InlineQueryResultVoiceNote,
    'inlineQueryResultsButton': InlineQueryResultsButton,
    'inlineQueryResults': InlineQueryResults,
    'InlineQueryResultsButtonType': InlineQueryResultsButtonType,
    'inlineQueryResultsButtonTypeStartBot': InlineQueryResultsButtonTypeStartBot,
    'inlineQueryResultsButtonTypeWebApp': InlineQueryResultsButtonTypeWebApp,
    'InputFile': InputFile,
    'InputBackground': InputBackground,
    'inputBackgroundLocal': InputBackgroundLocal,
    'inputBackgroundRemote': InputBackgroundRemote,
    'inputBackgroundPrevious': InputBackgroundPrevious,
    'InputChatPhoto': InputChatPhoto,
    'inputChatPhotoPrevious': InputChatPhotoPrevious,
    'inputChatPhotoStatic': InputChatPhotoStatic,
    'inputChatPhotoAnimation': InputChatPhotoAnimation,
    'inputChatPhotoSticker': InputChatPhotoSticker,
    'InputCredentials': InputCredentials,
    'inputCredentialsSaved': InputCredentialsSaved,
    'inputCredentialsNew': InputCredentialsNew,
    'inputCredentialsApplePay': InputCredentialsApplePay,
    'inputCredentialsGooglePay': InputCredentialsGooglePay,
    'inputFileId': InputFileId,
    'inputFileRemote': InputFileRemote,
    'inputFileLocal': InputFileLocal,
    'inputFileGenerated': InputFileGenerated,
    'inputIdentityDocument': InputIdentityDocument,
    'ReplyMarkup': ReplyMarkup,
    'InputInlineQueryResult': InputInlineQueryResult,
    'inputInlineQueryResultAnimation': InputInlineQueryResultAnimation,
    'inputInlineQueryResultArticle': InputInlineQueryResultArticle,
    'inputInlineQueryResultAudio': InputInlineQueryResultAudio,
    'inputInlineQueryResultContact': InputInlineQueryResultContact,
    'inputInlineQueryResultDocument': InputInlineQueryResultDocument,
    'inputInlineQueryResultGame': InputInlineQueryResultGame,
    'inputInlineQueryResultLocation': InputInlineQueryResultLocation,
    'inputInlineQueryResultPhoto': InputInlineQueryResultPhoto,
    'inputInlineQueryResultSticker': InputInlineQueryResultSticker,
    'inputInlineQueryResultVenue': InputInlineQueryResultVenue,
    'inputInlineQueryResultVideo': InputInlineQueryResultVideo,
    'inputInlineQueryResultVoiceNote': InputInlineQueryResultVoiceNote,
    'InputInvoice': InputInvoice,
    'inputInvoiceMessage': InputInvoiceMessage,
    'inputInvoiceName': InputInvoiceName,
    'MessageSelfDestructType': MessageSelfDestructType,
    'PollType': PollType,
    'inputThumbnail': InputThumbnail,
    'invoice': Invoice,
    'messageCopyOptions': MessageCopyOptions,
    'inputMessageText': InputMessageText,
    'inputMessageAnimation': InputMessageAnimation,
    'inputMessageAudio': InputMessageAudio,
    'inputMessageDocument': InputMessageDocument,
    'inputMessagePhoto': InputMessagePhoto,
    'inputMessageSticker': InputMessageSticker,
    'inputMessageVideo': InputMessageVideo,
    'inputMessageVideoNote': InputMessageVideoNote,
    'inputMessageVoiceNote': InputMessageVoiceNote,
    'inputMessageLocation': InputMessageLocation,
    'inputMessageVenue': InputMessageVenue,
    'inputMessageContact': InputMessageContact,
    'inputMessageDice': InputMessageDice,
    'inputMessageGame': InputMessageGame,
    'inputMessageInvoice': InputMessageInvoice,
    'inputMessagePoll': InputMessagePoll,
    'inputMessageStory': InputMessageStory,
    'inputMessageForwarded': InputMessageForwarded,
    'inputPersonalDocument': InputPersonalDocument,
    'personalDetails': PersonalDetails,
    'InputPassportElement': InputPassportElement,
    'inputPassportElementPersonalDetails': InputPassportElementPersonalDetails,
    'inputPassportElementPassport': InputPassportElementPassport,
    'inputPassportElementDriverLicense': InputPassportElementDriverLicense,
    'inputPassportElementIdentityCard': InputPassportElementIdentityCard,
    'inputPassportElementInternalPassport': InputPassportElementInternalPassport,
    'inputPassportElementAddress': InputPassportElementAddress,
    'inputPassportElementUtilityBill': InputPassportElementUtilityBill,
    'inputPassportElementBankStatement': InputPassportElementBankStatement,
    'inputPassportElementRentalAgreement': InputPassportElementRentalAgreement,
    'inputPassportElementPassportRegistration': InputPassportElementPassportRegistration,
    'inputPassportElementTemporaryRegistration': InputPassportElementTemporaryRegistration,
    'inputPassportElementPhoneNumber': InputPassportElementPhoneNumber,
    'inputPassportElementEmailAddress': InputPassportElementEmailAddress,
    'InputPassportElementErrorSource': InputPassportElementErrorSource,
    'inputPassportElementError': InputPassportElementError,
    'inputPassportElementErrorSourceUnspecified': InputPassportElementErrorSourceUnspecified,
    'inputPassportElementErrorSourceDataField': InputPassportElementErrorSourceDataField,
    'inputPassportElementErrorSourceFrontSide': InputPassportElementErrorSourceFrontSide,
    'inputPassportElementErrorSourceReverseSide': InputPassportElementErrorSourceReverseSide,
    'inputPassportElementErrorSourceSelfie': InputPassportElementErrorSourceSelfie,
    'inputPassportElementErrorSourceTranslationFile': InputPassportElementErrorSourceTranslationFile,
    'inputPassportElementErrorSourceTranslationFiles': InputPassportElementErrorSourceTranslationFiles,
    'inputPassportElementErrorSourceFile': InputPassportElementErrorSourceFile,
    'inputPassportElementErrorSourceFiles': InputPassportElementErrorSourceFiles,
    'maskPosition': MaskPosition,
    'inputSticker': InputSticker,
    'InputStoryAreaType': InputStoryAreaType,
    'storyAreaPosition': StoryAreaPosition,
    'inputStoryArea': InputStoryArea,
    'inputStoryAreaTypeLocation': InputStoryAreaTypeLocation,
    'inputStoryAreaTypeFoundVenue': InputStoryAreaTypeFoundVenue,
    'inputStoryAreaTypePreviousVenue': InputStoryAreaTypePreviousVenue,
    'inputStoryAreas': InputStoryAreas,
    'InputStoryContent': InputStoryContent,
    'inputStoryContentPhoto': InputStoryContentPhoto,
    'inputStoryContentVideo': InputStoryContentVideo,
    'ProxyType': ProxyType,
    'internalLinkTypeActiveSessions': InternalLinkTypeActiveSessions,
    'internalLinkTypeAttachmentMenuBot': InternalLinkTypeAttachmentMenuBot,
    'internalLinkTypeAuthenticationCode': InternalLinkTypeAuthenticationCode,
    'internalLinkTypeBackground': InternalLinkTypeBackground,
    'internalLinkTypeBotAddToChannel': InternalLinkTypeBotAddToChannel,
    'internalLinkTypeBotStart': InternalLinkTypeBotStart,
    'internalLinkTypeBotStartInGroup': InternalLinkTypeBotStartInGroup,
    'internalLinkTypeChangePhoneNumber': InternalLinkTypeChangePhoneNumber,
    'internalLinkTypeChatFilterInvite': InternalLinkTypeChatFilterInvite,
    'internalLinkTypeChatFilterSettings': InternalLinkTypeChatFilterSettings,
    'internalLinkTypeChatInvite': InternalLinkTypeChatInvite,
    'internalLinkTypeDefaultMessageAutoDeleteTimerSettings': InternalLinkTypeDefaultMessageAutoDeleteTimerSettings,
    'internalLinkTypeEditProfileSettings': InternalLinkTypeEditProfileSettings,
    'internalLinkTypeGame': InternalLinkTypeGame,
    'internalLinkTypeInstantView': InternalLinkTypeInstantView,
    'internalLinkTypeInvoice': InternalLinkTypeInvoice,
    'internalLinkTypeLanguagePack': InternalLinkTypeLanguagePack,
    'internalLinkTypeLanguageSettings': InternalLinkTypeLanguageSettings,
    'internalLinkTypeMessage': InternalLinkTypeMessage,
    'internalLinkTypeMessageDraft': InternalLinkTypeMessageDraft,
    'internalLinkTypePassportDataRequest': InternalLinkTypePassportDataRequest,
    'internalLinkTypePhoneNumberConfirmation': InternalLinkTypePhoneNumberConfirmation,
    'internalLinkTypePremiumFeatures': InternalLinkTypePremiumFeatures,
    'internalLinkTypePrivacyAndSecuritySettings': InternalLinkTypePrivacyAndSecuritySettings,
    'internalLinkTypeProxy': InternalLinkTypeProxy,
    'internalLinkTypePublicChat': InternalLinkTypePublicChat,
    'internalLinkTypeQrCodeAuthentication': InternalLinkTypeQrCodeAuthentication,
    'internalLinkTypeRestorePurchases': InternalLinkTypeRestorePurchases,
    'internalLinkTypeSettings': InternalLinkTypeSettings,
    'internalLinkTypeSideMenuBot': InternalLinkTypeSideMenuBot,
    'internalLinkTypeStickerSet': InternalLinkTypeStickerSet,
    'internalLinkTypeStory': InternalLinkTypeStory,
    'internalLinkTypeTheme': InternalLinkTypeTheme,
    'internalLinkTypeThemeSettings': InternalLinkTypeThemeSettings,
    'internalLinkTypeUnknownDeepLink': InternalLinkTypeUnknownDeepLink,
    'internalLinkTypeUnsupportedProxy': InternalLinkTypeUnsupportedProxy,
    'internalLinkTypeUserPhoneNumber': InternalLinkTypeUserPhoneNumber,
    'internalLinkTypeUserToken': InternalLinkTypeUserToken,
    'internalLinkTypeVideoChat': InternalLinkTypeVideoChat,
    'internalLinkTypeWebApp': InternalLinkTypeWebApp,
    'inviteLinkChatTypeBasicGroup': InviteLinkChatTypeBasicGroup,
    'inviteLinkChatTypeSupergroup': InviteLinkChatTypeSupergroup,
    'inviteLinkChatTypeChannel': InviteLinkChatTypeChannel,
    'labeledPricePart': LabeledPricePart,
    'JsonValue': JsonValue,
    'jsonObjectMember': JsonObjectMember,
    'jsonValueNull': JsonValueNull,
    'jsonValueBoolean': JsonValueBoolean,
    'jsonValueNumber': JsonValueNumber,
    'jsonValueString': JsonValueString,
    'jsonValueArray': JsonValueArray,
    'jsonValueObject': JsonValueObject,
    'KeyboardButtonType': KeyboardButtonType,
    'keyboardButton': KeyboardButton,
    'keyboardButtonTypeText': KeyboardButtonTypeText,
    'keyboardButtonTypeRequestPhoneNumber': KeyboardButtonTypeRequestPhoneNumber,
    'keyboardButtonTypeRequestLocation': KeyboardButtonTypeRequestLocation,
    'keyboardButtonTypeRequestPoll': KeyboardButtonTypeRequestPoll,
    'keyboardButtonTypeRequestUser': KeyboardButtonTypeRequestUser,
    'keyboardButtonTypeRequestChat': KeyboardButtonTypeRequestChat,
    'keyboardButtonTypeWebApp': KeyboardButtonTypeWebApp,
    'languagePackInfo': LanguagePackInfo,
    'LanguagePackStringValue': LanguagePackStringValue,
    'languagePackString': LanguagePackString,
    'languagePackStringValueOrdinary': LanguagePackStringValueOrdinary,
    'languagePackStringValuePluralized': LanguagePackStringValuePluralized,
    'languagePackStringValueDeleted': LanguagePackStringValueDeleted,
    'languagePackStrings': LanguagePackStrings,
    'localizationTargetInfo': LocalizationTargetInfo,
    'LogStream': LogStream,
    'logStreamDefault': LogStreamDefault,
    'logStreamFile': LogStreamFile,
    'logStreamEmpty': LogStreamEmpty,
    'logTags': LogTags,
    'logVerbosityLevel': LogVerbosityLevel,
    'LoginUrlInfo': LoginUrlInfo,
    'loginUrlInfoOpen': LoginUrlInfoOpen,
    'loginUrlInfoRequestConfirmation': LoginUrlInfoRequestConfirmation,
    'MaskPoint': MaskPoint,
    'maskPointForehead': MaskPointForehead,
    'maskPointEyes': MaskPointEyes,
    'maskPointMouth': MaskPointMouth,
    'maskPointChin': MaskPointChin,
    'MessageContent': MessageContent,
    'MessageReplyTo': MessageReplyTo,
    'MessageSchedulingState': MessageSchedulingState,
    'MessageSendingState': MessageSendingState,
    'messageForwardInfo': MessageForwardInfo,
    'messageInteractionInfo': MessageInteractionInfo,
    'unreadReaction': UnreadReaction,
    'messageAutoDeleteTime': MessageAutoDeleteTime,
    'messageCalendarDay': MessageCalendarDay,
    'messageCalendar': MessageCalendar,
    'MessageExtendedMedia': MessageExtendedMedia,
    'orderInfo': OrderInfo,
    'poll': Poll,
    'videoNote': VideoNote,
    'webPage': WebPage,
    'messageText': MessageText,
    'messageAnimation': MessageAnimation,
    'messageAudio': MessageAudio,
    'messageDocument': MessageDocument,
    'messagePhoto': MessagePhoto,
    'messageExpiredPhoto': MessageExpiredPhoto,
    'messageSticker': MessageSticker,
    'messageVideo': MessageVideo,
    'messageExpiredVideo': MessageExpiredVideo,
    'messageVideoNote': MessageVideoNote,
    'messageVoiceNote': MessageVoiceNote,
    'messageLocation': MessageLocation,
    'messageVenue': MessageVenue,
    'messageContact': MessageContact,
    'messageAnimatedEmoji': MessageAnimatedEmoji,
    'messageDice': MessageDice,
    'messageGame': MessageGame,
    'messagePoll': MessagePoll,
    'messageStory': MessageStory,
    'messageInvoice': MessageInvoice,
    'messageCall': MessageCall,
    'messageVideoChatScheduled': MessageVideoChatScheduled,
    'messageVideoChatStarted': MessageVideoChatStarted,
    'messageVideoChatEnded': MessageVideoChatEnded,
    'messageInviteVideoChatParticipants': MessageInviteVideoChatParticipants,
    'messageBasicGroupChatCreate': MessageBasicGroupChatCreate,
    'messageSupergroupChatCreate': MessageSupergroupChatCreate,
    'messageChatChangeTitle': MessageChatChangeTitle,
    'messageChatChangePhoto': MessageChatChangePhoto,
    'messageChatDeletePhoto': MessageChatDeletePhoto,
    'messageChatAddMembers': MessageChatAddMembers,
    'messageChatJoinByLink': MessageChatJoinByLink,
    'messageChatJoinByRequest': MessageChatJoinByRequest,
    'messageChatDeleteMember': MessageChatDeleteMember,
    'messageChatUpgradeTo': MessageChatUpgradeTo,
    'messageChatUpgradeFrom': MessageChatUpgradeFrom,
    'messagePinMessage': MessagePinMessage,
    'messageScreenshotTaken': MessageScreenshotTaken,
    'messageChatSetBackground': MessageChatSetBackground,
    'messageChatSetTheme': MessageChatSetTheme,
    'messageChatSetMessageAutoDeleteTime': MessageChatSetMessageAutoDeleteTime,
    'messageForumTopicCreated': MessageForumTopicCreated,
    'messageForumTopicEdited': MessageForumTopicEdited,
    'messageForumTopicIsClosedToggled': MessageForumTopicIsClosedToggled,
    'messageForumTopicIsHiddenToggled': MessageForumTopicIsHiddenToggled,
    'messageSuggestProfilePhoto': MessageSuggestProfilePhoto,
    'messageCustomServiceAction': MessageCustomServiceAction,
    'messageGameScore': MessageGameScore,
    'messagePaymentSuccessful': MessagePaymentSuccessful,
    'messagePaymentSuccessfulBot': MessagePaymentSuccessfulBot,
    'messageGiftedPremium': MessageGiftedPremium,
    'messageContactRegistered': MessageContactRegistered,
    'messageUserShared': MessageUserShared,
    'messageChatShared': MessageChatShared,
    'messageWebsiteConnected': MessageWebsiteConnected,
    'messageBotWriteAccessAllowed': MessageBotWriteAccessAllowed,
    'messageWebAppDataSent': MessageWebAppDataSent,
    'messageWebAppDataReceived': MessageWebAppDataReceived,
    'messagePassportDataSent': MessagePassportDataSent,
    'messagePassportDataReceived': MessagePassportDataReceived,
    'messageProximityAlertTriggered': MessageProximityAlertTriggered,
    'messageUnsupported': MessageUnsupported,
    'messageExtendedMediaPreview': MessageExtendedMediaPreview,
    'messageExtendedMediaPhoto': MessageExtendedMediaPhoto,
    'messageExtendedMediaVideo': MessageExtendedMediaVideo,
    'messageExtendedMediaUnsupported': MessageExtendedMediaUnsupported,
    'MessageFileType': MessageFileType,
    'messageFileTypePrivate': MessageFileTypePrivate,
    'messageFileTypeGroup': MessageFileTypeGroup,
    'messageFileTypeUnknown': MessageFileTypeUnknown,
    'MessageForwardOrigin': MessageForwardOrigin,
    'messageForwardOriginUser': MessageForwardOriginUser,
    'messageForwardOriginChat': MessageForwardOriginChat,
    'messageForwardOriginHiddenUser': MessageForwardOriginHiddenUser,
    'messageForwardOriginChannel': MessageForwardOriginChannel,
    'messageForwardOriginMessageImport': MessageForwardOriginMessageImport,
    'messageReaction': MessageReaction,
    'messageReplyInfo': MessageReplyInfo,
    'messageLink': MessageLink,
    'messageLinkInfo': MessageLinkInfo,
    'messagePosition': MessagePosition,
    'messagePositions': MessagePositions,
    'messageReplyToMessage': MessageReplyToMessage,
    'messageReplyToStory': MessageReplyToStory,
    'messageSchedulingStateSendAtDate': MessageSchedulingStateSendAtDate,
    'messageSchedulingStateSendWhenOnline': MessageSchedulingStateSendWhenOnline,
    'messageSelfDestructTypeTimer': MessageSelfDestructTypeTimer,
    'messageSelfDestructTypeImmediately': MessageSelfDestructTypeImmediately,
    'messageSendOptions': MessageSendOptions,
    'messageSenderUser': MessageSenderUser,
    'messageSenderChat': MessageSenderChat,
    'messageSenders': MessageSenders,
    'messageSendingStatePending': MessageSendingStatePending,
    'messageSendingStateFailed': MessageSendingStateFailed,
    'MessageSource': MessageSource,
    'messageSourceChatHistory': MessageSourceChatHistory,
    'messageSourceMessageThreadHistory': MessageSourceMessageThreadHistory,
    'messageSourceForumTopicHistory': MessageSourceForumTopicHistory,
    'messageSourceHistoryPreview': MessageSourceHistoryPreview,
    'messageSourceChatList': MessageSourceChatList,
    'messageSourceSearch': MessageSourceSearch,
    'messageSourceChatEventLog': MessageSourceChatEventLog,
    'messageSourceNotification': MessageSourceNotification,
    'messageSourceScreenshot': MessageSourceScreenshot,
    'messageSourceOther': MessageSourceOther,
    'MessageSponsorType': MessageSponsorType,
    'messageSponsor': MessageSponsor,
    'messageSponsorTypeBot': MessageSponsorTypeBot,
    'messageSponsorTypePublicChannel': MessageSponsorTypePublicChannel,
    'messageSponsorTypePrivateChannel': MessageSponsorTypePrivateChannel,
    'messageSponsorTypeWebsite': MessageSponsorTypeWebsite,
    'messageStatistics': MessageStatistics,
    'messageThreadInfo': MessageThreadInfo,
    'messageViewer': MessageViewer,
    'messageViewers': MessageViewers,
    'messages': Messages,
    'NetworkStatisticsEntry': NetworkStatisticsEntry,
    'networkStatistics': NetworkStatistics,
    'NetworkType': NetworkType,
    'networkStatisticsEntryFile': NetworkStatisticsEntryFile,
    'networkStatisticsEntryCall': NetworkStatisticsEntryCall,
    'networkTypeNone': NetworkTypeNone,
    'networkTypeMobile': NetworkTypeMobile,
    'networkTypeMobileRoaming': NetworkTypeMobileRoaming,
    'networkTypeWiFi': NetworkTypeWiFi,
    'networkTypeOther': NetworkTypeOther,
    'NotificationType': NotificationType,
    'notification': Notification,
    'NotificationGroupType': NotificationGroupType,
    'notificationGroup': NotificationGroup,
    'notificationGroupTypeMessages': NotificationGroupTypeMessages,
    'notificationGroupTypeMentions': NotificationGroupTypeMentions,
    'notificationGroupTypeSecretChat': NotificationGroupTypeSecretChat,
    'notificationGroupTypeCalls': NotificationGroupTypeCalls,
    'NotificationSettingsScope': NotificationSettingsScope,
    'notificationSettingsScopePrivateChats': NotificationSettingsScopePrivateChats,
    'notificationSettingsScopeGroupChats': NotificationSettingsScopeGroupChats,
    'notificationSettingsScopeChannelChats': NotificationSettingsScopeChannelChats,
    'notificationSound': NotificationSound,
    'notificationSounds': NotificationSounds,
    'PushMessageContent': PushMessageContent,
    'notificationTypeNewMessage': NotificationTypeNewMessage,
    'notificationTypeNewSecretChat': NotificationTypeNewSecretChat,
    'notificationTypeNewCall': NotificationTypeNewCall,
    'notificationTypeNewPushMessage': NotificationTypeNewPushMessage,
    'ok': Ok,
    'OptionValue': OptionValue,
    'optionValueBoolean': OptionValueBoolean,
    'optionValueEmpty': OptionValueEmpty,
    'optionValueInteger': OptionValueInteger,
    'optionValueString': OptionValueString,
    'PageBlock': PageBlock,
    'RichText': RichText,
    'pageBlockCaption': PageBlockCaption,
    'pageBlockListItem': PageBlockListItem,
    'pageBlockRelatedArticle': PageBlockRelatedArticle,
    'pageBlockTableCell': PageBlockTableCell,
    'pageBlockTitle': PageBlockTitle,
    'pageBlockSubtitle': PageBlockSubtitle,
    'pageBlockAuthorDate': PageBlockAuthorDate,
    'pageBlockHeader': PageBlockHeader,
    'pageBlockSubheader': PageBlockSubheader,
    'pageBlockKicker': PageBlockKicker,
    'pageBlockParagraph': PageBlockParagraph,
    'pageBlockPreformatted': PageBlockPreformatted,
    'pageBlockFooter': PageBlockFooter,
    'pageBlockDivider': PageBlockDivider,
    'pageBlockAnchor': PageBlockAnchor,
    'pageBlockList': PageBlockList,
    'pageBlockBlockQuote': PageBlockBlockQuote,
    'pageBlockPullQuote': PageBlockPullQuote,
    'pageBlockAnimation': PageBlockAnimation,
    'pageBlockAudio': PageBlockAudio,
    'pageBlockPhoto': PageBlockPhoto,
    'pageBlockVideo': PageBlockVideo,
    'pageBlockVoiceNote': PageBlockVoiceNote,
    'pageBlockCover': PageBlockCover,
    'pageBlockEmbedded': PageBlockEmbedded,
    'pageBlockEmbeddedPost': PageBlockEmbeddedPost,
    'pageBlockCollage': PageBlockCollage,
    'pageBlockSlideshow': PageBlockSlideshow,
    'pageBlockChatLink': PageBlockChatLink,
    'pageBlockTable': PageBlockTable,
    'pageBlockDetails': PageBlockDetails,
    'pageBlockRelatedArticles': PageBlockRelatedArticles,
    'pageBlockMap': PageBlockMap,
    'PageBlockHorizontalAlignment': PageBlockHorizontalAlignment,
    'pageBlockHorizontalAlignmentLeft': PageBlockHorizontalAlignmentLeft,
    'pageBlockHorizontalAlignmentCenter': PageBlockHorizontalAlignmentCenter,
    'pageBlockHorizontalAlignmentRight': PageBlockHorizontalAlignmentRight,
    'PageBlockVerticalAlignment': PageBlockVerticalAlignment,
    'pageBlockVerticalAlignmentTop': PageBlockVerticalAlignmentTop,
    'pageBlockVerticalAlignmentMiddle': PageBlockVerticalAlignmentMiddle,
    'pageBlockVerticalAlignmentBottom': PageBlockVerticalAlignmentBottom,
    'passportRequiredElement': PassportRequiredElement,
    'passportAuthorizationForm': PassportAuthorizationForm,
    'personalDocument': PersonalDocument,
    'PassportElement': PassportElement,
    'passportElementPersonalDetails': PassportElementPersonalDetails,
    'passportElementPassport': PassportElementPassport,
    'passportElementDriverLicense': PassportElementDriverLicense,
    'passportElementIdentityCard': PassportElementIdentityCard,
    'passportElementInternalPassport': PassportElementInternalPassport,
    'passportElementAddress': PassportElementAddress,
    'passportElementUtilityBill': PassportElementUtilityBill,
    'passportElementBankStatement': PassportElementBankStatement,
    'passportElementRentalAgreement': PassportElementRentalAgreement,
    'passportElementPassportRegistration': PassportElementPassportRegistration,
    'passportElementTemporaryRegistration': PassportElementTemporaryRegistration,
    'passportElementPhoneNumber': PassportElementPhoneNumber,
    'passportElementEmailAddress': PassportElementEmailAddress,
    'PassportElementErrorSource': PassportElementErrorSource,
    'passportElementError': PassportElementError,
    'passportElementErrorSourceUnspecified': PassportElementErrorSourceUnspecified,
    'passportElementErrorSourceDataField': PassportElementErrorSourceDataField,
    'passportElementErrorSourceFrontSide': PassportElementErrorSourceFrontSide,
    'passportElementErrorSourceReverseSide': PassportElementErrorSourceReverseSide,
    'passportElementErrorSourceSelfie': PassportElementErrorSourceSelfie,
    'passportElementErrorSourceTranslationFile': PassportElementErrorSourceTranslationFile,
    'passportElementErrorSourceTranslationFiles': PassportElementErrorSourceTranslationFiles,
    'passportElementErrorSourceFile': PassportElementErrorSourceFile,
    'passportElementErrorSourceFiles': PassportElementErrorSourceFiles,
    'passportElementTypePersonalDetails': PassportElementTypePersonalDetails,
    'passportElementTypePassport': PassportElementTypePassport,
    'passportElementTypeDriverLicense': PassportElementTypeDriverLicense,
    'passportElementTypeIdentityCard': PassportElementTypeIdentityCard,
    'passportElementTypeInternalPassport': PassportElementTypeInternalPassport,
    'passportElementTypeAddress': PassportElementTypeAddress,
    'passportElementTypeUtilityBill': PassportElementTypeUtilityBill,
    'passportElementTypeBankStatement': PassportElementTypeBankStatement,
    'passportElementTypeRentalAgreement': PassportElementTypeRentalAgreement,
    'passportElementTypePassportRegistration': PassportElementTypePassportRegistration,
    'passportElementTypeTemporaryRegistration': PassportElementTypeTemporaryRegistration,
    'passportElementTypePhoneNumber': PassportElementTypePhoneNumber,
    'passportElementTypeEmailAddress': PassportElementTypeEmailAddress,
    'passportElements': PassportElements,
    'passportElementsWithErrors': PassportElementsWithErrors,
    'passportSuitableElement': PassportSuitableElement,
    'passwordState': PasswordState,
    'PaymentProvider': PaymentProvider,
    'paymentOption': PaymentOption,
    'savedCredentials': SavedCredentials,
    'paymentForm': PaymentForm,
    'paymentProviderSmartGlocal': PaymentProviderSmartGlocal,
    'paymentProviderStripe': PaymentProviderStripe,
    'paymentProviderOther': PaymentProviderOther,
    'shippingOption': ShippingOption,
    'paymentReceipt': PaymentReceipt,
    'paymentResult': PaymentResult,
    'phoneNumberAuthenticationSettings': PhoneNumberAuthenticationSettings,
    'phoneNumberInfo': PhoneNumberInfo,
    'point': Point,
    'pollOption': PollOption,
    'pollTypeRegular': PollTypeRegular,
    'pollTypeQuiz': PollTypeQuiz,
    'PremiumFeature': PremiumFeature,
    'premiumFeatureIncreasedLimits': PremiumFeatureIncreasedLimits,
    'premiumFeatureIncreasedUploadFileSize': PremiumFeatureIncreasedUploadFileSize,
    'premiumFeatureImprovedDownloadSpeed': PremiumFeatureImprovedDownloadSpeed,
    'premiumFeatureVoiceRecognition': PremiumFeatureVoiceRecognition,
    'premiumFeatureDisabledAds': PremiumFeatureDisabledAds,
    'premiumFeatureUniqueReactions': PremiumFeatureUniqueReactions,
    'premiumFeatureUniqueStickers': PremiumFeatureUniqueStickers,
    'premiumFeatureCustomEmoji': PremiumFeatureCustomEmoji,
    'premiumFeatureAdvancedChatManagement': PremiumFeatureAdvancedChatManagement,
    'premiumFeatureProfileBadge': PremiumFeatureProfileBadge,
    'premiumFeatureEmojiStatus': PremiumFeatureEmojiStatus,
    'premiumFeatureAnimatedProfilePhoto': PremiumFeatureAnimatedProfilePhoto,
    'premiumFeatureForumTopicIcon': PremiumFeatureForumTopicIcon,
    'premiumFeatureAppIcons': PremiumFeatureAppIcons,
    'premiumFeatureRealTimeChatTranslation': PremiumFeatureRealTimeChatTranslation,
    'premiumFeatureUpgradedStories': PremiumFeatureUpgradedStories,
    'premiumFeaturePromotionAnimation': PremiumFeaturePromotionAnimation,
    'premiumLimit': PremiumLimit,
    'premiumFeatures': PremiumFeatures,
    'PremiumLimitType': PremiumLimitType,
    'premiumLimitTypeSupergroupCount': PremiumLimitTypeSupergroupCount,
    'premiumLimitTypePinnedChatCount': PremiumLimitTypePinnedChatCount,
    'premiumLimitTypeCreatedPublicChatCount': PremiumLimitTypeCreatedPublicChatCount,
    'premiumLimitTypeSavedAnimationCount': PremiumLimitTypeSavedAnimationCount,
    'premiumLimitTypeFavoriteStickerCount': PremiumLimitTypeFavoriteStickerCount,
    'premiumLimitTypeChatFilterCount': PremiumLimitTypeChatFilterCount,
    'premiumLimitTypeChatFilterChosenChatCount': PremiumLimitTypeChatFilterChosenChatCount,
    'premiumLimitTypePinnedArchivedChatCount': PremiumLimitTypePinnedArchivedChatCount,
    'premiumLimitTypeCaptionLength': PremiumLimitTypeCaptionLength,
    'premiumLimitTypeBioLength': PremiumLimitTypeBioLength,
    'premiumLimitTypeChatFilterInviteLinkCount': PremiumLimitTypeChatFilterInviteLinkCount,
    'premiumLimitTypeShareableChatFilterCount': PremiumLimitTypeShareableChatFilterCount,
    'premiumLimitTypeActiveStoryCount': PremiumLimitTypeActiveStoryCount,
    'premiumLimitTypeWeeklySentStoryCount': PremiumLimitTypeWeeklySentStoryCount,
    'premiumLimitTypeMonthlySentStoryCount': PremiumLimitTypeMonthlySentStoryCount,
    'premiumLimitTypeStoryCaptionLength': PremiumLimitTypeStoryCaptionLength,
    'premiumPaymentOption': PremiumPaymentOption,
    'PremiumStoryFeature': PremiumStoryFeature,
    'PremiumSource': PremiumSource,
    'premiumSourceLimitExceeded': PremiumSourceLimitExceeded,
    'premiumSourceFeature': PremiumSourceFeature,
    'premiumSourceStoryFeature': PremiumSourceStoryFeature,
    'premiumSourceLink': PremiumSourceLink,
    'premiumSourceSettings': PremiumSourceSettings,
    'premiumStatePaymentOption': PremiumStatePaymentOption,
    'premiumState': PremiumState,
    'premiumStoryFeaturePriorityOrder': PremiumStoryFeaturePriorityOrder,
    'premiumStoryFeatureStealthMode': PremiumStoryFeatureStealthMode,
    'premiumStoryFeaturePermanentViewsHistory': PremiumStoryFeaturePermanentViewsHistory,
    'premiumStoryFeatureCustomExpirationDuration': PremiumStoryFeatureCustomExpirationDuration,
    'premiumStoryFeatureSaveStories': PremiumStoryFeatureSaveStories,
    'premiumStoryFeatureLinksAndFormatting': PremiumStoryFeatureLinksAndFormatting,
    'profilePhoto': ProfilePhoto,
    'proxy': Proxy,
    'proxies': Proxies,
    'proxyTypeSocks5': ProxyTypeSocks5,
    'proxyTypeHttp': ProxyTypeHttp,
    'proxyTypeMtproto': ProxyTypeMtproto,
    'PublicChatType': PublicChatType,
    'publicChatTypeHasUsername': PublicChatTypeHasUsername,
    'publicChatTypeIsLocationBased': PublicChatTypeIsLocationBased,
    'pushMessageContentHidden': PushMessageContentHidden,
    'pushMessageContentAnimation': PushMessageContentAnimation,
    'pushMessageContentAudio': PushMessageContentAudio,
    'pushMessageContentContact': PushMessageContentContact,
    'pushMessageContentContactRegistered': PushMessageContentContactRegistered,
    'pushMessageContentDocument': PushMessageContentDocument,
    'pushMessageContentGame': PushMessageContentGame,
    'pushMessageContentGameScore': PushMessageContentGameScore,
    'pushMessageContentInvoice': PushMessageContentInvoice,
    'pushMessageContentLocation': PushMessageContentLocation,
    'pushMessageContentPhoto': PushMessageContentPhoto,
    'pushMessageContentPoll': PushMessageContentPoll,
    'pushMessageContentScreenshotTaken': PushMessageContentScreenshotTaken,
    'pushMessageContentSticker': PushMessageContentSticker,
    'pushMessageContentStory': PushMessageContentStory,
    'pushMessageContentText': PushMessageContentText,
    'pushMessageContentVideo': PushMessageContentVideo,
    'pushMessageContentVideoNote': PushMessageContentVideoNote,
    'pushMessageContentVoiceNote': PushMessageContentVoiceNote,
    'pushMessageContentBasicGroupChatCreate': PushMessageContentBasicGroupChatCreate,
    'pushMessageContentChatAddMembers': PushMessageContentChatAddMembers,
    'pushMessageContentChatChangePhoto': PushMessageContentChatChangePhoto,
    'pushMessageContentChatChangeTitle': PushMessageContentChatChangeTitle,
    'pushMessageContentChatSetBackground': PushMessageContentChatSetBackground,
    'pushMessageContentChatSetTheme': PushMessageContentChatSetTheme,
    'pushMessageContentChatDeleteMember': PushMessageContentChatDeleteMember,
    'pushMessageContentChatJoinByLink': PushMessageContentChatJoinByLink,
    'pushMessageContentChatJoinByRequest': PushMessageContentChatJoinByRequest,
    'pushMessageContentRecurringPayment': PushMessageContentRecurringPayment,
    'pushMessageContentSuggestProfilePhoto': PushMessageContentSuggestProfilePhoto,
    'pushMessageContentMessageForwards': PushMessageContentMessageForwards,
    'pushMessageContentMediaAlbum': PushMessageContentMediaAlbum,
    'pushReceiverId': PushReceiverId,
    'reactionTypeEmoji': ReactionTypeEmoji,
    'reactionTypeCustomEmoji': ReactionTypeCustomEmoji,
    'recommendedChatFilter': RecommendedChatFilter,
    'recommendedChatFilters': RecommendedChatFilters,
    'recoveryEmailAddress': RecoveryEmailAddress,
    'replyMarkupRemoveKeyboard': ReplyMarkupRemoveKeyboard,
    'replyMarkupForceReply': ReplyMarkupForceReply,
    'replyMarkupShowKeyboard': ReplyMarkupShowKeyboard,
    'replyMarkupInlineKeyboard': ReplyMarkupInlineKeyboard,
    'ReportReason': ReportReason,
    'reportReasonSpam': ReportReasonSpam,
    'reportReasonViolence': ReportReasonViolence,
    'reportReasonPornography': ReportReasonPornography,
    'reportReasonChildAbuse': ReportReasonChildAbuse,
    'reportReasonCopyright': ReportReasonCopyright,
    'reportReasonUnrelatedLocation': ReportReasonUnrelatedLocation,
    'reportReasonFake': ReportReasonFake,
    'reportReasonIllegalDrugs': ReportReasonIllegalDrugs,
    'reportReasonPersonalDetails': ReportReasonPersonalDetails,
    'reportReasonCustom': ReportReasonCustom,
    'ResetPasswordResult': ResetPasswordResult,
    'resetPasswordResultOk': ResetPasswordResultOk,
    'resetPasswordResultPending': ResetPasswordResultPending,
    'resetPasswordResultDeclined': ResetPasswordResultDeclined,
    'richTextPlain': RichTextPlain,
    'richTextBold': RichTextBold,
    'richTextItalic': RichTextItalic,
    'richTextUnderline': RichTextUnderline,
    'richTextStrikethrough': RichTextStrikethrough,
    'richTextFixed': RichTextFixed,
    'richTextUrl': RichTextUrl,
    'richTextEmailAddress': RichTextEmailAddress,
    'richTextSubscript': RichTextSubscript,
    'richTextSuperscript': RichTextSuperscript,
    'richTextMarked': RichTextMarked,
    'richTextPhoneNumber': RichTextPhoneNumber,
    'richTextIcon': RichTextIcon,
    'richTextReference': RichTextReference,
    'richTextAnchor': RichTextAnchor,
    'richTextAnchorLink': RichTextAnchorLink,
    'richTexts': RichTexts,
    'rtmpUrl': RtmpUrl,
    'scopeNotificationSettings': ScopeNotificationSettings,
    'SearchMessagesFilter': SearchMessagesFilter,
    'searchMessagesFilterEmpty': SearchMessagesFilterEmpty,
    'searchMessagesFilterAnimation': SearchMessagesFilterAnimation,
    'searchMessagesFilterAudio': SearchMessagesFilterAudio,
    'searchMessagesFilterDocument': SearchMessagesFilterDocument,
    'searchMessagesFilterPhoto': SearchMessagesFilterPhoto,
    'searchMessagesFilterVideo': SearchMessagesFilterVideo,
    'searchMessagesFilterVoiceNote': SearchMessagesFilterVoiceNote,
    'searchMessagesFilterPhotoAndVideo': SearchMessagesFilterPhotoAndVideo,
    'searchMessagesFilterUrl': SearchMessagesFilterUrl,
    'searchMessagesFilterChatPhoto': SearchMessagesFilterChatPhoto,
    'searchMessagesFilterVideoNote': SearchMessagesFilterVideoNote,
    'searchMessagesFilterVoiceAndVideoNote': SearchMessagesFilterVoiceAndVideoNote,
    'searchMessagesFilterMention': SearchMessagesFilterMention,
    'searchMessagesFilterUnreadMention': SearchMessagesFilterUnreadMention,
    'searchMessagesFilterUnreadReaction': SearchMessagesFilterUnreadReaction,
    'searchMessagesFilterFailedToSend': SearchMessagesFilterFailedToSend,
    'searchMessagesFilterPinned': SearchMessagesFilterPinned,
    'seconds': Seconds,
    'SecretChatState': SecretChatState,
    'secretChat': SecretChat,
    'secretChatStatePending': SecretChatStatePending,
    'secretChatStateReady': SecretChatStateReady,
    'secretChatStateClosed': SecretChatStateClosed,
    'sentWebAppMessage': SentWebAppMessage,
    'SessionType': SessionType,
    'session': Session,
    'sessionTypeAndroid': SessionTypeAndroid,
    'sessionTypeApple': SessionTypeApple,
    'sessionTypeBrave': SessionTypeBrave,
    'sessionTypeChrome': SessionTypeChrome,
    'sessionTypeEdge': SessionTypeEdge,
    'sessionTypeFirefox': SessionTypeFirefox,
    'sessionTypeIpad': SessionTypeIpad,
    'sessionTypeIphone': SessionTypeIphone,
    'sessionTypeLinux': SessionTypeLinux,
    'sessionTypeMac': SessionTypeMac,
    'sessionTypeOpera': SessionTypeOpera,
    'sessionTypeSafari': SessionTypeSafari,
    'sessionTypeUbuntu': SessionTypeUbuntu,
    'sessionTypeUnknown': SessionTypeUnknown,
    'sessionTypeVivaldi': SessionTypeVivaldi,
    'sessionTypeWindows': SessionTypeWindows,
    'sessionTypeXbox': SessionTypeXbox,
    'sessions': Sessions,
    'SpeechRecognitionResult': SpeechRecognitionResult,
    'speechRecognitionResultPending': SpeechRecognitionResultPending,
    'speechRecognitionResultText': SpeechRecognitionResultText,
    'speechRecognitionResultError': SpeechRecognitionResultError,
    'sponsoredMessage': SponsoredMessage,
    'sponsoredMessages': SponsoredMessages,
    'statisticalGraphData': StatisticalGraphData,
    'statisticalGraphAsync': StatisticalGraphAsync,
    'statisticalGraphError': StatisticalGraphError,
    'StickerFormat': StickerFormat,
    'StickerFullType': StickerFullType,
    'stickerFormatWebp': StickerFormatWebp,
    'stickerFormatTgs': StickerFormatTgs,
    'stickerFormatWebm': StickerFormatWebm,
    'stickerFullTypeRegular': StickerFullTypeRegular,
    'stickerFullTypeMask': StickerFullTypeMask,
    'stickerFullTypeCustomEmoji': StickerFullTypeCustomEmoji,
    'StickerType': StickerType,
    'stickerSet': StickerSet,
    'stickerSetInfo': StickerSetInfo,
    'stickerSets': StickerSets,
    'stickerTypeRegular': StickerTypeRegular,
    'stickerTypeMask': StickerTypeMask,
    'stickerTypeCustomEmoji': StickerTypeCustomEmoji,
    'stickers': Stickers,
    'storageStatisticsByChat': StorageStatisticsByChat,
    'storageStatistics': StorageStatistics,
    'storageStatisticsByFileType': StorageStatisticsByFileType,
    'storageStatisticsFast': StorageStatisticsFast,
    'StorePaymentPurpose': StorePaymentPurpose,
    'storePaymentPurposePremiumSubscription': StorePaymentPurposePremiumSubscription,
    'storePaymentPurposeGiftedPremium': StorePaymentPurposeGiftedPremium,
    'story': Story,
    'stories': Stories,
    'StoryContent': StoryContent,
    'StoryPrivacySettings': StoryPrivacySettings,
    'storyArea': StoryArea,
    'storyInteractionInfo': StoryInteractionInfo,
    'StoryAreaType': StoryAreaType,
    'storyAreaTypeLocation': StoryAreaTypeLocation,
    'storyAreaTypeVenue': StoryAreaTypeVenue,
    'storyVideo': StoryVideo,
    'storyContentPhoto': StoryContentPhoto,
    'storyContentVideo': StoryContentVideo,
    'storyContentUnsupported': StoryContentUnsupported,
    'storyListMain': StoryListMain,
    'storyListArchive': StoryListArchive,
    'storyPrivacySettingsEveryone': StoryPrivacySettingsEveryone,
    'storyPrivacySettingsContacts': StoryPrivacySettingsContacts,
    'storyPrivacySettingsCloseFriends': StoryPrivacySettingsCloseFriends,
    'storyPrivacySettingsSelectedUsers': StoryPrivacySettingsSelectedUsers,
    'storyViewer': StoryViewer,
    'storyViewers': StoryViewers,
    'SuggestedAction': SuggestedAction,
    'suggestedActionEnableArchiveAndMuteNewChats': SuggestedActionEnableArchiveAndMuteNewChats,
    'suggestedActionCheckPassword': SuggestedActionCheckPassword,
    'suggestedActionCheckPhoneNumber': SuggestedActionCheckPhoneNumber,
    'suggestedActionViewChecksHint': SuggestedActionViewChecksHint,
    'suggestedActionConvertToBroadcastGroup': SuggestedActionConvertToBroadcastGroup,
    'suggestedActionSetPassword': SuggestedActionSetPassword,
    'suggestedActionUpgradePremium': SuggestedActionUpgradePremium,
    'suggestedActionRestorePremium': SuggestedActionRestorePremium,
    'suggestedActionSubscribeToAnnualPremium': SuggestedActionSubscribeToAnnualPremium,
    'usernames': Usernames,
    'supergroup': Supergroup,
    'supergroupFullInfo': SupergroupFullInfo,
    'SupergroupMembersFilter': SupergroupMembersFilter,
    'supergroupMembersFilterRecent': SupergroupMembersFilterRecent,
    'supergroupMembersFilterContacts': SupergroupMembersFilterContacts,
    'supergroupMembersFilterAdministrators': SupergroupMembersFilterAdministrators,
    'supergroupMembersFilterSearch': SupergroupMembersFilterSearch,
    'supergroupMembersFilterRestricted': SupergroupMembersFilterRestricted,
    'supergroupMembersFilterBanned': SupergroupMembersFilterBanned,
    'supergroupMembersFilterMention': SupergroupMembersFilterMention,
    'supergroupMembersFilterBots': SupergroupMembersFilterBots,
    'TMeUrlType': TMeUrlType,
    'tMeUrl': TMeUrl,
    'tMeUrlTypeUser': TMeUrlTypeUser,
    'tMeUrlTypeSupergroup': TMeUrlTypeSupergroup,
    'tMeUrlTypeChatInvite': TMeUrlTypeChatInvite,
    'tMeUrlTypeStickerSet': TMeUrlTypeStickerSet,
    'tMeUrls': TMeUrls,
    'targetChatCurrent': TargetChatCurrent,
    'targetChatChosen': TargetChatChosen,
    'targetChatInternalLink': TargetChatInternalLink,
    'temporaryPasswordState': TemporaryPasswordState,
    'testBytes': TestBytes,
    'testInt': TestInt,
    'testString': TestString,
    'testVectorInt': TestVectorInt,
    'testVectorIntObject': TestVectorIntObject,
    'testVectorString': TestVectorString,
    'testVectorStringObject': TestVectorStringObject,
    'text': Text,
    'textEntities': TextEntities,
    'TextEntityType': TextEntityType,
    'textEntityTypeMention': TextEntityTypeMention,
    'textEntityTypeHashtag': TextEntityTypeHashtag,
    'textEntityTypeCashtag': TextEntityTypeCashtag,
    'textEntityTypeBotCommand': TextEntityTypeBotCommand,
    'textEntityTypeUrl': TextEntityTypeUrl,
    'textEntityTypeEmailAddress': TextEntityTypeEmailAddress,
    'textEntityTypePhoneNumber': TextEntityTypePhoneNumber,
    'textEntityTypeBankCardNumber': TextEntityTypeBankCardNumber,
    'textEntityTypeBold': TextEntityTypeBold,
    'textEntityTypeItalic': TextEntityTypeItalic,
    'textEntityTypeUnderline': TextEntityTypeUnderline,
    'textEntityTypeStrikethrough': TextEntityTypeStrikethrough,
    'textEntityTypeSpoiler': TextEntityTypeSpoiler,
    'textEntityTypeCode': TextEntityTypeCode,
    'textEntityTypePre': TextEntityTypePre,
    'textEntityTypePreCode': TextEntityTypePreCode,
    'textEntityTypeTextUrl': TextEntityTypeTextUrl,
    'textEntityTypeMentionName': TextEntityTypeMentionName,
    'textEntityTypeCustomEmoji': TextEntityTypeCustomEmoji,
    'textEntityTypeMediaTimestamp': TextEntityTypeMediaTimestamp,
    'TextParseMode': TextParseMode,
    'textParseModeMarkdown': TextParseModeMarkdown,
    'textParseModeHTML': TextParseModeHTML,
    'themeParameters': ThemeParameters,
    'ThumbnailFormat': ThumbnailFormat,
    'thumbnailFormatJpeg': ThumbnailFormatJpeg,
    'thumbnailFormatGif': ThumbnailFormatGif,
    'thumbnailFormatMpeg4': ThumbnailFormatMpeg4,
    'thumbnailFormatPng': ThumbnailFormatPng,
    'thumbnailFormatTgs': ThumbnailFormatTgs,
    'thumbnailFormatWebm': ThumbnailFormatWebm,
    'thumbnailFormatWebp': ThumbnailFormatWebp,
    'TopChatCategory': TopChatCategory,
    'topChatCategoryUsers': TopChatCategoryUsers,
    'topChatCategoryBots': TopChatCategoryBots,
    'topChatCategoryGroups': TopChatCategoryGroups,
    'topChatCategoryChannels': TopChatCategoryChannels,
    'topChatCategoryInlineBots': TopChatCategoryInlineBots,
    'topChatCategoryCalls': TopChatCategoryCalls,
    'topChatCategoryForwardChats': TopChatCategoryForwardChats,
    'trendingStickerSets': TrendingStickerSets,
    'unconfirmedSession': UnconfirmedSession,
    'UserPrivacySetting': UserPrivacySetting,
    'UserStatus': UserStatus,
    'user': User,
    'userFullInfo': UserFullInfo,
    'userPrivacySettingRules': UserPrivacySettingRules,
    'Update': Update,
    'updateAuthorizationState': UpdateAuthorizationState,
    'updateNewMessage': UpdateNewMessage,
    'updateMessageSendAcknowledged': UpdateMessageSendAcknowledged,
    'updateMessageSendSucceeded': UpdateMessageSendSucceeded,
    'updateMessageSendFailed': UpdateMessageSendFailed,
    'updateMessageContent': UpdateMessageContent,
    'updateMessageEdited': UpdateMessageEdited,
    'updateMessageIsPinned': UpdateMessageIsPinned,
    'updateMessageInteractionInfo': UpdateMessageInteractionInfo,
    'updateMessageContentOpened': UpdateMessageContentOpened,
    'updateMessageMentionRead': UpdateMessageMentionRead,
    'updateMessageUnreadReactions': UpdateMessageUnreadReactions,
    'updateMessageLiveLocationViewed': UpdateMessageLiveLocationViewed,
    'updateNewChat': UpdateNewChat,
    'updateChatTitle': UpdateChatTitle,
    'updateChatPhoto': UpdateChatPhoto,
    'updateChatPermissions': UpdateChatPermissions,
    'updateChatLastMessage': UpdateChatLastMessage,
    'updateChatPosition': UpdateChatPosition,
    'updateChatReadInbox': UpdateChatReadInbox,
    'updateChatReadOutbox': UpdateChatReadOutbox,
    'updateChatActionBar': UpdateChatActionBar,
    'updateChatAvailableReactions': UpdateChatAvailableReactions,
    'updateChatDraftMessage': UpdateChatDraftMessage,
    'updateChatMessageSender': UpdateChatMessageSender,
    'updateChatMessageAutoDeleteTime': UpdateChatMessageAutoDeleteTime,
    'updateChatNotificationSettings': UpdateChatNotificationSettings,
    'updateChatPendingJoinRequests': UpdateChatPendingJoinRequests,
    'updateChatReplyMarkup': UpdateChatReplyMarkup,
    'updateChatBackground': UpdateChatBackground,
    'updateChatTheme': UpdateChatTheme,
    'updateChatUnreadMentionCount': UpdateChatUnreadMentionCount,
    'updateChatUnreadReactionCount': UpdateChatUnreadReactionCount,
    'updateChatVideoChat': UpdateChatVideoChat,
    'updateChatDefaultDisableNotification': UpdateChatDefaultDisableNotification,
    'updateChatHasProtectedContent': UpdateChatHasProtectedContent,
    'updateChatIsTranslatable': UpdateChatIsTranslatable,
    'updateChatIsMarkedAsUnread': UpdateChatIsMarkedAsUnread,
    'updateChatBlockList': UpdateChatBlockList,
    'updateChatHasScheduledMessages': UpdateChatHasScheduledMessages,
    'updateChatFilters': UpdateChatFilters,
    'updateChatOnlineMemberCount': UpdateChatOnlineMemberCount,
    'updateForumTopicInfo': UpdateForumTopicInfo,
    'updateScopeNotificationSettings': UpdateScopeNotificationSettings,
    'updateNotification': UpdateNotification,
    'updateNotificationGroup': UpdateNotificationGroup,
    'updateActiveNotifications': UpdateActiveNotifications,
    'updateHavePendingNotifications': UpdateHavePendingNotifications,
    'updateDeleteMessages': UpdateDeleteMessages,
    'updateChatAction': UpdateChatAction,
    'updateUserStatus': UpdateUserStatus,
    'updateUser': UpdateUser,
    'updateBasicGroup': UpdateBasicGroup,
    'updateSupergroup': UpdateSupergroup,
    'updateSecretChat': UpdateSecretChat,
    'updateUserFullInfo': UpdateUserFullInfo,
    'updateBasicGroupFullInfo': UpdateBasicGroupFullInfo,
    'updateSupergroupFullInfo': UpdateSupergroupFullInfo,
    'updateServiceNotification': UpdateServiceNotification,
    'updateFile': UpdateFile,
    'updateFileGenerationStart': UpdateFileGenerationStart,
    'updateFileGenerationStop': UpdateFileGenerationStop,
    'updateFileDownloads': UpdateFileDownloads,
    'updateFileAddedToDownloads': UpdateFileAddedToDownloads,
    'updateFileDownload': UpdateFileDownload,
    'updateFileRemovedFromDownloads': UpdateFileRemovedFromDownloads,
    'updateCall': UpdateCall,
    'updateGroupCall': UpdateGroupCall,
    'updateGroupCallParticipant': UpdateGroupCallParticipant,
    'updateNewCallSignalingData': UpdateNewCallSignalingData,
    'updateUserPrivacySettingRules': UpdateUserPrivacySettingRules,
    'updateUnreadMessageCount': UpdateUnreadMessageCount,
    'updateUnreadChatCount': UpdateUnreadChatCount,
    'updateStory': UpdateStory,
    'updateStoryDeleted': UpdateStoryDeleted,
    'updateStorySendSucceeded': UpdateStorySendSucceeded,
    'updateStorySendFailed': UpdateStorySendFailed,
    'updateChatActiveStories': UpdateChatActiveStories,
    'updateStoryListChatCount': UpdateStoryListChatCount,
    'updateStoryStealthMode': UpdateStoryStealthMode,
    'updateOption': UpdateOption,
    'updateStickerSet': UpdateStickerSet,
    'updateInstalledStickerSets': UpdateInstalledStickerSets,
    'updateTrendingStickerSets': UpdateTrendingStickerSets,
    'updateRecentStickers': UpdateRecentStickers,
    'updateFavoriteStickers': UpdateFavoriteStickers,
    'updateSavedAnimations': UpdateSavedAnimations,
    'updateSavedNotificationSounds': UpdateSavedNotificationSounds,
    'updateSelectedBackground': UpdateSelectedBackground,
    'updateChatThemes': UpdateChatThemes,
    'updateLanguagePackStrings': UpdateLanguagePackStrings,
    'updateConnectionState': UpdateConnectionState,
    'updateTermsOfService': UpdateTermsOfService,
    'updateUsersNearby': UpdateUsersNearby,
    'updateUnconfirmedSession': UpdateUnconfirmedSession,
    'updateAttachmentMenuBots': UpdateAttachmentMenuBots,
    'updateWebAppMessageSent': UpdateWebAppMessageSent,
    'updateActiveEmojiReactions': UpdateActiveEmojiReactions,
    'updateDefaultReactionType': UpdateDefaultReactionType,
    'updateDiceEmojis': UpdateDiceEmojis,
    'updateAnimatedEmojiMessageClicked': UpdateAnimatedEmojiMessageClicked,
    'updateAnimationSearchParameters': UpdateAnimationSearchParameters,
    'updateSuggestedActions': UpdateSuggestedActions,
    'updateAddChatMembersPrivacyForbidden': UpdateAddChatMembersPrivacyForbidden,
    'updateAutosaveSettings': UpdateAutosaveSettings,
    'updateNewInlineQuery': UpdateNewInlineQuery,
    'updateNewChosenInlineResult': UpdateNewChosenInlineResult,
    'updateNewCallbackQuery': UpdateNewCallbackQuery,
    'updateNewInlineCallbackQuery': UpdateNewInlineCallbackQuery,
    'updateNewShippingQuery': UpdateNewShippingQuery,
    'updateNewPreCheckoutQuery': UpdateNewPreCheckoutQuery,
    'updateNewCustomEvent': UpdateNewCustomEvent,
    'updateNewCustomQuery': UpdateNewCustomQuery,
    'updatePoll': UpdatePoll,
    'updatePollAnswer': UpdatePollAnswer,
    'updateChatMember': UpdateChatMember,
    'updateNewChatJoinRequest': UpdateNewChatJoinRequest,
    'updates': Updates,
    'UserType': UserType,
    'userLink': UserLink,
    'userPrivacySettingShowStatus': UserPrivacySettingShowStatus,
    'userPrivacySettingShowProfilePhoto': UserPrivacySettingShowProfilePhoto,
    'userPrivacySettingShowLinkInForwardedMessages': UserPrivacySettingShowLinkInForwardedMessages,
    'userPrivacySettingShowPhoneNumber': UserPrivacySettingShowPhoneNumber,
    'userPrivacySettingShowBio': UserPrivacySettingShowBio,
    'userPrivacySettingAllowChatInvites': UserPrivacySettingAllowChatInvites,
    'userPrivacySettingAllowCalls': UserPrivacySettingAllowCalls,
    'userPrivacySettingAllowPeerToPeerCalls': UserPrivacySettingAllowPeerToPeerCalls,
    'userPrivacySettingAllowFindingByPhoneNumber': UserPrivacySettingAllowFindingByPhoneNumber,
    'userPrivacySettingAllowPrivateVoiceAndVideoNoteMessages': UserPrivacySettingAllowPrivateVoiceAndVideoNoteMessages,
    'UserPrivacySettingRule': UserPrivacySettingRule,
    'userPrivacySettingRuleAllowAll': UserPrivacySettingRuleAllowAll,
    'userPrivacySettingRuleAllowContacts': UserPrivacySettingRuleAllowContacts,
    'userPrivacySettingRuleAllowUsers': UserPrivacySettingRuleAllowUsers,
    'userPrivacySettingRuleAllowChatMembers': UserPrivacySettingRuleAllowChatMembers,
    'userPrivacySettingRuleRestrictAll': UserPrivacySettingRuleRestrictAll,
    'userPrivacySettingRuleRestrictContacts': UserPrivacySettingRuleRestrictContacts,
    'userPrivacySettingRuleRestrictUsers': UserPrivacySettingRuleRestrictUsers,
    'userPrivacySettingRuleRestrictChatMembers': UserPrivacySettingRuleRestrictChatMembers,
    'userStatusEmpty': UserStatusEmpty,
    'userStatusOnline': UserStatusOnline,
    'userStatusOffline': UserStatusOffline,
    'userStatusRecently': UserStatusRecently,
    'userStatusLastWeek': UserStatusLastWeek,
    'userStatusLastMonth': UserStatusLastMonth,
    'userSupportInfo': UserSupportInfo,
    'userTypeRegular': UserTypeRegular,
    'userTypeDeleted': UserTypeDeleted,
    'userTypeBot': UserTypeBot,
    'userTypeUnknown': UserTypeUnknown,
    'users': Users,
    'validatedOrderInfo': ValidatedOrderInfo,
    'vectorPathCommandLine': VectorPathCommandLine,
    'vectorPathCommandCubicBezierCurve': VectorPathCommandCubicBezierCurve,
    'webAppInfo': WebAppInfo,
    'webPageInstantView': WebPageInstantView,
}


def get_object(data):
    if isinstance(data, dict):
        return types[data['@type']](**data)
    if isinstance(data, list):
        return list(map(get_object, data))
    return data


def update_object(obj, data):
    obj.__init__(data)


def to_json(obj):
    if isinstance(obj, list):
        return list(map(to_json, obj))
    if hasattr(obj, '__dict__'):
        res = {'@type': obj.__class__.__name__[0].lower() + obj.__class__.__name__[1:]}
        for key, item in obj.__dict__.items():
            if not key.startswith('_'):
                res[key] = to_json(item)
        return res
    return obj


client = None


def acceptCall(call_id: int = None, protocol: CallProtocol = None, ):
    return get_object(client.func({
        '@type': 'acceptCall',
        'call_id': to_json(call_id),
        'protocol': to_json(protocol),
    }))


def acceptTermsOfService(terms_of_service_id: str = None, ):
    return get_object(client.func({
        '@type': 'acceptTermsOfService',
        'terms_of_service_id': to_json(terms_of_service_id),
    }))


def activateStoryStealthMode():
    return get_object(client.func({
        '@type': 'activateStoryStealthMode',
    }))


def addApplicationChangelog(previous_application_version: str = None, ):
    return get_object(client.func({
        '@type': 'addApplicationChangelog',
        'previous_application_version': to_json(previous_application_version),
    }))


def addChatFilterByInviteLink(invite_link: str = None, chat_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'addChatFilterByInviteLink',
        'invite_link': to_json(invite_link),
        'chat_ids': to_json(chat_ids),
    }))


def addChatMember(chat_id: int = None, user_id: int = None, forward_limit: int = None, ):
    return get_object(client.func({
        '@type': 'addChatMember',
        'chat_id': to_json(chat_id),
        'user_id': to_json(user_id),
        'forward_limit': to_json(forward_limit),
    }))


def addChatMembers(chat_id: int = None, user_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'addChatMembers',
        'chat_id': to_json(chat_id),
        'user_ids': to_json(user_ids),
    }))


def addChatToList(chat_id: int = None, chat_list: ChatList = None, ):
    return get_object(client.func({
        '@type': 'addChatToList',
        'chat_id': to_json(chat_id),
        'chat_list': to_json(chat_list),
    }))


def addContact(contact: Contact = None, share_phone_number: bool = None, ):
    return get_object(client.func({
        '@type': 'addContact',
        'contact': to_json(contact),
        'share_phone_number': to_json(share_phone_number),
    }))


def addCustomServerLanguagePack(language_pack_id: str = None, ):
    return get_object(client.func({
        '@type': 'addCustomServerLanguagePack',
        'language_pack_id': to_json(language_pack_id),
    }))


def addFavoriteSticker(sticker: InputFile = None, ):
    return get_object(client.func({
        '@type': 'addFavoriteSticker',
        'sticker': to_json(sticker),
    }))


def addFileToDownloads(file_id: int = None, chat_id: int = None, message_id: int = None, priority: int = None, ):
    return get_object(client.func({
        '@type': 'addFileToDownloads',
        'file_id': to_json(file_id),
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'priority': to_json(priority),
    }))


def addLocalMessage(chat_id: int = None, sender_id: MessageSender = None, reply_to: MessageReplyTo = None, disable_notification: bool = None, input_message_content: InputMessageContent = None, ):
    return get_object(client.func({
        '@type': 'addLocalMessage',
        'chat_id': to_json(chat_id),
        'sender_id': to_json(sender_id),
        'reply_to': to_json(reply_to),
        'disable_notification': to_json(disable_notification),
        'input_message_content': to_json(input_message_content),
    }))


def addLogMessage(verbosity_level: int = None, text: str = None, ):
    return get_object(client.func({
        '@type': 'addLogMessage',
        'verbosity_level': to_json(verbosity_level),
        'text': to_json(text),
    }))


def addMessageReaction(chat_id: int = None, message_id: int = None, reaction_type: ReactionType = None, is_big: bool = None, update_recent_reactions: bool = None, ):
    return get_object(client.func({
        '@type': 'addMessageReaction',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reaction_type': to_json(reaction_type),
        'is_big': to_json(is_big),
        'update_recent_reactions': to_json(update_recent_reactions),
    }))


def addNetworkStatistics(entry: NetworkStatisticsEntry = None, ):
    return get_object(client.func({
        '@type': 'addNetworkStatistics',
        'entry': to_json(entry),
    }))


def addProxy(server: str = None, port: int = None, enable: bool = None, type: ProxyType = None, ):
    return get_object(client.func({
        '@type': 'addProxy',
        'server': to_json(server),
        'port': to_json(port),
        'enable': to_json(enable),
        'type': to_json(type),
    }))


def addRecentSticker(is_attached: bool = None, sticker: InputFile = None, ):
    return get_object(client.func({
        '@type': 'addRecentSticker',
        'is_attached': to_json(is_attached),
        'sticker': to_json(sticker),
    }))


def addRecentlyFoundChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'addRecentlyFoundChat',
        'chat_id': to_json(chat_id),
    }))


def addSavedAnimation(animation: InputFile = None, ):
    return get_object(client.func({
        '@type': 'addSavedAnimation',
        'animation': to_json(animation),
    }))


def addSavedNotificationSound(sound: InputFile = None, ):
    return get_object(client.func({
        '@type': 'addSavedNotificationSound',
        'sound': to_json(sound),
    }))


def addStickerToSet(user_id: int = None, name: str = None, sticker: InputSticker = None, ):
    return get_object(client.func({
        '@type': 'addStickerToSet',
        'user_id': to_json(user_id),
        'name': to_json(name),
        'sticker': to_json(sticker),
    }))


def allowBotToSendMessages(bot_user_id: int = None, ):
    return get_object(client.func({
        '@type': 'allowBotToSendMessages',
        'bot_user_id': to_json(bot_user_id),
    }))


def answerCallbackQuery(callback_query_id: int = None, text: str = None, show_alert: bool = None, url: str = None, cache_time: int = None, ):
    return get_object(client.func({
        '@type': 'answerCallbackQuery',
        'callback_query_id': to_json(callback_query_id),
        'text': to_json(text),
        'show_alert': to_json(show_alert),
        'url': to_json(url),
        'cache_time': to_json(cache_time),
    }))


def answerCustomQuery(custom_query_id: int = None, data: str = None, ):
    return get_object(client.func({
        '@type': 'answerCustomQuery',
        'custom_query_id': to_json(custom_query_id),
        'data': to_json(data),
    }))


def answerInlineQuery(inline_query_id: int = None, is_personal: bool = None, button: InlineQueryResultsButton = None, results: list[InputInlineQueryResult] = None, cache_time: int = None, next_offset: str = None, ):
    return get_object(client.func({
        '@type': 'answerInlineQuery',
        'inline_query_id': to_json(inline_query_id),
        'is_personal': to_json(is_personal),
        'button': to_json(button),
        'results': to_json(results),
        'cache_time': to_json(cache_time),
        'next_offset': to_json(next_offset),
    }))


def answerPreCheckoutQuery(pre_checkout_query_id: int = None, error_message: str = None, ):
    return get_object(client.func({
        '@type': 'answerPreCheckoutQuery',
        'pre_checkout_query_id': to_json(pre_checkout_query_id),
        'error_message': to_json(error_message),
    }))


def answerShippingQuery(shipping_query_id: int = None, shipping_options: list[ShippingOption] = None, error_message: str = None, ):
    return get_object(client.func({
        '@type': 'answerShippingQuery',
        'shipping_query_id': to_json(shipping_query_id),
        'shipping_options': to_json(shipping_options),
        'error_message': to_json(error_message),
    }))


def answerWebAppQuery(web_app_query_id: str = None, result: InputInlineQueryResult = None, ):
    return get_object(client.func({
        '@type': 'answerWebAppQuery',
        'web_app_query_id': to_json(web_app_query_id),
        'result': to_json(result),
    }))


def assignAppStoreTransaction(receipt: bytes = None, purpose: StorePaymentPurpose = None, ):
    return get_object(client.func({
        '@type': 'assignAppStoreTransaction',
        'receipt': to_json(receipt),
        'purpose': to_json(purpose),
    }))


def assignGooglePlayTransaction(package_name: str = None, store_product_id: str = None, purchase_token: str = None, purpose: StorePaymentPurpose = None, ):
    return get_object(client.func({
        '@type': 'assignGooglePlayTransaction',
        'package_name': to_json(package_name),
        'store_product_id': to_json(store_product_id),
        'purchase_token': to_json(purchase_token),
        'purpose': to_json(purpose),
    }))


def banChatMember(chat_id: int = None, member_id: MessageSender = None, banned_until_date: int = None, revoke_messages: bool = None, ):
    return get_object(client.func({
        '@type': 'banChatMember',
        'chat_id': to_json(chat_id),
        'member_id': to_json(member_id),
        'banned_until_date': to_json(banned_until_date),
        'revoke_messages': to_json(revoke_messages),
    }))


def blockMessageSenderFromReplies(message_id: int = None, delete_message: bool = None, delete_all_messages: bool = None, report_spam: bool = None, ):
    return get_object(client.func({
        '@type': 'blockMessageSenderFromReplies',
        'message_id': to_json(message_id),
        'delete_message': to_json(delete_message),
        'delete_all_messages': to_json(delete_all_messages),
        'report_spam': to_json(report_spam),
    }))


def canBotSendMessages(bot_user_id: int = None, ):
    return get_object(client.func({
        '@type': 'canBotSendMessages',
        'bot_user_id': to_json(bot_user_id),
    }))


def canPurchasePremium(purpose: StorePaymentPurpose = None, ):
    return get_object(client.func({
        '@type': 'canPurchasePremium',
        'purpose': to_json(purpose),
    }))


def canSendStory():
    return get_object(client.func({
        '@type': 'canSendStory',
    }))


def canTransferOwnership():
    return get_object(client.func({
        '@type': 'canTransferOwnership',
    }))


def cancelDownloadFile(file_id: int = None, only_if_pending: bool = None, ):
    return get_object(client.func({
        '@type': 'cancelDownloadFile',
        'file_id': to_json(file_id),
        'only_if_pending': to_json(only_if_pending),
    }))


def cancelPasswordReset():
    return get_object(client.func({
        '@type': 'cancelPasswordReset',
    }))


def cancelPreliminaryUploadFile(file_id: int = None, ):
    return get_object(client.func({
        '@type': 'cancelPreliminaryUploadFile',
        'file_id': to_json(file_id),
    }))


def changeImportedContacts(contacts: list[Contact] = None, ):
    return get_object(client.func({
        '@type': 'changeImportedContacts',
        'contacts': to_json(contacts),
    }))


def changePhoneNumber(phone_number: str = None, settings: PhoneNumberAuthenticationSettings = None, ):
    return get_object(client.func({
        '@type': 'changePhoneNumber',
        'phone_number': to_json(phone_number),
        'settings': to_json(settings),
    }))


def changeStickerSet(set_id: int = None, is_installed: bool = None, is_archived: bool = None, ):
    return get_object(client.func({
        '@type': 'changeStickerSet',
        'set_id': to_json(set_id),
        'is_installed': to_json(is_installed),
        'is_archived': to_json(is_archived),
    }))


def checkAuthenticationBotToken(token: str = None, ):
    return get_object(client.func({
        '@type': 'checkAuthenticationBotToken',
        'token': to_json(token),
    }))


def checkAuthenticationCode(code: str = None, ):
    return get_object(client.func({
        '@type': 'checkAuthenticationCode',
        'code': to_json(code),
    }))


def checkAuthenticationEmailCode(code: EmailAddressAuthentication = None, ):
    return get_object(client.func({
        '@type': 'checkAuthenticationEmailCode',
        'code': to_json(code),
    }))


def checkAuthenticationPassword(password: str = None, ):
    return get_object(client.func({
        '@type': 'checkAuthenticationPassword',
        'password': to_json(password),
    }))


def checkAuthenticationPasswordRecoveryCode(recovery_code: str = None, ):
    return get_object(client.func({
        '@type': 'checkAuthenticationPasswordRecoveryCode',
        'recovery_code': to_json(recovery_code),
    }))


def checkChangePhoneNumberCode(code: str = None, ):
    return get_object(client.func({
        '@type': 'checkChangePhoneNumberCode',
        'code': to_json(code),
    }))


def checkChatFilterInviteLink(invite_link: str = None, ):
    return get_object(client.func({
        '@type': 'checkChatFilterInviteLink',
        'invite_link': to_json(invite_link),
    }))


def checkChatInviteLink(invite_link: str = None, ):
    return get_object(client.func({
        '@type': 'checkChatInviteLink',
        'invite_link': to_json(invite_link),
    }))


def checkChatUsername(chat_id: int = None, username: str = None, ):
    return get_object(client.func({
        '@type': 'checkChatUsername',
        'chat_id': to_json(chat_id),
        'username': to_json(username),
    }))


def checkCreatedPublicChatsLimit(type: PublicChatType = None, ):
    return get_object(client.func({
        '@type': 'checkCreatedPublicChatsLimit',
        'type': to_json(type),
    }))


def checkEmailAddressVerificationCode(code: str = None, ):
    return get_object(client.func({
        '@type': 'checkEmailAddressVerificationCode',
        'code': to_json(code),
    }))


def checkLoginEmailAddressCode(code: EmailAddressAuthentication = None, ):
    return get_object(client.func({
        '@type': 'checkLoginEmailAddressCode',
        'code': to_json(code),
    }))


def checkPasswordRecoveryCode(recovery_code: str = None, ):
    return get_object(client.func({
        '@type': 'checkPasswordRecoveryCode',
        'recovery_code': to_json(recovery_code),
    }))


def checkPhoneNumberConfirmationCode(code: str = None, ):
    return get_object(client.func({
        '@type': 'checkPhoneNumberConfirmationCode',
        'code': to_json(code),
    }))


def checkPhoneNumberVerificationCode(code: str = None, ):
    return get_object(client.func({
        '@type': 'checkPhoneNumberVerificationCode',
        'code': to_json(code),
    }))


def checkRecoveryEmailAddressCode(code: str = None, ):
    return get_object(client.func({
        '@type': 'checkRecoveryEmailAddressCode',
        'code': to_json(code),
    }))


def checkStickerSetName(name: str = None, ):
    return get_object(client.func({
        '@type': 'checkStickerSetName',
        'name': to_json(name),
    }))


def cleanFileName(file_name: str = None, ):
    return get_object(client.func({
        '@type': 'cleanFileName',
        'file_name': to_json(file_name),
    }))


def clearAllDraftMessages(exclude_secret_chats: bool = None, ):
    return get_object(client.func({
        '@type': 'clearAllDraftMessages',
        'exclude_secret_chats': to_json(exclude_secret_chats),
    }))


def clearAutosaveSettingsExceptions():
    return get_object(client.func({
        '@type': 'clearAutosaveSettingsExceptions',
    }))


def clearImportedContacts():
    return get_object(client.func({
        '@type': 'clearImportedContacts',
    }))


def clearRecentEmojiStatuses():
    return get_object(client.func({
        '@type': 'clearRecentEmojiStatuses',
    }))


def clearRecentReactions():
    return get_object(client.func({
        '@type': 'clearRecentReactions',
    }))


def clearRecentStickers(is_attached: bool = None, ):
    return get_object(client.func({
        '@type': 'clearRecentStickers',
        'is_attached': to_json(is_attached),
    }))


def clearRecentlyFoundChats():
    return get_object(client.func({
        '@type': 'clearRecentlyFoundChats',
    }))


def clickAnimatedEmojiMessage(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'clickAnimatedEmojiMessage',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def clickChatSponsoredMessage(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'clickChatSponsoredMessage',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def clickPremiumSubscriptionButton():
    return get_object(client.func({
        '@type': 'clickPremiumSubscriptionButton',
    }))


def close():
    return get_object(client.func({
        '@type': 'close',
    }))


def closeChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'closeChat',
        'chat_id': to_json(chat_id),
    }))


def closeSecretChat(secret_chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'closeSecretChat',
        'secret_chat_id': to_json(secret_chat_id),
    }))


def closeStory(story_sender_chat_id: int = None, story_id: int = None, ):
    return get_object(client.func({
        '@type': 'closeStory',
        'story_sender_chat_id': to_json(story_sender_chat_id),
        'story_id': to_json(story_id),
    }))


def closeWebApp(web_app_launch_id: int = None, ):
    return get_object(client.func({
        '@type': 'closeWebApp',
        'web_app_launch_id': to_json(web_app_launch_id),
    }))


def confirmQrCodeAuthentication(link: str = None, ):
    return get_object(client.func({
        '@type': 'confirmQrCodeAuthentication',
        'link': to_json(link),
    }))


def confirmSession(session_id: int = None, ):
    return get_object(client.func({
        '@type': 'confirmSession',
        'session_id': to_json(session_id),
    }))


def createBasicGroupChat(basic_group_id: int = None, force: bool = None, ):
    return get_object(client.func({
        '@type': 'createBasicGroupChat',
        'basic_group_id': to_json(basic_group_id),
        'force': to_json(force),
    }))


def createCall(user_id: int = None, protocol: CallProtocol = None, is_video: bool = None, ):
    return get_object(client.func({
        '@type': 'createCall',
        'user_id': to_json(user_id),
        'protocol': to_json(protocol),
        'is_video': to_json(is_video),
    }))


def createChatFilter(filter: ChatFilter = None, ):
    return get_object(client.func({
        '@type': 'createChatFilter',
        'filter': to_json(filter),
    }))


def createChatFilterInviteLink(chat_filter_id: int = None, name: str = None, chat_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'createChatFilterInviteLink',
        'chat_filter_id': to_json(chat_filter_id),
        'name': to_json(name),
        'chat_ids': to_json(chat_ids),
    }))


def createChatInviteLink(chat_id: int = None, name: str = None, expiration_date: int = None, member_limit: int = None, creates_join_request: bool = None, ):
    return get_object(client.func({
        '@type': 'createChatInviteLink',
        'chat_id': to_json(chat_id),
        'name': to_json(name),
        'expiration_date': to_json(expiration_date),
        'member_limit': to_json(member_limit),
        'creates_join_request': to_json(creates_join_request),
    }))


def createForumTopic(chat_id: int = None, name: str = None, icon: ForumTopicIcon = None, ):
    return get_object(client.func({
        '@type': 'createForumTopic',
        'chat_id': to_json(chat_id),
        'name': to_json(name),
        'icon': to_json(icon),
    }))


def createInvoiceLink(invoice: InputMessageContent = None, ):
    return get_object(client.func({
        '@type': 'createInvoiceLink',
        'invoice': to_json(invoice),
    }))


def createNewBasicGroupChat(user_ids: list[int] = None, title: str = None, message_auto_delete_time: int = None, ):
    return get_object(client.func({
        '@type': 'createNewBasicGroupChat',
        'user_ids': to_json(user_ids),
        'title': to_json(title),
        'message_auto_delete_time': to_json(message_auto_delete_time),
    }))


def createNewSecretChat(user_id: int = None, ):
    return get_object(client.func({
        '@type': 'createNewSecretChat',
        'user_id': to_json(user_id),
    }))


def createNewStickerSet(user_id: int = None, title: str = None, name: str = None, sticker_format: StickerFormat = None, sticker_type: StickerType = None, needs_repainting: bool = None, stickers: list[InputSticker] = None, source: str = None, ):
    return get_object(client.func({
        '@type': 'createNewStickerSet',
        'user_id': to_json(user_id),
        'title': to_json(title),
        'name': to_json(name),
        'sticker_format': to_json(sticker_format),
        'sticker_type': to_json(sticker_type),
        'needs_repainting': to_json(needs_repainting),
        'stickers': to_json(stickers),
        'source': to_json(source),
    }))


def createNewSupergroupChat(title: str = None, is_forum: bool = None, is_channel: bool = None, description: str = None, location: ChatLocation = None, message_auto_delete_time: int = None, for_import: bool = None, ):
    return get_object(client.func({
        '@type': 'createNewSupergroupChat',
        'title': to_json(title),
        'is_forum': to_json(is_forum),
        'is_channel': to_json(is_channel),
        'description': to_json(description),
        'location': to_json(location),
        'message_auto_delete_time': to_json(message_auto_delete_time),
        'for_import': to_json(for_import),
    }))


def createPrivateChat(user_id: int = None, force: bool = None, ):
    return get_object(client.func({
        '@type': 'createPrivateChat',
        'user_id': to_json(user_id),
        'force': to_json(force),
    }))


def createSecretChat(secret_chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'createSecretChat',
        'secret_chat_id': to_json(secret_chat_id),
    }))


def createSupergroupChat(supergroup_id: int = None, force: bool = None, ):
    return get_object(client.func({
        '@type': 'createSupergroupChat',
        'supergroup_id': to_json(supergroup_id),
        'force': to_json(force),
    }))


def createTemporaryPassword(password: str = None, valid_for: int = None, ):
    return get_object(client.func({
        '@type': 'createTemporaryPassword',
        'password': to_json(password),
        'valid_for': to_json(valid_for),
    }))


def createVideoChat(chat_id: int = None, title: str = None, start_date: int = None, is_rtmp_stream: bool = None, ):
    return get_object(client.func({
        '@type': 'createVideoChat',
        'chat_id': to_json(chat_id),
        'title': to_json(title),
        'start_date': to_json(start_date),
        'is_rtmp_stream': to_json(is_rtmp_stream),
    }))


def deleteAccount(reason: str = None, password: str = None, ):
    return get_object(client.func({
        '@type': 'deleteAccount',
        'reason': to_json(reason),
        'password': to_json(password),
    }))


def deleteAllCallMessages(revoke: bool = None, ):
    return get_object(client.func({
        '@type': 'deleteAllCallMessages',
        'revoke': to_json(revoke),
    }))


def deleteAllRevokedChatInviteLinks(chat_id: int = None, creator_user_id: int = None, ):
    return get_object(client.func({
        '@type': 'deleteAllRevokedChatInviteLinks',
        'chat_id': to_json(chat_id),
        'creator_user_id': to_json(creator_user_id),
    }))


def deleteChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'deleteChat',
        'chat_id': to_json(chat_id),
    }))


def deleteChatFilter(chat_filter_id: int = None, leave_chat_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'deleteChatFilter',
        'chat_filter_id': to_json(chat_filter_id),
        'leave_chat_ids': to_json(leave_chat_ids),
    }))


def deleteChatFilterInviteLink(chat_filter_id: int = None, invite_link: str = None, ):
    return get_object(client.func({
        '@type': 'deleteChatFilterInviteLink',
        'chat_filter_id': to_json(chat_filter_id),
        'invite_link': to_json(invite_link),
    }))


def deleteChatHistory(chat_id: int = None, remove_from_chat_list: bool = None, revoke: bool = None, ):
    return get_object(client.func({
        '@type': 'deleteChatHistory',
        'chat_id': to_json(chat_id),
        'remove_from_chat_list': to_json(remove_from_chat_list),
        'revoke': to_json(revoke),
    }))


def deleteChatMessagesByDate(chat_id: int = None, min_date: int = None, max_date: int = None, revoke: bool = None, ):
    return get_object(client.func({
        '@type': 'deleteChatMessagesByDate',
        'chat_id': to_json(chat_id),
        'min_date': to_json(min_date),
        'max_date': to_json(max_date),
        'revoke': to_json(revoke),
    }))


def deleteChatMessagesBySender(chat_id: int = None, sender_id: MessageSender = None, ):
    return get_object(client.func({
        '@type': 'deleteChatMessagesBySender',
        'chat_id': to_json(chat_id),
        'sender_id': to_json(sender_id),
    }))


def deleteChatReplyMarkup(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'deleteChatReplyMarkup',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def deleteCommands(scope: BotCommandScope = None, language_code: str = None, ):
    return get_object(client.func({
        '@type': 'deleteCommands',
        'scope': to_json(scope),
        'language_code': to_json(language_code),
    }))


def deleteFile(file_id: int = None, ):
    return get_object(client.func({
        '@type': 'deleteFile',
        'file_id': to_json(file_id),
    }))


def deleteForumTopic(chat_id: int = None, message_thread_id: int = None, ):
    return get_object(client.func({
        '@type': 'deleteForumTopic',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
    }))


def deleteLanguagePack(language_pack_id: str = None, ):
    return get_object(client.func({
        '@type': 'deleteLanguagePack',
        'language_pack_id': to_json(language_pack_id),
    }))


def deleteMessages(chat_id: int = None, message_ids: list[int] = None, revoke: bool = None, ):
    return get_object(client.func({
        '@type': 'deleteMessages',
        'chat_id': to_json(chat_id),
        'message_ids': to_json(message_ids),
        'revoke': to_json(revoke),
    }))


def deletePassportElement(type: PassportElementType = None, ):
    return get_object(client.func({
        '@type': 'deletePassportElement',
        'type': to_json(type),
    }))


def deleteProfilePhoto(profile_photo_id: int = None, ):
    return get_object(client.func({
        '@type': 'deleteProfilePhoto',
        'profile_photo_id': to_json(profile_photo_id),
    }))


def deleteRevokedChatInviteLink(chat_id: int = None, invite_link: str = None, ):
    return get_object(client.func({
        '@type': 'deleteRevokedChatInviteLink',
        'chat_id': to_json(chat_id),
        'invite_link': to_json(invite_link),
    }))


def deleteSavedCredentials():
    return get_object(client.func({
        '@type': 'deleteSavedCredentials',
    }))


def deleteSavedOrderInfo():
    return get_object(client.func({
        '@type': 'deleteSavedOrderInfo',
    }))


def deleteStickerSet(name: str = None, ):
    return get_object(client.func({
        '@type': 'deleteStickerSet',
        'name': to_json(name),
    }))


def deleteStory(story_id: int = None, ):
    return get_object(client.func({
        '@type': 'deleteStory',
        'story_id': to_json(story_id),
    }))


def destroy():
    return get_object(client.func({
        '@type': 'destroy',
    }))


def disableAllSupergroupUsernames(supergroup_id: int = None, ):
    return get_object(client.func({
        '@type': 'disableAllSupergroupUsernames',
        'supergroup_id': to_json(supergroup_id),
    }))


def disableProxy():
    return get_object(client.func({
        '@type': 'disableProxy',
    }))


def discardCall(call_id: int = None, is_disconnected: bool = None, duration: int = None, is_video: bool = None, connection_id: int = None, ):
    return get_object(client.func({
        '@type': 'discardCall',
        'call_id': to_json(call_id),
        'is_disconnected': to_json(is_disconnected),
        'duration': to_json(duration),
        'is_video': to_json(is_video),
        'connection_id': to_json(connection_id),
    }))


def disconnectAllWebsites():
    return get_object(client.func({
        '@type': 'disconnectAllWebsites',
    }))


def disconnectWebsite(website_id: int = None, ):
    return get_object(client.func({
        '@type': 'disconnectWebsite',
        'website_id': to_json(website_id),
    }))


def downloadFile(file_id: int = None, priority: int = None, offset: int = None, limit: int = None, synchronous: bool = None, ):
    return get_object(client.func({
        '@type': 'downloadFile',
        'file_id': to_json(file_id),
        'priority': to_json(priority),
        'offset': to_json(offset),
        'limit': to_json(limit),
        'synchronous': to_json(synchronous),
    }))


def editChatFilter(chat_filter_id: int = None, filter: ChatFilter = None, ):
    return get_object(client.func({
        '@type': 'editChatFilter',
        'chat_filter_id': to_json(chat_filter_id),
        'filter': to_json(filter),
    }))


def editChatFilterInviteLink(chat_filter_id: int = None, invite_link: str = None, name: str = None, chat_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'editChatFilterInviteLink',
        'chat_filter_id': to_json(chat_filter_id),
        'invite_link': to_json(invite_link),
        'name': to_json(name),
        'chat_ids': to_json(chat_ids),
    }))


def editChatInviteLink(chat_id: int = None, invite_link: str = None, name: str = None, expiration_date: int = None, member_limit: int = None, creates_join_request: bool = None, ):
    return get_object(client.func({
        '@type': 'editChatInviteLink',
        'chat_id': to_json(chat_id),
        'invite_link': to_json(invite_link),
        'name': to_json(name),
        'expiration_date': to_json(expiration_date),
        'member_limit': to_json(member_limit),
        'creates_join_request': to_json(creates_join_request),
    }))


def editCustomLanguagePackInfo(info: LanguagePackInfo = None, ):
    return get_object(client.func({
        '@type': 'editCustomLanguagePackInfo',
        'info': to_json(info),
    }))


def editForumTopic(chat_id: int = None, message_thread_id: int = None, name: str = None, edit_icon_custom_emoji: bool = None, icon_custom_emoji_id: int = None, ):
    return get_object(client.func({
        '@type': 'editForumTopic',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'name': to_json(name),
        'edit_icon_custom_emoji': to_json(edit_icon_custom_emoji),
        'icon_custom_emoji_id': to_json(icon_custom_emoji_id),
    }))


def editInlineMessageCaption(inline_message_id: str = None, reply_markup: ReplyMarkup = None, caption: FormattedText = None, ):
    return get_object(client.func({
        '@type': 'editInlineMessageCaption',
        'inline_message_id': to_json(inline_message_id),
        'reply_markup': to_json(reply_markup),
        'caption': to_json(caption),
    }))


def editInlineMessageLiveLocation(inline_message_id: str = None, reply_markup: ReplyMarkup = None, location: Location = None, heading: int = None, proximity_alert_radius: int = None, ):
    return get_object(client.func({
        '@type': 'editInlineMessageLiveLocation',
        'inline_message_id': to_json(inline_message_id),
        'reply_markup': to_json(reply_markup),
        'location': to_json(location),
        'heading': to_json(heading),
        'proximity_alert_radius': to_json(proximity_alert_radius),
    }))


def editInlineMessageMedia(inline_message_id: str = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None, ):
    return get_object(client.func({
        '@type': 'editInlineMessageMedia',
        'inline_message_id': to_json(inline_message_id),
        'reply_markup': to_json(reply_markup),
        'input_message_content': to_json(input_message_content),
    }))


def editInlineMessageReplyMarkup(inline_message_id: str = None, reply_markup: ReplyMarkup = None, ):
    return get_object(client.func({
        '@type': 'editInlineMessageReplyMarkup',
        'inline_message_id': to_json(inline_message_id),
        'reply_markup': to_json(reply_markup),
    }))


def editInlineMessageText(inline_message_id: str = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None, ):
    return get_object(client.func({
        '@type': 'editInlineMessageText',
        'inline_message_id': to_json(inline_message_id),
        'reply_markup': to_json(reply_markup),
        'input_message_content': to_json(input_message_content),
    }))


def editMessageCaption(chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, caption: FormattedText = None, ):
    return get_object(client.func({
        '@type': 'editMessageCaption',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reply_markup': to_json(reply_markup),
        'caption': to_json(caption),
    }))


def editMessageLiveLocation(chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, location: Location = None, heading: int = None, proximity_alert_radius: int = None, ):
    return get_object(client.func({
        '@type': 'editMessageLiveLocation',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reply_markup': to_json(reply_markup),
        'location': to_json(location),
        'heading': to_json(heading),
        'proximity_alert_radius': to_json(proximity_alert_radius),
    }))


def editMessageMedia(chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None, ):
    return get_object(client.func({
        '@type': 'editMessageMedia',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reply_markup': to_json(reply_markup),
        'input_message_content': to_json(input_message_content),
    }))


def editMessageReplyMarkup(chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, ):
    return get_object(client.func({
        '@type': 'editMessageReplyMarkup',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reply_markup': to_json(reply_markup),
    }))


def editMessageSchedulingState(chat_id: int = None, message_id: int = None, scheduling_state: MessageSchedulingState = None, ):
    return get_object(client.func({
        '@type': 'editMessageSchedulingState',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'scheduling_state': to_json(scheduling_state),
    }))


def editMessageText(chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None, ):
    return get_object(client.func({
        '@type': 'editMessageText',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reply_markup': to_json(reply_markup),
        'input_message_content': to_json(input_message_content),
    }))


def editProxy(proxy_id: int = None, server: str = None, port: int = None, enable: bool = None, type: ProxyType = None, ):
    return get_object(client.func({
        '@type': 'editProxy',
        'proxy_id': to_json(proxy_id),
        'server': to_json(server),
        'port': to_json(port),
        'enable': to_json(enable),
        'type': to_json(type),
    }))


def editStory(story_id: int = None, content: InputStoryContent = None, areas: InputStoryAreas = None, caption: FormattedText = None, ):
    return get_object(client.func({
        '@type': 'editStory',
        'story_id': to_json(story_id),
        'content': to_json(content),
        'areas': to_json(areas),
        'caption': to_json(caption),
    }))


def enableProxy(proxy_id: int = None, ):
    return get_object(client.func({
        '@type': 'enableProxy',
        'proxy_id': to_json(proxy_id),
    }))


def endGroupCall(group_call_id: int = None, ):
    return get_object(client.func({
        '@type': 'endGroupCall',
        'group_call_id': to_json(group_call_id),
    }))


def endGroupCallRecording(group_call_id: int = None, ):
    return get_object(client.func({
        '@type': 'endGroupCallRecording',
        'group_call_id': to_json(group_call_id),
    }))


def endGroupCallScreenSharing(group_call_id: int = None, ):
    return get_object(client.func({
        '@type': 'endGroupCallScreenSharing',
        'group_call_id': to_json(group_call_id),
    }))


def finishFileGeneration(generation_id: int = None, error: Error = None, ):
    return get_object(client.func({
        '@type': 'finishFileGeneration',
        'generation_id': to_json(generation_id),
        'error': to_json(error),
    }))


def forwardMessages(chat_id: int = None, message_thread_id: int = None, from_chat_id: int = None, message_ids: list[int] = None, options: MessageSendOptions = None, send_copy: bool = None, remove_caption: bool = None, only_preview: bool = None, ):
    return get_object(client.func({
        '@type': 'forwardMessages',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'from_chat_id': to_json(from_chat_id),
        'message_ids': to_json(message_ids),
        'options': to_json(options),
        'send_copy': to_json(send_copy),
        'remove_caption': to_json(remove_caption),
        'only_preview': to_json(only_preview),
    }))


def getAccountTtl():
    return get_object(client.func({
        '@type': 'getAccountTtl',
    }))


def getActiveLiveLocationMessages():
    return get_object(client.func({
        '@type': 'getActiveLiveLocationMessages',
    }))


def getActiveSessions():
    return get_object(client.func({
        '@type': 'getActiveSessions',
    }))


def getAllPassportElements(password: str = None, ):
    return get_object(client.func({
        '@type': 'getAllPassportElements',
        'password': to_json(password),
    }))


def getAllStickerEmojis(sticker_type: StickerType = None, query: str = None, chat_id: int = None, return_only_main_emoji: bool = None, ):
    return get_object(client.func({
        '@type': 'getAllStickerEmojis',
        'sticker_type': to_json(sticker_type),
        'query': to_json(query),
        'chat_id': to_json(chat_id),
        'return_only_main_emoji': to_json(return_only_main_emoji),
    }))


def getAnimatedEmoji(emoji: str = None, ):
    return get_object(client.func({
        '@type': 'getAnimatedEmoji',
        'emoji': to_json(emoji),
    }))


def getApplicationConfig():
    return get_object(client.func({
        '@type': 'getApplicationConfig',
    }))


def getApplicationDownloadLink():
    return get_object(client.func({
        '@type': 'getApplicationDownloadLink',
    }))


def getArchiveChatListSettings():
    return get_object(client.func({
        '@type': 'getArchiveChatListSettings',
    }))


def getArchivedStickerSets(sticker_type: StickerType = None, offset_sticker_set_id: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getArchivedStickerSets',
        'sticker_type': to_json(sticker_type),
        'offset_sticker_set_id': to_json(offset_sticker_set_id),
        'limit': to_json(limit),
    }))


def getArchivedStories(from_story_id: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getArchivedStories',
        'from_story_id': to_json(from_story_id),
        'limit': to_json(limit),
    }))


def getAttachedStickerSets(file_id: int = None, ):
    return get_object(client.func({
        '@type': 'getAttachedStickerSets',
        'file_id': to_json(file_id),
    }))


def getAttachmentMenuBot(bot_user_id: int = None, ):
    return get_object(client.func({
        '@type': 'getAttachmentMenuBot',
        'bot_user_id': to_json(bot_user_id),
    }))


def getAuthorizationState():
    return get_object(client.func({
        '@type': 'getAuthorizationState',
    }))


def getAutoDownloadSettingsPresets():
    return get_object(client.func({
        '@type': 'getAutoDownloadSettingsPresets',
    }))


def getAutosaveSettings():
    return get_object(client.func({
        '@type': 'getAutosaveSettings',
    }))


def getBackgroundUrl(name: str = None, type: BackgroundType = None, ):
    return get_object(client.func({
        '@type': 'getBackgroundUrl',
        'name': to_json(name),
        'type': to_json(type),
    }))


def getBackgrounds(for_dark_theme: bool = None, ):
    return get_object(client.func({
        '@type': 'getBackgrounds',
        'for_dark_theme': to_json(for_dark_theme),
    }))


def getBankCardInfo(bank_card_number: str = None, ):
    return get_object(client.func({
        '@type': 'getBankCardInfo',
        'bank_card_number': to_json(bank_card_number),
    }))


def getBasicGroup(basic_group_id: int = None, ):
    return get_object(client.func({
        '@type': 'getBasicGroup',
        'basic_group_id': to_json(basic_group_id),
    }))


def getBasicGroupFullInfo(basic_group_id: int = None, ):
    return get_object(client.func({
        '@type': 'getBasicGroupFullInfo',
        'basic_group_id': to_json(basic_group_id),
    }))


def getBlockedMessageSenders(block_list: BlockList = None, offset: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getBlockedMessageSenders',
        'block_list': to_json(block_list),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getBotInfoDescription(bot_user_id: int = None, language_code: str = None, ):
    return get_object(client.func({
        '@type': 'getBotInfoDescription',
        'bot_user_id': to_json(bot_user_id),
        'language_code': to_json(language_code),
    }))


def getBotInfoShortDescription(bot_user_id: int = None, language_code: str = None, ):
    return get_object(client.func({
        '@type': 'getBotInfoShortDescription',
        'bot_user_id': to_json(bot_user_id),
        'language_code': to_json(language_code),
    }))


def getBotName(bot_user_id: int = None, language_code: str = None, ):
    return get_object(client.func({
        '@type': 'getBotName',
        'bot_user_id': to_json(bot_user_id),
        'language_code': to_json(language_code),
    }))


def getCallbackQueryAnswer(chat_id: int = None, message_id: int = None, payload: CallbackQueryPayload = None, ):
    return get_object(client.func({
        '@type': 'getCallbackQueryAnswer',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'payload': to_json(payload),
    }))


def getCallbackQueryMessage(chat_id: int = None, message_id: int = None, callback_query_id: int = None, ):
    return get_object(client.func({
        '@type': 'getCallbackQueryMessage',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'callback_query_id': to_json(callback_query_id),
    }))


def getChat(chat_id: int = None, ):
    client.send({
        '@type': 'getChat',
        'chat_id': to_json(chat_id),
    })


def getChatActiveStories(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatActiveStories',
        'chat_id': to_json(chat_id),
    }))


def getChatAdministrators(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatAdministrators',
        'chat_id': to_json(chat_id),
    }))


def getChatAvailableMessageSenders(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatAvailableMessageSenders',
        'chat_id': to_json(chat_id),
    }))


def getChatEventLog(chat_id: int = None, query: str = None, from_event_id: int = None, limit: int = None, filters: ChatEventLogFilters = None, user_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'getChatEventLog',
        'chat_id': to_json(chat_id),
        'query': to_json(query),
        'from_event_id': to_json(from_event_id),
        'limit': to_json(limit),
        'filters': to_json(filters),
        'user_ids': to_json(user_ids),
    }))


def getChatFilter(chat_filter_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatFilter',
        'chat_filter_id': to_json(chat_filter_id),
    }))


def getChatFilterChatCount(filter: ChatFilter = None, ):
    return get_object(client.func({
        '@type': 'getChatFilterChatCount',
        'filter': to_json(filter),
    }))


def getChatFilterChatsToLeave(chat_filter_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatFilterChatsToLeave',
        'chat_filter_id': to_json(chat_filter_id),
    }))


def getChatFilterDefaultIconName(filter: ChatFilter = None, ):
    return get_object(client.func({
        '@type': 'getChatFilterDefaultIconName',
        'filter': to_json(filter),
    }))


def getChatFilterInviteLinks(chat_filter_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatFilterInviteLinks',
        'chat_filter_id': to_json(chat_filter_id),
    }))


def getChatFilterNewChats(chat_filter_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatFilterNewChats',
        'chat_filter_id': to_json(chat_filter_id),
    }))


def getChatHistory(chat_id: int = None, from_message_id: int = None, offset: int = None, limit: int = None, only_local: bool = None, ):
    return get_object(client.func({
        '@type': 'getChatHistory',
        'chat_id': to_json(chat_id),
        'from_message_id': to_json(from_message_id),
        'offset': to_json(offset),
        'limit': to_json(limit),
        'only_local': to_json(only_local),
    }))


def getChatInviteLink(chat_id: int = None, invite_link: str = None, ):
    return get_object(client.func({
        '@type': 'getChatInviteLink',
        'chat_id': to_json(chat_id),
        'invite_link': to_json(invite_link),
    }))


def getChatInviteLinkCounts(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatInviteLinkCounts',
        'chat_id': to_json(chat_id),
    }))


def getChatInviteLinkMembers(chat_id: int = None, invite_link: str = None, offset_member: ChatInviteLinkMember = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getChatInviteLinkMembers',
        'chat_id': to_json(chat_id),
        'invite_link': to_json(invite_link),
        'offset_member': to_json(offset_member),
        'limit': to_json(limit),
    }))


def getChatInviteLinks(chat_id: int = None, creator_user_id: int = None, is_revoked: bool = None, offset_date: int = None, offset_invite_link: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getChatInviteLinks',
        'chat_id': to_json(chat_id),
        'creator_user_id': to_json(creator_user_id),
        'is_revoked': to_json(is_revoked),
        'offset_date': to_json(offset_date),
        'offset_invite_link': to_json(offset_invite_link),
        'limit': to_json(limit),
    }))


def getChatJoinRequests(chat_id: int = None, invite_link: str = None, query: str = None, offset_request: ChatJoinRequest = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getChatJoinRequests',
        'chat_id': to_json(chat_id),
        'invite_link': to_json(invite_link),
        'query': to_json(query),
        'offset_request': to_json(offset_request),
        'limit': to_json(limit),
    }))


def getChatListsToAddChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatListsToAddChat',
        'chat_id': to_json(chat_id),
    }))


def getChatMember(chat_id: int = None, member_id: MessageSender = None, ):
    return get_object(client.func({
        '@type': 'getChatMember',
        'chat_id': to_json(chat_id),
        'member_id': to_json(member_id),
    }))


def getChatMessageByDate(chat_id: int = None, date: int = None, ):
    return get_object(client.func({
        '@type': 'getChatMessageByDate',
        'chat_id': to_json(chat_id),
        'date': to_json(date),
    }))


def getChatMessageCalendar(chat_id: int = None, filter: SearchMessagesFilter = None, from_message_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatMessageCalendar',
        'chat_id': to_json(chat_id),
        'filter': to_json(filter),
        'from_message_id': to_json(from_message_id),
    }))


def getChatMessageCount(chat_id: int = None, filter: SearchMessagesFilter = None, return_local: bool = None, ):
    return get_object(client.func({
        '@type': 'getChatMessageCount',
        'chat_id': to_json(chat_id),
        'filter': to_json(filter),
        'return_local': to_json(return_local),
    }))


def getChatMessagePosition(chat_id: int = None, message_id: int = None, filter: SearchMessagesFilter = None, message_thread_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatMessagePosition',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'filter': to_json(filter),
        'message_thread_id': to_json(message_thread_id),
    }))


def getChatNotificationSettingsExceptions(scope: NotificationSettingsScope = None, compare_sound: bool = None, ):
    return get_object(client.func({
        '@type': 'getChatNotificationSettingsExceptions',
        'scope': to_json(scope),
        'compare_sound': to_json(compare_sound),
    }))


def getChatPinnedMessage(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatPinnedMessage',
        'chat_id': to_json(chat_id),
    }))


def getChatPinnedStories(chat_id: int = None, from_story_id: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getChatPinnedStories',
        'chat_id': to_json(chat_id),
        'from_story_id': to_json(from_story_id),
        'limit': to_json(limit),
    }))


def getChatScheduledMessages(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatScheduledMessages',
        'chat_id': to_json(chat_id),
    }))


def getChatSparseMessagePositions(chat_id: int = None, filter: SearchMessagesFilter = None, from_message_id: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getChatSparseMessagePositions',
        'chat_id': to_json(chat_id),
        'filter': to_json(filter),
        'from_message_id': to_json(from_message_id),
        'limit': to_json(limit),
    }))


def getChatSponsoredMessages(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatSponsoredMessages',
        'chat_id': to_json(chat_id),
    }))


def getChatStatistics(chat_id: int = None, is_dark: bool = None, ):
    return get_object(client.func({
        '@type': 'getChatStatistics',
        'chat_id': to_json(chat_id),
        'is_dark': to_json(is_dark),
    }))


def getChats(chat_list: ChatList = None, limit: int = None, ):
    client.send({
        '@type': 'getChats',
        'chat_list': to_json(chat_list),
        'limit': to_json(limit),
    })


def getChatsForChatFilterInviteLink(chat_filter_id: int = None, ):
    return get_object(client.func({
        '@type': 'getChatsForChatFilterInviteLink',
        'chat_filter_id': to_json(chat_filter_id),
    }))


def getCloseFriends():
    return get_object(client.func({
        '@type': 'getCloseFriends',
    }))


def getCommands(scope: BotCommandScope = None, language_code: str = None, ):
    return get_object(client.func({
        '@type': 'getCommands',
        'scope': to_json(scope),
        'language_code': to_json(language_code),
    }))


def getConnectedWebsites():
    return get_object(client.func({
        '@type': 'getConnectedWebsites',
    }))


def getContacts():
    return get_object(client.func({
        '@type': 'getContacts',
    }))


def getCountries():
    return get_object(client.func({
        '@type': 'getCountries',
    }))


def getCountryCode():
    return get_object(client.func({
        '@type': 'getCountryCode',
    }))


def getCreatedPublicChats(type: PublicChatType = None, ):
    return get_object(client.func({
        '@type': 'getCreatedPublicChats',
        'type': to_json(type),
    }))


def getCurrentState():
    return get_object(client.func({
        '@type': 'getCurrentState',
    }))


def getCustomEmojiReactionAnimations():
    return get_object(client.func({
        '@type': 'getCustomEmojiReactionAnimations',
    }))


def getCustomEmojiStickers(custom_emoji_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'getCustomEmojiStickers',
        'custom_emoji_ids': to_json(custom_emoji_ids),
    }))


def getDatabaseStatistics():
    return get_object(client.func({
        '@type': 'getDatabaseStatistics',
    }))


def getDeepLinkInfo(link: str = None, ):
    return get_object(client.func({
        '@type': 'getDeepLinkInfo',
        'link': to_json(link),
    }))


def getDefaultChatPhotoCustomEmojiStickers():
    return get_object(client.func({
        '@type': 'getDefaultChatPhotoCustomEmojiStickers',
    }))


def getDefaultEmojiStatuses():
    return get_object(client.func({
        '@type': 'getDefaultEmojiStatuses',
    }))


def getDefaultMessageAutoDeleteTime():
    return get_object(client.func({
        '@type': 'getDefaultMessageAutoDeleteTime',
    }))


def getDefaultProfilePhotoCustomEmojiStickers():
    return get_object(client.func({
        '@type': 'getDefaultProfilePhotoCustomEmojiStickers',
    }))


def getEmojiCategories(type: EmojiCategoryType = None, ):
    return get_object(client.func({
        '@type': 'getEmojiCategories',
        'type': to_json(type),
    }))


def getEmojiReaction(emoji: str = None, ):
    return get_object(client.func({
        '@type': 'getEmojiReaction',
        'emoji': to_json(emoji),
    }))


def getEmojiSuggestionsUrl(language_code: str = None, ):
    return get_object(client.func({
        '@type': 'getEmojiSuggestionsUrl',
        'language_code': to_json(language_code),
    }))


def getExternalLink(link: str = None, allow_write_access: bool = None, ):
    return get_object(client.func({
        '@type': 'getExternalLink',
        'link': to_json(link),
        'allow_write_access': to_json(allow_write_access),
    }))


def getExternalLinkInfo(link: str = None, ):
    return get_object(client.func({
        '@type': 'getExternalLinkInfo',
        'link': to_json(link),
    }))


def getFavoriteStickers():
    return get_object(client.func({
        '@type': 'getFavoriteStickers',
    }))


def getFile(file_id: int = None, ):
    return get_object(client.func({
        '@type': 'getFile',
        'file_id': to_json(file_id),
    }))


def getFileDownloadedPrefixSize(file_id: int = None, offset: int = None, ):
    return get_object(client.func({
        '@type': 'getFileDownloadedPrefixSize',
        'file_id': to_json(file_id),
        'offset': to_json(offset),
    }))


def getFileExtension(mime_type: str = None, ):
    return get_object(client.func({
        '@type': 'getFileExtension',
        'mime_type': to_json(mime_type),
    }))


def getFileMimeType(file_name: str = None, ):
    return get_object(client.func({
        '@type': 'getFileMimeType',
        'file_name': to_json(file_name),
    }))


def getForumTopic(chat_id: int = None, message_thread_id: int = None, ):
    return get_object(client.func({
        '@type': 'getForumTopic',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
    }))


def getForumTopicDefaultIcons():
    return get_object(client.func({
        '@type': 'getForumTopicDefaultIcons',
    }))


def getForumTopicLink(chat_id: int = None, message_thread_id: int = None, ):
    return get_object(client.func({
        '@type': 'getForumTopicLink',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
    }))


def getForumTopics(chat_id: int = None, query: str = None, offset_date: int = None, offset_message_id: int = None, offset_message_thread_id: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getForumTopics',
        'chat_id': to_json(chat_id),
        'query': to_json(query),
        'offset_date': to_json(offset_date),
        'offset_message_id': to_json(offset_message_id),
        'offset_message_thread_id': to_json(offset_message_thread_id),
        'limit': to_json(limit),
    }))


def getGameHighScores(chat_id: int = None, message_id: int = None, user_id: int = None, ):
    return get_object(client.func({
        '@type': 'getGameHighScores',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'user_id': to_json(user_id),
    }))


def getGroupCall(group_call_id: int = None, ):
    return get_object(client.func({
        '@type': 'getGroupCall',
        'group_call_id': to_json(group_call_id),
    }))


def getGroupCallInviteLink(group_call_id: int = None, can_self_unmute: bool = None, ):
    return get_object(client.func({
        '@type': 'getGroupCallInviteLink',
        'group_call_id': to_json(group_call_id),
        'can_self_unmute': to_json(can_self_unmute),
    }))


def getGroupCallStreamSegment(group_call_id: int = None, time_offset: int = None, scale: int = None, channel_id: int = None, video_quality: GroupCallVideoQuality = None, ):
    return get_object(client.func({
        '@type': 'getGroupCallStreamSegment',
        'group_call_id': to_json(group_call_id),
        'time_offset': to_json(time_offset),
        'scale': to_json(scale),
        'channel_id': to_json(channel_id),
        'video_quality': to_json(video_quality),
    }))


def getGroupCallStreams(group_call_id: int = None, ):
    return get_object(client.func({
        '@type': 'getGroupCallStreams',
        'group_call_id': to_json(group_call_id),
    }))


def getGroupsInCommon(user_id: int = None, offset_chat_id: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getGroupsInCommon',
        'user_id': to_json(user_id),
        'offset_chat_id': to_json(offset_chat_id),
        'limit': to_json(limit),
    }))


def getImportedContactCount():
    return get_object(client.func({
        '@type': 'getImportedContactCount',
    }))


def getInactiveSupergroupChats():
    return get_object(client.func({
        '@type': 'getInactiveSupergroupChats',
    }))


def getInlineGameHighScores(inline_message_id: str = None, user_id: int = None, ):
    return get_object(client.func({
        '@type': 'getInlineGameHighScores',
        'inline_message_id': to_json(inline_message_id),
        'user_id': to_json(user_id),
    }))


def getInlineQueryResults(bot_user_id: int = None, chat_id: int = None, user_location: Location = None, query: str = None, offset: str = None, ):
    return get_object(client.func({
        '@type': 'getInlineQueryResults',
        'bot_user_id': to_json(bot_user_id),
        'chat_id': to_json(chat_id),
        'user_location': to_json(user_location),
        'query': to_json(query),
        'offset': to_json(offset),
    }))


def getInstalledStickerSets(sticker_type: StickerType = None, ):
    return get_object(client.func({
        '@type': 'getInstalledStickerSets',
        'sticker_type': to_json(sticker_type),
    }))


def getInternalLink(type: InternalLinkType = None, is_http: bool = None, ):
    return get_object(client.func({
        '@type': 'getInternalLink',
        'type': to_json(type),
        'is_http': to_json(is_http),
    }))


def getInternalLinkType(link: str = None, ):
    return get_object(client.func({
        '@type': 'getInternalLinkType',
        'link': to_json(link),
    }))


def getJsonString(json_value: JsonValue = None, ):
    return get_object(client.func({
        '@type': 'getJsonString',
        'json_value': to_json(json_value),
    }))


def getJsonValue(json: str = None, ):
    return get_object(client.func({
        '@type': 'getJsonValue',
        'json': to_json(json),
    }))


def getLanguagePackInfo(language_pack_id: str = None, ):
    return get_object(client.func({
        '@type': 'getLanguagePackInfo',
        'language_pack_id': to_json(language_pack_id),
    }))


def getLanguagePackString(language_pack_database_path: str = None, localization_target: str = None, language_pack_id: str = None, key: str = None, ):
    return get_object(client.func({
        '@type': 'getLanguagePackString',
        'language_pack_database_path': to_json(language_pack_database_path),
        'localization_target': to_json(localization_target),
        'language_pack_id': to_json(language_pack_id),
        'key': to_json(key),
    }))


def getLanguagePackStrings(language_pack_id: str = None, keys: list[str] = None, ):
    return get_object(client.func({
        '@type': 'getLanguagePackStrings',
        'language_pack_id': to_json(language_pack_id),
        'keys': to_json(keys),
    }))


def getLocalizationTargetInfo(only_local: bool = None, ):
    return get_object(client.func({
        '@type': 'getLocalizationTargetInfo',
        'only_local': to_json(only_local),
    }))


def getLogStream():
    return get_object(client.func({
        '@type': 'getLogStream',
    }))


def getLogTagVerbosityLevel(tag: str = None, ):
    return get_object(client.func({
        '@type': 'getLogTagVerbosityLevel',
        'tag': to_json(tag),
    }))


def getLogTags():
    return get_object(client.func({
        '@type': 'getLogTags',
    }))


def getLogVerbosityLevel():
    return get_object(client.func({
        '@type': 'getLogVerbosityLevel',
    }))


def getLoginUrl(chat_id: int = None, message_id: int = None, button_id: int = None, allow_write_access: bool = None, ):
    return get_object(client.func({
        '@type': 'getLoginUrl',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'button_id': to_json(button_id),
        'allow_write_access': to_json(allow_write_access),
    }))


def getLoginUrlInfo(chat_id: int = None, message_id: int = None, button_id: int = None, ):
    return get_object(client.func({
        '@type': 'getLoginUrlInfo',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'button_id': to_json(button_id),
    }))


def getMapThumbnailFile(location: Location = None, zoom: int = None, width: int = None, height: int = None, scale: int = None, chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getMapThumbnailFile',
        'location': to_json(location),
        'zoom': to_json(zoom),
        'width': to_json(width),
        'height': to_json(height),
        'scale': to_json(scale),
        'chat_id': to_json(chat_id),
    }))


def getMarkdownText(text: FormattedText = None, ):
    return get_object(client.func({
        '@type': 'getMarkdownText',
        'text': to_json(text),
    }))


def getMe():
    return get_object(client.func({
        '@type': 'getMe',
    }))


def getMenuButton(user_id: int = None, ):
    return get_object(client.func({
        '@type': 'getMenuButton',
        'user_id': to_json(user_id),
    }))


def getMessage(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'getMessage',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def getMessageAddedReactions(chat_id: int = None, message_id: int = None, reaction_type: ReactionType = None, offset: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getMessageAddedReactions',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reaction_type': to_json(reaction_type),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getMessageAvailableReactions(chat_id: int = None, message_id: int = None, row_size: int = None, ):
    return get_object(client.func({
        '@type': 'getMessageAvailableReactions',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'row_size': to_json(row_size),
    }))


def getMessageEmbeddingCode(chat_id: int = None, message_id: int = None, for_album: bool = None, ):
    return get_object(client.func({
        '@type': 'getMessageEmbeddingCode',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'for_album': to_json(for_album),
    }))


def getMessageFileType(message_file_head: str = None, ):
    return get_object(client.func({
        '@type': 'getMessageFileType',
        'message_file_head': to_json(message_file_head),
    }))


def getMessageImportConfirmationText(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getMessageImportConfirmationText',
        'chat_id': to_json(chat_id),
    }))


def getMessageLink(chat_id: int = None, message_id: int = None, media_timestamp: int = None, for_album: bool = None, in_message_thread: bool = None, ):
    return get_object(client.func({
        '@type': 'getMessageLink',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'media_timestamp': to_json(media_timestamp),
        'for_album': to_json(for_album),
        'in_message_thread': to_json(in_message_thread),
    }))


def getMessageLinkInfo(url: str = None, ):
    return get_object(client.func({
        '@type': 'getMessageLinkInfo',
        'url': to_json(url),
    }))


def getMessageLocally(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'getMessageLocally',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def getMessagePublicForwards(chat_id: int = None, message_id: int = None, offset: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getMessagePublicForwards',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getMessageStatistics(chat_id: int = None, message_id: int = None, is_dark: bool = None, ):
    return get_object(client.func({
        '@type': 'getMessageStatistics',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'is_dark': to_json(is_dark),
    }))


def getMessageThread(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'getMessageThread',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def getMessageThreadHistory(chat_id: int = None, message_id: int = None, from_message_id: int = None, offset: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getMessageThreadHistory',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'from_message_id': to_json(from_message_id),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getMessageViewers(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'getMessageViewers',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def getMessages(chat_id: int = None, message_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'getMessages',
        'chat_id': to_json(chat_id),
        'message_ids': to_json(message_ids),
    }))


def getNetworkStatistics(only_current: bool = None, ):
    return get_object(client.func({
        '@type': 'getNetworkStatistics',
        'only_current': to_json(only_current),
    }))


def getOption(name: str = None, ):
    return get_object(client.func({
        '@type': 'getOption',
        'name': to_json(name),
    }))


def getPassportAuthorizationForm(bot_user_id: int = None, scope: str = None, public_key: str = None, nonce: str = None, ):
    return get_object(client.func({
        '@type': 'getPassportAuthorizationForm',
        'bot_user_id': to_json(bot_user_id),
        'scope': to_json(scope),
        'public_key': to_json(public_key),
        'nonce': to_json(nonce),
    }))


def getPassportAuthorizationFormAvailableElements(authorization_form_id: int = None, password: str = None, ):
    return get_object(client.func({
        '@type': 'getPassportAuthorizationFormAvailableElements',
        'authorization_form_id': to_json(authorization_form_id),
        'password': to_json(password),
    }))


def getPassportElement(type: PassportElementType = None, password: str = None, ):
    return get_object(client.func({
        '@type': 'getPassportElement',
        'type': to_json(type),
        'password': to_json(password),
    }))


def getPasswordState():
    return get_object(client.func({
        '@type': 'getPasswordState',
    }))


def getPaymentForm(input_invoice: InputInvoice = None, theme: ThemeParameters = None, ):
    return get_object(client.func({
        '@type': 'getPaymentForm',
        'input_invoice': to_json(input_invoice),
        'theme': to_json(theme),
    }))


def getPaymentReceipt(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'getPaymentReceipt',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def getPhoneNumberInfo(phone_number_prefix: str = None, ):
    return get_object(client.func({
        '@type': 'getPhoneNumberInfo',
        'phone_number_prefix': to_json(phone_number_prefix),
    }))


def getPhoneNumberInfoSync(language_code: str = None, phone_number_prefix: str = None, ):
    return get_object(client.func({
        '@type': 'getPhoneNumberInfoSync',
        'language_code': to_json(language_code),
        'phone_number_prefix': to_json(phone_number_prefix),
    }))


def getPollVoters(chat_id: int = None, message_id: int = None, option_id: int = None, offset: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getPollVoters',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'option_id': to_json(option_id),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getPreferredCountryLanguage(country_code: str = None, ):
    return get_object(client.func({
        '@type': 'getPreferredCountryLanguage',
        'country_code': to_json(country_code),
    }))


def getPremiumFeatures(source: PremiumSource = None, ):
    return get_object(client.func({
        '@type': 'getPremiumFeatures',
        'source': to_json(source),
    }))


def getPremiumLimit(limit_type: PremiumLimitType = None, ):
    return get_object(client.func({
        '@type': 'getPremiumLimit',
        'limit_type': to_json(limit_type),
    }))


def getPremiumState():
    return get_object(client.func({
        '@type': 'getPremiumState',
    }))


def getPremiumStickerExamples():
    return get_object(client.func({
        '@type': 'getPremiumStickerExamples',
    }))


def getPremiumStickers(limit: int = None, ):
    return get_object(client.func({
        '@type': 'getPremiumStickers',
        'limit': to_json(limit),
    }))


def getProxies():
    return get_object(client.func({
        '@type': 'getProxies',
    }))


def getProxyLink(proxy_id: int = None, ):
    return get_object(client.func({
        '@type': 'getProxyLink',
        'proxy_id': to_json(proxy_id),
    }))


def getPushReceiverId(payload: str = None, ):
    return get_object(client.func({
        '@type': 'getPushReceiverId',
        'payload': to_json(payload),
    }))


def getRecentEmojiStatuses():
    return get_object(client.func({
        '@type': 'getRecentEmojiStatuses',
    }))


def getRecentInlineBots():
    return get_object(client.func({
        '@type': 'getRecentInlineBots',
    }))


def getRecentStickers(is_attached: bool = None, ):
    return get_object(client.func({
        '@type': 'getRecentStickers',
        'is_attached': to_json(is_attached),
    }))


def getRecentlyOpenedChats(limit: int = None, ):
    return get_object(client.func({
        '@type': 'getRecentlyOpenedChats',
        'limit': to_json(limit),
    }))


def getRecentlyVisitedTMeUrls(referrer: str = None, ):
    return get_object(client.func({
        '@type': 'getRecentlyVisitedTMeUrls',
        'referrer': to_json(referrer),
    }))


def getRecommendedChatFilters():
    return get_object(client.func({
        '@type': 'getRecommendedChatFilters',
    }))


def getRecoveryEmailAddress(password: str = None, ):
    return get_object(client.func({
        '@type': 'getRecoveryEmailAddress',
        'password': to_json(password),
    }))


def getRemoteFile(remote_file_id: str = None, file_type: FileType = None, ):
    return get_object(client.func({
        '@type': 'getRemoteFile',
        'remote_file_id': to_json(remote_file_id),
        'file_type': to_json(file_type),
    }))


def getRepliedMessage(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'getRepliedMessage',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def getSavedAnimations():
    return get_object(client.func({
        '@type': 'getSavedAnimations',
    }))


def getSavedNotificationSound(notification_sound_id: int = None, ):
    return get_object(client.func({
        '@type': 'getSavedNotificationSound',
        'notification_sound_id': to_json(notification_sound_id),
    }))


def getSavedNotificationSounds():
    return get_object(client.func({
        '@type': 'getSavedNotificationSounds',
    }))


def getSavedOrderInfo():
    return get_object(client.func({
        '@type': 'getSavedOrderInfo',
    }))


def getScopeNotificationSettings(scope: NotificationSettingsScope = None, ):
    return get_object(client.func({
        '@type': 'getScopeNotificationSettings',
        'scope': to_json(scope),
    }))


def getSecretChat(secret_chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getSecretChat',
        'secret_chat_id': to_json(secret_chat_id),
    }))


def getStatisticalGraph(chat_id: int = None, token: str = None, x: int = None, ):
    return get_object(client.func({
        '@type': 'getStatisticalGraph',
        'chat_id': to_json(chat_id),
        'token': to_json(token),
        'x': to_json(x),
    }))


def getStickerEmojis(sticker: InputFile = None, ):
    return get_object(client.func({
        '@type': 'getStickerEmojis',
        'sticker': to_json(sticker),
    }))


def getStickerSet(set_id: int = None, ):
    return get_object(client.func({
        '@type': 'getStickerSet',
        'set_id': to_json(set_id),
    }))


def getStickers(sticker_type: StickerType = None, query: str = None, limit: int = None, chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getStickers',
        'sticker_type': to_json(sticker_type),
        'query': to_json(query),
        'limit': to_json(limit),
        'chat_id': to_json(chat_id),
    }))


def getStorageStatistics(chat_limit: int = None, ):
    return get_object(client.func({
        '@type': 'getStorageStatistics',
        'chat_limit': to_json(chat_limit),
    }))


def getStorageStatisticsFast():
    return get_object(client.func({
        '@type': 'getStorageStatisticsFast',
    }))


def getStory(story_sender_chat_id: int = None, story_id: int = None, only_local: bool = None, ):
    return get_object(client.func({
        '@type': 'getStory',
        'story_sender_chat_id': to_json(story_sender_chat_id),
        'story_id': to_json(story_id),
        'only_local': to_json(only_local),
    }))


def getStoryAvailableReactions(row_size: int = None, ):
    return get_object(client.func({
        '@type': 'getStoryAvailableReactions',
        'row_size': to_json(row_size),
    }))


def getStoryNotificationSettingsExceptions():
    return get_object(client.func({
        '@type': 'getStoryNotificationSettingsExceptions',
    }))


def getStoryViewers(story_id: int = None, query: str = None, only_contacts: bool = None, prefer_with_reaction: bool = None, offset: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getStoryViewers',
        'story_id': to_json(story_id),
        'query': to_json(query),
        'only_contacts': to_json(only_contacts),
        'prefer_with_reaction': to_json(prefer_with_reaction),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getSuggestedFileName(file_id: int = None, directory: str = None, ):
    return get_object(client.func({
        '@type': 'getSuggestedFileName',
        'file_id': to_json(file_id),
        'directory': to_json(directory),
    }))


def getSuggestedStickerSetName(title: str = None, ):
    return get_object(client.func({
        '@type': 'getSuggestedStickerSetName',
        'title': to_json(title),
    }))


def getSuitableDiscussionChats():
    return get_object(client.func({
        '@type': 'getSuitableDiscussionChats',
    }))


def getSupergroup(supergroup_id: int = None, ):
    return get_object(client.func({
        '@type': 'getSupergroup',
        'supergroup_id': to_json(supergroup_id),
    }))


def getSupergroupFullInfo(supergroup_id: int = None, ):
    return get_object(client.func({
        '@type': 'getSupergroupFullInfo',
        'supergroup_id': to_json(supergroup_id),
    }))


def getSupergroupMembers(supergroup_id: int = None, filter: SupergroupMembersFilter = None, offset: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getSupergroupMembers',
        'supergroup_id': to_json(supergroup_id),
        'filter': to_json(filter),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getSupportName():
    return get_object(client.func({
        '@type': 'getSupportName',
    }))


def getSupportUser():
    return get_object(client.func({
        '@type': 'getSupportUser',
    }))


def getTemporaryPasswordState():
    return get_object(client.func({
        '@type': 'getTemporaryPasswordState',
    }))


def getTextEntities(text: str = None, ):
    return get_object(client.func({
        '@type': 'getTextEntities',
        'text': to_json(text),
    }))


def getThemeParametersJsonString(theme: ThemeParameters = None, ):
    return get_object(client.func({
        '@type': 'getThemeParametersJsonString',
        'theme': to_json(theme),
    }))


def getThemedEmojiStatuses():
    return get_object(client.func({
        '@type': 'getThemedEmojiStatuses',
    }))


def getTopChats(category: TopChatCategory = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getTopChats',
        'category': to_json(category),
        'limit': to_json(limit),
    }))


def getTrendingStickerSets(sticker_type: StickerType = None, offset: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getTrendingStickerSets',
        'sticker_type': to_json(sticker_type),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getUser(user_id: int = None, ):
    return get_object(client.func({
        '@type': 'getUser',
        'user_id': to_json(user_id),
    }))


def getUserFullInfo(user_id: int = None, ):
    return get_object(client.func({
        '@type': 'getUserFullInfo',
        'user_id': to_json(user_id),
    }))


def getUserLink():
    return get_object(client.func({
        '@type': 'getUserLink',
    }))


def getUserPrivacySettingRules(setting: UserPrivacySetting = None, ):
    return get_object(client.func({
        '@type': 'getUserPrivacySettingRules',
        'setting': to_json(setting),
    }))


def getUserProfilePhotos(user_id: int = None, offset: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'getUserProfilePhotos',
        'user_id': to_json(user_id),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def getUserSupportInfo(user_id: int = None, ):
    return get_object(client.func({
        '@type': 'getUserSupportInfo',
        'user_id': to_json(user_id),
    }))


def getVideoChatAvailableParticipants(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getVideoChatAvailableParticipants',
        'chat_id': to_json(chat_id),
    }))


def getVideoChatRtmpUrl(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'getVideoChatRtmpUrl',
        'chat_id': to_json(chat_id),
    }))


def getWebAppLinkUrl(chat_id: int = None, bot_user_id: int = None, web_app_short_name: str = None, start_parameter: str = None, theme: ThemeParameters = None, application_name: str = None, allow_write_access: bool = None, ):
    return get_object(client.func({
        '@type': 'getWebAppLinkUrl',
        'chat_id': to_json(chat_id),
        'bot_user_id': to_json(bot_user_id),
        'web_app_short_name': to_json(web_app_short_name),
        'start_parameter': to_json(start_parameter),
        'theme': to_json(theme),
        'application_name': to_json(application_name),
        'allow_write_access': to_json(allow_write_access),
    }))


def getWebAppUrl(bot_user_id: int = None, url: str = None, theme: ThemeParameters = None, application_name: str = None, ):
    return get_object(client.func({
        '@type': 'getWebAppUrl',
        'bot_user_id': to_json(bot_user_id),
        'url': to_json(url),
        'theme': to_json(theme),
        'application_name': to_json(application_name),
    }))


def getWebPageInstantView(url: str = None, force_full: bool = None, ):
    return get_object(client.func({
        '@type': 'getWebPageInstantView',
        'url': to_json(url),
        'force_full': to_json(force_full),
    }))


def getWebPagePreview(text: FormattedText = None, ):
    return get_object(client.func({
        '@type': 'getWebPagePreview',
        'text': to_json(text),
    }))


def hideSuggestedAction(action: SuggestedAction = None, ):
    return get_object(client.func({
        '@type': 'hideSuggestedAction',
        'action': to_json(action),
    }))


def importContacts(contacts: list[Contact] = None, ):
    return get_object(client.func({
        '@type': 'importContacts',
        'contacts': to_json(contacts),
    }))


def importMessages(chat_id: int = None, message_file: InputFile = None, attached_files: list[InputFile] = None, ):
    return get_object(client.func({
        '@type': 'importMessages',
        'chat_id': to_json(chat_id),
        'message_file': to_json(message_file),
        'attached_files': to_json(attached_files),
    }))


def inviteGroupCallParticipants(group_call_id: int = None, user_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'inviteGroupCallParticipants',
        'group_call_id': to_json(group_call_id),
        'user_ids': to_json(user_ids),
    }))


def joinChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'joinChat',
        'chat_id': to_json(chat_id),
    }))


def joinChatByInviteLink(invite_link: str = None, ):
    return get_object(client.func({
        '@type': 'joinChatByInviteLink',
        'invite_link': to_json(invite_link),
    }))


def joinGroupCall(group_call_id: int = None, participant_id: MessageSender = None, audio_source_id: int = None, payload: str = None, is_muted: bool = None, is_my_video_enabled: bool = None, invite_hash: str = None, ):
    return get_object(client.func({
        '@type': 'joinGroupCall',
        'group_call_id': to_json(group_call_id),
        'participant_id': to_json(participant_id),
        'audio_source_id': to_json(audio_source_id),
        'payload': to_json(payload),
        'is_muted': to_json(is_muted),
        'is_my_video_enabled': to_json(is_my_video_enabled),
        'invite_hash': to_json(invite_hash),
    }))


def leaveChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'leaveChat',
        'chat_id': to_json(chat_id),
    }))


def leaveGroupCall(group_call_id: int = None, ):
    return get_object(client.func({
        '@type': 'leaveGroupCall',
        'group_call_id': to_json(group_call_id),
    }))


def loadActiveStories(story_list: StoryList = None, ):
    return get_object(client.func({
        '@type': 'loadActiveStories',
        'story_list': to_json(story_list),
    }))


def loadChats(chat_list: ChatList = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'loadChats',
        'chat_list': to_json(chat_list),
        'limit': to_json(limit),
    }))


def loadGroupCallParticipants(group_call_id: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'loadGroupCallParticipants',
        'group_call_id': to_json(group_call_id),
        'limit': to_json(limit),
    }))


def logOut():
    return get_object(client.func({
        '@type': 'logOut',
    }))


def openChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'openChat',
        'chat_id': to_json(chat_id),
    }))


def openMessageContent(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'openMessageContent',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def openStory(story_sender_chat_id: int = None, story_id: int = None, ):
    return get_object(client.func({
        '@type': 'openStory',
        'story_sender_chat_id': to_json(story_sender_chat_id),
        'story_id': to_json(story_id),
    }))


def openWebApp(chat_id: int = None, bot_user_id: int = None, url: str = None, theme: ThemeParameters = None, application_name: str = None, message_thread_id: int = None, reply_to: MessageReplyTo = None, ):
    return get_object(client.func({
        '@type': 'openWebApp',
        'chat_id': to_json(chat_id),
        'bot_user_id': to_json(bot_user_id),
        'url': to_json(url),
        'theme': to_json(theme),
        'application_name': to_json(application_name),
        'message_thread_id': to_json(message_thread_id),
        'reply_to': to_json(reply_to),
    }))


def optimizeStorage(size: int = None, ttl: int = None, count: int = None, immunity_delay: int = None, file_types: list[FileType] = None, chat_ids: list[int] = None, exclude_chat_ids: list[int] = None, return_deleted_file_statistics: bool = None, chat_limit: int = None, ):
    return get_object(client.func({
        '@type': 'optimizeStorage',
        'size': to_json(size),
        'ttl': to_json(ttl),
        'count': to_json(count),
        'immunity_delay': to_json(immunity_delay),
        'file_types': to_json(file_types),
        'chat_ids': to_json(chat_ids),
        'exclude_chat_ids': to_json(exclude_chat_ids),
        'return_deleted_file_statistics': to_json(return_deleted_file_statistics),
        'chat_limit': to_json(chat_limit),
    }))


def parseMarkdown(text: FormattedText = None, ):
    return get_object(client.func({
        '@type': 'parseMarkdown',
        'text': to_json(text),
    }))


def parseTextEntities(text: str = None, parse_mode: TextParseMode = None, ):
    return get_object(client.func({
        '@type': 'parseTextEntities',
        'text': to_json(text),
        'parse_mode': to_json(parse_mode),
    }))


def pinChatMessage(chat_id: int = None, message_id: int = None, disable_notification: bool = None, only_for_self: bool = None, ):
    return get_object(client.func({
        '@type': 'pinChatMessage',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'disable_notification': to_json(disable_notification),
        'only_for_self': to_json(only_for_self),
    }))


def pingProxy(proxy_id: int = None, ):
    return get_object(client.func({
        '@type': 'pingProxy',
        'proxy_id': to_json(proxy_id),
    }))


def preliminaryUploadFile(file: InputFile = None, file_type: FileType = None, priority: int = None, ):
    return get_object(client.func({
        '@type': 'preliminaryUploadFile',
        'file': to_json(file),
        'file_type': to_json(file_type),
        'priority': to_json(priority),
    }))


def processChatFilterNewChats(chat_filter_id: int = None, added_chat_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'processChatFilterNewChats',
        'chat_filter_id': to_json(chat_filter_id),
        'added_chat_ids': to_json(added_chat_ids),
    }))


def processChatJoinRequest(chat_id: int = None, user_id: int = None, approve: bool = None, ):
    return get_object(client.func({
        '@type': 'processChatJoinRequest',
        'chat_id': to_json(chat_id),
        'user_id': to_json(user_id),
        'approve': to_json(approve),
    }))


def processChatJoinRequests(chat_id: int = None, invite_link: str = None, approve: bool = None, ):
    return get_object(client.func({
        '@type': 'processChatJoinRequests',
        'chat_id': to_json(chat_id),
        'invite_link': to_json(invite_link),
        'approve': to_json(approve),
    }))


def processPushNotification(payload: str = None, ):
    return get_object(client.func({
        '@type': 'processPushNotification',
        'payload': to_json(payload),
    }))


def rateSpeechRecognition(chat_id: int = None, message_id: int = None, is_good: bool = None, ):
    return get_object(client.func({
        '@type': 'rateSpeechRecognition',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'is_good': to_json(is_good),
    }))


def readAllChatMentions(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'readAllChatMentions',
        'chat_id': to_json(chat_id),
    }))


def readAllChatReactions(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'readAllChatReactions',
        'chat_id': to_json(chat_id),
    }))


def readAllMessageThreadMentions(chat_id: int = None, message_thread_id: int = None, ):
    return get_object(client.func({
        '@type': 'readAllMessageThreadMentions',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
    }))


def readAllMessageThreadReactions(chat_id: int = None, message_thread_id: int = None, ):
    return get_object(client.func({
        '@type': 'readAllMessageThreadReactions',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
    }))


def readChatList(chat_list: ChatList = None, ):
    return get_object(client.func({
        '@type': 'readChatList',
        'chat_list': to_json(chat_list),
    }))


def readFilePart(file_id: int = None, offset: int = None, count: int = None, ):
    return get_object(client.func({
        '@type': 'readFilePart',
        'file_id': to_json(file_id),
        'offset': to_json(offset),
        'count': to_json(count),
    }))


def recognizeSpeech(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'recognizeSpeech',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def recoverAuthenticationPassword(recovery_code: str = None, new_password: str = None, new_hint: str = None, ):
    return get_object(client.func({
        '@type': 'recoverAuthenticationPassword',
        'recovery_code': to_json(recovery_code),
        'new_password': to_json(new_password),
        'new_hint': to_json(new_hint),
    }))


def recoverPassword(recovery_code: str = None, new_password: str = None, new_hint: str = None, ):
    return get_object(client.func({
        '@type': 'recoverPassword',
        'recovery_code': to_json(recovery_code),
        'new_password': to_json(new_password),
        'new_hint': to_json(new_hint),
    }))


def registerDevice(device_token: DeviceToken = None, other_user_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'registerDevice',
        'device_token': to_json(device_token),
        'other_user_ids': to_json(other_user_ids),
    }))


def registerUser(first_name: str = None, last_name: str = None, ):
    return get_object(client.func({
        '@type': 'registerUser',
        'first_name': to_json(first_name),
        'last_name': to_json(last_name),
    }))


def removeAllFilesFromDownloads(only_active: bool = None, only_completed: bool = None, delete_from_cache: bool = None, ):
    return get_object(client.func({
        '@type': 'removeAllFilesFromDownloads',
        'only_active': to_json(only_active),
        'only_completed': to_json(only_completed),
        'delete_from_cache': to_json(delete_from_cache),
    }))


def removeBackground(background_id: int = None, ):
    return get_object(client.func({
        '@type': 'removeBackground',
        'background_id': to_json(background_id),
    }))


def removeChatActionBar(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'removeChatActionBar',
        'chat_id': to_json(chat_id),
    }))


def removeContacts(user_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'removeContacts',
        'user_ids': to_json(user_ids),
    }))


def removeFavoriteSticker(sticker: InputFile = None, ):
    return get_object(client.func({
        '@type': 'removeFavoriteSticker',
        'sticker': to_json(sticker),
    }))


def removeFileFromDownloads(file_id: int = None, delete_from_cache: bool = None, ):
    return get_object(client.func({
        '@type': 'removeFileFromDownloads',
        'file_id': to_json(file_id),
        'delete_from_cache': to_json(delete_from_cache),
    }))


def removeMessageReaction(chat_id: int = None, message_id: int = None, reaction_type: ReactionType = None, ):
    return get_object(client.func({
        '@type': 'removeMessageReaction',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reaction_type': to_json(reaction_type),
    }))


def removeNotification(notification_group_id: int = None, notification_id: int = None, ):
    return get_object(client.func({
        '@type': 'removeNotification',
        'notification_group_id': to_json(notification_group_id),
        'notification_id': to_json(notification_id),
    }))


def removeNotificationGroup(notification_group_id: int = None, max_notification_id: int = None, ):
    return get_object(client.func({
        '@type': 'removeNotificationGroup',
        'notification_group_id': to_json(notification_group_id),
        'max_notification_id': to_json(max_notification_id),
    }))


def removeProxy(proxy_id: int = None, ):
    return get_object(client.func({
        '@type': 'removeProxy',
        'proxy_id': to_json(proxy_id),
    }))


def removeRecentHashtag(hashtag: str = None, ):
    return get_object(client.func({
        '@type': 'removeRecentHashtag',
        'hashtag': to_json(hashtag),
    }))


def removeRecentSticker(is_attached: bool = None, sticker: InputFile = None, ):
    return get_object(client.func({
        '@type': 'removeRecentSticker',
        'is_attached': to_json(is_attached),
        'sticker': to_json(sticker),
    }))


def removeRecentlyFoundChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'removeRecentlyFoundChat',
        'chat_id': to_json(chat_id),
    }))


def removeSavedAnimation(animation: InputFile = None, ):
    return get_object(client.func({
        '@type': 'removeSavedAnimation',
        'animation': to_json(animation),
    }))


def removeSavedNotificationSound(notification_sound_id: int = None, ):
    return get_object(client.func({
        '@type': 'removeSavedNotificationSound',
        'notification_sound_id': to_json(notification_sound_id),
    }))


def removeStickerFromSet(sticker: InputFile = None, ):
    return get_object(client.func({
        '@type': 'removeStickerFromSet',
        'sticker': to_json(sticker),
    }))


def removeTopChat(category: TopChatCategory = None, chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'removeTopChat',
        'category': to_json(category),
        'chat_id': to_json(chat_id),
    }))


def reorderActiveUsernames(usernames: list[str] = None, ):
    return get_object(client.func({
        '@type': 'reorderActiveUsernames',
        'usernames': to_json(usernames),
    }))


def reorderBotActiveUsernames(bot_user_id: int = None, usernames: list[str] = None, ):
    return get_object(client.func({
        '@type': 'reorderBotActiveUsernames',
        'bot_user_id': to_json(bot_user_id),
        'usernames': to_json(usernames),
    }))


def reorderChatFilters(chat_filter_ids: list[int] = None, main_chat_list_position: int = None, ):
    return get_object(client.func({
        '@type': 'reorderChatFilters',
        'chat_filter_ids': to_json(chat_filter_ids),
        'main_chat_list_position': to_json(main_chat_list_position),
    }))


def reorderInstalledStickerSets(sticker_type: StickerType = None, sticker_set_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'reorderInstalledStickerSets',
        'sticker_type': to_json(sticker_type),
        'sticker_set_ids': to_json(sticker_set_ids),
    }))


def reorderSupergroupActiveUsernames(supergroup_id: int = None, usernames: list[str] = None, ):
    return get_object(client.func({
        '@type': 'reorderSupergroupActiveUsernames',
        'supergroup_id': to_json(supergroup_id),
        'usernames': to_json(usernames),
    }))


def replacePrimaryChatInviteLink(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'replacePrimaryChatInviteLink',
        'chat_id': to_json(chat_id),
    }))


def replaceVideoChatRtmpUrl(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'replaceVideoChatRtmpUrl',
        'chat_id': to_json(chat_id),
    }))


def reportChat(chat_id: int = None, message_ids: list[int] = None, reason: ReportReason = None, text: str = None, ):
    return get_object(client.func({
        '@type': 'reportChat',
        'chat_id': to_json(chat_id),
        'message_ids': to_json(message_ids),
        'reason': to_json(reason),
        'text': to_json(text),
    }))


def reportChatPhoto(chat_id: int = None, file_id: int = None, reason: ReportReason = None, text: str = None, ):
    return get_object(client.func({
        '@type': 'reportChatPhoto',
        'chat_id': to_json(chat_id),
        'file_id': to_json(file_id),
        'reason': to_json(reason),
        'text': to_json(text),
    }))


def reportMessageReactions(chat_id: int = None, message_id: int = None, sender_id: MessageSender = None, ):
    return get_object(client.func({
        '@type': 'reportMessageReactions',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'sender_id': to_json(sender_id),
    }))


def reportStory(story_sender_chat_id: int = None, story_id: int = None, reason: ReportReason = None, text: str = None, ):
    return get_object(client.func({
        '@type': 'reportStory',
        'story_sender_chat_id': to_json(story_sender_chat_id),
        'story_id': to_json(story_id),
        'reason': to_json(reason),
        'text': to_json(text),
    }))


def reportSupergroupAntiSpamFalsePositive(supergroup_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'reportSupergroupAntiSpamFalsePositive',
        'supergroup_id': to_json(supergroup_id),
        'message_id': to_json(message_id),
    }))


def reportSupergroupSpam(supergroup_id: int = None, message_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'reportSupergroupSpam',
        'supergroup_id': to_json(supergroup_id),
        'message_ids': to_json(message_ids),
    }))


def requestAuthenticationPasswordRecovery():
    return get_object(client.func({
        '@type': 'requestAuthenticationPasswordRecovery',
    }))


def requestPasswordRecovery():
    return get_object(client.func({
        '@type': 'requestPasswordRecovery',
    }))


def requestQrCodeAuthentication(other_user_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'requestQrCodeAuthentication',
        'other_user_ids': to_json(other_user_ids),
    }))


def resendAuthenticationCode():
    return get_object(client.func({
        '@type': 'resendAuthenticationCode',
    }))


def resendChangePhoneNumberCode():
    return get_object(client.func({
        '@type': 'resendChangePhoneNumberCode',
    }))


def resendEmailAddressVerificationCode():
    return get_object(client.func({
        '@type': 'resendEmailAddressVerificationCode',
    }))


def resendLoginEmailAddressCode():
    return get_object(client.func({
        '@type': 'resendLoginEmailAddressCode',
    }))


def resendMessages(chat_id: int = None, message_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'resendMessages',
        'chat_id': to_json(chat_id),
        'message_ids': to_json(message_ids),
    }))


def resendPhoneNumberConfirmationCode():
    return get_object(client.func({
        '@type': 'resendPhoneNumberConfirmationCode',
    }))


def resendPhoneNumberVerificationCode():
    return get_object(client.func({
        '@type': 'resendPhoneNumberVerificationCode',
    }))


def resendRecoveryEmailAddressCode():
    return get_object(client.func({
        '@type': 'resendRecoveryEmailAddressCode',
    }))


def resetAllNotificationSettings():
    return get_object(client.func({
        '@type': 'resetAllNotificationSettings',
    }))


def resetAuthenticationEmailAddress():
    return get_object(client.func({
        '@type': 'resetAuthenticationEmailAddress',
    }))


def resetBackgrounds():
    return get_object(client.func({
        '@type': 'resetBackgrounds',
    }))


def resetNetworkStatistics():
    return get_object(client.func({
        '@type': 'resetNetworkStatistics',
    }))


def resetPassword():
    return get_object(client.func({
        '@type': 'resetPassword',
    }))


def revokeChatInviteLink(chat_id: int = None, invite_link: str = None, ):
    return get_object(client.func({
        '@type': 'revokeChatInviteLink',
        'chat_id': to_json(chat_id),
        'invite_link': to_json(invite_link),
    }))


def revokeGroupCallInviteLink(group_call_id: int = None, ):
    return get_object(client.func({
        '@type': 'revokeGroupCallInviteLink',
        'group_call_id': to_json(group_call_id),
    }))


def saveApplicationLogEvent(type: str = None, chat_id: int = None, data: JsonValue = None, ):
    return get_object(client.func({
        '@type': 'saveApplicationLogEvent',
        'type': to_json(type),
        'chat_id': to_json(chat_id),
        'data': to_json(data),
    }))


def searchBackground(name: str = None, ):
    return get_object(client.func({
        '@type': 'searchBackground',
        'name': to_json(name),
    }))


def searchCallMessages(offset: str = None, limit: int = None, only_missed: bool = None, ):
    return get_object(client.func({
        '@type': 'searchCallMessages',
        'offset': to_json(offset),
        'limit': to_json(limit),
        'only_missed': to_json(only_missed),
    }))


def searchChatMembers(chat_id: int = None, query: str = None, limit: int = None, filter: ChatMembersFilter = None, ):
    return get_object(client.func({
        '@type': 'searchChatMembers',
        'chat_id': to_json(chat_id),
        'query': to_json(query),
        'limit': to_json(limit),
        'filter': to_json(filter),
    }))


def searchChatMessages(chat_id: int = None, query: str = None, sender_id: MessageSender = None, from_message_id: int = None, offset: int = None, limit: int = None, filter: SearchMessagesFilter = None, message_thread_id: int = None, ):
    return get_object(client.func({
        '@type': 'searchChatMessages',
        'chat_id': to_json(chat_id),
        'query': to_json(query),
        'sender_id': to_json(sender_id),
        'from_message_id': to_json(from_message_id),
        'offset': to_json(offset),
        'limit': to_json(limit),
        'filter': to_json(filter),
        'message_thread_id': to_json(message_thread_id),
    }))


def searchChatRecentLocationMessages(chat_id: int = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchChatRecentLocationMessages',
        'chat_id': to_json(chat_id),
        'limit': to_json(limit),
    }))


def searchChats(query: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchChats',
        'query': to_json(query),
        'limit': to_json(limit),
    }))


def searchChatsNearby(location: Location = None, ):
    return get_object(client.func({
        '@type': 'searchChatsNearby',
        'location': to_json(location),
    }))


def searchChatsOnServer(query: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchChatsOnServer',
        'query': to_json(query),
        'limit': to_json(limit),
    }))


def searchContacts(query: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchContacts',
        'query': to_json(query),
        'limit': to_json(limit),
    }))


def searchEmojis(text: str = None, exact_match: bool = None, input_language_codes: list[str] = None, ):
    return get_object(client.func({
        '@type': 'searchEmojis',
        'text': to_json(text),
        'exact_match': to_json(exact_match),
        'input_language_codes': to_json(input_language_codes),
    }))


def searchFileDownloads(query: str = None, only_active: bool = None, only_completed: bool = None, offset: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchFileDownloads',
        'query': to_json(query),
        'only_active': to_json(only_active),
        'only_completed': to_json(only_completed),
        'offset': to_json(offset),
        'limit': to_json(limit),
    }))


def searchHashtags(prefix: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchHashtags',
        'prefix': to_json(prefix),
        'limit': to_json(limit),
    }))


def searchInstalledStickerSets(sticker_type: StickerType = None, query: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchInstalledStickerSets',
        'sticker_type': to_json(sticker_type),
        'query': to_json(query),
        'limit': to_json(limit),
    }))


def searchMessages(chat_list: ChatList = None, query: str = None, offset: str = None, limit: int = None, filter: SearchMessagesFilter = None, min_date: int = None, max_date: int = None, ):
    return get_object(client.func({
        '@type': 'searchMessages',
        'chat_list': to_json(chat_list),
        'query': to_json(query),
        'offset': to_json(offset),
        'limit': to_json(limit),
        'filter': to_json(filter),
        'min_date': to_json(min_date),
        'max_date': to_json(max_date),
    }))


def searchOutgoingDocumentMessages(query: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchOutgoingDocumentMessages',
        'query': to_json(query),
        'limit': to_json(limit),
    }))


def searchPublicChat(username: str = None, ):
    return get_object(client.func({
        '@type': 'searchPublicChat',
        'username': to_json(username),
    }))


def searchPublicChats(query: str = None, ):
    return get_object(client.func({
        '@type': 'searchPublicChats',
        'query': to_json(query),
    }))


def searchRecentlyFoundChats(query: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchRecentlyFoundChats',
        'query': to_json(query),
        'limit': to_json(limit),
    }))


def searchSecretMessages(chat_id: int = None, query: str = None, offset: str = None, limit: int = None, filter: SearchMessagesFilter = None, ):
    return get_object(client.func({
        '@type': 'searchSecretMessages',
        'chat_id': to_json(chat_id),
        'query': to_json(query),
        'offset': to_json(offset),
        'limit': to_json(limit),
        'filter': to_json(filter),
    }))


def searchStickerSet(name: str = None, ):
    return get_object(client.func({
        '@type': 'searchStickerSet',
        'name': to_json(name),
    }))


def searchStickerSets(query: str = None, ):
    return get_object(client.func({
        '@type': 'searchStickerSets',
        'query': to_json(query),
    }))


def searchStickers(sticker_type: StickerType = None, emojis: str = None, limit: int = None, ):
    return get_object(client.func({
        '@type': 'searchStickers',
        'sticker_type': to_json(sticker_type),
        'emojis': to_json(emojis),
        'limit': to_json(limit),
    }))


def searchStringsByPrefix(strings: list[str] = None, query: str = None, limit: int = None, return_none_for_empty_query: bool = None, ):
    return get_object(client.func({
        '@type': 'searchStringsByPrefix',
        'strings': to_json(strings),
        'query': to_json(query),
        'limit': to_json(limit),
        'return_none_for_empty_query': to_json(return_none_for_empty_query),
    }))


def searchUserByPhoneNumber(phone_number: str = None, ):
    return get_object(client.func({
        '@type': 'searchUserByPhoneNumber',
        'phone_number': to_json(phone_number),
    }))


def searchUserByToken(token: str = None, ):
    return get_object(client.func({
        '@type': 'searchUserByToken',
        'token': to_json(token),
    }))


def searchWebApp(bot_user_id: int = None, web_app_short_name: str = None, ):
    return get_object(client.func({
        '@type': 'searchWebApp',
        'bot_user_id': to_json(bot_user_id),
        'web_app_short_name': to_json(web_app_short_name),
    }))


def sendAuthenticationFirebaseSms(token: str = None, ):
    return get_object(client.func({
        '@type': 'sendAuthenticationFirebaseSms',
        'token': to_json(token),
    }))


def sendBotStartMessage(bot_user_id: int = None, chat_id: int = None, parameter: str = None, ):
    return get_object(client.func({
        '@type': 'sendBotStartMessage',
        'bot_user_id': to_json(bot_user_id),
        'chat_id': to_json(chat_id),
        'parameter': to_json(parameter),
    }))


def sendCallDebugInformation(call_id: int = None, debug_information: str = None, ):
    return get_object(client.func({
        '@type': 'sendCallDebugInformation',
        'call_id': to_json(call_id),
        'debug_information': to_json(debug_information),
    }))


def sendCallLog(call_id: int = None, log_file: InputFile = None, ):
    return get_object(client.func({
        '@type': 'sendCallLog',
        'call_id': to_json(call_id),
        'log_file': to_json(log_file),
    }))


def sendCallRating(call_id: int = None, rating: int = None, comment: str = None, problems: list[CallProblem] = None, ):
    return get_object(client.func({
        '@type': 'sendCallRating',
        'call_id': to_json(call_id),
        'rating': to_json(rating),
        'comment': to_json(comment),
        'problems': to_json(problems),
    }))


def sendCallSignalingData(call_id: int = None, data: bytes = None, ):
    return get_object(client.func({
        '@type': 'sendCallSignalingData',
        'call_id': to_json(call_id),
        'data': to_json(data),
    }))


def sendChatAction(chat_id: int = None, message_thread_id: int = None, action: ChatAction = None, ):
    return get_object(client.func({
        '@type': 'sendChatAction',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'action': to_json(action),
    }))


def sendCustomRequest(method: str = None, parameters: str = None, ):
    return get_object(client.func({
        '@type': 'sendCustomRequest',
        'method': to_json(method),
        'parameters': to_json(parameters),
    }))


def sendEmailAddressVerificationCode(email_address: str = None, ):
    return get_object(client.func({
        '@type': 'sendEmailAddressVerificationCode',
        'email_address': to_json(email_address),
    }))


def sendInlineQueryResultMessage(chat_id: int = None, message_thread_id: int = None, reply_to: MessageReplyTo = None, options: MessageSendOptions = None, query_id: int = None, result_id: str = None, hide_via_bot: bool = None, ):
    return get_object(client.func({
        '@type': 'sendInlineQueryResultMessage',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'reply_to': to_json(reply_to),
        'options': to_json(options),
        'query_id': to_json(query_id),
        'result_id': to_json(result_id),
        'hide_via_bot': to_json(hide_via_bot),
    }))


def sendMessage(chat_id: int = None, message_thread_id: int = None, reply_to: MessageReplyTo = None, options: MessageSendOptions = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None, ):
    return get_object(client.func({
        '@type': 'sendMessage',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'reply_to': to_json(reply_to),
        'options': to_json(options),
        'reply_markup': to_json(reply_markup),
        'input_message_content': to_json(input_message_content),
    }))


def sendMessageAlbum(chat_id: int = None, message_thread_id: int = None, reply_to: MessageReplyTo = None, options: MessageSendOptions = None, input_message_contents: list[InputMessageContent] = None, only_preview: bool = None, ):
    return get_object(client.func({
        '@type': 'sendMessageAlbum',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'reply_to': to_json(reply_to),
        'options': to_json(options),
        'input_message_contents': to_json(input_message_contents),
        'only_preview': to_json(only_preview),
    }))


def sendPassportAuthorizationForm(authorization_form_id: int = None, types: list[PassportElementType] = None, ):
    return get_object(client.func({
        '@type': 'sendPassportAuthorizationForm',
        'authorization_form_id': to_json(authorization_form_id),
        'types': to_json(types),
    }))


def sendPaymentForm(input_invoice: InputInvoice = None, payment_form_id: int = None, order_info_id: str = None, shipping_option_id: str = None, credentials: InputCredentials = None, tip_amount: int = None, ):
    return get_object(client.func({
        '@type': 'sendPaymentForm',
        'input_invoice': to_json(input_invoice),
        'payment_form_id': to_json(payment_form_id),
        'order_info_id': to_json(order_info_id),
        'shipping_option_id': to_json(shipping_option_id),
        'credentials': to_json(credentials),
        'tip_amount': to_json(tip_amount),
    }))


def sendPhoneNumberConfirmationCode(hash: str = None, phone_number: str = None, settings: PhoneNumberAuthenticationSettings = None, ):
    return get_object(client.func({
        '@type': 'sendPhoneNumberConfirmationCode',
        'hash': to_json(hash),
        'phone_number': to_json(phone_number),
        'settings': to_json(settings),
    }))


def sendPhoneNumberVerificationCode(phone_number: str = None, settings: PhoneNumberAuthenticationSettings = None, ):
    return get_object(client.func({
        '@type': 'sendPhoneNumberVerificationCode',
        'phone_number': to_json(phone_number),
        'settings': to_json(settings),
    }))


def sendStory(content: InputStoryContent = None, areas: InputStoryAreas = None, caption: FormattedText = None, privacy_settings: StoryPrivacySettings = None, active_period: int = None, is_pinned: bool = None, protect_content: bool = None, ):
    return get_object(client.func({
        '@type': 'sendStory',
        'content': to_json(content),
        'areas': to_json(areas),
        'caption': to_json(caption),
        'privacy_settings': to_json(privacy_settings),
        'active_period': to_json(active_period),
        'is_pinned': to_json(is_pinned),
        'protect_content': to_json(protect_content),
    }))


def sendWebAppCustomRequest(bot_user_id: int = None, method: str = None, parameters: str = None, ):
    return get_object(client.func({
        '@type': 'sendWebAppCustomRequest',
        'bot_user_id': to_json(bot_user_id),
        'method': to_json(method),
        'parameters': to_json(parameters),
    }))


def sendWebAppData(bot_user_id: int = None, button_text: str = None, data: str = None, ):
    return get_object(client.func({
        '@type': 'sendWebAppData',
        'bot_user_id': to_json(bot_user_id),
        'button_text': to_json(button_text),
        'data': to_json(data),
    }))


def setAccountTtl(ttl: AccountTtl = None, ):
    return get_object(client.func({
        '@type': 'setAccountTtl',
        'ttl': to_json(ttl),
    }))


def setAlarm(seconds: float = None, ):
    return get_object(client.func({
        '@type': 'setAlarm',
        'seconds': to_json(seconds),
    }))


def setArchiveChatListSettings(settings: ArchiveChatListSettings = None, ):
    return get_object(client.func({
        '@type': 'setArchiveChatListSettings',
        'settings': to_json(settings),
    }))


def setAuthenticationEmailAddress(email_address: str = None, ):
    return get_object(client.func({
        '@type': 'setAuthenticationEmailAddress',
        'email_address': to_json(email_address),
    }))


def setAuthenticationPhoneNumber(phone_number: str = None, settings: PhoneNumberAuthenticationSettings = None, ):
    return get_object(client.func({
        '@type': 'setAuthenticationPhoneNumber',
        'phone_number': to_json(phone_number),
        'settings': to_json(settings),
    }))


def setAutoDownloadSettings(settings: AutoDownloadSettings = None, type: NetworkType = None, ):
    return get_object(client.func({
        '@type': 'setAutoDownloadSettings',
        'settings': to_json(settings),
        'type': to_json(type),
    }))


def setAutosaveSettings(scope: AutosaveSettingsScope = None, settings: ScopeAutosaveSettings = None, ):
    return get_object(client.func({
        '@type': 'setAutosaveSettings',
        'scope': to_json(scope),
        'settings': to_json(settings),
    }))


def setBackground(background: InputBackground = None, type: BackgroundType = None, for_dark_theme: bool = None, ):
    return get_object(client.func({
        '@type': 'setBackground',
        'background': to_json(background),
        'type': to_json(type),
        'for_dark_theme': to_json(for_dark_theme),
    }))


def setBio(bio: str = None, ):
    return get_object(client.func({
        '@type': 'setBio',
        'bio': to_json(bio),
    }))


def setBotInfoDescription(bot_user_id: int = None, language_code: str = None, description: str = None, ):
    return get_object(client.func({
        '@type': 'setBotInfoDescription',
        'bot_user_id': to_json(bot_user_id),
        'language_code': to_json(language_code),
        'description': to_json(description),
    }))


def setBotInfoShortDescription(bot_user_id: int = None, language_code: str = None, short_description: str = None, ):
    return get_object(client.func({
        '@type': 'setBotInfoShortDescription',
        'bot_user_id': to_json(bot_user_id),
        'language_code': to_json(language_code),
        'short_description': to_json(short_description),
    }))


def setBotName(bot_user_id: int = None, language_code: str = None, name: str = None, ):
    return get_object(client.func({
        '@type': 'setBotName',
        'bot_user_id': to_json(bot_user_id),
        'language_code': to_json(language_code),
        'name': to_json(name),
    }))


def setBotProfilePhoto(bot_user_id: int = None, photo: InputChatPhoto = None, ):
    return get_object(client.func({
        '@type': 'setBotProfilePhoto',
        'bot_user_id': to_json(bot_user_id),
        'photo': to_json(photo),
    }))


def setBotUpdatesStatus(pending_update_count: int = None, error_message: str = None, ):
    return get_object(client.func({
        '@type': 'setBotUpdatesStatus',
        'pending_update_count': to_json(pending_update_count),
        'error_message': to_json(error_message),
    }))


def setChatActiveStoriesList(chat_id: int = None, story_list: StoryList = None, ):
    return get_object(client.func({
        '@type': 'setChatActiveStoriesList',
        'chat_id': to_json(chat_id),
        'story_list': to_json(story_list),
    }))


def setChatAvailableReactions(chat_id: int = None, available_reactions: ChatAvailableReactions = None, ):
    return get_object(client.func({
        '@type': 'setChatAvailableReactions',
        'chat_id': to_json(chat_id),
        'available_reactions': to_json(available_reactions),
    }))


def setChatBackground(chat_id: int = None, background: InputBackground = None, type: BackgroundType = None, dark_theme_dimming: int = None, ):
    return get_object(client.func({
        '@type': 'setChatBackground',
        'chat_id': to_json(chat_id),
        'background': to_json(background),
        'type': to_json(type),
        'dark_theme_dimming': to_json(dark_theme_dimming),
    }))


def setChatClientData(chat_id: int = None, client_data: str = None, ):
    return get_object(client.func({
        '@type': 'setChatClientData',
        'chat_id': to_json(chat_id),
        'client_data': to_json(client_data),
    }))


def setChatDescription(chat_id: int = None, description: str = None, ):
    return get_object(client.func({
        '@type': 'setChatDescription',
        'chat_id': to_json(chat_id),
        'description': to_json(description),
    }))


def setChatDiscussionGroup(chat_id: int = None, discussion_chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'setChatDiscussionGroup',
        'chat_id': to_json(chat_id),
        'discussion_chat_id': to_json(discussion_chat_id),
    }))


def setChatDraftMessage(chat_id: int = None, message_thread_id: int = None, draft_message: DraftMessage = None, ):
    return get_object(client.func({
        '@type': 'setChatDraftMessage',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'draft_message': to_json(draft_message),
    }))


def setChatLocation(chat_id: int = None, location: ChatLocation = None, ):
    return get_object(client.func({
        '@type': 'setChatLocation',
        'chat_id': to_json(chat_id),
        'location': to_json(location),
    }))


def setChatMemberStatus(chat_id: int = None, member_id: MessageSender = None, status: ChatMemberStatus = None, ):
    return get_object(client.func({
        '@type': 'setChatMemberStatus',
        'chat_id': to_json(chat_id),
        'member_id': to_json(member_id),
        'status': to_json(status),
    }))


def setChatMessageAutoDeleteTime(chat_id: int = None, message_auto_delete_time: int = None, ):
    return get_object(client.func({
        '@type': 'setChatMessageAutoDeleteTime',
        'chat_id': to_json(chat_id),
        'message_auto_delete_time': to_json(message_auto_delete_time),
    }))


def setChatMessageSender(chat_id: int = None, message_sender_id: MessageSender = None, ):
    return get_object(client.func({
        '@type': 'setChatMessageSender',
        'chat_id': to_json(chat_id),
        'message_sender_id': to_json(message_sender_id),
    }))


def setChatNotificationSettings(chat_id: int = None, notification_settings: ChatNotificationSettings = None, ):
    return get_object(client.func({
        '@type': 'setChatNotificationSettings',
        'chat_id': to_json(chat_id),
        'notification_settings': to_json(notification_settings),
    }))


def setChatPermissions(chat_id: int = None, permissions: ChatPermissions = None, ):
    return get_object(client.func({
        '@type': 'setChatPermissions',
        'chat_id': to_json(chat_id),
        'permissions': to_json(permissions),
    }))


def setChatPhoto(chat_id: int = None, photo: InputChatPhoto = None, ):
    return get_object(client.func({
        '@type': 'setChatPhoto',
        'chat_id': to_json(chat_id),
        'photo': to_json(photo),
    }))


def setChatSlowModeDelay(chat_id: int = None, slow_mode_delay: int = None, ):
    return get_object(client.func({
        '@type': 'setChatSlowModeDelay',
        'chat_id': to_json(chat_id),
        'slow_mode_delay': to_json(slow_mode_delay),
    }))


def setChatTheme(chat_id: int = None, theme_name: str = None, ):
    return get_object(client.func({
        '@type': 'setChatTheme',
        'chat_id': to_json(chat_id),
        'theme_name': to_json(theme_name),
    }))


def setChatTitle(chat_id: int = None, title: str = None, ):
    return get_object(client.func({
        '@type': 'setChatTitle',
        'chat_id': to_json(chat_id),
        'title': to_json(title),
    }))


def setCloseFriends(user_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'setCloseFriends',
        'user_ids': to_json(user_ids),
    }))


def setCommands(scope: BotCommandScope = None, language_code: str = None, commands: list[BotCommand] = None, ):
    return get_object(client.func({
        '@type': 'setCommands',
        'scope': to_json(scope),
        'language_code': to_json(language_code),
        'commands': to_json(commands),
    }))


def setCustomEmojiStickerSetThumbnail(name: str = None, custom_emoji_id: int = None, ):
    return get_object(client.func({
        '@type': 'setCustomEmojiStickerSetThumbnail',
        'name': to_json(name),
        'custom_emoji_id': to_json(custom_emoji_id),
    }))


def setCustomLanguagePack(info: LanguagePackInfo = None, strings: list[LanguagePackString] = None, ):
    return get_object(client.func({
        '@type': 'setCustomLanguagePack',
        'info': to_json(info),
        'strings': to_json(strings),
    }))


def setCustomLanguagePackString(language_pack_id: str = None, new_string: LanguagePackString = None, ):
    return get_object(client.func({
        '@type': 'setCustomLanguagePackString',
        'language_pack_id': to_json(language_pack_id),
        'new_string': to_json(new_string),
    }))


def setDatabaseEncryptionKey(new_encryption_key: bytes = None, ):
    return get_object(client.func({
        '@type': 'setDatabaseEncryptionKey',
        'new_encryption_key': to_json(new_encryption_key),
    }))


def setDefaultChannelAdministratorRights(default_channel_administrator_rights: ChatAdministratorRights = None, ):
    return get_object(client.func({
        '@type': 'setDefaultChannelAdministratorRights',
        'default_channel_administrator_rights': to_json(default_channel_administrator_rights),
    }))


def setDefaultGroupAdministratorRights(default_group_administrator_rights: ChatAdministratorRights = None, ):
    return get_object(client.func({
        '@type': 'setDefaultGroupAdministratorRights',
        'default_group_administrator_rights': to_json(default_group_administrator_rights),
    }))


def setDefaultMessageAutoDeleteTime(message_auto_delete_time: MessageAutoDeleteTime = None, ):
    return get_object(client.func({
        '@type': 'setDefaultMessageAutoDeleteTime',
        'message_auto_delete_time': to_json(message_auto_delete_time),
    }))


def setDefaultReactionType(reaction_type: ReactionType = None, ):
    return get_object(client.func({
        '@type': 'setDefaultReactionType',
        'reaction_type': to_json(reaction_type),
    }))


def setEmojiStatus(emoji_status: EmojiStatus = None, ):
    return get_object(client.func({
        '@type': 'setEmojiStatus',
        'emoji_status': to_json(emoji_status),
    }))


def setFileGenerationProgress(generation_id: int = None, expected_size: int = None, local_prefix_size: int = None, ):
    return get_object(client.func({
        '@type': 'setFileGenerationProgress',
        'generation_id': to_json(generation_id),
        'expected_size': to_json(expected_size),
        'local_prefix_size': to_json(local_prefix_size),
    }))


def setForumTopicNotificationSettings(chat_id: int = None, message_thread_id: int = None, notification_settings: ChatNotificationSettings = None, ):
    return get_object(client.func({
        '@type': 'setForumTopicNotificationSettings',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'notification_settings': to_json(notification_settings),
    }))


def setGameScore(chat_id: int = None, message_id: int = None, edit_message: bool = None, user_id: int = None, score: int = None, force: bool = None, ):
    return get_object(client.func({
        '@type': 'setGameScore',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'edit_message': to_json(edit_message),
        'user_id': to_json(user_id),
        'score': to_json(score),
        'force': to_json(force),
    }))


def setGroupCallParticipantIsSpeaking(group_call_id: int = None, audio_source: int = None, is_speaking: bool = None, ):
    return get_object(client.func({
        '@type': 'setGroupCallParticipantIsSpeaking',
        'group_call_id': to_json(group_call_id),
        'audio_source': to_json(audio_source),
        'is_speaking': to_json(is_speaking),
    }))


def setGroupCallParticipantVolumeLevel(group_call_id: int = None, participant_id: MessageSender = None, volume_level: int = None, ):
    return get_object(client.func({
        '@type': 'setGroupCallParticipantVolumeLevel',
        'group_call_id': to_json(group_call_id),
        'participant_id': to_json(participant_id),
        'volume_level': to_json(volume_level),
    }))


def setGroupCallTitle(group_call_id: int = None, title: str = None, ):
    return get_object(client.func({
        '@type': 'setGroupCallTitle',
        'group_call_id': to_json(group_call_id),
        'title': to_json(title),
    }))


def setInactiveSessionTtl(inactive_session_ttl_days: int = None, ):
    return get_object(client.func({
        '@type': 'setInactiveSessionTtl',
        'inactive_session_ttl_days': to_json(inactive_session_ttl_days),
    }))


def setInlineGameScore(inline_message_id: str = None, edit_message: bool = None, user_id: int = None, score: int = None, force: bool = None, ):
    return get_object(client.func({
        '@type': 'setInlineGameScore',
        'inline_message_id': to_json(inline_message_id),
        'edit_message': to_json(edit_message),
        'user_id': to_json(user_id),
        'score': to_json(score),
        'force': to_json(force),
    }))


def setLocation(location: Location = None, ):
    return get_object(client.func({
        '@type': 'setLocation',
        'location': to_json(location),
    }))


def setLogStream(log_stream: LogStream = None, ):
    return get_object(client.func({
        '@type': 'setLogStream',
        'log_stream': to_json(log_stream),
    }))


def setLogTagVerbosityLevel(tag: str = None, new_verbosity_level: int = None, ):
    return get_object(client.func({
        '@type': 'setLogTagVerbosityLevel',
        'tag': to_json(tag),
        'new_verbosity_level': to_json(new_verbosity_level),
    }))


def setLogVerbosityLevel(new_verbosity_level: int = None, ):
    return get_object(client.func({
        '@type': 'setLogVerbosityLevel',
        'new_verbosity_level': to_json(new_verbosity_level),
    }))


def setLoginEmailAddress(new_login_email_address: str = None, ):
    return get_object(client.func({
        '@type': 'setLoginEmailAddress',
        'new_login_email_address': to_json(new_login_email_address),
    }))


def setMenuButton(user_id: int = None, menu_button: BotMenuButton = None, ):
    return get_object(client.func({
        '@type': 'setMenuButton',
        'user_id': to_json(user_id),
        'menu_button': to_json(menu_button),
    }))


def setMessageSenderBlockList(sender_id: MessageSender = None, block_list: BlockList = None, ):
    return get_object(client.func({
        '@type': 'setMessageSenderBlockList',
        'sender_id': to_json(sender_id),
        'block_list': to_json(block_list),
    }))


def setName(first_name: str = None, last_name: str = None, ):
    return get_object(client.func({
        '@type': 'setName',
        'first_name': to_json(first_name),
        'last_name': to_json(last_name),
    }))


def setNetworkType(type: NetworkType = None, ):
    return get_object(client.func({
        '@type': 'setNetworkType',
        'type': to_json(type),
    }))


def setOption(name: str = None, value: OptionValue = None, ):
    return get_object(client.func({
        '@type': 'setOption',
        'name': to_json(name),
        'value': to_json(value),
    }))


def setPassportElement(element: InputPassportElement = None, password: str = None, ):
    return get_object(client.func({
        '@type': 'setPassportElement',
        'element': to_json(element),
        'password': to_json(password),
    }))


def setPassportElementErrors(user_id: int = None, errors: list[InputPassportElementError] = None, ):
    return get_object(client.func({
        '@type': 'setPassportElementErrors',
        'user_id': to_json(user_id),
        'errors': to_json(errors),
    }))


def setPassword(old_password: str = None, new_password: str = None, new_hint: str = None, set_recovery_email_address: bool = None, new_recovery_email_address: str = None, ):
    return get_object(client.func({
        '@type': 'setPassword',
        'old_password': to_json(old_password),
        'new_password': to_json(new_password),
        'new_hint': to_json(new_hint),
        'set_recovery_email_address': to_json(set_recovery_email_address),
        'new_recovery_email_address': to_json(new_recovery_email_address),
    }))


def setPinnedChats(chat_list: ChatList = None, chat_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'setPinnedChats',
        'chat_list': to_json(chat_list),
        'chat_ids': to_json(chat_ids),
    }))


def setPinnedForumTopics(chat_id: int = None, message_thread_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'setPinnedForumTopics',
        'chat_id': to_json(chat_id),
        'message_thread_ids': to_json(message_thread_ids),
    }))


def setPollAnswer(chat_id: int = None, message_id: int = None, option_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'setPollAnswer',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'option_ids': to_json(option_ids),
    }))


def setProfilePhoto(photo: InputChatPhoto = None, is_public: bool = None, ):
    return get_object(client.func({
        '@type': 'setProfilePhoto',
        'photo': to_json(photo),
        'is_public': to_json(is_public),
    }))


def setRecoveryEmailAddress(password: str = None, new_recovery_email_address: str = None, ):
    return get_object(client.func({
        '@type': 'setRecoveryEmailAddress',
        'password': to_json(password),
        'new_recovery_email_address': to_json(new_recovery_email_address),
    }))


def setScopeNotificationSettings(scope: NotificationSettingsScope = None, notification_settings: ScopeNotificationSettings = None, ):
    return get_object(client.func({
        '@type': 'setScopeNotificationSettings',
        'scope': to_json(scope),
        'notification_settings': to_json(notification_settings),
    }))


def setStickerEmojis(sticker: InputFile = None, emojis: str = None, ):
    return get_object(client.func({
        '@type': 'setStickerEmojis',
        'sticker': to_json(sticker),
        'emojis': to_json(emojis),
    }))


def setStickerKeywords(sticker: InputFile = None, keywords: list[str] = None, ):
    return get_object(client.func({
        '@type': 'setStickerKeywords',
        'sticker': to_json(sticker),
        'keywords': to_json(keywords),
    }))


def setStickerMaskPosition(sticker: InputFile = None, mask_position: MaskPosition = None, ):
    return get_object(client.func({
        '@type': 'setStickerMaskPosition',
        'sticker': to_json(sticker),
        'mask_position': to_json(mask_position),
    }))


def setStickerPositionInSet(sticker: InputFile = None, position: int = None, ):
    return get_object(client.func({
        '@type': 'setStickerPositionInSet',
        'sticker': to_json(sticker),
        'position': to_json(position),
    }))


def setStickerSetThumbnail(user_id: int = None, name: str = None, thumbnail: InputFile = None, ):
    return get_object(client.func({
        '@type': 'setStickerSetThumbnail',
        'user_id': to_json(user_id),
        'name': to_json(name),
        'thumbnail': to_json(thumbnail),
    }))


def setStickerSetTitle(name: str = None, title: str = None, ):
    return get_object(client.func({
        '@type': 'setStickerSetTitle',
        'name': to_json(name),
        'title': to_json(title),
    }))


def setStoryPrivacySettings(story_id: int = None, privacy_settings: StoryPrivacySettings = None, ):
    return get_object(client.func({
        '@type': 'setStoryPrivacySettings',
        'story_id': to_json(story_id),
        'privacy_settings': to_json(privacy_settings),
    }))


def setStoryReaction(story_sender_chat_id: int = None, story_id: int = None, reaction_type: ReactionType = None, update_recent_reactions: bool = None, ):
    return get_object(client.func({
        '@type': 'setStoryReaction',
        'story_sender_chat_id': to_json(story_sender_chat_id),
        'story_id': to_json(story_id),
        'reaction_type': to_json(reaction_type),
        'update_recent_reactions': to_json(update_recent_reactions),
    }))


def setSupergroupStickerSet(supergroup_id: int = None, sticker_set_id: int = None, ):
    return get_object(client.func({
        '@type': 'setSupergroupStickerSet',
        'supergroup_id': to_json(supergroup_id),
        'sticker_set_id': to_json(sticker_set_id),
    }))


def setSupergroupUsername(supergroup_id: int = None, username: str = None, ):
    return get_object(client.func({
        '@type': 'setSupergroupUsername',
        'supergroup_id': to_json(supergroup_id),
        'username': to_json(username),
    }))


def setTdlibParameters(use_test_dc: bool = None, database_directory: str = None, files_directory: str = None, database_encryption_key: bytes = None, use_file_database: bool = None, use_chat_info_database: bool = None, use_message_database: bool = None, use_secret_chats: bool = None, api_id: int = None, api_hash: str = None, system_language_code: str = None, device_model: str = None, system_version: str = None, application_version: str = None, enable_storage_optimizer: bool = None, ignore_file_names: bool = None, ):
    return get_object(client.func({
        '@type': 'setTdlibParameters',
        'use_test_dc': to_json(use_test_dc),
        'database_directory': to_json(database_directory),
        'files_directory': to_json(files_directory),
        'database_encryption_key': to_json(database_encryption_key),
        'use_file_database': to_json(use_file_database),
        'use_chat_info_database': to_json(use_chat_info_database),
        'use_message_database': to_json(use_message_database),
        'use_secret_chats': to_json(use_secret_chats),
        'api_id': to_json(api_id),
        'api_hash': to_json(api_hash),
        'system_language_code': to_json(system_language_code),
        'device_model': to_json(device_model),
        'system_version': to_json(system_version),
        'application_version': to_json(application_version),
        'enable_storage_optimizer': to_json(enable_storage_optimizer),
        'ignore_file_names': to_json(ignore_file_names),
    }))


def setUserPersonalProfilePhoto(user_id: int = None, photo: InputChatPhoto = None, ):
    return get_object(client.func({
        '@type': 'setUserPersonalProfilePhoto',
        'user_id': to_json(user_id),
        'photo': to_json(photo),
    }))


def setUserPrivacySettingRules(setting: UserPrivacySetting = None, rules: UserPrivacySettingRules = None, ):
    return get_object(client.func({
        '@type': 'setUserPrivacySettingRules',
        'setting': to_json(setting),
        'rules': to_json(rules),
    }))


def setUserSupportInfo(user_id: int = None, message: FormattedText = None, ):
    return get_object(client.func({
        '@type': 'setUserSupportInfo',
        'user_id': to_json(user_id),
        'message': to_json(message),
    }))


def setUsername(username: str = None, ):
    return get_object(client.func({
        '@type': 'setUsername',
        'username': to_json(username),
    }))


def setVideoChatDefaultParticipant(chat_id: int = None, default_participant_id: MessageSender = None, ):
    return get_object(client.func({
        '@type': 'setVideoChatDefaultParticipant',
        'chat_id': to_json(chat_id),
        'default_participant_id': to_json(default_participant_id),
    }))


def shareChatWithBot(chat_id: int = None, message_id: int = None, button_id: int = None, shared_chat_id: int = None, only_check: bool = None, ):
    return get_object(client.func({
        '@type': 'shareChatWithBot',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'button_id': to_json(button_id),
        'shared_chat_id': to_json(shared_chat_id),
        'only_check': to_json(only_check),
    }))


def sharePhoneNumber(user_id: int = None, ):
    return get_object(client.func({
        '@type': 'sharePhoneNumber',
        'user_id': to_json(user_id),
    }))


def shareUserWithBot(chat_id: int = None, message_id: int = None, button_id: int = None, shared_user_id: int = None, only_check: bool = None, ):
    return get_object(client.func({
        '@type': 'shareUserWithBot',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'button_id': to_json(button_id),
        'shared_user_id': to_json(shared_user_id),
        'only_check': to_json(only_check),
    }))


def startGroupCallRecording(group_call_id: int = None, title: str = None, record_video: bool = None, use_portrait_orientation: bool = None, ):
    return get_object(client.func({
        '@type': 'startGroupCallRecording',
        'group_call_id': to_json(group_call_id),
        'title': to_json(title),
        'record_video': to_json(record_video),
        'use_portrait_orientation': to_json(use_portrait_orientation),
    }))


def startGroupCallScreenSharing(group_call_id: int = None, audio_source_id: int = None, payload: str = None, ):
    return get_object(client.func({
        '@type': 'startGroupCallScreenSharing',
        'group_call_id': to_json(group_call_id),
        'audio_source_id': to_json(audio_source_id),
        'payload': to_json(payload),
    }))


def startScheduledGroupCall(group_call_id: int = None, ):
    return get_object(client.func({
        '@type': 'startScheduledGroupCall',
        'group_call_id': to_json(group_call_id),
    }))


def stopPoll(chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, ):
    return get_object(client.func({
        '@type': 'stopPoll',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'reply_markup': to_json(reply_markup),
    }))


def suggestUserProfilePhoto(user_id: int = None, photo: InputChatPhoto = None, ):
    return get_object(client.func({
        '@type': 'suggestUserProfilePhoto',
        'user_id': to_json(user_id),
        'photo': to_json(photo),
    }))


def synchronizeLanguagePack(language_pack_id: str = None, ):
    return get_object(client.func({
        '@type': 'synchronizeLanguagePack',
        'language_pack_id': to_json(language_pack_id),
    }))


def terminateAllOtherSessions():
    return get_object(client.func({
        '@type': 'terminateAllOtherSessions',
    }))


def terminateSession(session_id: int = None, ):
    return get_object(client.func({
        '@type': 'terminateSession',
        'session_id': to_json(session_id),
    }))


def testCallBytes(x: bytes = None, ):
    return get_object(client.func({
        '@type': 'testCallBytes',
        'x': to_json(x),
    }))


def testCallEmpty():
    return get_object(client.func({
        '@type': 'testCallEmpty',
    }))


def testCallString(x: str = None, ):
    return get_object(client.func({
        '@type': 'testCallString',
        'x': to_json(x),
    }))


def testCallVectorInt(x: list[int] = None, ):
    return get_object(client.func({
        '@type': 'testCallVectorInt',
        'x': to_json(x),
    }))


def testCallVectorIntObject(x: list[TestInt] = None, ):
    return get_object(client.func({
        '@type': 'testCallVectorIntObject',
        'x': to_json(x),
    }))


def testCallVectorString(x: list[str] = None, ):
    return get_object(client.func({
        '@type': 'testCallVectorString',
        'x': to_json(x),
    }))


def testCallVectorStringObject(x: list[TestString] = None, ):
    return get_object(client.func({
        '@type': 'testCallVectorStringObject',
        'x': to_json(x),
    }))


def testGetDifference():
    return get_object(client.func({
        '@type': 'testGetDifference',
    }))


def testNetwork():
    return get_object(client.func({
        '@type': 'testNetwork',
    }))


def testProxy(server: str = None, port: int = None, type: ProxyType = None, dc_id: int = None, timeout: float = None, ):
    return get_object(client.func({
        '@type': 'testProxy',
        'server': to_json(server),
        'port': to_json(port),
        'type': to_json(type),
        'dc_id': to_json(dc_id),
        'timeout': to_json(timeout),
    }))


def testReturnError(error: Error = None, ):
    return get_object(client.func({
        '@type': 'testReturnError',
        'error': to_json(error),
    }))


def testSquareInt(x: int = None, ):
    return get_object(client.func({
        '@type': 'testSquareInt',
        'x': to_json(x),
    }))


def testUseUpdate():
    return get_object(client.func({
        '@type': 'testUseUpdate',
    }))


def toggleAllDownloadsArePaused(are_paused: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleAllDownloadsArePaused',
        'are_paused': to_json(are_paused),
    }))


def toggleBotIsAddedToAttachmentMenu(bot_user_id: int = None, is_added: bool = None, allow_write_access: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleBotIsAddedToAttachmentMenu',
        'bot_user_id': to_json(bot_user_id),
        'is_added': to_json(is_added),
        'allow_write_access': to_json(allow_write_access),
    }))


def toggleBotUsernameIsActive(bot_user_id: int = None, username: str = None, is_active: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleBotUsernameIsActive',
        'bot_user_id': to_json(bot_user_id),
        'username': to_json(username),
        'is_active': to_json(is_active),
    }))


def toggleChatDefaultDisableNotification(chat_id: int = None, default_disable_notification: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleChatDefaultDisableNotification',
        'chat_id': to_json(chat_id),
        'default_disable_notification': to_json(default_disable_notification),
    }))


def toggleChatHasProtectedContent(chat_id: int = None, has_protected_content: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleChatHasProtectedContent',
        'chat_id': to_json(chat_id),
        'has_protected_content': to_json(has_protected_content),
    }))


def toggleChatIsMarkedAsUnread(chat_id: int = None, is_marked_as_unread: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleChatIsMarkedAsUnread',
        'chat_id': to_json(chat_id),
        'is_marked_as_unread': to_json(is_marked_as_unread),
    }))


def toggleChatIsPinned(chat_list: ChatList = None, chat_id: int = None, is_pinned: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleChatIsPinned',
        'chat_list': to_json(chat_list),
        'chat_id': to_json(chat_id),
        'is_pinned': to_json(is_pinned),
    }))


def toggleChatIsTranslatable(chat_id: int = None, is_translatable: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleChatIsTranslatable',
        'chat_id': to_json(chat_id),
        'is_translatable': to_json(is_translatable),
    }))


def toggleDownloadIsPaused(file_id: int = None, is_paused: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleDownloadIsPaused',
        'file_id': to_json(file_id),
        'is_paused': to_json(is_paused),
    }))


def toggleForumTopicIsClosed(chat_id: int = None, message_thread_id: int = None, is_closed: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleForumTopicIsClosed',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'is_closed': to_json(is_closed),
    }))


def toggleForumTopicIsPinned(chat_id: int = None, message_thread_id: int = None, is_pinned: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleForumTopicIsPinned',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
        'is_pinned': to_json(is_pinned),
    }))


def toggleGeneralForumTopicIsHidden(chat_id: int = None, is_hidden: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleGeneralForumTopicIsHidden',
        'chat_id': to_json(chat_id),
        'is_hidden': to_json(is_hidden),
    }))


def toggleGroupCallEnabledStartNotification(group_call_id: int = None, enabled_start_notification: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleGroupCallEnabledStartNotification',
        'group_call_id': to_json(group_call_id),
        'enabled_start_notification': to_json(enabled_start_notification),
    }))


def toggleGroupCallIsMyVideoEnabled(group_call_id: int = None, is_my_video_enabled: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleGroupCallIsMyVideoEnabled',
        'group_call_id': to_json(group_call_id),
        'is_my_video_enabled': to_json(is_my_video_enabled),
    }))


def toggleGroupCallIsMyVideoPaused(group_call_id: int = None, is_my_video_paused: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleGroupCallIsMyVideoPaused',
        'group_call_id': to_json(group_call_id),
        'is_my_video_paused': to_json(is_my_video_paused),
    }))


def toggleGroupCallMuteNewParticipants(group_call_id: int = None, mute_new_participants: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleGroupCallMuteNewParticipants',
        'group_call_id': to_json(group_call_id),
        'mute_new_participants': to_json(mute_new_participants),
    }))


def toggleGroupCallParticipantIsHandRaised(group_call_id: int = None, participant_id: MessageSender = None, is_hand_raised: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleGroupCallParticipantIsHandRaised',
        'group_call_id': to_json(group_call_id),
        'participant_id': to_json(participant_id),
        'is_hand_raised': to_json(is_hand_raised),
    }))


def toggleGroupCallParticipantIsMuted(group_call_id: int = None, participant_id: MessageSender = None, is_muted: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleGroupCallParticipantIsMuted',
        'group_call_id': to_json(group_call_id),
        'participant_id': to_json(participant_id),
        'is_muted': to_json(is_muted),
    }))


def toggleGroupCallScreenSharingIsPaused(group_call_id: int = None, is_paused: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleGroupCallScreenSharingIsPaused',
        'group_call_id': to_json(group_call_id),
        'is_paused': to_json(is_paused),
    }))


def toggleSessionCanAcceptCalls(session_id: int = None, can_accept_calls: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSessionCanAcceptCalls',
        'session_id': to_json(session_id),
        'can_accept_calls': to_json(can_accept_calls),
    }))


def toggleSessionCanAcceptSecretChats(session_id: int = None, can_accept_secret_chats: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSessionCanAcceptSecretChats',
        'session_id': to_json(session_id),
        'can_accept_secret_chats': to_json(can_accept_secret_chats),
    }))


def toggleStoryIsPinned(story_id: int = None, is_pinned: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleStoryIsPinned',
        'story_id': to_json(story_id),
        'is_pinned': to_json(is_pinned),
    }))


def toggleSupergroupHasAggressiveAntiSpamEnabled(supergroup_id: int = None, has_aggressive_anti_spam_enabled: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupHasAggressiveAntiSpamEnabled',
        'supergroup_id': to_json(supergroup_id),
        'has_aggressive_anti_spam_enabled': to_json(has_aggressive_anti_spam_enabled),
    }))


def toggleSupergroupHasHiddenMembers(supergroup_id: int = None, has_hidden_members: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupHasHiddenMembers',
        'supergroup_id': to_json(supergroup_id),
        'has_hidden_members': to_json(has_hidden_members),
    }))


def toggleSupergroupIsAllHistoryAvailable(supergroup_id: int = None, is_all_history_available: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupIsAllHistoryAvailable',
        'supergroup_id': to_json(supergroup_id),
        'is_all_history_available': to_json(is_all_history_available),
    }))


def toggleSupergroupIsBroadcastGroup(supergroup_id: int = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupIsBroadcastGroup',
        'supergroup_id': to_json(supergroup_id),
    }))


def toggleSupergroupIsForum(supergroup_id: int = None, is_forum: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupIsForum',
        'supergroup_id': to_json(supergroup_id),
        'is_forum': to_json(is_forum),
    }))


def toggleSupergroupJoinByRequest(supergroup_id: int = None, join_by_request: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupJoinByRequest',
        'supergroup_id': to_json(supergroup_id),
        'join_by_request': to_json(join_by_request),
    }))


def toggleSupergroupJoinToSendMessages(supergroup_id: int = None, join_to_send_messages: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupJoinToSendMessages',
        'supergroup_id': to_json(supergroup_id),
        'join_to_send_messages': to_json(join_to_send_messages),
    }))


def toggleSupergroupSignMessages(supergroup_id: int = None, sign_messages: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupSignMessages',
        'supergroup_id': to_json(supergroup_id),
        'sign_messages': to_json(sign_messages),
    }))


def toggleSupergroupUsernameIsActive(supergroup_id: int = None, username: str = None, is_active: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleSupergroupUsernameIsActive',
        'supergroup_id': to_json(supergroup_id),
        'username': to_json(username),
        'is_active': to_json(is_active),
    }))


def toggleUsernameIsActive(username: str = None, is_active: bool = None, ):
    return get_object(client.func({
        '@type': 'toggleUsernameIsActive',
        'username': to_json(username),
        'is_active': to_json(is_active),
    }))


def transferChatOwnership(chat_id: int = None, user_id: int = None, password: str = None, ):
    return get_object(client.func({
        '@type': 'transferChatOwnership',
        'chat_id': to_json(chat_id),
        'user_id': to_json(user_id),
        'password': to_json(password),
    }))


def translateMessageText(chat_id: int = None, message_id: int = None, to_language_code: str = None, ):
    return get_object(client.func({
        '@type': 'translateMessageText',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
        'to_language_code': to_json(to_language_code),
    }))


def translateText(text: FormattedText = None, to_language_code: str = None, ):
    return get_object(client.func({
        '@type': 'translateText',
        'text': to_json(text),
        'to_language_code': to_json(to_language_code),
    }))


def unpinAllChatMessages(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'unpinAllChatMessages',
        'chat_id': to_json(chat_id),
    }))


def unpinAllMessageThreadMessages(chat_id: int = None, message_thread_id: int = None, ):
    return get_object(client.func({
        '@type': 'unpinAllMessageThreadMessages',
        'chat_id': to_json(chat_id),
        'message_thread_id': to_json(message_thread_id),
    }))


def unpinChatMessage(chat_id: int = None, message_id: int = None, ):
    return get_object(client.func({
        '@type': 'unpinChatMessage',
        'chat_id': to_json(chat_id),
        'message_id': to_json(message_id),
    }))


def upgradeBasicGroupChatToSupergroupChat(chat_id: int = None, ):
    return get_object(client.func({
        '@type': 'upgradeBasicGroupChatToSupergroupChat',
        'chat_id': to_json(chat_id),
    }))


def uploadStickerFile(user_id: int = None, sticker_format: StickerFormat = None, sticker: InputFile = None, ):
    return get_object(client.func({
        '@type': 'uploadStickerFile',
        'user_id': to_json(user_id),
        'sticker_format': to_json(sticker_format),
        'sticker': to_json(sticker),
    }))


def validateOrderInfo(input_invoice: InputInvoice = None, order_info: OrderInfo = None, allow_save: bool = None, ):
    return get_object(client.func({
        '@type': 'validateOrderInfo',
        'input_invoice': to_json(input_invoice),
        'order_info': to_json(order_info),
        'allow_save': to_json(allow_save),
    }))


def viewMessages(chat_id: int = None, message_ids: list[int] = None, source: MessageSource = None, force_read: bool = None, ):
    return get_object(client.func({
        '@type': 'viewMessages',
        'chat_id': to_json(chat_id),
        'message_ids': to_json(message_ids),
        'source': to_json(source),
        'force_read': to_json(force_read),
    }))


def viewPremiumFeature(feature: PremiumFeature = None, ):
    return get_object(client.func({
        '@type': 'viewPremiumFeature',
        'feature': to_json(feature),
    }))


def viewTrendingStickerSets(sticker_set_ids: list[int] = None, ):
    return get_object(client.func({
        '@type': 'viewTrendingStickerSets',
        'sticker_set_ids': to_json(sticker_set_ids),
    }))


def writeGeneratedFilePart(generation_id: int = None, offset: int = None, data: bytes = None, ):
    return get_object(client.func({
        '@type': 'writeGeneratedFilePart',
        'generation_id': to_json(generation_id),
        'offset': to_json(offset),
        'data': to_json(data),
    }))


