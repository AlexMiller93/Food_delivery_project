from django.urls import path

from .views.auth_views import *
from .views.accounts_views import *
from .views.cards_views import *

app_name = 'accounts'

urlpatterns = [

    # --> auth
    # http://localhost:8000/users/login
    # http://localhost:8000/users/logout
    # http://localhost:8000/users/register

    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # --> users
    # http://localhost:8000/users/admin
    path('admin', AllUsersView.as_view(), name='all_users'),

    # --> accounts CBV
    path('admin/accounts/', AllAccountsView.as_view(), name='all_accounts'),
    path('workers/', AllWorkersView.as_view(), name='all_workers'),

    path('admin/accounts/<int:pk>', AccountAdminView.as_view(), name='get_account'),
    path('accounts/<int:pk>', AccountDetailView.as_view(), name='account_detail'),
    path('accounts/add', AccountCreateView.as_view(), name='create_account'),

    # --> cards
    # http://localhost:8000/users/admin/cards/
    # http://localhost:8000/users/account/cards/
    # http://localhost:8000/users/account/cards/pk/
    ## CBV
    path('admin/cards', GetAllCardsView.as_view(), name='all_cards'),
    path('accounts/cards/', GetAllUserCardsView.as_view(), name='all_user_cards'),
    path('accounts/cards/<int:pk>', GetUserCardView.as_view(), name='get_user_card'),

    ## FBV
    # path('admin/cards', all_cards, name='all_cards'),
    # path('account/cards/', all_user_cards, name='all_user_cards'),
    # path('account/cards/<int:pk>', get_user_card, name='get_user_card'),

]
