# document/element.py
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class BaseElement:
    id: str = None
    meta: Optional[Dict] = None


@dataclass
class TextElement(BaseElement):
    text: str = ""


@dataclass
class LatexElement(BaseElement):
    latex: str = ""


@dataclass
class PlotElement(BaseElement):
    code: str = ""
    kind: str = "2d_latex"


@dataclass
class ImageElement(BaseElement):
    src: str = ""
    width: Optional[int] = None


class PythonElement(BaseElement):
    def __init__(self, code: str, elem_id: str = None):
        super().__init__(id=elem_id)
        self.code = code
        self.output: Optional[str] = None