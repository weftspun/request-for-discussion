# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Measure comment density of our own source, counting docstrings as comments."""

import ast
import io
import os
import tokenize

SOURCE_EXT = {".py", ".ex", ".exs"}


def _python(text):
    comment = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                comment.add(tok.start[0])
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    try:
        tree = ast.parse(text)
    except SyntaxError:
        tree = None
    if tree is not None:
        for node in ast.walk(tree):
            body = getattr(node, "body", None)
            if not isinstance(body, list):
                continue
            for stmt in body:
                if (isinstance(stmt, ast.Expr)
                        and isinstance(stmt.value, ast.Constant)
                        and isinstance(stmt.value.value, str)):
                    comment.update(range(stmt.lineno, (stmt.end_lineno or stmt.lineno) + 1))
    return comment


def _elixir(lines):
    comment = set()
    in_doc = False
    for n, raw in enumerate(lines, 1):
        s = raw.strip()
        if in_doc:
            comment.add(n)
            if '"""' in s:
                in_doc = False
            continue
        if s.startswith("#"):
            comment.add(n)
        elif s.startswith(("@moduledoc", "@doc", "@shortdoc", "@typedoc")):
            comment.add(n)
            if s.count('"""') == 1:
                in_doc = True
    return comment


def density(text, ext):
    """Returns (comment lines, code lines, ratio). Blank lines count as neither."""
    lines = text.splitlines()
    marked = _python(text) if ext == ".py" else _elixir(lines)
    comment = code = 0
    for n, raw in enumerate(lines, 1):
        if not raw.strip():
            continue
        if n in marked:
            comment += 1
        else:
            code += 1
    total = comment + code
    return comment, code, (comment / total if total else 0.0)


def is_source(path):
    return os.path.splitext(path)[1] in SOURCE_EXT
