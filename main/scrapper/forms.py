from django import forms
from core.models import User


class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dynamic_fields = kwargs.pop('dynamic_fields')
        super(DynamicForm, self).__init__(*args, **kwargs)
        for key, value in dynamic_fields:
            self.fields[key.slug] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=value)


# class RegisterForm(forms.Form):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     first_name = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}, ))
#     last_name = forms.ImageField(widget=forms.FileInput())


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердить пароль', widget=forms.PasswordInput)
    description = forms.CharField(max_length=500, label="Описание", widget=forms.Textarea, help_text="test")
    image = forms.ImageField(label="Фотография профиля")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'description', 'image')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
