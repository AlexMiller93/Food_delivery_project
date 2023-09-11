from django.urls import path

from accounts.views.auth_views import *
from accounts.views.accounts_views import *
from accounts.views.cards_views import *

urlpatterns = [

    ### auth
    # http://localhost:8000/users/login
    # http://localhost:8000/users/logout
    # http://localhost:8000/users/register

    path('login', LoginView.as_view(), name='user-logout'),
    # path('logout', LogoutView.as_view(), name='user-logout'),
    path('register', user_register, name='user-register'),

    ### users
    # http://localhost:8000/users/admin
    path('admin', all_users, name='all-users'),

    ### accounts
    # http://localhost:8000/users/admin/accounts/
    # http://localhost:8000/users/workers/
    path('admin/accounts/', all_accounts, name='all-accounts'),
    # path('workers', views.workers),

    # http://localhost:8000/users/admin/account/pk/
    # http://localhost:8000/users/account/
    path('admin/account/<int:pk>', get_account, name='get-account'),
    path('account/', account_detail, name='account-detail'),

    ### cards
    # http://localhost:8000/users/admin/cards/
    # http://localhost:8000/users/account/cards/
    # http://localhost:8000/users/account/card/pk/
    path('admin/cards', all_cards, name='all-cards'),
    path('account/cards/', all_user_cards, name='all-user-cards'),
    path('account/card/<int:pk>', get_user_card, name='get-user-card'),

]
