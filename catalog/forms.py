from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Transaction, Reward
from django.forms.models import inlineformset_factory
from django.core.validators import MaxValueValidator

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email' )


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('game','num_reward')

	# first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
 #    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
 #    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # def clean_game(self):
    # 	 data = self.cleaned_data['game']
    # 	 return data
    # def clean_reward_set(self):
    # 	data = self.cleaned_data['reward_set']
    # 	return data
    # class Meta:
    #     model = Transaction
    #     fields = ('game', 'reward_set' )

class RewardForm(ModelForm):
    class Meta:
        model = Reward
        fields = ('date',)
    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super(Reward, self).__init__(*args, **kwargs)
        self.fields["owner"].queryset = Subject.objects.filter(owner=owner)

RewardFormSet = inlineformset_factory(Transaction, Reward,fields=('date',), can_delete=False,form=RewardForm)


