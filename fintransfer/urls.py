

"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [
     path('cabinet/', include('cabinet.urls')),
]


# Добавьте URL соотношения, чтобы перенаправить запросы с корневового URL, на URL приложения
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/cabinet/invoice', permanent=True)),
]

# Используйте static() чтобы добавить соотношения для статических файлов
# Только на период разработки
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name="registration/logged_out.html"), name='logout'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name = "registration/password_reset_confirm.html"),
        name='password_reset_confirm')

]