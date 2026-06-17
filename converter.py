import ast
from ollama import chat

MODEL_NAME = "qwen2.5-coder:1.5b"

SMALL_FILE_LIMIT = 100
CHUNK_LINE_LIMIT = 80


def clean_output(result):
    tags = [
        "```php",
        "```python",
        "```java",
        "```cpp",
        "```c++",
        "```javascript",
        "```js",
        "```html",
        "```css",
        "```"
    ]

    for tag in tags:
        result = result.replace(tag, "")

    bad_lines = [
        "Sure!",
        "Here is",
        "Here’s",
        "Explanation:",
        "Note:",
        "It seems",
        "This code",
        "The following",
        "Below is"
    ]

    cleaned = []

    for line in result.splitlines():
        stripped = line.strip()

        if any(stripped.startswith(bad) for bad in bad_lines):
            continue

        cleaned.append(line)

    return "\n".join(cleaned).strip()


def remove_extra_php_tags(code):
    code = code.replace("?>\n<?php", "")
    code = code.replace("?>\r\n<?php", "")

    parts = code.split("<?php")

    if len(parts) > 2:
        code = "<?php" + "".join(parts[1:])

    return code.strip()


def is_valid_python(code):
    try:
        ast.parse(code)
        return True
    except Exception:
        return False


def recover_python_indentation(code):
    lines = code.splitlines()

    recovered = []

    indent = 0

    block_keywords = (
        "if ",
        "elif ",
        "else",
        "for ",
        "while ",
        "def ",
        "class ",
        "try",
        "except"
    )

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith(("elif", "else", "except")):
            indent = max(indent - 1, 0)

        recovered.append(
            "    " * indent + stripped
        )

        if (
            stripped.endswith(":")
            or stripped.startswith(block_keywords)
        ):
            indent += 1

    return "\n".join(recovered)


def looks_valid_general(code):
    open_braces = code.count("{")
    close_braces = code.count("}")

    open_paren = code.count("(")
    close_paren = code.count(")")

    if abs(open_braces - close_braces) > 2:
        return False

    if abs(open_paren - close_paren) > 2:
        return False

    return True
def needs_recovery(source, code):
    if source == "Python":

        if is_valid_python(code):
            return False

        recovered = recover_python_indentation(code)

        if is_valid_python(recovered):
            return True

        return True

    if source in [
        "JavaScript",
        "PHP",
        "Laravel",
        "Java",
        "C++"
    ]:
        return not looks_valid_general(code)

    if source in ["HTML", "CSS"]:
        return False

    return False


def smart_split_code(code):
    lines = code.splitlines()
    chunks = []
    current = []

    for line in lines:
        stripped = line.strip()

        is_new_block = (
            stripped.startswith("def ")
            or stripped.startswith("class ")
            or stripped.startswith("function ")
            or stripped.startswith("public class")
            or stripped.startswith("#include")
            or stripped.startswith("if __name__")
        )

        if is_new_block and len(current) >= 20:
            chunks.append("\n".join(current))
            current = []

        current.append(line)

        if len(current) >= CHUNK_LINE_LIMIT:
            chunks.append("\n".join(current))
            current = []

    if current:
        chunks.append("\n".join(current))

    return chunks


def build_prompt(source, target, code, recovery_mode, chunk_number=None, total_chunks=None):
    chunk_text = ""

    if chunk_number and total_chunks:
        chunk_text = (
            f"This is part {chunk_number} of {total_chunks}. "
            f"Convert only this part completely."
        )

    if recovery_mode:
        mode_text = """
The input may contain:
- Indentation errors
- Missing line breaks
- Missing semicolons
- Missing braces
- Multiple statements on one line
- Minor typos like 'eturn' instead of 'return'
- Messy but understandable structure

Before conversion:
1. Understand the intended logic.
2. Reconstruct the most likely correct structure.
3. Fix minor syntax and formatting errors.
4. Do not reject code just because formatting is wrong.
5. If the input is Python with missing indentation, rebuild correct indentation.
6. Only return "Unable to determine the intended logic." if the input is completely meaningless.
"""
    else:
        mode_text = """
The input is valid source code.
Convert it directly without changing the original logic.
"""

    prompt = f"""
You are CodeBridge, a strict code converter.

Convert {source} code to {target}.

{mode_text}

Rules:
1. Return ONLY final converted code.
2. No explanations.
3. No markdown.
4. No code fences.
5. Do not summarize.
6. Do not write "continue".
7. Convert every function and class completely.
8. Preserve the same logic.
9. Follow correct syntax of {target}.
10. If target is PHP or Laravel:
    - Every variable must start with $
    - Use semicolons correctly
    - Add <?php only once
11. If target is Laravel:
    - Generate Laravel-style route/controller code where suitable.

{chunk_text}

Input Code:
{code}
"""

    return prompt
def convert_with_model(
    source,
    target,
    code,
    recovery_mode,
    chunk_number=None,
    total_chunks=None
):
    prompt = build_prompt(
        source,
        target,
        code,
        recovery_mode,
        chunk_number,
        total_chunks
    )

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a code conversion engine. "
                    "Output only valid converted code. "
                    "Never explain."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"]

    return clean_output(result)


def convert_code(source, target, code):
    total_lines = len(code.splitlines())

    recovery_mode = needs_recovery(
        source,
        code
    )

    # SMALL FILE MODE
    if total_lines <= SMALL_FILE_LIMIT:

        if source == "Python" and recovery_mode:
            code = recover_python_indentation(code)

        result = convert_with_model(
            source,
            target,
            code,
            recovery_mode
        )

        if target in ["PHP", "Laravel"]:
            result = remove_extra_php_tags(result)

        mode = (
            "Intelligent Recovery Mode"
            if recovery_mode
            else "Normal Conversion Mode"
        )

        info = (
            f"{mode} used with {MODEL_NAME}. "
            f"Lines: {total_lines}."
        )

        return result, info

    # LARGE FILE MODE
    chunks = smart_split_code(code)

    converted_chunks = []

    total_chunks = len(chunks)

    for index, chunk in enumerate(chunks, start=1):

        chunk_recovery = needs_recovery(
            source,
            chunk
        )

        if source == "Python" and chunk_recovery:
            chunk = recover_python_indentation(chunk)

        converted = convert_with_model(
            source,
            target,
            chunk,
            chunk_recovery,
            index,
            total_chunks
        )

        converted_chunks.append(converted)

    final_output = "\n\n".join(converted_chunks)

    if target in ["PHP", "Laravel"]:
        final_output = remove_extra_php_tags(
            final_output
        )

    info = (
        f"Large File Mode used with {MODEL_NAME}. "
        f"Lines: {total_lines}. "
        f"Chunks: {total_chunks}."
    )

    return final_output, info