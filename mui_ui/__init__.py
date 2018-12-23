#

from mui_ui.matrix import Matrix, check_diff_range
from mui_ui.display import Display
from mui_ui.display_manager import DisplayManager, DisplayEventListener
from mui_ui.muifont import MuiFont
from mui_ui.parts import AbsParts, OnTouchEventListener, OnUpdateRequestListener
from mui_ui.text import Text, Border, TextAlignment
from mui_ui.autoscroll_text import AutoScrollText
from mui_ui.typewriter_text import TypeWriterText
from mui_ui.image import Image
from mui_ui.widget import Widget
from mui_ui.input import MotionEvent, InputEventListener, InputHandler, VALUE_DOWN, VALUE_MOVE, VALUE_UP
from mui_ui.gesturedetector import GestureListener, GestureDetector
from mui_ui.application import AbsApp, AppEventListener
from mui_ui.app_message import Message
from mui_ui.clock import DigitalClock
from mui_ui.slider import Slider, SliderEventListener

# lib version
__version__ = '0.0.1'

# mui Β Display size
DISPLAY_WIDTH = 200
DISPLAY_HEIGHT = 32