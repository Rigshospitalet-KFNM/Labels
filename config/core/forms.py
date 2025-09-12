from django import forms
from .models import Component

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ["name", "tied_model", "tied_field", "info_text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If a tied_model is already chosen (editing) or passed in POST
        tied_model = (
            self.data.get("tied_model") or getattr(self.instance, "tied_model", None)
        )

        if tied_model:
            if tied_model == "element":
                self.fields["tied_field"].widget = forms.Select(
                    choices=[
                        ("symbol", "Symbol"),
                        ("name", "Name"),
                        ("radioactive", "Radioactive"),
                    ]
                )
            elif tied_model == "signatory":
                self.fields["tied_field"].widget = forms.Select(
                    choices=[
                        ("name", "Name"),
                        ("initials", "Initials"),
                    ]
                )
        else:
            self.fields["tied_field"].widget = forms.Select(choices=[])
