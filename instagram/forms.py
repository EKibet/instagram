from django import forms
from .models import Image,Comment
from user.models import Profile

class PhotoUploadModelForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image', 'title']
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_path', 'bio']