from allauth.account.forms import LoginForm as BaseLoginForm

class CustomLoginForm(BaseLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'Email'