from django.shortcuts import render,redirect
import json
from django .http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from collections import defaultdict as dd 

def makematrix(subs, tot_sub):
    # print()
    # print()
    # print(subs)
    # print()
    mat=[[0 for i in range(tot_sub)]for i in range(tot_sub)]
    for sub in subs:
        # print(sub)

        l=len(sub)        
        for i in range(l):
            for j in range(i+1,l):
                # print(sub[i]['id'])
                a,b = sub[i]['id']-1 , sub[j]['id']-1
                mat[a][b], mat[b][a] = 1,1

    for m in mat:
        print(*m) 
    return mat




def timetable(mat):
    l = len(mat)
    ans = [0 for i in range(l)]
    k=0
    color = 1
    while k>=0 :
        for i in range(l):
            print(k,i,mat[k][i])
            if mat[k][i]==1:
                if ans[i]==color:
                    print("---------------------------")
                    color+=1
                    continue

        ans[k]=color
        print(ans)
        color=1
        k+=1
        if k==l:
            break;

    print(ans)
    return ans


# Create your views here.
def start(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    not_admin=False
    all_subjects = Subject.objects.values()
    reg_subjects = []
    uid = 'admin123'
    if request.user.username!='admin':
        not_admin=True
        mapping = Mapping.objects.get(user=request.user)
        reg_subjects = mapping.sub.values()
        print(mapping, reg_subjects)
        uid = mapping
    regno = len(reg_subjects)

    aval_subjects=[]
    for sub in all_subjects:
        if sub not in reg_subjects:
            aval_subjects.append(sub)
    # print(reg_subjects[1]['name'])
    print(all_subjects[6]['name'])
    prms = {'regno':regno,'uid':uid, 'all_sub':aval_subjects,'reg_sub':reg_subjects,'is_admin':not not_admin}
    return render(request, 'start.html', prms)


def generate(request):
    if not request.user.is_authenticated :
        return redirect('/login/')
    if request.user.username != 'admin':
        return redirect('/')
    mappings = Mapping.objects.all()
    subjects = Subject.objects.values()
    print(subjects)

    limit = subjects.count()
    if request.method=="POST":
        limit=request.POST.get('limit')
    
    tot_sub = subjects.count()
    subs=[]
    for mapping in mappings:
        print(mapping.uid, mapping.user, mapping.sub.all())
        subs.append(list(mapping.sub.values()))
        # print(mapping.uid,mapping.user,mapping.sub)
    print(subs)
    mat = makematrix(subs, tot_sub)

    ans = timetable(mat)
    # print()
    # print(len(set(ans)))
    # print()

    res=[[] for i in range(len(set(ans)))]
    # print(res)

    for subject in subjects:
        i=subject['id']-1
        # print(i,subject)
        res[ans[i]-1].append(subject['name'])
        # print(res)
    print(res)

    return render(request, 'table.html',{'res':res})


def register(request,sid):
    sub = Subject.objects.get(id=sid)
    user = request.user
    mapping = Mapping.objects.get(user=user)
    mapping.sub.add(sub)
    return redirect('/')


def unregister(request,sid):
    sub = Subject.objects.get(id=sid)
    user = request.user
    mapping = Mapping.objects.get(user=user)
    mapping.sub.remove(sub)
    return redirect('/')


def signin(request):
	if request.method=="POST":
		username=request.POST.get('user')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('/')
		else:
			messages.error(request,"Wrong credentials,Please try again !")
			return redirect('/login/')

	if request.method == 'GET':
		return render(request, "login.html")


def signout(request):
	logout(request)
	messages.success(request,'Successfully logged out')
	return redirect('/login/')
