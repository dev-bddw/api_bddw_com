from django import forms

from .models import DropDownMenu
from .widgets import CodeMirrorWidget


class DropDownMenuModelForm(forms.ModelForm):
    class Meta:
        model = DropDownMenu
        fields = "__all__"
        widgets = {
            "data": CodeMirrorWidget(),
        }
