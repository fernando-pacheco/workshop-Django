from django import forms

class PeriodForm(forms.Form):
    PERIOD_CHOICES = (
        (7, '7 Dias'),
        (15, '15 Dias'),
        (30, '30 Dias'),
    )
    period = forms.ChoiceField(choices=PERIOD_CHOICES)
