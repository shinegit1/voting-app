from django.urls import path
from polls import views

app_name = 'polls'
urlpatterns = [
    path('',views.home_page,name='welcome'),
    path('home/', views.IndexView.as_view(), name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup,name='signup'),
    path('logout/', views.user_logout,name='logout'),
]