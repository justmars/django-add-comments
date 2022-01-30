from django import forms

from .models import Comment


class CommentModelForm(forms.ModelForm):
    """This should be rendered inside a <section> to use swapping functions."""

    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "4", "class": "form-control"})
    )
    is_public = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "role": "switch"}
        ),
    )

    class Meta:
        model = Comment
        fields = ("content", "is_public")
