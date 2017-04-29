from django.contrib import admin
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import  Genre, Game, Transaction,Tag, Reward,Platform

#admin.site.register(Genre)
#admin.site.register(Game)
#admin.site.register(Transaction)



@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'display_game')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'display_game')

# Register the Admin classes for Book using the decorator


class GamesInline(admin.TabularInline):
    model = Transaction.game.through

    


# Register the Admin classes for BookInstance using the decorator



@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id','name','featured', 'display_platform','description','display_genre','display_tag','price')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','num_reward',  'display_game', 'display_used_reward','display_origin_price','display_trading_price','buyer')


@admin.register(Tag)   
class TagAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'owner','display_game')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
	list_display = ('id','date' ,'owner','due_date','status','transaction')