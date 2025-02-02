from ...Renderer import VertexArray, VertexBuffer, IndexBuffer
from ...Logging.logger   import PI_CORE_ASSERT, PI_CORE_DEBUG

from OpenGL.GL import \
    glGenVertexArrays, glDeleteVertexArrays, glDeleteBuffers, \
    glBindVertexArray, glEnableVertexAttribArray, glVertexAttribPointer

class OpenGLVertexArray(VertexArray):
    __slots__ = "__RendererID", \
        "__VertexBuffers", "__IndexBuffer"

    def __init__(self) -> None:
        self.__RendererID = glGenVertexArrays(1)
        self.__VertexBuffers = []

    def __del__(self) -> None:
        glDeleteVertexArrays(1, [self.__RendererID])

    def Bind(self) -> None:
        glBindVertexArray(self.__RendererID)
    
    def Unbind(self) -> None:
        glBindVertexArray(0)

    def AddVertexBuffer(self, buffer: VertexBuffer) -> None:
        glBindVertexArray(self.__RendererID)
        buffer.Bind()

        elements = buffer.Layout.Elements
        PI_CORE_ASSERT(bool(len(elements)), "Layout of VertexBuffer if not set!")
          
        for i, element in enumerate(elements):      
            glEnableVertexAttribArray(i)
            glVertexAttribPointer(i,
                element.ComponentCount,
                element.OpenGLBaseType,
                element.Normalized,
                buffer.Layout.Stride,
                element.Offset
            )

        self.__VertexBuffers.append(buffer)

    def SetIndexBuffer(self, buffer: IndexBuffer) -> None:
        glBindVertexArray(self.__RendererID)
        buffer.Bind()

        self.__IndexBuffer = buffer

    @property
    def VertexBuffers(self) -> list:
        return self.__VertexBuffers

    @property
    def IndexBuffer(self) -> IndexBuffer:
        return self.__IndexBuffer
