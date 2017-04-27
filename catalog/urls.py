from django.conf.urls import url

from . import views



urlpatterns = [
url(r'^profile/$', views.profile, name='profile'),
# url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
url(r'^$', views.index, name='index'),
url(r'^genres/$', views.GenreListView.as_view(), name='genres'),
url(r'^genre/(?P<pk>\d+)$', views.GenreDetailView.as_view(), name='genre-detail'),
url(r'^games/$', views.GameListView.as_view(), name='games'),
url(r'^game/(?P<pk>\d+)$', views.GameDetailView.as_view(), name='game-detail'),
url(r'^transactions/$', views.TransactionListView.as_view(), name='transactions'),
url(r'^transactions/(?P<pk>\d+)$', views.TransactionDetailView.as_view(), name='transaction-detail'),
url(r'^tags/$', views.TagListView.as_view(), name='tags'),
url(r'^tag/(?P<pk>\d+)$', views.TagDetailView.as_view(), name='tag-detail'),
url(r'^reward/(?P<pk>\d+)$', views.RewardDetailView.as_view(), name='reward-detail'),
]

urlpatterns += [   
url(r'^mygames/$', views.BoughtGamesByUserListView.as_view(), name='my-bought'),
url(r'^mytags/$', views.OwnedTagsByUserListView.as_view(), name='my-tags'),
url(r'^myrewards/$', views.OwnedRewardsByUserListView.as_view(), name='my-rewards'),
]


urlpatterns += [  
url(r'^transaction/create/$', views.TransactionCreate.as_view(),name='transaction-create',),
url(r'^transaction/(?P<pk>\d+)/update/$', views.TransactionUpdate.as_view(), name='transaction-update'),
url(r'^transaction/(?P<pk>\d+)/delete/$', views.TransactionDelete.as_view(), name='transaction-delete'),
]


urlpatterns += [  
url(r'^tag/create/$', views.TagCreate.as_view(), name='tag-create'),
url(r'^tag/(?P<pk>\d+)/update/$', views.TagUpdate.as_view(), name='tag-update'),
url(r'^tag/(?P<pk>\d+)/delete/$', views.TagDelete.as_view(), name='tag-delete'),
]