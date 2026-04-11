from django import forms
from .models import User

class UserSignupForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(
                attrs={
                    'type':'password',
                    'name': 'password2',
                    'required':True,
                    'class': 'w-full px-5 py-4 border border-ink-light rounded-xl focus:outline-none focus:ring-2 focus:ring-ink-accent/30 focus:border-ink-accent transition placeholder-ink-gray/60',
                    'placeholder':'••••••••'
                }))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'account_type']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class':'w-full px-5 py-4 border border-ink-light rounded-xl focus:outline-none focus:ring-2 focus:ring-ink-accent/30 focus:border-ink-accent transition placeholder-ink-gray/60',
                    'required':True,
                    'placeholder': 'Choose a username',
                    'type':'text', 
                    'name':'username'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'type':'email',
                    'name': 'email',
                    'required':True,
                    'class': 'w-full px-5 py-4 border border-ink-light rounded-xl focus:outline-none focus:ring-2 focus:ring-ink-accent/30 focus:border-ink-accent transition placeholder-ink-gray/60',
                    'placeholder':'basseydora@gmail.com'
                }

            ),
            'password': forms.PasswordInput(
                attrs={
                    'type':'password',
                    'name': 'password',
                    'required':True,
                    'class': 'w-full px-5 py-4 border border-ink-light rounded-xl focus:outline-none focus:ring-2 focus:ring-ink-accent/30 focus:border-ink-accent transition placeholder-ink-gray/60',
                    'placeholder':'••••••••'
                }
            )
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            self.add_error('password', 'Password Mismatch!')
            self.add_error('password2', 'Password Mismatch!')
        return cd.get('password2')
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
             self.add_error('email', 'Email already in use!')
        return self.cleaned_data.get('email')

class WriterCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['pen_name', 'profile_picture', 'writer_bio', 'genres']

        widgets = {
            'pen_name': forms.TextInput(attrs={
                'type':'text', 'name':'pen_name', 'requried':True,
                'class':'w-full px-5 py-4 border border-ink-light rounded-xl focus:outline-none focus:ring-2 focus:ring-ink-accent/30 focus:border-ink-accent transition placeholder-ink-gray/60',
                'placeholder':'The name readers will see'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'type':'file', 'name':'profile_picture', 'accept':'image/jpeg,image/png,image/webp',
                'class':'w-full px-5 py-4 border border-ink-light rounded-xl file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-ink-light file:text-ink-text hover:file:bg-ink-accent/10'
            }),
            'writer_bio': forms.Textarea(
                attrs={
                    'name':'writer_bio', 'rows':'6', 'required':'True',
                    'class':'w-full px-6 py-5 border border-ink-light rounded-xl focus:outline-none focus:ring-2 focus:ring-ink-accent/30 focus:border-ink-accent transition placeholder-ink-gray/60 resize-y',
                    'placeholder':'Tell readers about your writing journey, style, influences....'
                }
            ),
            'genres':forms.TextInput( attrs={
                'type':'text', 'name':'genres',
                'class':'w-full px-5 py-4 border border-ink-light rounded-xl focus:outline-none focus:ring-2 focus:ring-ink-accent/30 focus:border-ink-accent transition placeholder-ink-gray/60',
                'placeholder':'e.g. Poetry, Personal Essays, Speculative Fiction',
                'required':True
                }
            )
        }