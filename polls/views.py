from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from polls.models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from polls.forms import UserSignUp
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def home_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    else:
        return render(request, 'polls/welcome.html')


# Index page after log in by user
class IndexView(generic.ListView): 
    template_name = 'polls/index.html' 
    context_object_name = 'latest_question_list' 
    def get_queryset(self): 
        """Return the last five published questions.""" 
        return Question.objects.filter( pub_date__lte=timezone.now() ).order_by('-pub_date')[:10]

# voting details view here
class DetailView(generic.DetailView): 
    model = Question 
    template_name = 'polls/detail.html' 
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# results view here
class ResultsView(generic.DetailView): 
    model = Question 
    template_name = 'polls/result.html'

# To vote for desired option by user
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question,
        'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# user login view here
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/home/')
        else:
            fm=AuthenticationForm()
        return render(request, 'polls/login.html', {'form':fm})
    else:
        return HttpResponseRedirect('/login/')

# user logout view here
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# sign up by user
def user_signup(request):
    if request.method=='POST':
        fm=UserSignUp(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Account created successfully. Please Log in now.')
    else:
        fm=UserSignUp()
        messages.success(request, 'Sign Up for only New User')
    return render(request, 'polls/signup.html', {'form':fm})

