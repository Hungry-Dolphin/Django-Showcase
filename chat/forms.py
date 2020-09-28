from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import ChatMessage

User = get_user_model()


class MessageForm(forms.ModelForm):
    content = forms.CharField(max_length=500, label="Message:")

    class Meta:
        model = ChatMessage
        fields = [
            'content'
        ]


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username:')
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Wrong password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
            return super(UserLoginForm, self).clean()


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=24, label='Username:')
    email = forms.EmailField(label='Email address:')
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')
    ConfirmPassword = forms.CharField(widget=forms.PasswordInput, label='Confirm pass:')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'ConfirmPassword'
        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('ConfirmPassword')
        if password != password1:
            raise forms.ValidationError("Passwords don't match")
        if len(password) < 8:
            raise forms.ValidationError("Passwords needs to have a minimum of 8 characters")
        return super(UserRegisterForm, self).clean()
