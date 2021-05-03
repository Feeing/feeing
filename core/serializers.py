from rest_framework import serializers
from .models import Group, Transactions, Notice, Question, Answer
from accounts.models import CustomUser

class GroupSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Group
        fields = ['group_id', 'group_name', 'founder', 'account_owner', 'account_number', 'renew_time', 'start_date']


class UserDetailSerializer(serializers.ModelSerializer) :
    in_groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'phone', 'bank_account', 'in_groups']

class TransactionSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Transactions
        fields = ['group_id', 'title', 'content', 'money', 'balance', 'date', 'memo']

class TransactionGroupSerializer(serializers.ModelSerializer) :
    founder_name = serializers.CharField(source='group_id.founder.username')
    class Meta:
        model = Transactions
        fields = ['group_id', 'id', 'title', 'content', 'money', 'balance', 'date', 'memo', 'founder_name']


class NoticeSerializer(serializers.ModelSerializer) :
    founder_name = serializers.CharField(source='group_id.founder.username')
    class Meta:
        model = Notice
        fields = ['group_id', 'id', 'title', 'pub_date', 'writer', 'body', 'founder_name']


class QuestionSerializer(serializers.ModelSerializer) :
    founder_name = serializers.CharField(source='group_id.founder.username')
    class Meta :
        model = Question
        fields = ['group_id', 'id', 'title', 'pub_date', 'writer', 'body', 'is_answered', 'founder_name']


class AnswerSerializer(serializers.ModelSerializer) :
    writer = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'name'
    )
    class Meta : 
        model = Answer
        fields = ['question', 'writer', 'content']


class QnASerializer(serializers.ModelSerializer) :
    answers = AnswerSerializer(many=True, read_only=True)
    writer = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'name'
    )

    class Meta:
        model = Question
        fields = ['group_id', 'id', 'title', 'pub_date', 'writer', 'body', 'answers']