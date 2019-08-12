from django import forms

from camp.models import Camp


class CampForm(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ["title", "content", 'category', "starter_date", 'starter_time', 'location']

    def __init__(self, *args, **kwargs):
        super(CampForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
