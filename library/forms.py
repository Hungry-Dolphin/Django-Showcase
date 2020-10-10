from django import forms
from django.contrib.auth import get_user_model
from .models import Comments, Book, upload

User = get_user_model()


def validate_clearance():
    pass


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=500, label="Message:")

    class Meta:
        model = Comments
        fields = [
            'content'
        ]


class BookForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['clearance'] = forms.ChoiceField(
            choices=user.profile.choices
        )

    title = forms.CharField(max_length=100, label="Title:")
    pdf = forms.FileField()
    clearance = forms.ChoiceField(choices='', label="Clearance:", validators=[validate_clearance])

    class Meta:
        model = Book
        fields = [
            'title', 'pdf', 'clearance'
        ]
