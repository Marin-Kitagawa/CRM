from django.urls import path

from django.contrib.auth import views as auth_views

from .import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('account/', views.accountSettings, name='account'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('user/', views.userPage, name='user-page'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),  # Making the url dynamic
    path('create_order/<str:primary_key_>/', views.createOrder, name='create_order'),
    path('update_order/<str:primary_key_>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:primary_key_>/', views.deleteOrder, name='delete_order'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', html_email_template_name='accounts/password_reset_email.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),
]
