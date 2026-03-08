
import ast
import gradio as gr

def generate_docstring(func_node: ast.FunctionDef) -> str:
    """Generate a simple Google-style docstring for a function."""
    
    func_name = func_node.name
    args = [arg.arg for arg in func_node.args.args]

    doc = f'"""Summary of {func_name}.\n\n'

    if args:
        doc += "Args:\n"
        for arg in args:
            doc += f"    {arg} (type): Description.\n"

    doc += "\nReturns:\n"
    doc += "    type: Description.\n"
    doc += '"""'

    return doc


def process_code(code: str) -> str:
    try:
        tree = ast.parse(code)
        output = code

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                doc = generate_docstring(node)

                lines = output.split("\n")
                insert_line = node.body[0].lineno - 1
                indent = " " * (node.body[0].col_offset)

                lines.insert(insert_line, indent + doc)
                output = "\n".join(lines)

        return output

    except Exception as e:
        return f"Error: {e}"


def ui_generate(code):
    return process_code(code)


demo = gr.Interface(
    fn=ui_generate,
    inputs=gr.Textbox(lines=20, label="Paste Python Code"),
    outputs=gr.Textbox(lines=20, label="Code with Docstrings"),
    title="Doc-Genie: Python Docstring Generator",
    description="Automatically generates docstrings using AST analysis."
)

if __name__ == "__main__":
    demo.launch()
