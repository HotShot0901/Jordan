from ..Logging.logger import PI_CORE_ASSERT

class WindowProperties:
    __slots__ = "Title", "Width", "Height"
    
    def __init__(self, title: str="PI",
                 width: int=640,
                 height: int=360) -> None:
        self.Title = title
        self.Width = width
        self.Height = height

class OS:
    Null    : int = 0
    Windows : int = 1

# Interface representing a DESKTOP system based Window
class Window:
    __OS: int

    def __del__(self) -> None:
        pass

    def OnUpdate(self) -> None:
        pass

    @property
    def Width(self) -> int:
        pass
    
    @property
    def Height(self) -> int:
        pass

    @property
    def AspectRatio(self) -> float:
        try:
            return self.Width / self.Height
        except:
            return 1

    def SetEventCallback(self, callback) -> None:
        pass

    def SetVSync(self, enable: bool) -> None:
        pass

    @property
    def NativeWindow(self):
        pass

    @property
    def IsVsync(self) -> None:
        pass

    @staticmethod
    def GetOS() -> int:
        return Window.__OS

    def SetOS(os: int) -> None:
        Window.__OS = os

    @staticmethod
    def Create(props: WindowProperties=WindowProperties()):
        if Window.__OS == OS.Null:
            PI_CORE_ASSERT(False, "OS.Null not yet supported!")
            return None

        elif Window.__OS == OS.Windows:
            from ..Platform.Windows.WindowsWindow import WindowsWindow
            return WindowsWindow.Create(props)

        PI_CORE_ASSERT(False, "Unknown OS!")
        return None
