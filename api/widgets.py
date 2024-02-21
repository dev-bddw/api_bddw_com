import subprocess

from django.forms.widgets import Widget
from django.utils.safestring import mark_safe


def pretify(data):
    json_str = data
    prettier_path = "prettier"
    result = subprocess.run([prettier_path, "--parser", "json"], input=json_str, text=True, capture_output=True)
    # check if the formatting was successful
    if result.returncode == 0:
        formatted_json = result.stdout
        print("formatted json:", formatted_json)
        return formatted_json


class CodeMirrorWidget(Widget):
    # class Media:
    #     css = {
    #         'all': ('path/to/your/css/custom-style.css',)
    #     }
    #     js = ('path/to/your/js/custom-script.js',)
    #
    def render(self, name, value, attrs=None, renderer=None):

        html = f'<textarea name="{name}" id="{name}">{pretify(value)}</textarea>'  # Customize as needed
        # Include any additional HTML or JavaScript here as needed
        return mark_safe(html)
