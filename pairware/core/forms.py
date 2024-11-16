from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Item, Message

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class ItemForm(forms.ModelForm):
    category = forms.CharField(max_length=100, help_text='Enter the category of your item (e.g., sock, glove)')

    class Meta:
        model = Item
        fields = ['category', 'description', 'image', 'location']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }