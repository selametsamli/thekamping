from django import forms

from camp.models import Camp, Photo


class CampForm(forms.ModelForm):
    starter_date = forms.DateField(input_formats=("%d.%m.%Y",), widget=forms.DateInput(format="%d.%m.%Y"),
                                   required=True,
                                   label="Başlangıç Günü")

    class Meta:
        model = Camp
        fields = ["title", "content", "starter_date", 'starter_time', 'location', 'size']

    def __init__(self, *args, **kwargs):
        super(CampForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control', 'id': field}
        DATEPICKER = {
            'type': 'text',
            'class': 'form-control',
            'autocomplete': 'off'
        }

        self.fields['starter_date'].widget.attrs.update(DATEPICKER)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file',)


class AForm(forms.Form):
    a = forms.CharField(max_length=53)
