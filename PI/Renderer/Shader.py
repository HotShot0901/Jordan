from ..Logging.logger  import PI_CORE_ASSERT
from ..Core.Base import PI_DEBUG
from ..Core.StateManager import StateManager
from .RendererAPI import RendererAPI

import pyrr
from abc import ABC, abstractmethod

class Shader(ABC):
    __slots__ = ("__NativeAPI", "_Path")

    @staticmethod
    def Init() -> None:
        if (RendererAPI.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (RendererAPI.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLShader import OpenGLShader
            Shader.__NativeAPI = OpenGLShader
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @abstractmethod
    def _GetUniformLocation(self, name: str) -> int: ...
    @abstractmethod
    def SetMat4(self, name: str, matrix: pyrr.Matrix44) -> None: ...
    @abstractmethod
    def SetFloat3(self, name: str, vector: pyrr.Vector3) -> None: ...
    @abstractmethod
    def SetFloat4(self, name: str, vector: pyrr.Vector4) -> None: ...
    @abstractmethod
    def SetFloat2(self, name: str, x: float, y: float) -> None: ...
    @abstractmethod
    def SetFloat(self, name: str, value: float) -> None: ...
    @abstractmethod
    def SetInt(self, name: str, value: int) -> None: ...
    @abstractmethod
    def SetBool(self, name: str, value: bool) -> None: ...

    @property
    def Name(self) -> int: ...
    @property
    def Path(self) -> str: return self._Path

    @abstractmethod
    def __del__(self) -> None: ...
    @abstractmethod
    def Bind(self) -> None: ...
    @abstractmethod
    def Unbind(self) -> None: ...

    @staticmethod
    def Create(shaderFile: str):
        return Shader.__NativeAPI(shaderFile)
