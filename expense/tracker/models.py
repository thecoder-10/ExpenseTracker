from django.db import models

# Create your models here.

class account(models.Model):
    User_Id = models.IntegerField(primary_key=True)
    Username = models.CharField(max_length=225)
    Password = models.CharField(max_length=225)

    def __unicode__(self):
        return self.User_Id

class category(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=225)

    def __unicode__(self):
        return self.cat_id

class User(models.Model):
    User_Id = models.ForeignKey(account,  on_delete=models.CASCADE)
    Name = models.CharField(max_length=225)
    contact = models.BigIntegerField()
    email = models.CharField(max_length=225)
    dob = models.DateField()

    def __unicode__(self):
        return self.User_Id

class Bank(models.Model):
    User_Id =  models.ForeignKey(account,  on_delete=models.CASCADE)
    Bankac_id = models.IntegerField()
    Bank_name = models.CharField(max_length=225)
    Total_balance = models.FloatField()
    Budget = models.FloatField()

    def __unicode__(self):
        return self.Bankac_id

class Expenses(models.Model):
    UserId =  models.ForeignKey(account,  on_delete=models.CASCADE)
    catid = models.ForeignKey(category,  on_delete=models.CASCADE)
    Amount = models.FloatField()
    Date = models.DateField(auto_now_add=True, blank=True)
    Bankac_id = models.ForeignKey(Bank,  on_delete=models.CASCADE)
    

class Income(models.Model):
    User_Id =  models.ForeignKey(account,  on_delete=models.CASCADE)
    Income = models.FloatField()
    Otherpay = models.FloatField()
    Date = models.DateField(auto_now_add=True, blank=True)
    Bankac_id = models.ForeignKey(Bank,  on_delete=models.CASCADE)
    Total = models.FloatField()


