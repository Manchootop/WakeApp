from django import forms
from .models import FriendshipRequest

class FriendshipRequestForm(forms.ModelForm):
    class Meta:
        model = FriendshipRequest
        fields = ['receiver', 'status']
        widgets = {
            'receiver': forms.HiddenInput(),
            'status': forms.HiddenInput()
        }

class CreateFriendShip:
    pass