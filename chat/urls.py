from django.urls import path
from . import views

urlpatterns = [
    path('show/<int:user_id>/', views.ShowMessageApiView.as_view()),
    path('direct/',views.DirectMessageGetApiView.as_view()),
    path('group/create/', views.GroupCreateView.as_view()),
    path('group/list/', views.GroupListView.as_view()),
    path('group/add/<int:group_id>/', views.GroupAddMemberView.as_view()),
    path('group/message/<int:group_id>/', views.GroupMessagesView.as_view()),
    path('group/members/<int:group_id>/', views.GroupMembersView.as_view()),
]