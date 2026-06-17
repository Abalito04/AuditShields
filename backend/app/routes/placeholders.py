from flask import render_template


def render_section(title: str, description: str, module: str):
    return render_template(
        "placeholders/section.html",
        title=title,
        description=description,
        module=module,
    )
