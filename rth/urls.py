from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
app_name='rth'
urlpatterns = [
    path('',views.index , name='index'),
    path('logout/', views.logout),
    path('register/', views.register),
    path('login/', views.login),
    # path('admin/logout/', views.logout),
    path('inbox/',views.inbox),
    path('search/', views.search),
    path('cart/', views.cart),
    path('addcart/<str:id>/<str:qty>/', views.add_to_cart),
    # path('myprofile', views.myprofile, name='myprofile'),
    #path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        # email_template_name='registration/password_reset_email.html',
        # subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    path('my/', views.myprofile, name="profile"),
    path('my/inbox/' , views.myInbox),
    path('my/orders/',views.myorders),
    path('orders/',views.ordersView),

    path('api/myorders/',views.MyOrderapi.as_view()),

    path('my/products/', views.profile1, name="profile1"),
    path('myprofile/delete/<str:number>', views.deletemyproduct, name='deletemyproduct'),
    path('myprofile/updatemyproduct/', views.updatemyproduct, name='updatemyproduct'),
    path('api/myproducts/', views.Myproductapi.as_view()),
    path('api/mysellerorders/', views.MySellerOrderapi.as_view()),
    # path('mpesa/callback/', views.mpesaCallback.as_view())
    path('mpesa/callback/', views.MpesaIPN)
]
