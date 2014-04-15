from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.db.models import Max
from brothers.models import Brother
from django.contrib.auth.models import User as DJuser
from django.contrib.auth import authenticate, login as DJlogin, logout as DJlogout
from django.contrib.auth.decorators import login_required
from email.utils import parseaddr
from django.core.mail import send_mail
from time import strftime, localtime
from django.contrib import messages
from brothers.forms import UserForm, LoginForm, MessageForm, MessageEmailForm, ForgotForm, newPassForm, EditForm
from django import forms
from django.core.validators import validate_email
import string
import random


def home(request):
    if request.user.is_authenticated() and request.user.is_active:
        return render(request, 'brothers/home.html',{'user':request.user.first_name,'form':MessageForm()})
    else:
    	form = LoginForm()
        return render(request, 'brothers/login.html',{'form':form})

@login_required(login_url="brothers.views.login")
def index(request):
    return redirect('/')
@login_required(login_url="brothers.views.login")
def detail(request, scroll):
    b = Brother.objects.get(scroll=scroll)
    return render(request, 'brothers/index.html',{'brother':b,'littles':Brother.objects.filter(bigS=b.scroll),'lastScroll':Brother.objects.all().aggregate(Max('scroll'))['scroll__max'],'tree':getTree(b.scroll),'form':MessageForm()})

def editBrother(request,scroll):
    if not request.user.is_superuser:
        return redirect('/brothers/'+scroll)
    if request.method == "POST":
        form = EditForm(request.POST,b=Brother.objects.get(scroll=scroll))
        if form.is_valid():
            brother = Brother.objects.get(scroll=scroll)
            brother.fname = request.POST["fname"]
            brother.lname = request.POST["lname"]
            brother.name = request.POST["name"]
            brother.pc = request.POST["pc"]
            brother.nickname = request.POST["nickname"]
            brother.big = request.POST["big"]
            if brother.big != "Unknown":
                brother.bigS = Brother.objects.get(name=brother.big).scroll
            brother.save()
            return redirect('/brothers/'+scroll)
        else:
            return render(request,'brothers/edit.html',{'form':form})
    else:
        return render(request,'brothers/edit.html',{'form':EditForm(b=Brother.objects.get(scroll=scroll))})



@login_required(login_url="brothers.views.login")
def scroll(request):
    return render(request, 'brothers/scroll.html',{'brothers':Brother.objects.all()})
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
            	DJlogin(request,user)
            	return redirect('/')
            else:
            	return TemplateResponse(request,'brothers/login.html',{'form':form,'error':"Invalid Username or Password."})
        else:
            return TemplateResponse(request,'brothers/login.html',{'form':form})
    else:
    	form = LoginForm()
        return TemplateResponse(request,'brothers/login.html',{'form':form})
@login_required(login_url="brothers.views.login")
def logout(request):
    DJlogout(request)
    return redirect('/')
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            emailaddr = request.POST['email']
            authentication = request.POST['authKey']
            newUser = DJuser.objects.create_user(username,emailaddr,password)
            newUser.first_name = request.POST['fname']
            newUser.last_name = request.POST['lname']
            newUser.save()
            user = authenticate(username=username,password=password)
            DJlogin(request,user)
            return redirect('/')
        else:
            messForm = MessageEmailForm()
            return TemplateResponse(request,'brothers/register.html',{'form':form,'messForm':messForm})
    else:
        form = UserForm()
        messForm = MessageEmailForm()
        return TemplateResponse(request, 'brothers/register.html',{'form':form,'messForm':messForm})

def forgot(request):
    if request.method == "POST":
        form = ForgotForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            #raise forms.ValidationError("Username: "+username+"  Email: "+email)
            if username == "" and email == "":
                return redirect('/')
            if username != "":
                email = DJuser.objects.get(username=username).email
            user = DJuser.objects.get(email=email)
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            message = "This message is intended for "+user.first_name+" "+user.last_name+". If this is not you, please disregard this message.\n"
            message+= "Your previous password is void. Enter the code below on the webpage, and you will be able to make a new password.\n"
            message+= "Activation Code: "+code+"\n"
            message+= "Next time, don't forget your password, ya dingus."
            send_mail("New Password for TKE DB",message,"from",[email],fail_silently=False)
            user.set_password(code)
            user.save()
            return redirect('/newPass/'+user.username)
        return render(request, 'brothers/forgot.html',{'form':form})
    else:
        return render(request, 'brothers/forgot.html',{'form':ForgotForm()})

def newPass(request,username):
    if request.method=="POST":
        form = newPassForm(request.POST)
        user = DJuser.objects.get(username=username)
        if form.is_valid():
            if user.check_password(request.POST['code']):
                user.set_password(request.POST['newPass'])
                user.save()
                return redirect('/')
        return render(request, 'brothers/newPass.html',{'form':form,'user':username})
    else:
        return render(request, 'brothers/newPass.html',{'form':newPassForm(),'user':username})

def goHome(request):
    return redirect('/')

def message(request):
    if request.method == "POST":
        if request.POST.get("type","Cancel") == "Send":
            eadd = ""
            mess = ""
            if not request.user.is_authenticated() and not request.user.is_active:
                form = MessageEmailForm(request.POST)
                if form.is_valid():                
                    eadd = request.POST['email']
                    mess += "Sent: "+strftime("%m/%d/%y at %H:%M:%S",localtime())+"\n\""+request.POST.get('message')+"\"\nReturn Address: "+eadd
                    send_mail("TKE DB KEY REQUEST",mess,"from",['sfried8@gmail.com'],fail_silently=False)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return TemplateResponse(request,'brothers/register.html',{'messForm':form,'form':UserForm(),'errors':True})                 
            else:
                form = MessageForm(request.POST)
                if form.is_valid():
                    mess += "Message from "+request.user.first_name+" "+request.user.last_name+":\n\""+request.POST.get('message')+"\"\non page "+request.META.get('HTTP_REFERER')
                    send_mail("TKE DB ISSUE",mess,"from",['sfried8@gmail.com'],fail_silently=False)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return render(request,'brothers/home.html',{'form':form,'errors':True,'user':request.user.first_name}) 
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('/')


@login_required(login_url="brothers.views.login")
def search(request):
    if request.method == "GET":
        q = request.GET.get('q',None)
        if q:
            if q == '':
                return redirect('/search/')
            if request.GET.get("type","Search Brothers") == "Scroll":
                try:
                    if int(q) <= 0 or int(q) > len(Brother.objects.all())-1:
                        return redirect('/search/')
                    return(redirect('/brothers/'+q))
                except:
                        return redirect('/search/')
            if request.GET.get("type","Search Brothers") == "Search PC":
                try:
                    if int(q) <= 0 or int(q) > Brother.objects.get(id=len(Brother.objects.all())-1).pc:
                        return redirect('/search/')
                    return redirect('/PC/'+q)
                except:
                    return redirect('/search/')
            else:
                b1 = Brother.objects.filter(name__icontains=q)
                b2 = Brother.objects.filter(nickname__icontains=q)

            return render(request, 'brothers/search_form.html',{'b1':b1,'b2':b2})
        return render(request, 'brothers/search_form.html')
    return redirect('/search/')
@login_required(login_url="brothers.views.login")
def PC(request,pc):
    return render(request, 'brothers/PC.html',{'brothers':Brother.objects.filter(pc=pc),'pc':pc})

def getTree(scroll):
    tree = []
    curr = Brother.objects.get(scroll=scroll)
    i=0
    while curr.scroll!=0 and i<11:
        tree.append(curr)
        curr = Brother.objects.get(scroll=curr.bigS)
        i+=1
    tree.reverse()
    return tree

def findMaxGap():
    maximum = 0
    top = []
    for b in Brother.objects.all():
        if b.name != "Removed" and b.bigS!=0:
            gap = b.scroll - b.bigS
            if gap > maximum:
                maximum = gap
                top = [b]
            elif gap == maximum:
                top.append(b)
    return [top[0],maximum]
def findMostLittles():
    maximum = 0
    top = []
    for b in Brother.objects.all():
        if b.name != "Removed" and b.bigS!=0:
            numLittles = len(Brother.objects.filter(bigS=b.scroll))
            if numLittles > maximum:
                maximum = numLittles
                top = [b]
            elif numLittles == maximum:
                top.append(b)
    return [top[0],maximum]
def findLargestPC():
    maximum = 0
    top = [[-1,-1]]*Brother.objects.all().aggregate(Max('pc'))['pc__max']
    for b in Brother.objects.all():
        if b.pc >= 1:
            if top[b.pc-1] == [-1,-1]:
                top[b.pc-1] = [b.pc,1]
            else:
                top[b.pc-1][1] += 1
    return sorted(top, key=lambda pc: pc[1])[-1] 
def longestNickname():
    b = Brother.objects.all()
    b2=[]
    for temp in b:
        b2.append(temp.nickname)
    b3 = sorted(b2,key=lambda nickname: len(nickname))[-1]
    return Brother.objects.get(nickname=b3)

def longestName():
    b = Brother.objects.all()
    b2=[]
    for temp in b:
        b2.append(temp.name)
    b3 = sorted(b2,key=lambda name: len(name))[-1]
    return Brother.objects.get(name=b3)

@login_required(login_url="brothers.views.login")
def facts(request):
    biggestGap=findMaxGap()
    mostLittles=findMostLittles()
    largestPC=findLargestPC()
    return render(request, 'brothers/stats.html',{'biggestGap':biggestGap[0],'biggestGapNum':biggestGap[1],'mostLittles':mostLittles[0],'mostLittlesNum':mostLittles[1],'largestPC':largestPC[0],'largestPCNum':largestPC[1]})

            
