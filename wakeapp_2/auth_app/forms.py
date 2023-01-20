from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from wakeapp_2.auth_app.models import WakeAppProfile

UserModel = get_user_model()


class UserRegisterForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=WakeAppProfile.FIRST_NAME_MAX_LENGTH,
    )

    last_name = forms.CharField(
        max_length=WakeAppProfile.LAST_NAME_MAX_LENGTH,
    )

    picture = forms.ImageField()
    date_of_birth = forms.DateField()
    description = forms.CharField(
        widget=forms.Textarea,
    )
    email = forms.EmailField()

    gender = forms.ChoiceField(
        choices=WakeAppProfile.GENDERS,
    )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = WakeAppProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            description=self.cleaned_data['description'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'picture', 'description')

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Upload profile image',
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'min': '1920-01-01',
                }
            )
        }


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['gender'] = WakeAppProfile.DO_NOT_SHOW

    class Meta:
        model = WakeAppProfile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Upload profile picture',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter description',
                    'rows': 3,
                },
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'min': '1920-01-01',
                }
            )
        }


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        pass
        # Not good
        # # should be done with signals
        # # because this breaks the abstraction of the auth app
        # pets = list(self.instance.pet_set.all())
        # PetPhoto.objects.filter(tagged_pets__in=pets).delete()
        # self.instance.delete()
        #
        # return self.instance

    class Meta:
        model = WakeAppProfile
        fields = ()
