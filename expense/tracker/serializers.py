from rest_framework import serializers
from .models import *

class accountSerializer(serializers.ModelSerializer):
  class Meta:
    model = account
    fields = ('User_Id', 'Username', 'Password')

class categorySerializer(serializers.ModelSerializer):
  class Meta:
    model = category
    fields = ('cat_id', 'Name')

class userSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('User_Id', 'Name', 'contact', 'email', 'dob')

class expensesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Expenses
    fields = ('UserId', 'catid', 'Amount', 'Date', 'AccountNo')

class incomeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Income
    fields = ('User_Id', 'Income', 'Otherpay', 'Date', 'Bankac_id', 'Total')

class bankSerializer(serializers.ModelSerializer):
  class Meta:
    model = Bank
    fields = ('User_Id','Bankac_id', 'Bank_name', 'Total_balance','Budget')

