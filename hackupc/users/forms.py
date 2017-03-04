from django.forms import forms, fields


class ValidateProfileForm(forms.Form):
    frontal_photo = fields.ImageField(required=True)
    back_photo = fields.ImageField(required=True)
