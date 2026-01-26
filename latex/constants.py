"""
EQ-Note internal control characters.

【注意】
- 這些字元只用於系統內部 token
- 不得顯示給使用者
- 不得進入 Markdown / HTML escape
"""

# Unicode Private Use Area
MATH_TOKEN_L = "\uFFF0"
MATH_TOKEN_R = "\uFFF1"
