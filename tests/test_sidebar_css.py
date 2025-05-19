import os


def test_sidebar_max_height():
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'styles.css')
    with open(css_path, 'r') as f:
        css = f.read()
    assert 'max-height: calc(100vh - 4rem);' in css
    assert 'overflow-y: auto;' in css
