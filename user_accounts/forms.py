from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser




class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('contactNumber',)


# collects data for user creation.
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))

 
    class Meta:
        model = CustomUser

        fields = (
            'username',
            'first_name',
            'last_name',
            'contactNumber',
            'email',
            'terms',
        )

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
                'type': 'email'
            }), 

            'contactNumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact number',
            }),

            'terms': forms.CheckboxInput(attrs={
                'required': True,
            }),       
                      
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


# this form is presented before the registration form.
# for the purpose of determining if the user is a Job Seeker of a Company interested in Job Seekers
class PreRegistrationForm(forms.Form):
   USER_TYPES = [
       ('Truck Driver', 'Truck Driver'),
       ('Company', 'Company'),
   ] 
   user_type = forms.CharField(required=True, widget=forms.RadioSelect(
       choices=USER_TYPES,
       attrs={
           'class': 'control-form user_types_radios'
        }
    ))
