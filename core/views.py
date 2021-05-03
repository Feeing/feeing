from django.shortcuts import render
from .models import Group, Transactions, Notice, Question, Answer
from accounts.models import CustomUser
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .serializers import GroupSerializer, UserDetailSerializer, TransactionSerializer, NoticeSerializer, QuestionSerializer, AnswerSerializer, QnASerializer, TransactionGroupSerializer
import requests
import json
import datetime
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

class UserDetail(RetrieveAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    serializer_class = UserDetailSerializer

class GroupList(ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupCreate(CreateAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        #instance = GroupSerializer(data=request.data)
        #instance_serializer = User_groupSerializer({'user' : serializer['founder'], 'group' : serializer['group_id'], 'is_owner' : True})
        return serializer.save(founder = self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = CustomUser.objects.get(username=self.request.user)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        serializer.is_valid()
        user.in_groups.add(instance.group_id)
        user.save()
        null_data(instance.group_id)
        return Response(serializer.data)


def null_data(group_id) :
    null_transaction = Transactions()
    null_transaction.group_id = Group.objects.get(group_id=group_id)
    null_transaction.date = '2100-05-02'
    null_transaction.save()



class GroupDetail(RetrieveUpdateDestroyAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TransactionList (ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer

class TransactionAboutGroupList(ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TransactionGroupSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        queryset = Transactions.objects.filter(group_id=group_id)
        return queryset.order_by('-date')

def renew(request) :
    serializer = TransactionSerializer
    base_url = 'https://openapi.wooribank.com:444'
    url = '/oai/wb/v1/finance/getAccTransList/'
    groups = Group.objects.all()
    #print(groups)
    for group in groups :
    #print("app키 포스트요")
        app_key = 'l7xx9AYjYkHemmIcWdeehaAWW9sQxlTUCIH2'
        headers = {
            'Content-Type' : 'application/json; charset=utf-8',
            'appKey' : app_key,
            #'token' : '',
        }
        values  = {
            "dataHeader": {
                "UTZPE_CNCT_IPAD": "",
                "UTZPE_CNCT_MCHR_UNQ_ID": "",
                "UTZPE_CNCT_TEL_NO_TXT": "",
                "UTZPE_CNCT_MCHR_IDF_SRNO": "",
                "UTZ_MCHR_OS_DSCD": "",
                "UTZ_MCHR_OS_VER_NM": "",
                "UTZ_MCHR_MDL_NM": "",
                "UTZ_MCHR_APP_VER_NM": ""
            },
            "dataBody": {
                "INQ_ACNO": group.account_number,
                "INQ_STA_DT": group.start_date.strftime('%Y%m%d'),
                "INQ_END_DT": datetime.datetime.now().strftime('%Y%m%d'),
                "NEW_DT": "",
                "ACCT_KND": "P",
                "CUCD": "KRW"
            }
        }
        core_url = base_url+url
        response = requests.post(core_url, headers=headers, data=json.dumps(values))
        print(request)
        #response = urlopen(requests)
        rescode = response.status_code
        print(group)
        if(rescode == 200):
            response_all = response.json()
            #results = json.loads(response_body)
            print(response_all)
            response_body = response_all['dataBody']
            dataset = response_body['GRID']
            count = Group.objects.count()
            transaction_last = Transactions.objects.order_by('-date')[count+1]
            for element in dataset :
                money = (int(float(element['RCV_AM'])) if int(float(element['RCV_AM'])) > 0 else -int(float(element['PAY_AM'])))
                date = element['TRN_DT']
                content = element['TRN_TXT']
                balance = int(float(element['DPS_BAL']))
                last_date = 0
                real_date = transaction_last.date
                #if (transaction_last) :
                #    last_date = transaction_last.date
                date_string = "".join(date.split('-'))
                if(last_date < int(date_string)) :
                    transaction = Transactions()
                    transaction.group_id = group
                    transaction.content = content
                    transaction.money = money
                    transaction.balance = balance
                    transaction.date = date
                    transaction.save()
                    transactions_results = Transactions.objects.filter(date__gte = last_date)
                    AddGroupToUser(transactions_results)
        else : print("rescode 잘못 됨.")
    return HttpResponse("renew completed")

#class NoticeCreate(CreateAPIView) :
    #permission_classes = (permissions.IsAuthenticated, )
    #serializer_class = NoticeSerializer

    #def perform_create(self, serializer) :
        #serializer.save(writer = self.request.user, group_id = group_id)


def renew_group(request, group_id) :
    serializer = TransactionSerializer
    base_url = 'https://openapi.wooribank.com:444'
    url = '/oai/wb/v1/finance/getAccTransList/'
    group = Group.objects.get(pk = group_id)
    #print(groups)
    #print("app키 포스트요")
    app_key = 'l7xx9AYjYkHemmIcWdeehaAWW9sQxlTUCIH2'
    headers = {
        'Content-Type' : 'application/json; charset=utf-8',
        'appKey' : app_key,
        #'token' : '',
    }
    values  = {
        "dataHeader": {
            "UTZPE_CNCT_IPAD": "",
            "UTZPE_CNCT_MCHR_UNQ_ID": "",
            "UTZPE_CNCT_TEL_NO_TXT": "",
            "UTZPE_CNCT_MCHR_IDF_SRNO": "",
            "UTZ_MCHR_OS_DSCD": "",
            "UTZ_MCHR_OS_VER_NM": "",
            "UTZ_MCHR_MDL_NM": "",
            "UTZ_MCHR_APP_VER_NM": ""
        },
        "dataBody": {
            "INQ_ACNO": group.account_number,
            "INQ_STA_DT": group.start_date.strftime('%Y%m%d'),
            "INQ_END_DT": datetime.datetime.now().strftime('%Y%m%d'),
            "NEW_DT": "",
            "ACCT_KND": "P",
            "CUCD": "KRW"
        }
    }
    core_url = base_url+url
    response = requests.post(core_url, headers=headers, data=json.dumps(values))
    #response = urlopen(requests)
    rescode = response.status_code
    print(rescode)
    if(rescode == 200):
        response_all = response.json()
        #results = json.loads(response_body)
        print(response_all)
        response_body = response_all['dataBody']
        dataset = response_body['GRID']
        transaction_last = Transactions.objects.last()
        for element in dataset :
            money = (int(float(element['RCV_AM'])) if int(float(element['RCV_AM'])) > 0 else -int(float(element['PAY_AM'])))
            date = element['TRN_DT']
            content = element['TRN_TXT']
            balance = int(float(element['DPS_BAL']))
            last_date = 0
            if (transaction_last) :
                last_date = transaction_last.date
            print(last_date)
            print(money)
            print(content)
            print(date)
            if(last_date < date) :
                transaction = Transactions()
                transaction.group_id = group
                transaction.content = content
                transaction.money = money
                transaction.balance = balance
                transaction.date = date
                transaction.save()
            transactions_results = Transactions.objects.filter(date__gt = last_date)
            AddGroupToUser(transactions_results)
    else : print("rescode 잘못 됨.")
    return HttpResponse("renew completed")



class NoticeList(ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()

class NoticeOfGroup(ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = NoticeSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        queryset = Notice.objects.filter(group_id=group_id)
        return queryset.order_by('-pub_date')

class NoticeDetail(RetrieveUpdateDestroyAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class QuestionList(ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class QuestionOfGroup(ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        group_id = self.kwargs['group_id']
        queryset = Notice.objects.filter(group_id = group_id)
        return queryset.order_by('-pub_date')

class QuestionDetail(RetrieveUpdateDestroyAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Notice.objects.all()
    serializer_class = QuestionSerializer

class AnswerList(ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerDetail(RetrieveUpdateDestroyAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class QnADetail(ListAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = QnASerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        queryset = Question.objects.filter(group_id=group_id)
        return queryset.order_by('-pub_date')


def home(request) :
    return render(request, 'home.html')


def AddGroupToUser(transactions_results) :
    for transaction in transactions_results :
        content = transaction.content
        group_id = transaction.group_id
        try :
            update_user = CustomUser.objects.get(username = content)
            update_user.in_groups.add(group_id)
        except : 
            pass

class UpdateTitle(RetrieveUpdateDestroyAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    #def get_queryset(self):
    #    transaction_id = self.kwargs['pk']
    #    title = self.kwargs['title']
    #    queryset = Transactions.objects.get(id = transaction_id)
    #    print(queryset)
    #    print(transaction_id)
    #    print(type(transaction_id))
    #    queryset.title = title
    #    return queryset


class UpdateMemo(RetrieveUpdateDestroyAPIView) :
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer