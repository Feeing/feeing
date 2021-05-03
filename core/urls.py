from django.urls import include
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GroupList, GroupDetail, GroupCreate, UserDetail, renew, renew_group, TransactionAboutGroupList, TransactionList, NoticeList, NoticeOfGroup, NoticeDetail, QuestionList, QuestionDetail, QuestionOfGroup, AnswerList, QnADetail, UpdateTitle, UpdateMemo

urlpatterns = [
    path('groups/', GroupList.as_view()),
    path('groups/create/', GroupCreate.as_view()),
    path('groups/<int:pk>/', GroupDetail.as_view()),
    path('users/<str:username>/', UserDetail.as_view()),
    path('transaction/renew/', renew, name='renew'),
    path('transaction/renew/group/<int:group_id>', renew_group, name='renew_group'),
    path('transaction/group/<int:group_id>', TransactionAboutGroupList.as_view()),
    path('transaction/list', TransactionList.as_view()),
    #path('notice/create/', NoticeCreate.as_view()),
    path('notice/list', NoticeList.as_view()),
    path('notice/list/group/<int:group_id>', NoticeOfGroup.as_view()),
    path('notice/<int:pk>', NoticeDetail.as_view()),
    path('question/list', QuestionList.as_view()),
    path('question/list/group/<int:group_id>', QuestionOfGroup.as_view()),
    path('question/<int:pk>', QuestionDetail.as_view()),
    path('question/list/group/detail/<int:group_id>', QnADetail.as_view()),
    path('answer/list', AnswerList.as_view()),
    path('transaction/modify/title/<int:pk>', UpdateTitle.as_view()),
    path('transaction/modify/memo/<int:pk>', UpdateMemo.as_view())

]

urlpatterns+=[
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]