from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# The checkout form will set addresses, countries, and Zip code for both shipping and billing


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=True)
    shipping_address2 = forms.CharField(required=True)
    shipping_country = CountryField().formfield(
        required=True,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=True)

    billing_address = forms.CharField(required=True)
    billing_address2 = forms.CharField(required=True)
    billing_country = CountryField().formfield(
        required=True,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=True)

    same_billing_address = forms.BooleanField(required=False)
