from django.db import models
# from django.utils import ErrorList
from django.shortcuts import render
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Genre,Game,Transaction, Tag, Reward
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, EditProfileForm, TransactionForm,RewardFormSet ,RewardForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
import datetime
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.functional import curry
from django.views.generic import TemplateView
from django.forms.models import inlineformset_factory



def profile(request):
    if request.user.is_authenticated():
        user = request.user
        return render(
            request,
            'catalog/profile.html',
            context={ 'first_name':user.first_name, 'last_name':user.last_name,'email':user.email}
            )
    return render(
            request,
            'catalog/profile.html',
            context={}
            )




# def edit_profile(request):
#     user = Article.objects.get(username=request.ue)
#     form = EditProfileForm(request.POST or None, initial={'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email})
#     if request.method == 'POST':
#         if form.is_valid():
#             user.first_name=request.POST.get('first_name')
#             user.last_name=request.POST.get('last_name')
#             user.email=request.POST.get('email')
#             user.save()
#             return HttpResponseRedirect('%s'%(reverse('profile')))
#     context = {
#         "form": form
#     }
#     return render(request, 'catalog/edit_profile.html', context)



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class OwnedTagsByUserListView(LoginRequiredMixin,generic.ListView):
    model = Tag
    template_name ='catalog/tag_list_owned_user.html'
    paginate_by = 10
    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user).order_by('id')



def index(request):
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    num_genres=Genre.objects.all().count()
    num_games=Game.objects.all().count()
    num_tags=Tag.objects.all().count()
    if request.user.is_authenticated():
        if num_visits==1:
            gift = Reward( owner=request.user)
            gift.save()
        return render(
            request,
            'index.html',
            context={ 'num_visits':num_visits,'num_genres':num_genres, 'num_games':num_games,'num_tags':num_tags,'games_rcmd':Game.objects.filter(tag__game__transaction__buyer=request.user).distinct().exclude(transaction__buyer=request.user).distinct()[:3],'accumulated_amount':sum([game.price for game in Game.objects.filter(transaction__buyer=request.user)])}
            )
    return render(
        	request,
        	'index.html',
        	context={'num_genres':num_genres, 'num_games':num_games,'num_tags':num_tags}
        	)

class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class GenreDetailView(generic.DetailView):
    model = Genre



class TagListView(generic.ListView):
    model = Tag
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class TagDetailView(generic.DetailView):
    model = Tag

class RewardDetailView(generic.DetailView):
    model = Reward

class GameListView(generic.ListView):
    model = Game
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class GameDetailView(generic.DetailView):
    model = Game

class TransactionListView(generic.ListView):
    model = Transaction
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class TransactionDetailView(generic.DetailView):
    model = Transaction

from django.contrib.auth.mixins import LoginRequiredMixin

class BoughtGamesByUserListView(LoginRequiredMixin,generic.ListView):
    model = Transaction
    template_name ='catalog/transaction_list_bought_user.html'
    paginate_by = 10
    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user).order_by('id')

class OwnedTagsByUserListView(LoginRequiredMixin,generic.ListView):
    model = Tag
    template_name ='catalog/tag_list_owned_user.html'
    paginate_by = 10
    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user).order_by('id')


class OwnedRewardsByUserListView(LoginRequiredMixin,generic.ListView):
    model = Reward
    template_name ='catalog/reward_list_owned_user.html'
    paginate_by = 10
    def get_queryset(self):
        return Reward.objects.filter(owner=self.request.user).order_by('id')


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



class TransactionCreate(CreateView):
    model = Transaction
    fields = ['game','num_reward']
    def form_valid(self, form):
        form.instance.buyer = self.request.user
        num=form.instance.num_reward
        if num <0 or num >10 or  not Reward.check_num(self.request.user,num):
            return self.form_invalid(form)
        return super(TransactionCreate, self).form_valid(form)
    def get_success_url(self):
        Reward.use_reward(self.request.user,self.object.num_reward,self.object)
        return reverse('index')
       

class TransactionUpdate(UpdateView):
    model = Transaction
    fields = '__all__'

class TransactionDelete(DeleteView):
    model = Transaction
    success_url = reverse_lazy('transactions')

class TagCreate(CreateView):
    model = Tag
    fields = ['name','game']
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(TagCreate, self).form_valid(form)

class TagUpdate(UpdateView):
    model = Tag
    fields = '__all__'

class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('tags')




