from django import forms
from contact.models import Application, ApplicationCreate
from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

    def clean_email(self):
        email = self.cleaned_data['email']
        if "example.com" in email:
            raise forms.ValidationError("Example.com manzilini ishlatmaslik kerak")
        return email


class ApplicationCreateForm(forms.ModelForm):
    class Meta:
        model = ApplicationCreate
        fields = "__all__"
        widgets = {
            "status": forms.Select(attrs={'class': 'block appearance-none w-full bg-grey-200 border border-grey-200 text-grey-darker py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-grey', 'id': 'grid-state'}),
            "application": forms.Select(attrs={'class': 'form-control', 'readonly': True}),
         }
