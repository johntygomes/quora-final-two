from mywebsite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
##################################################################
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import RegisterUserForm, LoginForm, NewQuestionForm, NewResponseForm, NewReplyForm
##################################################################
from utils.mail.mail_sender import MailSender
################################################################
from .models import User
################################################################
from authentication.serializers import setAuthenticationFalse,GOOGLE_AUTHENTICATED

# Create your views here.

def registerPage(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def loginPage(request):
    form = LoginForm()
    from authentication.serializers import MAIN_USER_IS_AUTHENTICATED,GOOGLE_AUTHENTICATED

    if request.method == 'POST':
        try:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise
    # context = {'form': form}
    context = {'MAIN_USER_IS_AUTHENTICATED':MAIN_USER_IS_AUTHENTICATED,
                'GOOGLE_AUTHENTICATED':GOOGLE_AUTHENTICATED}

    return render(request, 'login.html', context)

# @login_required(login_url='register')
def logoutPage(request):
    setAuthenticationFalse()
    return redirect('login-new')

# @login_required(login_url='register')
def newQuestionPage(request):
    from authentication.serializers import MAIN_USER_IS_AUTHENTICATED, MAIN_USER_ID
    form = NewQuestionForm()
    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = User.objects.get(id=MAIN_USER_ID)
                question.save()
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {'form': form,'MAIN_USER_IS_AUTHENTICATED':MAIN_USER_IS_AUTHENTICATED}
    return render(request, 'new-question.html', context)


def homePage(request):
    from authentication.serializers import MAIN_USER_IS_AUTHENTICATED,GOOGLE_AUTHENTICATED
    questions = Question.objects.all().order_by('-created_at')
    context = {
        'questions': questions,
        'MAIN_USER_IS_AUTHENTICATED':MAIN_USER_IS_AUTHENTICATED,
        'GOOGLE_AUTHENTICATED':GOOGLE_AUTHENTICATED
    }
    return render(request, 'homepage.html', context)

@csrf_exempt
def questionPage(request, id):
    from authentication.serializers import MAIN_USER_IS_AUTHENTICATED, MAIN_USER_ID
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = User.objects.get(id=MAIN_USER_ID)
                response.question = Question(id=id)
                question_object = Question.objects.get(id=id)
                mail = MailSender(question_object.author.email)
                mail.sendUserAnswerNotification(question_object, response.user)
                response.save()
                return redirect('/question/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
        'MAIN_USER_IS_AUTHENTICATED': MAIN_USER_IS_AUTHENTICATED
    }
    return render(request, 'question.html', context)


# @login_required(login_url='register')
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                question_object = Question.objects.get(id=question_id)
                # mail = MailSender(question_object.author.email)
                # mail.sendUserAnswerNotification(question_object, reply.user)
                reply.save()
                return redirect('/question/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise

    return redirect('index')

def emailverified(request):
    return render(request, 'email-verified.html')

def emailverificationfailed(request):
    return render(request, 'email-verification-failed.html')


def loginNew(request):
    return render(request, 'login-new.html')

def registerNew(request):
    return render(request, 'register-new.html')
    

