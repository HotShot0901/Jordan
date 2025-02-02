from ..Logging import PI_CLIENT_WARN

import imgui
import pyrr
from typing import Callable, Iterable, List, Tuple, Any

class UILib:
    class _FILE_DIALOGUE_RESOURCES:
        IsLoaded: bool = False
        
        _Root = None

        LoadFileLoader  : Callable[[ Iterable[Tuple[str, str]] ], str]
        SaveFileLoader  : Callable[[ Iterable[Tuple[str, str]] ], str]
        DirectoryLoader : Callable[[                           ], str]

        @staticmethod
        def Init() -> None:
            if UILib._FILE_DIALOGUE_RESOURCES.IsLoaded: return

            import tkinter as tk
            from   tkinter import filedialog
            
            UILib._FILE_DIALOGUE_RESOURCES._Root = tk.Tk()
            UILib._FILE_DIALOGUE_RESOURCES._Root.withdraw()

            UILib._FILE_DIALOGUE_RESOURCES.LoadFileLoader  = filedialog.askopenfilename
            UILib._FILE_DIALOGUE_RESOURCES.SaveFileLoader  = filedialog.asksaveasfilename
            UILib._FILE_DIALOGUE_RESOURCES.DirectoryLoader = filedialog.askdirectory

            UILib._FILE_DIALOGUE_RESOURCES.IsLoaded = True

    @staticmethod
    def TooltipIfHovered(tooltip: str=None) -> None:
        if tooltip and imgui.is_item_hovered():
            imgui.begin_tooltip()
            imgui.text(tooltip)
            imgui.end_tooltip()

    @staticmethod
    def DrawButton(lable: str, tooltip: str=None) -> bool:
        pressed = imgui.button(lable)
        UILib.TooltipIfHovered(tooltip)
        return pressed

    @staticmethod
    def DrawVector3Controls(
        lable: str, values: pyrr.Vector3, resetValue: float=0,
        speed: float=0.05, columnWidth: float=100
        ) -> Tuple[bool, pyrr.Vector3]:
        imgui.push_id(lable)

        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()

        imgui.push_item_width(imgui.calculate_item_width()/3)
        imgui.push_item_width(imgui.calculate_item_width()/2.5*2)
        imgui.push_item_width(imgui.calculate_item_width())

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, imgui.Vec2( 0, 1 ))
        lineHeight = 23.5

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0.1, 0.15, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9, 0.2, 0.2, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.8, 0.1, 0.15, 1.0 )
        if imgui.button("X", lineHeight + 3.0, lineHeight): values.x = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        XHasChanged, XChanged = imgui.drag_float("##X", values.x, speed, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.2, 0.7, 0.2, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.3, 0.8, 0.3, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.2, 0.7, 0.2, 1.0 )
        if imgui.button("Y", lineHeight + 3.0, lineHeight): values.y = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        YHasChanged, YChanged = imgui.drag_float("##Y", values.y, speed, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.1, 0.25, 0.8, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.2, 0.35, 0.9, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.1, 0.25, 0.8, 1.0 )
        if imgui.button("Z", lineHeight + 3.0, lineHeight): values.z = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        ZHasChanged, ZChanged = imgui.drag_float("##Z", values.z, speed, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()

        imgui.pop_style_var()
        imgui.columns(1)
        imgui.pop_id()

        if XHasChanged or YHasChanged or ZHasChanged: return True, pyrr.Vector3([ XChanged, YChanged, ZChanged ])
        else: return False, pyrr.Vector3([ values.x, values.y, values.z ])

    @staticmethod
    def DrawTextFieldControls(
        lable: str, value: str, columnWidth: float=50,
        acceptDragDrop: bool=False, filter: Tuple[str]=None, tooltip: str=None
    ) -> Tuple[bool, str, Any]:
        imgui.push_id(lable)

        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        
        imgui.push_item_width(imgui.calculate_item_width() * 1.5)
        changed, newText = imgui.input_text("##Filter", value, 512)
        imgui.pop_item_width()

        UILib.TooltipIfHovered(tooltip)

        dragDrop = False
        if acceptDragDrop:
            if imgui.begin_drag_drop_target():
                data: bytes = imgui.accept_drag_drop_payload("CONTENT_BROWSER_ITEM")
                if data:
                    data = data.decode('utf-8')
                    if not filter: changed, newText, dragDrop = True, data, True
                    else:
                        if data.lower().endswith(filter): changed, newText, dragDrop = True, data, True
                        else: PI_CLIENT_WARN("This text field only accepts {} files", filter)
                imgui.end_drag_drop_target()

        imgui.columns(1)
        imgui.pop_id()

        if not acceptDragDrop: return changed, newText
        return changed, newText, dragDrop

    @staticmethod
    def DrawSelectableFileField(
        lable: str, value: str, columnWidth: float=50,
        filetypes=Iterable[Tuple[str, str]], acceptDragDrop: bool=False,
        textfieldTooltip: str=None, selectorTooltip: str=None
    ) -> Tuple[bool, str]:
        imgui.push_id(lable)

        imgui.columns(3)
        imgui.set_column_width(0, columnWidth)
        imgui.set_column_width(1, imgui.get_window_content_region_max()[0] - 130)

        imgui.text(lable)
        imgui.next_column()
        
        imgui.push_item_width(imgui.calculate_item_width() * 1.5)
        changed, newText = imgui.input_text("##Filter", value, 512)
        imgui.pop_item_width()

        UILib.TooltipIfHovered(textfieldTooltip)

        dragDrop = False
        if acceptDragDrop:
            if imgui.begin_drag_drop_target():
                data: bytes = imgui.accept_drag_drop_payload("CONTENT_BROWSER_ITEM")
                if data:
                    data = data.decode('utf-8')
                    if not filter: changed, newText, dragDrop = True, data, True
                    else:
                        if data.lower().endswith(".exe"): changed, newText, dragDrop = True, data, True
                        else: PI_CLIENT_WARN("This text field only accepts {} files", ".exe")
                imgui.end_drag_drop_target()

        imgui.next_column()
        if UILib.DrawButton("...", tooltip=selectorTooltip):
            cancelled, filename = UILib.DrawFileLoadDialog(filetypes)

            if cancelled:
                imgui.columns(1)
                imgui.pop_id()
                if not acceptDragDrop: return True, ""
                return True, "", False
        
            imgui.columns(1)
            imgui.pop_id()
            if not acceptDragDrop: return True, filename
            return True, filename, False

        imgui.columns(1)
        imgui.pop_id()

        if not acceptDragDrop: return changed, newText
        return changed, newText, dragDrop
    
    @staticmethod
    def DrawSelectableDirField(
        lable: str, value: str, columnWidth: float=50,
        textfieldTooltip: str=None, selectorTooltip: str=None
    ) -> Tuple[bool, str]:
        imgui.push_id(lable)

        imgui.columns(3)
        imgui.set_column_width(0, columnWidth)
        imgui.set_column_width(1, imgui.get_window_content_region_max()[0] - 130)

        imgui.text(lable)
        imgui.next_column()
        
        imgui.push_item_width(imgui.calculate_item_width() * 1.5)
        changed, newText = imgui.input_text("##Filter", value, 512)
        imgui.pop_item_width()

        UILib.TooltipIfHovered(textfieldTooltip)

        imgui.next_column()
        if UILib.DrawButton("...", tooltip=selectorTooltip):
            cancelled, filename = UILib.DrawDirLoadDialog()

            if cancelled:
                imgui.columns(1)
                imgui.pop_id()
                return True, ""
        
            imgui.columns(1)
            imgui.pop_id()
            return True, filename

        imgui.columns(1)
        imgui.pop_id()

        return changed, newText

    @staticmethod
    def DrawTextLable(lable: str, value: str, columnWidth: float=50) -> None:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        imgui.text(value)
        imgui.columns(1)
        imgui.pop_id()

    # Output -> ( changed, index, value )
    @staticmethod
    def DrawDropdown(lable: str, index: int, values: List[str], columnWidth: float=50) -> Tuple[bool, int, str]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()

        imgui.push_item_width(imgui.calculate_item_width() * 1.5)
        
        changed, index = imgui.combo(f"##combo_{lable}", index, values)

        imgui.pop_item_width()

        imgui.columns(1)
        imgui.pop_id()

        return changed, index, values[index]

    @staticmethod
    def DrawFloatControls(
            lable: str, value: float, speed: float=0.05,
            minValue: float=0.0, maxValue: float=0.0,
            columnWidth: float=100,
            tooltip: str=None, inActive: bool=False
        ) -> Tuple[bool, float]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        
        changed, value = imgui.drag_float(
            "##Value", value, change_speed=speed, min_value=minValue, max_value=maxValue, format="%.2f"
        )

        UILib.TooltipIfHovered(tooltip)
        imgui.columns(1)
        imgui.pop_id()

        return changed, value
        
    @staticmethod
    def DrawIntControls(lable: str, value: int, speed: float=0.05,
        minValue: int=0.0, maxValue: int=0.0,
        columnWidth: float=100) -> Tuple[bool, int]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        changed, value = imgui.drag_int("##Value", value, change_speed=speed, min_value=minValue, max_value=maxValue)
        imgui.columns(1)
        imgui.pop_id()

        return changed, value

    @staticmethod
    def DrawBoolControls(lable: str, state: bool, columnWidth: float=100) -> Tuple[bool, bool]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        changed, state = imgui.checkbox("##Value", state)
        imgui.columns(1)
        imgui.pop_id()

        return changed, state

    @staticmethod
    def DrawColor4Controls(lable: str, value: pyrr.Vector4, columnWidth: float=100) -> Tuple[bool, pyrr.Vector4]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        changed, value = imgui.color_edit4("##Value", value[0], value[1], value[2], value[3])
        imgui.columns(1)
        imgui.pop_id()

        return changed, value

    @staticmethod
    def DrawColor3Controls(lable: str, value: pyrr.Vector3, columnWidth: float=100) -> Tuple[bool, pyrr.Vector3]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        changed, value = imgui.color_edit3("##Value", value[0], value[1], value[2])
        imgui.columns(1)
        imgui.pop_id()

        return changed, value

    @staticmethod
    def DrawFileLoadDialog(filetypes=Iterable[Tuple[str, str]]) -> Tuple[bool, str]:
        UILib._FILE_DIALOGUE_RESOURCES.Init()
        fileName = UILib._FILE_DIALOGUE_RESOURCES.LoadFileLoader(filetypes=filetypes)
        return fileName == "", fileName
        
    @staticmethod
    def DrawFileSaveDialog(filetypes=Iterable[Tuple[str, str]]) -> Tuple[bool, str]:
        UILib._FILE_DIALOGUE_RESOURCES.Init()
        fileName = UILib._FILE_DIALOGUE_RESOURCES.SaveFileLoader(filetypes=filetypes)
        return fileName == "", fileName
    
    @staticmethod
    def DrawDirLoadDialog() -> Tuple[bool, str]:
        UILib._FILE_DIALOGUE_RESOURCES.Init()
        fileName = UILib._FILE_DIALOGUE_RESOURCES.DirectoryLoader()
        return fileName == "", fileName
