from django import forms
from .models import Friendship

class FriendshipRequestForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ['receiver', 'status']
        widgets = {
            'receiver': forms.HiddenInput(),
            'status': forms.HiddenInput()
        }