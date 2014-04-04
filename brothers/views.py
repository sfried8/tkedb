from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse
from brothers.models import Brother

def home(request):
    return render(request, 'brothers/home.html',{'maxGap':findMaxGap(),'mostLittles':findMostLittles()})
def index(request):
    return redirect('/')
def detail(request, scroll):
    b = Brother.objects.get(scroll=scroll)
    vis='Show'
    if request.method == "GET" and request.GET.get('tree','temp') == "Show Family Tree":
        vis = 'Hide'
    return render(request, 'brothers/index.html',{'brother':b,'littles':Brother.objects.filter(bigS=b.scroll),'vis':vis,'tree':getTree(b.scroll)})
def scroll(request):
    return render(request, 'brothers/scroll.html',{'brothers':Brother.objects.all()})
def search(request):
    if request.method == "GET":
        q = request.GET.get('q',None)
        if q:
            if q == '':
                return redirect('/search/')
            if request.GET.get("type","Search Brothers") == "Search PC":
            	if int(q) <= 0 or int(q) > Brother.objects.get(id=len(Brother.objects.all())-1).pc:
            		return redirect('/search/')
            	return redirect('/PC/'+q)
            else:
	            if q.isdigit():
	                if int(q) <= 0 or int(q) > len(Brother.objects.all())-1:
	                    return redirect('/search/')
	                return(redirect('/brothers/'+q))
	            b1 = Brother.objects.filter(name__icontains=q)
	            b2 = Brother.objects.filter(nickname__icontains=q)

            return render(request, 'brothers/search_form.html',{'b1':b1,'b2':b2})
        return render(request, 'brothers/search_form.html')
    return redirect('/search/')
def PC(request,pc):
    return render(request, 'brothers/PC.html',{'brothers':Brother.objects.filter(pc=pc),'pc':pc})
def getTree(scroll):
    tree = []
    curr = Brother.objects.get(scroll=scroll)
    while curr.scroll!=0:
        tree.append(curr)
        curr = Brother.objects.get(scroll=curr.bigS)
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
	return top
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
	return top
def largestPC():
	maximum = 0
	top = []
	for b in Brother.objects.all():
		if b.pc >= 1:
			pass
			