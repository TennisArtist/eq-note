# document/document_model.py

from typing import List
from .element import BaseElement


class DocumentModel:
    """單一筆記文件的抽象模型。"""

    def __init__(self, elements: List[BaseElement] | None = None):
        self.elements: List[BaseElement] = elements or []

    def add_element(self, elem: BaseElement):
        self.elements.append(elem)

    def clear(self):
        self.elements.clear()
