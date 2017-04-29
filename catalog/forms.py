from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Transaction, Reward,Tag,Game
from django.forms.models import inlineformset_factory
from django.core.validators import MaxValueValidator

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    picture = forms.FileField(help_text='Your Icon')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','picture' )

class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email' )



# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ('description', 'document', )

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('game','num_reward')
    def __init__(self, *args, **kwargs):
        buyer = kwargs.pop('owner')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields["game"].queryset = Game.objects.all().exclude(transaction__buyer=buyer)


class TransactionSingleForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('num_reward',)


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ('name','game',)
    def __init__(self, *args, **kwargs):
        buyer = kwargs.pop('owner')
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields["game"].queryset = Game.objects.filter(transaction__buyer=buyer).distinct()

# class ReviewForm(ModelForm):
#     class Meta:
#         model = Review
#         fields = ('content',)
    # def __init__(self, *args, **kwargs):
    #     buyer = kwargs.pop('owner')
    #     super(TagForm, self).__init__(*args, **kwargs)
    #     self.fields["game"].queryset = Game.objects.filter(transaction__buyer=buyer).distinct()

class TagSingleForm(ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
    # def __init__(self, *args, **kwargs):
    #     buyer = kwargs.pop('owner')
    #     super(TagForm, self).__init__(*args, **kwargs)

class RewardForm(ModelForm):
    class Meta:
        model = Reward
        fields = ('date',)
    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super(Reward, self).__init__(*args, **kwargs)
        self.fields["owner"].queryset = Subject.objects.filter(owner=owner)

RewardFormSet = inlineformset_factory(Transaction, Reward,fields=('date',), can_delete=False,form=RewardForm)


