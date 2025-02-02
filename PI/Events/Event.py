# This just shifts 1 to i th BIT
def BIT(i: int) -> int:
    return int(1 << i)

# This class is equvalent to a C++ enum
class EventType:
    Null,                                                                   \
    WindowClose, WindowResize, WindowFocus, WindowMoved,                    \
    AppTick, AppUpdate, AppRender,                                          \
    KeyPressed, KeyReleased, CharInput,                                               \
    MouseButtonPressed, MouseButtonReleased, MouseMoved, MouseScrolled      \
        = range(0, 15)

# This class is equvalent to a C++ enum

# It uses bitstream to represent flags, so
# a single Event can have multiple flags
class EventCategory:
    Null = 0
    Application    = BIT(0)
    Input          = BIT(1)
    Keyboard       = BIT(2)
    Mouse          = BIT(3)
    MouseButton    = BIT(4)

class Event:
    Handled = False

    @property
    def EventType(self) -> int:
        pass

    @property    
    def Name(self) -> str:
        return type(self)

    @property    
    def CategoryFlags(self) -> int:
        pass

    def ToString(self) -> str:
        return self.GetName()

    def IsInCategory(self, category: int) -> bool:
        return bool(self.CategoryFlags & category)

    def __repr__(self) -> str:
        return self.ToString()

class EventDispatcher:
    __slots__ = ("_Event",)

    def __init__(self, event: Event) -> None:
        self._Event = event

    def Dispach(self, func, eventType: int) -> bool:
        if (self._Event.EventType == eventType):
            handeled = func(self._Event)
            self._Event.Handled = handeled
            return True

        return False
