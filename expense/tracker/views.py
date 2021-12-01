from django.conf.urls import url
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import *
from .serializers import *
from rest_framework import generics, response
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import datetime
import pytesseract
import cv2
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet 
from django import forms
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')    
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
                
    else:
        form = UserRegistrationForm()
        
    return render(request, {'form' : form})

@login_required()
def login_request(request):
    r = request.get(url)
    result = r.json()
    print(result)
        

def ocr(request):
    PHOTO = 'bill3.png'
    image=cv2.imread(PHOTO,0)

    #convert it into text
    text=(pytesseract.image_to_string(image)).lower()
    print(text)

    #identify the date

    match=re.findall(r'\d+[/.-]\d+[/.-]\d+', text)

    st=" "
    st=st.join(match)
    #date
    print(st)


    nltk.download('punkt',quiet=True)
    nltk.download('wordnet',quiet=True)

    #lets try to extract title
    sent_tokens=nltk.sent_tokenize(text)
    #print(sent_tokens)
    y = sent_tokens[0].splitlines()[0]

    #lets find the price of the category.
    price=re.findall(r'[\$\£\€](\d+(?:\.\d{1,2})?)',text)
    price = list(map(float,price)) 
    print(max(price))
    x=max(price) 

    #till here we have extracted date,title and amount.
    #now its time to categorise bill whether it is shopping or grocery like wise
    #so i will first tokenise the text and search for key words
    print(word_tokenize(text))

    #we will remove punctuation
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    new_words = tokenizer.tokenize(text)
    print(new_words)

    #stop_words = set(nltk.corpus.stopwords.words('english')) 
    nltk.download('stopwords')

    #there are stop words like a ,an,the etc which are not required
    #so we need to filter them
    stop_words = set(nltk.corpus.stopwords.words('english')) 

    #there is the filetred list
    filtered_list=[w for w in new_words if w not in stop_words ]
    print(filtered_list)

    #entertainment
    entertainment = [] 
    for syn in wordnet.synsets("entertainment"): 
        for l in syn.lemmas(): 
            entertainment.append(l.name()) 
            
    l=['happy','restaurant','food','kitchen','hotel','room','park','movie','cinema','popcorn','combo meal']
    entertainment=entertainment+l


    #grocery
    
    grocery=[] 
    for syn in wordnet.synsets("grocery"): 
        for l in syn.lemmas(): 
            grocery.append(l.name())
    l3=['bigbasket','milk','atta','sugar','suflower','oil','bread','vegetabe','fruit','salt','paneer']
    grocery+=l3

    #investment
    investment=[] 
    for syn in wordnet.synsets("investment"): 
        for l in syn.lemmas(): 
            investment.append(l.name()) 
    l1=['endowment','grant','loan','applicant','income','expenditure','profit','interest','expense','finance','property','money','fixed','deposit','kissan','vikas']
    investment=investment+l1


    #shopping
    shopping=[]
    for syn in wordnet.synsets("dress"): 
        for l in syn.lemmas(): 
            shopping.append(l.name()) 
    l4=['iphone','laptop','saree','max','pantaloons','westside','vedic','makeup','lipstick','cosmetics','mac','facewash','heels','crocs','footwear','purse']
    shopping+=l4

    #here we will check that the bill belongs to which category
    #we will make that category true.
    for word in filtered_list:
        if word in entertainment:
            e=True
            break
        elif word in investment:
            inv=True
            break
        elif word in grocery:
            g=True
            break
        elif word in shopping:
            s=True
            break

                
    #question 2
    #this code the category in which the bill belongs to
    #if e is true then entertainment categrory and we will ,ake filename as entertainment.csv using
    #formatting
    if(e):
        cat = "entertainment"
    elif(inv):
        cat = "investment"
    elif(s):
        cat = "shopping"
    elif(g):
        cat = "grocery"
    else:
        cat = "others"

    
    sql = "Insert into Expenses values ({}, {}, {}, {})".format(id, cat, x, st)

    Expenses.objects.raw(sql)

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("templates\home.html")

def help(request):
    now = datetime.datetime.now()
    data = request.GET.get()
    return response(data)

def piechart(request):
    sql = "Select SUM(amount) from Expenses where MONTH(Date) = MONTH(CURRENT_DATE()) AND YEAR(columnName) = YEAR(CURRENT_DATE()) and User_Id = "
    key = "1"
    qu = sql+key
    test1 = Expenses.objects.raw(qu)
    test2 = Bank.objects.raw("Select budget from Bank where User_Id = key;")
    
    return response(test1)

class accountList(generics.ListCreateAPIView):
    queryset = account.objects.all()
    serializer_class = accountSerializer(queryset)
    

class accountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = account.objects.all()
    serializer_class = accountSerializer

class categoryList(generics.ListCreateAPIView):
    queryset = category.objects.all()
    serializer_class = categorySerializer

class categoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = category.objects.all()
    serializer_class = categorySerializer

class userList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializer

class userDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializer

class expenseList(generics.ListCreateAPIView):
    queryset = Expenses.objects.all()
    serializer_class = expensesSerializer

class expenseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expenses.objects.all()
    serializer_class = expensesSerializer

class incomeList(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = incomeSerializer

class incomeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = incomeSerializer

class bankList(generics.ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = bankSerializer

class bankDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bank.objects.all()
    serializer_class = bankSerializer

