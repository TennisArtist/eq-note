"""
【設計原則】
- 此 tokenizer 只負責「保護 LaTeX 語法」
- 絕對不可改變任何換行或段落結構
- 不做 Markdown、不做 HTML、不做 escape
"""

from dataclasses import dataclass
from typing import Dict, Tuple
import re


@dataclass
class LatexToken:
    kind: str          # "inline" | "block"
    content: str       # 不含 $ 的內容
    raw: str           # 含 delimiters 的原始字串


class LatexTokenizer:

    def __init__(self):
        self._counter = 0
        self._token_map: Dict[str, LatexToken] = {}

    def _new_token(self, kind: str, raw: str, content: str) -> str:
        token = f"⟦LATEX_{self._counter}⟧"
        self._counter += 1
        self._token_map[token] = LatexToken(
            kind=kind,
            content=content,
            raw=raw
        )
        return token

    def protect(self, text: str) -> Tuple[str, Dict[str, LatexToken]]:
        """
        將 text 中的 LaTeX 替換為 token
        嚴禁改變任何換行結構
        """
        self._counter = 0
        self._token_map.clear()

        text = self._protect_block(text)
        text = self._protect_inline(text)

        return text, dict(self._token_map)

    # =========================================================
    # Block LaTeX：$$ ... $$
    # =========================================================
    def _protect_block(self, text: str) -> str:
        pattern = re.compile(r"\$\$(.*?)\$\$", flags=re.DOTALL)

        def repl(match):
            raw = match.group(0)          # $$ ... $$
            content = match.group(1)      # 內部
            return self._new_token(
                kind="block",
                raw=raw,
                content=content
            )

        return pattern.sub(repl, text)

    # =========================================================
    # Inline LaTeX：$ ... $（同一行內）
    # =========================================================
    def _protect_inline(self, text: str) -> str:
        pattern = re.compile(
            r"(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)"
        )

        def repl(match):
            raw = match.group(0)
            content = match.group(1)
            return self._new_token(
                kind="inline",
                raw=raw,
                content=content
            )

        return pattern.sub(repl, text)

