from django import forms
from .models import Event, Booking, Profile, CustomUser, Register, Membership, Course

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'category', 'description', 'date', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class RegisterForm(forms.ModelForm):
    membership_type = forms.CharField(
        initial='Individual Membership', 
        disabled=True  # Make the field greyed out (read-only)
    )

    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'interests', 'gender', 'membership_type']

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = '__all__'
        widgets = {
            'name': forms.Select(choices=Membership.objects.values_list('name', 'name'), attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'benefits': forms.SelectMultiple(attrs={'class': 'form-control'}),  # Allow multiple benefit selection
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'category', 'date', 'description', 'image']