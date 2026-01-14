from django.urls import path

from . import views

urlpatterns = [

  path('client-dashboard', views.client_dashboard, name="client-dashboard"),

  path('account-management-2', views.account_management, name="account-management-2"),

  path('delete-account-2', views.delete_account, name="delete-account-2"),

  path('article/<str:pk>/', views.client_article_detail, name='client-article-detail'),
  
  path('create-checkout-session/<str:plan_id>/', views.create_stripe_checkout, name='create-checkout-session'),
   
  path('subscription-success/', views.subscription_success, name='subscription-success'),
   
  path('subscription-cancel/', views.subscription_cancel, name='subscription-cancel'),
   
  path('webhook/', views.stripe_webhook, name='stripe-webhook'),

  path('subscription-request/', views.subscription_request, name='subscription-request'),

  path('donation/', views.donation_request, name='donation-request'),

  path('create-donation-session/', views.create_donation_checkout, name='create-donation-session'),

  path('donation-success/', views.donation_success, name='donation-success'),
  
  path('donation-cancel/', views.donation_cancel, name='donation-cancel'),
  
  

]   