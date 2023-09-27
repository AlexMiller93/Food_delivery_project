from django.urls import path

from accounts.views.auth_views import *
from accounts.views.accounts_views import *
from accounts.views.cards_views import *

app_name = 'accounts'

urlpatterns = [

    ### auth
    # http://localhost:8000/users/login
    # http://localhost:8000/users/logout
    # http://localhost:8000/users/register

    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    ### users
    # http://localhost:8000/users/admin
    # path('admin', all_users, name='all-users'),

    ### accounts
    # http://localhost:8000/users/admin/accounts/
    # http://localhost:8000/users/workers/
    path('admin/accounts/', all_accounts, name='all_accounts'),
    # path('workers', views.workers),

    # http://localhost:8000/users/admin/account/pk/
    # http://localhost:8000/users/account/
    # http://localhost:8000/users/account/add
    path('admin/account/<int:pk>', get_account, name='get_account'),
    path('account/', account_detail, name='account_detail'),
    path('account/add', create_account, name='create_account'),

    ### cards
    # http://localhost:8000/users/admin/cards/
    # http://localhost:8000/users/account/cards/
    # http://localhost:8000/users/account/cards/pk/
    path('admin/cards', all_cards, name='all_cards'),
    path('account/cards/', all_user_cards, name='all_user_cards'),
    path('account/cards/<int:pk>', get_user_card, name='get_user_card'),

]


