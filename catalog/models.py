from __future__ import unicode_literals
import time
import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import date
import decimal
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances


class Platform(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a game genre (e.g. War, Sports.)")
    def __str__(self):
        return self.name
    def display_game(self):
        return ', '.join([ game.name for game in self.game_set.all()[:10] ])
        display_game.short_description = 'Game'


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a game genre (e.g. War, Sports.)")
    def __str__(self):

        return self.name
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])
    def display_game(self):
        return ', '.join([ game.name for game in self.game_set.all()[:10] ])
        display_game.short_description = 'Game'

class Game(models.Model):
    platform = models.ManyToManyField(Platform, help_text="Select platforms for this game")
    genre = models.ManyToManyField(Genre, help_text="Select genres for this game")
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the game")
    price= models.DecimalField(max_digits=5, decimal_places=2)
    featured=models.BooleanField(default=False)
    def __str__(self):
        return self.name    
    def get_absolute_url(self):
        return reverse('game-detail', args=[str(self.id)])
    def display_platform(self):
        return ', '.join([ platform.name for platform in self.platform.all()[:3] ])
        display_platform.short_description = 'Platform'
    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
        display_genre.short_description = 'Genre'

    def display_tag(self):
        return ', '.join([ tag.name for tag in self.tag_set.all()[:3] ])
        display_tag.short_description = 'Tag'

class Tag(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a game tag(e.g. Excellent, Funny.)")
    game = models.ManyToManyField(Game, help_text="Select a genre for this game")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('tag-detail', args=[str(self.id)])   
    def display_game(self):
        return ', '.join([ game.name for game in self.game.all()[:10] ])
        display_game.short_description = 'Game'     

class Transaction(models.Model):
    game = models.ManyToManyField(Game, help_text="Select the games to be bought")
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    num_reward = models.IntegerField()
    def get_absolute_url(self):
        return reverse('transaction-detail', args=[str(self.id)])
    def __str__(self):
        return '%s (%s)' % (self.id,self.game.name)
    def display_game(self):
        return ', '.join([ game.name for game in self.game.all()[:10] ])
        display_game.short_description = 'Game'
    def display_used_reward(self):
        return ', '.join([ str(reward.id) for reward in self.reward_set.all() ])
        display_reward.short_description = 'Reward'
    def display_origin_price(self):
        return round(sum([game.price for game in self.game.all()]),3)
    def display_trading_price(self):
        return round(sum([game.price for game in self.game.all()])*decimal.Decimal(1-0.2*self.reward_set.count()),3)

class Reward(models.Model):
    date=models.DateField( default=datetime.date.today)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    transaction= models.ForeignKey(Transaction, blank=True,null=True)
    def __str__(self):
        return str(self.id)
    def due_date(self):
        return self.date+datetime.timedelta(days=120)
    def status(self):
        if self.transaction==None:
            if self.due_date() >self.date:
                return 'Valid'
            return 'Unvalid'
        return 'Used'
    def get_absolute_url(self):
        return reverse('reward-detail', args=[str(self.id)])  

    @staticmethod 
    def check_num(user,num):
        tmptNum=0;
        for i in Reward.objects.filter(owner=user):
            if i.status()=='Valid':
                tmptNum=tmptNum+1
        if tmptNum<num:           
            return False
        return True

    @staticmethod 
    def use_reward(user,num,trans):
        for i in range(num):
            tmpt=0
            for j in Reward.objects.filter(owner=user).order_by('date'):
                if tmpt==num:
                    return
                if j.status()=='Valid':
                    j.transaction=trans
                    j.save()
                    tmpt=tmpt+1
    @staticmethod               
    def update_reward(user):
        while sum([t.display_trading_price() for t in Transaction.objects.filter(buyer=user)])-100*(Reward.objects.filter(owner=user).count()-1)>100:
            gift = Reward( owner=user)
            gift.save()



