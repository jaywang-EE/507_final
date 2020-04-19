from django import forms
from store.models import Pic
from django.core.files.uploadedfile import InMemoryUploadedFile
from store.humanize import naturalsize

class CreateForm(forms.ModelForm):
    max_upload_limit = 10 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    picture = forms.FileField(required=True, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Pic
        fields = ['picture']  # Picture is manual

    # Validate the size of the picture
    def clean(self) :
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None : 
            self.add_error('picture', "please select a picture!")
        elif len(pic) > self.max_upload_limit:
            self.add_error('picture', " > "+self.max_upload_limit_text+" bytes!")
            
    def save(self, commit=True) :
        instance = super(CreateForm, self).save(commit=False)

        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read();
            instance.content_type = f.content_type
            instance.picture = bytearr

        if commit:
            instance.save()

        return instance

