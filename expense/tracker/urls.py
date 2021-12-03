from django.urls import path
from tracker import views

urlpatterns = [


    path("login/", views.login_request, name="login"),
    path("signup/", views.register, name="signup"),

    path('account/', views.accountList.as_view()),
    path('account/<int:pk>/', views.accountDetail.as_view()),

    path('category/', views.categoryList.as_view()),
    path('category/<int:pk>/', views.categoryDetail.as_view()),

    path('user/', views.userList.as_view()),
    path('user/<int:pk>/', views.userDetail.as_view()),

    path('expense/', views.expenseinput, name="inpute"),
    path('expense/<int:pk>/', views.expenseDetail.as_view()),

    path('income/', views.incomeList.as_view()),
    path('income/<int:pk>/', views.incomeDetail.as_view()),

    path('bank/', views.bankList.as_view()),
    path('bank/<int:pk>/', views.bankDetail.as_view()),

    path('help/', views.help, name="help"),
    path('chart/', views.piechart, name="chart"),

    path('upload/', views.ocr, name="chart"),
]
