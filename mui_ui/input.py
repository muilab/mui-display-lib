
# mui touch panel event class
# -*- coding: utf-8 -*-

import sys
import asyncio
from evdev import InputDevice, categorize, ecodes, list_devices, KeyEvent, util, AbsInfo


EV_SYN = 0x00   # event type sync
SYN_REPORT = 0  # event code sync report

EV_KEY = 0x01       # event type key (touch down or up or hold)
BTN_TOUCH = 0x14a   # event code touch
VALUE_UP = 0        # evnet value up
VALUE_DOWN = 1      # event value down
VALUE_MOVE = 2      # event value move

EV_ABS = 0x03   # event type Axis postion report
ABS_X = 0x00    # event code Axis X
ABS_Y = 0x01    # event code Axis Y
ABS_PRESSURE = 24 # event code Pressure

EV_MSC = 0x04 # event type MSC
MSC_SERIAL = 0 # event code MSC_SERIAL

####
# Keys and buttons defination from Linux Kernel (input-event-codes.h)
####
#define KEY_RESERVED		0
#define KEY_ESC			1
#define KEY_1			2
#define KEY_2			3
#define KEY_3			4
#define KEY_4			5
#define KEY_5			6
#define KEY_6			7
#define KEY_7			8
#define KEY_8			9
#define KEY_9			10
#define KEY_0			11
#define KEY_MINUS		12
#define KEY_EQUAL		13
#define KEY_BACKSPACE		14
#define KEY_TAB			15
#define KEY_Q			16
#define KEY_W			17
#define KEY_E			18
#define KEY_R			19
#define KEY_T			20
#define KEY_Y			21
#define KEY_U			22
#define KEY_I			23
#define KEY_O			24
#define KEY_P			25
#define KEY_LEFTBRACE		26
#define KEY_RIGHTBRACE		27
#define KEY_ENTER		28
#define KEY_LEFTCTRL		29
#define KEY_A			30
#define KEY_S			31
#define KEY_D			32
#define KEY_F			33
#define KEY_G			34
#define KEY_H			35
#define KEY_J			36
#define KEY_K			37
#define KEY_L			38
#define KEY_SEMICOLON		39
#define KEY_APOSTROPHE		40
#define KEY_GRAVE		41
#define KEY_LEFTSHIFT		42
#define KEY_BACKSLASH		43
#define KEY_Z			44
#define KEY_X			45
#define KEY_C			46
#define KEY_V			47
#define KEY_B			48
#define KEY_N			49
#define KEY_M			50
#define KEY_COMMA		51
#define KEY_DOT			52
#define KEY_SLASH		53
#define KEY_RIGHTSHIFT		54
#define KEY_KPASTERISK		55
#define KEY_LEFTALT		56
#define KEY_SPACE		57
#define KEY_CAPSLOCK		58
#define KEY_F1			59
#define KEY_F2			60
#define KEY_F3			61
#define KEY_F4			62
#define KEY_F5			63
#define KEY_F6			64
#define KEY_F7			65
#define KEY_F8			66
#define KEY_F9			67
#define KEY_F10			68
#define KEY_NUMLOCK		69
#define KEY_SCROLLLOCK		70
#define KEY_KP7			71
#define KEY_KP8			72
#define KEY_KP9			73
#define KEY_KPMINUS		74
#define KEY_KP4			75
#define KEY_KP5			76
#define KEY_KP6			77
#define KEY_KPPLUS		78
#define KEY_KP1			79
#define KEY_KP2			80
#define KEY_KP3			81
#define KEY_KP0			82
#define KEY_KPDOT		83

#define KEY_ZENKAKUHANKAKU	85
#define KEY_102ND		86
#define KEY_F11			87
#define KEY_F12			88
#define KEY_RO			89
#define KEY_KATAKANA		90
#define KEY_HIRAGANA		91
#define KEY_HENKAN		92
#define KEY_KATAKANAHIRAGANA	93
#define KEY_MUHENKAN		94
#define KEY_KPJPCOMMA		95
#define KEY_KPENTER		96
#define KEY_RIGHTCTRL		97
#define KEY_KPSLASH		98
#define KEY_SYSRQ		99
#define KEY_RIGHTALT		100
#define KEY_LINEFEED		101
#define KEY_HOME		102
#define KEY_UP			103
#define KEY_PAGEUP		104
#define KEY_LEFT		105
#define KEY_RIGHT		106
#define KEY_END			107
#define KEY_DOWN		108
#define KEY_PAGEDOWN		109
#define KEY_INSERT		110
#define KEY_DELETE		111
#define KEY_MACRO		112
#define KEY_MUTE		113
#define KEY_VOLUMEDOWN		114
#define KEY_VOLUMEUP		115
#define KEY_POWER		116	/* SC System Power Down */
#define KEY_KPEQUAL		117
#define KEY_KPPLUSMINUS		118
#define KEY_PAUSE		119
#define KEY_SCALE		120	/* AL Compiz Scale (Expose) */

#define KEY_KPCOMMA		121
#define KEY_HANGEUL		122
#define KEY_HANGUEL		KEY_HANGEUL
#define KEY_HANJA		123
#define KEY_YEN			124
#define KEY_LEFTMETA		125
#define KEY_RIGHTMETA		126
#define KEY_COMPOSE		127

#define KEY_STOP		128	/* AC Stop */
#define KEY_AGAIN		129
#define KEY_PROPS		130	/* AC Properties */
#define KEY_UNDO		131	/* AC Undo */
#define KEY_FRONT		132
#define KEY_COPY		133	/* AC Copy */
#define KEY_OPEN		134	/* AC Open */
#define KEY_PASTE		135	/* AC Paste */
#define KEY_FIND		136	/* AC Search */
#define KEY_CUT			137	/* AC Cut */
#define KEY_HELP		138	/* AL Integrated Help Center */
#define KEY_MENU		139	/* Menu (show menu) */
#define KEY_CALC		140	/* AL Calculator */
#define KEY_SETUP		141
#define KEY_SLEEP		142	/* SC System Sleep */
#define KEY_WAKEUP		143	/* System Wake Up */
#define KEY_FILE		144	/* AL Local Machine Browser */
#define KEY_SENDFILE		145
#define KEY_DELETEFILE		146
#define KEY_XFER		147
#define KEY_PROG1		148
#define KEY_PROG2		149
#define KEY_WWW			150	/* AL Internet Browser */
#define KEY_MSDOS		151
#define KEY_COFFEE		152	/* AL Terminal Lock/Screensaver */
#define KEY_SCREENLOCK		KEY_COFFEE
#define KEY_ROTATE_DISPLAY	153	/* Display orientation for e.g. tablets */
#define KEY_DIRECTION		KEY_ROTATE_DISPLAY
#define KEY_CYCLEWINDOWS	154
#define KEY_MAIL		155
#define KEY_BOOKMARKS		156	/* AC Bookmarks */
#define KEY_COMPUTER		157
#define KEY_BACK		158	/* AC Back */
#define KEY_FORWARD		159	/* AC Forward */
#define KEY_CLOSECD		160
#define KEY_EJECTCD		161
#define KEY_EJECTCLOSECD	162
#define KEY_NEXTSONG		163
#define KEY_PLAYPAUSE		164
#define KEY_PREVIOUSSONG	165
#define KEY_STOPCD		166
#define KEY_RECORD		167
#define KEY_REWIND		168
#define KEY_PHONE		169	/* Media Select Telephone */
#define KEY_ISO			170
#define KEY_CONFIG		171	/* AL Consumer Control Configuration */
#define KEY_HOMEPAGE		172	/* AC Home */
#define KEY_REFRESH		173	/* AC Refresh */
#define KEY_EXIT		174	/* AC Exit */
#define KEY_MOVE		175
#define KEY_EDIT		176
#define KEY_SCROLLUP		177
#define KEY_SCROLLDOWN		178
#define KEY_KPLEFTPAREN		179
#define KEY_KPRIGHTPAREN	180
#define KEY_NEW			181	/* AC New */
#define KEY_REDO		182	/* AC Redo/Repeat */

#define KEY_F13			183
#define KEY_F14			184
#define KEY_F15			185
#define KEY_F16			186
#define KEY_F17			187
#define KEY_F18			188
#define KEY_F19			189
#define KEY_F20			190
#define KEY_F21			191
#define KEY_F22			192
#define KEY_F23			193
#define KEY_F24			194

#define KEY_PLAYCD		200
#define KEY_PAUSECD		201
#define KEY_PROG3		202
#define KEY_PROG4		203
#define KEY_DASHBOARD		204	/* AL Dashboard */
#define KEY_SUSPEND		205
#define KEY_CLOSE		206	/* AC Close */
#define KEY_PLAY		207
#define KEY_FASTFORWARD		208
#define KEY_BASSBOOST		209
#define KEY_PRINT		210	/* AC Print */
#define KEY_HP			211
#define KEY_CAMERA		212
#define KEY_SOUND		213
#define KEY_QUESTION		214
#define KEY_EMAIL		215
#define KEY_CHAT		216
#define KEY_SEARCH		217
#define KEY_CONNECT		218
#define KEY_FINANCE		219	/* AL Checkbook/Finance */
#define KEY_SPORT		220
#define KEY_SHOP		221
#define KEY_ALTERASE		222
#define KEY_CANCEL		223	/* AC Cancel */
#define KEY_BRIGHTNESSDOWN	224
#define KEY_BRIGHTNESSUP	225
#define KEY_MEDIA		226

#define KEY_SWITCHVIDEOMODE	227	# /* Cycle between available video
					            # outputs (Monitor/LCD/TV-out/etc) */
#define KEY_KBDILLUMTOGGLE	228
#define KEY_KBDILLUMDOWN	229
#define KEY_KBDILLUMUP		230

#define KEY_SEND		231	/* AC Send */
#define KEY_REPLY		232	/* AC Reply */
#define KEY_FORWARDMAIL		233	/* AC Forward Msg */
#define KEY_SAVE		234	/* AC Save */
#define KEY_DOCUMENTS		235

#define KEY_BATTERY		236

#define KEY_BLUETOOTH		237
#define KEY_WLAN		238
#define KEY_UWB			239

#define KEY_UNKNOWN		240

#define KEY_VIDEO_NEXT		241	/* drive next video source */
#define KEY_VIDEO_PREV		242	/* drive previous video source */
#define KEY_BRIGHTNESS_CYCLE	243	/* brightness up, after max is min */
#define KEY_BRIGHTNESS_AUTO	244	# /* Set Auto Brightness: manual
					            # brightness control is off,
					            # rely on ambient */
#define KEY_BRIGHTNESS_ZERO	KEY_BRIGHTNESS_AUTO
#define KEY_DISPLAY_OFF		245	/* display device to off state */

#define KEY_WWAN		246	/* Wireless WAN (LTE, UMTS, GSM, etc.) */
#define KEY_WIMAX		KEY_WWAN
#define KEY_RFKILL		247	/* Key that controls all radios */

#define KEY_MICMUTE		248	/* Mute / unmute the microphone */

#
# /* Code 255 is reserved for special needs of AT keyboard driver */
#

#define BTN_MISC		0x100
#define BTN_0			0x100
#define BTN_1			0x101
#define BTN_2			0x102
#define BTN_3			0x103
#define BTN_4			0x104
#define BTN_5			0x105
#define BTN_6			0x106
#define BTN_7			0x107
#define BTN_8			0x108
#define BTN_9			0x109

#define BTN_MOUSE		0x110
#define BTN_LEFT		0x110
#define BTN_RIGHT		0x111
#define BTN_MIDDLE		0x112
#define BTN_SIDE		0x113
#define BTN_EXTRA		0x114
#define BTN_FORWARD		0x115
#define BTN_BACK		0x116
#define BTN_TASK		0x117

#define BTN_JOYSTICK		0x120
#define BTN_TRIGGER		0x120
#define BTN_THUMB		0x121
#define BTN_THUMB2		0x122
#define BTN_TOP			0x123
#define BTN_TOP2		0x124
#define BTN_PINKIE		0x125
#define BTN_BASE		0x126
#define BTN_BASE2		0x127
#define BTN_BASE3		0x128
#define BTN_BASE4		0x129
#define BTN_BASE5		0x12a
#define BTN_BASE6		0x12b
#define BTN_DEAD		0x12f

#define BTN_GAMEPAD		0x130
#define BTN_SOUTH		0x130
#define BTN_A			BTN_SOUTH
#define BTN_EAST		0x131
#define BTN_B			BTN_EAST
#define BTN_C			0x132
#define BTN_NORTH		0x133
#define BTN_X			BTN_NORTH
#define BTN_WEST		0x134
#define BTN_Y			BTN_WEST
#define BTN_Z			0x135
#define BTN_TL			0x136
#define BTN_TR			0x137
#define BTN_TL2			0x138
#define BTN_TR2			0x139
#define BTN_SELECT		0x13a
#define BTN_START		0x13b
#define BTN_MODE		0x13c
#define BTN_THUMBL		0x13d
#define BTN_THUMBR		0x13e

#define BTN_DIGI		0x140
#define BTN_TOOL_PEN		0x140
#define BTN_TOOL_RUBBER		0x141
#define BTN_TOOL_BRUSH		0x142
#define BTN_TOOL_PENCIL		0x143
#define BTN_TOOL_AIRBRUSH	0x144
#define BTN_TOOL_FINGER		0x145
#define BTN_TOOL_MOUSE		0x146
#define BTN_TOOL_LENS		0x147
#define BTN_TOOL_QUINTTAP	0x148	/* Five fingers on trackpad */
#define BTN_STYLUS3		0x149
#define BTN_TOUCH		0x14a
#define BTN_STYLUS		0x14b
#define BTN_STYLUS2		0x14c
#define BTN_TOOL_DOUBLETAP	0x14d
#define BTN_TOOL_TRIPLETAP	0x14e
#define BTN_TOOL_QUADTAP	0x14f	/* Four fingers on trackpad */

#define BTN_WHEEL		0x150
#define BTN_GEAR_DOWN		0x150
#define BTN_GEAR_UP		0x151

#define KEY_OK			0x160
#define KEY_SELECT		0x161
#define KEY_GOTO		0x162
#define KEY_CLEAR		0x163
#define KEY_POWER2		0x164
#define KEY_OPTION		0x165
#define KEY_INFO		0x166	/* AL OEM Features/Tips/Tutorial */
#define KEY_TIME		0x167
#define KEY_VENDOR		0x168
#define KEY_ARCHIVE		0x169
#define KEY_PROGRAM		0x16a	/* Media Select Program Guide */
#define KEY_CHANNEL		0x16b
#define KEY_FAVORITES		0x16c
#define KEY_EPG			0x16d
#define KEY_PVR			0x16e	/* Media Select Home */
#define KEY_MHP			0x16f
#define KEY_LANGUAGE		0x170
#define KEY_TITLE		0x171
#define KEY_SUBTITLE		0x172
#define KEY_ANGLE		0x173
#define KEY_FULL_SCREEN		0x174	/* AC View Toggle */
#define KEY_ZOOM		KEY_FULL_SCREEN
#define KEY_MODE		0x175
#define KEY_KEYBOARD		0x176
#define KEY_ASPECT_RATIO	0x177	/* HUTRR37: Aspect */
#define KEY_SCREEN		KEY_ASPECT_RATIO
#define KEY_PC			0x178	/* Media Select Computer */
#define KEY_TV			0x179	/* Media Select TV */
#define KEY_TV2			0x17a	/* Media Select Cable */
#define KEY_VCR			0x17b	/* Media Select VCR */
#define KEY_VCR2		0x17c	/* VCR Plus */
#define KEY_SAT			0x17d	/* Media Select Satellite */
#define KEY_SAT2		0x17e
#define KEY_CD			0x17f	/* Media Select CD */
#define KEY_TAPE		0x180	/* Media Select Tape */
#define KEY_RADIO		0x181
#define KEY_TUNER		0x182	/* Media Select Tuner */
#define KEY_PLAYER		0x183
#define KEY_TEXT		0x184
#define KEY_DVD			0x185	/* Media Select DVD */
#define KEY_AUX			0x186
#define KEY_MP3			0x187
#define KEY_AUDIO		0x188	/* AL Audio Browser */
#define KEY_VIDEO		0x189	/* AL Movie Browser */
#define KEY_DIRECTORY		0x18a
#define KEY_LIST		0x18b
#define KEY_MEMO		0x18c	/* Media Select Messages */
#define KEY_CALENDAR		0x18d
#define KEY_RED			0x18e
#define KEY_GREEN		0x18f
#define KEY_YELLOW		0x190
#define KEY_BLUE		0x191
#define KEY_CHANNELUP		0x192	/* Channel Increment */
#define KEY_CHANNELDOWN		0x193	/* Channel Decrement */
#define KEY_FIRST		0x194
#define KEY_LAST		0x195	/* Recall Last */
#define KEY_AB			0x196
#define KEY_NEXT		0x197
#define KEY_RESTART		0x198
#define KEY_SLOW		0x199
#define KEY_SHUFFLE		0x19a
#define KEY_BREAK		0x19b
#define KEY_PREVIOUS		0x19c
#define KEY_DIGITS		0x19d
#define KEY_TEEN		0x19e
#define KEY_TWEN		0x19f
#define KEY_VIDEOPHONE		0x1a0	/* Media Select Video Phone */
#define KEY_GAMES		0x1a1	/* Media Select Games */
#define KEY_ZOOMIN		0x1a2	/* AC Zoom In */
#define KEY_ZOOMOUT		0x1a3	/* AC Zoom Out */
#define KEY_ZOOMRESET		0x1a4	/* AC Zoom */
#define KEY_WORDPROCESSOR	0x1a5	/* AL Word Processor */
#define KEY_EDITOR		0x1a6	/* AL Text Editor */
#define KEY_SPREADSHEET		0x1a7	/* AL Spreadsheet */
#define KEY_GRAPHICSEDITOR	0x1a8	/* AL Graphics Editor */
#define KEY_PRESENTATION	0x1a9	/* AL Presentation App */
#define KEY_DATABASE		0x1aa	/* AL Database App */
#define KEY_NEWS		0x1ab	/* AL Newsreader */
#define KEY_VOICEMAIL		0x1ac	/* AL Voicemail */
#define KEY_ADDRESSBOOK		0x1ad	/* AL Contacts/Address Book */
#define KEY_MESSENGER		0x1ae	/* AL Instant Messaging */
#define KEY_DISPLAYTOGGLE	0x1af	/* Turn display (LCD) on and off */
#define KEY_BRIGHTNESS_TOGGLE	KEY_DISPLAYTOGGLE
#define KEY_SPELLCHECK		0x1b0   /* AL Spell Check */
#define KEY_LOGOFF		0x1b1   /* AL Logoff */

#define KEY_DOLLAR		0x1b2
#define KEY_EURO		0x1b3

#define KEY_FRAMEBACK		0x1b4	/* Consumer - transport controls */
#define KEY_FRAMEFORWARD	0x1b5
#define KEY_CONTEXT_MENU	0x1b6	/* GenDesc - system context menu */
#define KEY_MEDIA_REPEAT	0x1b7	/* Consumer - transport control */
#define KEY_10CHANNELSUP	0x1b8	/* 10 channels up (10+) */
#define KEY_10CHANNELSDOWN	0x1b9	/* 10 channels down (10-) */
#define KEY_IMAGES		0x1ba	/* AL Image Browser */

#define KEY_DEL_EOL		0x1c0
#define KEY_DEL_EOS		0x1c1
#define KEY_INS_LINE		0x1c2
#define KEY_DEL_LINE		0x1c3

#define KEY_FN			0x1d0
#define KEY_FN_ESC		0x1d1
#define KEY_FN_F1		0x1d2
#define KEY_FN_F2		0x1d3
#define KEY_FN_F3		0x1d4
#define KEY_FN_F4		0x1d5
#define KEY_FN_F5		0x1d6
#define KEY_FN_F6		0x1d7
#define KEY_FN_F7		0x1d8
#define KEY_FN_F8		0x1d9
#define KEY_FN_F9		0x1da
#define KEY_FN_F10		0x1db
#define KEY_FN_F11		0x1dc
#define KEY_FN_F12		0x1dd
#define KEY_FN_1		0x1de
#define KEY_FN_2		0x1df
#define KEY_FN_D		0x1e0
#define KEY_FN_E		0x1e1
#define KEY_FN_F		0x1e2
#define KEY_FN_S		0x1e3
#define KEY_FN_B		0x1e4

#define KEY_BRL_DOT1		0x1f1
#define KEY_BRL_DOT2		0x1f2
#define KEY_BRL_DOT3		0x1f3
#define KEY_BRL_DOT4		0x1f4
#define KEY_BRL_DOT5		0x1f5
#define KEY_BRL_DOT6		0x1f6
#define KEY_BRL_DOT7		0x1f7
#define KEY_BRL_DOT8		0x1f8
#define KEY_BRL_DOT9		0x1f9
#define KEY_BRL_DOT10		0x1fa

#define KEY_NUMERIC_0		0x200	/* used by phones, remote controls, */
#define KEY_NUMERIC_1		0x201	/* and other keypads */
#define KEY_NUMERIC_2		0x202
#define KEY_NUMERIC_3		0x203
#define KEY_NUMERIC_4		0x204
#define KEY_NUMERIC_5		0x205
#define KEY_NUMERIC_6		0x206
#define KEY_NUMERIC_7		0x207
#define KEY_NUMERIC_8		0x208
#define KEY_NUMERIC_9		0x209
#define KEY_NUMERIC_STAR	0x20a
#define KEY_NUMERIC_POUND	0x20b
#define KEY_NUMERIC_A		0x20c	/* Phone key A - HUT Telephony 0xb9 */
#define KEY_NUMERIC_B		0x20d
#define KEY_NUMERIC_C		0x20e
#define KEY_NUMERIC_D		0x20f

#define KEY_CAMERA_FOCUS	0x210
#define KEY_WPS_BUTTON		0x211	/* WiFi Protected Setup key */

#define KEY_TOUCHPAD_TOGGLE	0x212	/* Request switch touchpad on or off */
#define KEY_TOUCHPAD_ON		0x213
#define KEY_TOUCHPAD_OFF	0x214

#define KEY_CAMERA_ZOOMIN	0x215
#define KEY_CAMERA_ZOOMOUT	0x216
#define KEY_CAMERA_UP		0x217
#define KEY_CAMERA_DOWN		0x218
#define KEY_CAMERA_LEFT		0x219
#define KEY_CAMERA_RIGHT	0x21a

#define KEY_ATTENDANT_ON	0x21b
#define KEY_ATTENDANT_OFF	0x21c
#define KEY_ATTENDANT_TOGGLE	0x21d	/* Attendant call on or off */
#define KEY_LIGHTS_TOGGLE	0x21e	/* Reading light on or off */

#define BTN_DPAD_UP		0x220
#define BTN_DPAD_DOWN		0x221
#define BTN_DPAD_LEFT		0x222
#define BTN_DPAD_RIGHT		0x223

#define KEY_ALS_TOGGLE		0x230	/* Ambient light sensor */
#define KEY_ROTATE_LOCK_TOGGLE	0x231	/* Display rotation lock */

#define KEY_BUTTONCONFIG		0x240	/* AL Button Configuration */
#define KEY_TASKMANAGER		0x241	/* AL Task/Project Manager */
#define KEY_JOURNAL		0x242	/* AL Log/Journal/Timecard */
#define KEY_CONTROLPANEL		0x243	/* AL Control Panel */
#define KEY_APPSELECT		0x244	/* AL Select Task/Application */
#define KEY_SCREENSAVER		0x245	/* AL Screen Saver */
#define KEY_VOICECOMMAND		0x246	/* Listening Voice Command */
#define KEY_ASSISTANT		0x247	/* AL Context-aware desktop assistant */
#define KEY_KBD_LAYOUT_NEXT	0x248	/* AC Next Keyboard Layout Select */

#define KEY_BRIGHTNESS_MIN		0x250	/* Set Brightness to Minimum */
#define KEY_BRIGHTNESS_MAX		0x251	/* Set Brightness to Maximum */

#define KEY_KBDINPUTASSIST_PREV		0x260
#define KEY_KBDINPUTASSIST_NEXT		0x261
#define KEY_KBDINPUTASSIST_PREVGROUP		0x262
#define KEY_KBDINPUTASSIST_NEXTGROUP		0x263
#define KEY_KBDINPUTASSIST_ACCEPT		0x264
#define KEY_KBDINPUTASSIST_CANCEL		0x265

## Diagonal movement keys
#define KEY_RIGHT_UP			0x266
#define KEY_RIGHT_DOWN			0x267
#define KEY_LEFT_UP			0x268
#define KEY_LEFT_DOWN			0x269


class MotionEvent(object):
    """
    Touch event class

    Attributes
    -----------
    timestamp :  float
        timestamp

    action : int
        touch action type. VALUE_UP or VALUE_DOWN or VALUE_MOVE

    x : int
        touch x position

    y : int
        touch y position
    """

    def __init__(self):
        self._dev_name = ''
        self._timestamp = 0
        self._action = VALUE_UP
        self._x = 0
        self._y = 0

    def __str__(self):
        msg = '--- MotionEvent at {:f}, device : {:s}, action {:d}, x {:d}, y {:d} ---'
        return msg.format(self.timestamp, self.dev_name, self.action, self.x, self.y)

    def copy(self, e: 'MotionEvent'):
        self._dev_name = e.dev_name
        self._timestamp = e.timestamp
        self._action = e.action
        self._x = e.x
        self._y = e.y
        

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def dev_name(self):
        return self._dev_name

    @property
    def action(self):
        return self._action

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @timestamp.setter
    def timestamp(self, t):
        self._timestamp = t

    @dev_name.setter
    def dev_name(self, n):
        self._dev_name = n

    @action.setter
    def action(self, action):
        self._action = action

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y
        

class InputEvent(MotionEvent):
    """
    input event class. 
    this event include all events of input(touch, buttons, keys, digital-pen).

    Attributes
    -----------
    code : int
        input event code
    """

    def __init__(self):
        super().__init__()
        self._code = 0
        self._id = 0
        self._press = -1

    def __str__(self):
        if self.code == BTN_TOUCH:
            msg = '--- InputEvent at {:f}, code {}, device : {}, device serial : {}, action {:d}, x {:f}, y {:f}, press {} ---'
            return msg.format(self.timestamp, util.resolve_ecodes_dict({1:[self.code]}).__next__()[1], self.dev_name, self.id, self.action, self.x, self.y, self.press)
        else:
            msg = '--- InputEvent at {:f}, code {}, device : {}, device serial : {}, action {:d} press {}---'
            return msg.format(self.timestamp, util.resolve_ecodes_dict({1:[self.code]}).__next__()[1], self.dev_name, self.id, self.action, self.press)

    def copy(self, e: 'InputEvent'):
        self._id = e.id
        self._press = e.press
        self._dev_name = e.dev_name
        self._timestamp = e.timestamp
        self._code = e.code
        self._action = e.action
        self._x = e.x
        self._y = e.y
        
    @property
    def id(self):
        return self._id

    @property
    def press(self):
        return self._press

    @property
    def code(self):
        return self._code

    @id.setter
    def id(self, id):
        self._id = id

    @press.setter
    def press(self, press):
        self._press = press

    @code.setter
    def code(self, code):
        self._code = code


class InputEventListener(object):
    """
    Interface definition class for a callback to be invoked when a touch event will occur.
    If you want to receive touch event, please override onInputEvent method.
    """

    def onInputEvent(self, e:InputEvent):
        """
        input event callback

        Parameters
        -----------
        e : InputEvent
        """
        raise NotImplementedError


class InputHandler(object):
    """
    InputHandler is handling input event(touch, keys, buttons).

    Examples
    --------
    from mui_ui import InputHandler, InputEventListener, InputEvent

    class App(InputEventListener):
        def __init__(self):
            # create input event handler
            self._input = InputHandler(self)

        def mainLoop(self):
            # start capture touch event
            self._input.startEventLoop()

        def onInputEvent(self, e: InputEvent):
            # handling input event. for instance, pass to UI(dispatchTouchEvent())
            if e.code == BTN_TOUCH:
                # in this case, InputEvent is touch event.
                # please pass to UI(dispathTouchEvent())
            elif:
                # in this case, InputEvent is key or button event.


    # start application
    app = App()
    app.mainLoop()

    Deprecated
    ----------
    target_device
        this parameter no in used. this class can capture all input device event now.

    See Also
    --------
    InputEventListener
    MotionEvent
    InputEvent
    """

    def __init__(self, listener:InputEventListener):
        """
        Parameters
        ------------
        listener : InputEventListener
            callback

        target_device : str
            touch device name(DO NOT NEED CHANGE)
        """
        self.inputEvent = None
        self.inputEventListener = listener

        self._devices = {}

        # get all input devices
        self.devices = [InputDevice(path) for path in list_devices()]
        for device in self.devices:
            print(device.name)
            caps = device.capabilities(absinfo=True)
            for k, v in caps.items():
                if k != 3:
                    continue

                # store AbsInfo
                print(v[ABS_X][1])
                print(v[ABS_Y][1])
                absInfo = {}
                absInfo[ABS_X] = v[ABS_X][1]
                absInfo[ABS_Y] = v[ABS_Y][1]
                self._devices[device.path] = absInfo

    
    def startEventLoop(self):
        self.loop = asyncio.get_event_loop()
        for device in self.devices:
            asyncio.ensure_future(self.eventLoop(device))
        self.loop.run_forever()

    async def eventLoop(self, device):
        changeKey = False
        async for ev in device.async_read_loop():
            # print(ev)

            # handle input event
            if self.inputEvent == None:
                self.inputEvent = InputEvent()

            if ev.type == EV_SYN:
                # digital pen hover event
                if self.inputEvent.press == -1:
                    # print('--hover--')
                    continue

                # last data sing for multi part touch events.
                if changeKey == False:
                    self.inputEvent.action = VALUE_MOVE

                self.inputEvent.dev_name = device.name
                self.inputEvent.timestamp = ev.timestamp()

                self.handleInputEvent(self.inputEvent)

                if self.inputEvent.action == VALUE_UP:
                    self.inputEvent.press = -1

                changeKey = False
                
            if (ev.type == EV_ABS and ev.code == ABS_X):
                factor_x = self._devices[device.path][ABS_X].max / 200
                self.inputEvent.x = int(ev.value // factor_x)

            if (ev.type == EV_ABS and ev.code == ABS_Y):
                factor_y = self._devices[device.path][ABS_Y].max / 32
                self.inputEvent.y = int(ev.value // factor_y)

            if (ev.type == EV_ABS and ev.code == ABS_PRESSURE):
                self.inputEvent.press = ev.value

            if (ev.type == EV_MSC and ev.code == MSC_SERIAL):
                self.inputEvent.id = ev.value

            if (ev.type == EV_KEY):
                self.inputEvent.action = ev.value
                if (ev.value == VALUE_DOWN):
                    self.inputEvent.press = 0
                self.inputEvent.code = ev.code
                changeKey = True

    def handleInputEvent(self, e:InputEvent):
        self.inputEventListener.onInputEvent(e)



# for test
class TestInputEventListener(InputEventListener):
    def __init__(self):
        super().__init__()

    def onInputEvent(self, e:InputEvent):
        print(e)

if __name__ == '__main__':
    try:
        listener = TestInputEventListener()
        input = InputHandler(listener)
        input.startEventLoop()
    except (KeyboardInterrupt, EOFError):
        pass
    sys.exit(0)
