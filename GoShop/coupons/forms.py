from django.forms import forms

class ApplyCouponForm(forms.Form):
    code = forms.CharField()
