from django.urls import path
from . import views

urlpatterns = [
    path('info/<str:id>/', views.UserInfoView.as_view(), name='home'),
    path('info/change/username/', views.UsernameUpdateView.as_view(), name='change-username'),
    path('info/change/update/',views.UserInfoUpdateView.as_view(), name='change-info'),
    path('search/<str:user_name>/', views.SearchUserView.as_view(), name='search-user'),
    path('toggle/follow/<int:user_id>/',views.ToggleFollowUserView.as_view(), name='follow'),
    path('is/follow/<int:user_id>/',views.IsFollowUserView.as_view(), name='is-follow'),
    path('followers/', views.FollowersView.as_view(), name='followers'),
    path('following/', views.FollowingView.as_view(), name='followers'),
    path('toggle/Not_Interested/<int:user_id>/', views.ToggleNotInterestedUserView.as_view(), name='Toggle_Not_Interested'),
    path('Not_Interested/all', views.NotInterestedView.as_view(), name='Show_all_Not_Interested'),
    path('is/Not_Interested/<int:user_id>/',views.IsNotinterestedUserView.as_view(), name='is-IsNotinterested'),

]
