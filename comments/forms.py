from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Field, Layout
from django import forms

from .models import Comment


class InputCommentModelForm(forms.ModelForm):
    """This should be rendered inside a <section> to use swapping functions."""

    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "4"}))
    is_public = forms.BooleanField(required=False)

    class Meta:

        model = Comment
        fields = ("content", "is_public")

    def __init__(self, *args, **kwargs):
        submit_url = kwargs.pop("submit_url", None)
        revert_url = kwargs.pop("revert_url", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {
            "hx_target": "closest section",  # inherited below
            "hx_swap": "outerHTML",  # inherited below
        }
        self.helper.layout = Layout(
            Field("content"),
            Field("is_public"),
            Button(
                "submit",
                "Submit",
                hx_post=submit_url,  # POST; submits form, redirects to created
                hx_trigger="click",
            ),
            Button(
                "cancel",
                "Cancel",
                hidden=False if revert_url else True,  # only shows up in edit
                hx_get=revert_url,  # GET; reverts to original comment
                hx_trigger="click",
            ),
        )
