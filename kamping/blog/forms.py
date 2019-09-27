from django import forms
from .models import Blog
from ckeditor.widgets import CKEditorWidget


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        content = forms.CharField(widget=CKEditorWidget())

        fields = ['title', 'content','cover_photo']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
