from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from catalog import views as views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
url(
    r'^admin/password_reset/$',auth_views.password_reset,name='admin_password_reset',
),
url(
    r'^admin/password_reset/done/$',auth_views.password_reset_done,name='password_reset_done',
),
url(
    r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
    auth_views.password_reset_confirm,
    name='password_reset_confirm',
),
url(
    r'^reset/done/$',
    auth_views.password_reset_complete,
    name='password_reset_complete',
),

    url(r'^admin/',admin.site.urls)
]


urlpatterns += [
    url(r'^catalog/', include('catalog.urls')),
]

urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/catalog/', permanent=True)),
]

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
   url(r'^accounts/signup/$', views.signup, name='signup'),
   url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
]
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
