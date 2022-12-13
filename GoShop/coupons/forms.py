from django import forms

class ApplyCouponForm(forms.Form):
    code = forms.CharField()
