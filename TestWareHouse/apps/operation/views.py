import re
import random
import copy
import json

import redis
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.users.models import UserProfile
from apps.operation.forms import ChangePasswordForm, ChangeEmailForm
from method_base.random_method import random_str_code
from method_base.test_method import choice_method, text_method, check_method
from method_base.email_method import send_email_code, send_change_email_code
from apps.test.models import Test, TestSubject, TestPoint
from apps.operation.models import UserTest, UserFavourite, UserSubmit, TestVerify, TestObjection

class UserHomeView(LoginRequiredMixin, View):
    login_url="/testhouse/login/"
    def get(self, request):
        if request.user.is_staff=="1":
            return redirect("staffhomepage")
        return render(request, "user_home_page.html")

class ChangeUserNameView(LoginRequiredMixin, View):
    login_url="/testhouse/login/"
    def post(self, request):
        username=request.POST.get("username")
        print(username)
        if username==request.user.username:
            return JsonResponse({"res": 1})
        else:
            find_user=UserProfile.objects.filter(username=username)
            if find_user:
                return JsonResponse({"res": 2})
            else:
                request.user.username=username
                request.user.save()
                return JsonResponse({"res": 3})

class ChangePasswordView(LoginRequiredMixin, View):
    login_url="/testhouse/login/"
    def post(self, request):
        p=ChangePasswordForm(request.POST)
        if p.is_valid():
            password=p.cleaned_data["password"]
            print(password)
            if not check_password(password, request.user.password):
                return JsonResponse({"res": 1})
            new_password=p.cleaned_data["password_1"]
            user=request.user
            user.set_password(new_password)
            user.save()
            login(request, user)
            return JsonResponse({"res": 2})
        else:
            return JsonResponse({"res": 3})

class ChangeEmailView(LoginRequiredMixin, View):
    login_url="/testhouse/login/"
    def post(self, request):
        r=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
        p=ChangeEmailForm(request.POST)
        if p.is_valid():
            new_email=p.cleaned_data["email"]
            if  UserProfile.objects.filter(email=new_email) or r.get(new_email):
                return JsonResponse({"res": 1})
            else:
                r.set(new_email, "1")
                r.expire(new_email, 3601)
                ran=random.randint(12,18)
                random_token=random_str_code(ran)
                r.set(random_token, str([request.user.username, new_email]))
                r.expire(random_token, 3600)
                result=send_change_email_code(new_email,random_token)
                if not result:
                    return JsonResponse({"res": 2})
                else:
                    return JsonResponse({"res": 3})

class ChangeEmailCodeView(LoginRequiredMixin, View):
    login_url="/testhouse/login/"
    def get(self, request, email_code):
        print(email_code)
        r=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
        data_list=r.get(email_code)
        if not data_list:
            pass
        else:
            data_list=eval(data_list)
            username=data_list[0]
            email=data_list[1]
            if r.get(email):
                user=UserProfile.objects.filter(username=username)[0]
                user.email=email
                user.save()
                r.delete(email)
                r.delete(email_code)
                login(request, user)
            else:
                pass
            return HttpResponseRedirect(reverse('userhome'))

class WrongTestListView(View):
    login_url="/testhouse/login/"
    def get(self, request, *args, **kargs):
        if request.user.is_staff=="1":
            return redirect("staffhomepage")
        user=request.user.id
        subject=request.GET.get("subject","")
        point=request.GET.get("point","")
        difficulty=request.GET.get("difficulty","")
        id=request.GET.get("id","")
        istf=request.GET.get("istf","00")
        if istf.isdigit() and len(istf)==2:
            is_true=int(istf[0])
            is_false=int(istf[1])
        else:
            is_true=0
            is_false=0

        if id and id.isdigit():
            id=int(id)
            if is_true==1 and is_false!=1:
                usertest=UserTest.objects.filter(user=user, is_true=1, is_active=1).values_list("test_id")
            elif is_true==1 and is_false==1:
                usertest=UserTest.objects.filter(user=user, is_false=1, is_true=1, is_active=1).values_list("test_id")
            elif is_true!=1 and is_false==1:
                usertest=UserTest.objects.filter(user=user, is_false=1, is_active=1).values_list("test_id")
            else:
                usertest=UserTest.objects.filter(user=user, is_active=1).values_list("test_id")

            usertest_list=Test.objects.filter(id__in=usertest)
            test_list=usertest_list
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif difficulty and not subject and not point:#001
                test_list=usertest_list.filter(difficulty=difficulty)
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)

            test_example=test_list[id]
            m=UserTest.objects.get(user=user, test_id=test_example.id)
            k=UserFavourite.objects.get(user=user, test_id=test_example.id)
            if test_example.style=="1" or test_example.style=="3":
                test=choice_method(test_example)
            elif test_example.style=="4":
                test=text_method(test_example)
            elif test_example.style=="2":
                test=check_method(test_example)
            return render(request, 'user_test_detail.html',{"test":test,'is_true':m.is_true, "is_false":m.is_false, 'id':test_example.id,'is_favourite':k.is_active})

        else:
            subject_list=TestSubject.objects.all()
            if is_true==1 and is_false!=1:
                usertest=UserTest.objects.filter(user=user, is_true=1, is_active=1).values_list("test_id")
            elif is_true==1 and is_false==1:
                usertest=UserTest.objects.filter(user=user, is_false=1, is_true=1, is_active=1).values_list("test_id")
            elif is_true!=1 and is_false==1:
                usertest=UserTest.objects.filter(user=user, is_false=1, is_active=1).values_list("test_id")
            else:
                usertest=UserTest.objects.filter(user=user, is_active=1).values_list("test_id")

            usertest_list=Test.objects.filter(id__in=usertest)
            test_list=usertest_list

            pt_list=[]
            if subject:
                pt_list=TestPoint.objects.filter(subject=subject).values_list("point")
                pt_list=[i[0] for i in list(pt_list)]
            elif point and not subject:#010,011
                pass
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif difficulty and not subject and not point:#001
                test_list=usertest_list.filter(difficulty=difficulty)
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)

            result_list=[]
            idt=-1
            for i in test_list:
                idt+=1
                l=[]
                l.append(i)
                m=UserTest.objects.get(user=user, test_id=i.id)
                l.append(m.is_true)
                l.append(m.is_false)
                l.append(idt)
                result_list.append(l)

            if subject.isdigit():
                subject=int(subject)
            try:
                page=request.GET.get('page',1)
            except PageNotAnInteger:
                page=1
  
            p=Paginator(result_list, per_page=1, request=request)
            test_page=p.page(page)

            return render(request, 'wrong_test_list.html',{"subject_re":subject, "point_re":point, "difficulty_re":difficulty, "test_list":test_page, "subject_list":subject_list, "point_list":pt_list, "istf_re":istf})

class AjaxWrongTestView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def post(self,request):
        user_id=request.POST.get("user_id", "")
        test_id=request.POST.get("test_id","")
        tp=request.POST.get("type", "")
        if test_id and user_id and tp:
            if tp=="delete_test":
                m=UserTest.objects.get(user_id=user_id, test_id=test_id)
                if m:
                    if m.is_active!=0:
                        m.is_active=0
                        m.save()
                    return JsonResponse({"res": 1})
                else:
                    return JsonResponse({"res": 2})
            elif tp=="delete_wrong":
                m=UserTest.objects.get(user_id=user_id, test_id=test_id)
                if m:
                    if m.is_false!=0:
                        m.is_false=0
                        m.save()
                    return JsonResponse({"res": 1})
                else:
                    return JsonResponse({"res": 2})




class FavouriteTestListView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def get(self, request, *args, **kargs):
        if request.user.is_staff=="1":
            return redirect("staffhomepage")
        user=request.user.id
        subject=request.GET.get("subject","")
        point=request.GET.get("point","")
        difficulty=request.GET.get("difficulty","")
        id=request.GET.get("id","")


        if id and id.isdigit():
            id=int(id)
            habit=request.user.habit
            usertest=UserFavourite.objects.filter(user=user, is_active=1).values_list("test_id")

            usertest_list=Test.objects.filter(id__in=usertest)
            test_list=usertest_list
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif difficulty and not subject and not point:#001
                test_list=usertest_list.filter(difficulty=difficulty)
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)

            test_example=test_list[id]
            m=UserTest.objects.get(user=user, test_id=test_example.id)
            k=UserFavourite.objects.get(user=user, test_id=test_example.id)
            
            if test_example.style=="1" or test_example.style=="3":
                test=choice_method(test_example)
            elif test_example.style=="4":
                test=text_method(test_example)
            elif test_example.style=="2":
                test=check_method(test_example)
            return render(request, 'user_test_detail.html',{"test":test,'is_true':m.is_true, "is_false":m.is_false, 'id':test_example.id,'is_favourite':k.is_active, 'style':2, 'habit':habit})

        else:
            subject_list=TestSubject.objects.all()

            usertest=UserFavourite.objects.filter(user=user, is_active=1).values_list("test_id")

            usertest_list=Test.objects.filter(id__in=usertest)
            test_list=usertest_list

            pt_list=[]
            if subject:
                pt_list=TestPoint.objects.filter(subject=subject).values_list("point")
                pt_list=[i[0] for i in list(pt_list)]
            elif point and not subject:#010,011
                pass
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif difficulty and not subject and not point:#001
                test_list=usertest_list.filter(difficulty=difficulty)
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)

            result_list=[]
            idt=-1
            for i in test_list:
                idt+=1
                l=[]
                l.append(i)
                l.append(idt)
                result_list.append(l)

            if subject.isdigit():
                subject=int(subject)
            try:
                page=request.GET.get('page',1)
            except PageNotAnInteger:
                page=1
  
            p=Paginator(result_list, per_page=1, request=request)
            test_page=p.page(page)

            return render(request, 'favourite_test_list.html',{"subject_re":subject, "point_re":point, "difficulty_re":difficulty, "test_list":test_page, "subject_list":subject_list, "point_list":pt_list})

class AjaxFavouriteTestView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def post(self,request):
        user_id=request.POST.get("user_id", "")
        test_id=request.POST.get("test_id","")
        tp=request.POST.get("type", "")
        print(user_id,test_id,tp)
        if test_id and user_id and tp:
            if tp=="delete_favourite":
                try:
                    m=UserFavourite.objects.get(user_id=user_id, test_id=test_id)
                except:
                    return JsonResponse({"res": 1, 'id':test_id})
                else:
                    if m.is_active!=0:
                        m.is_active=0
                        m.save()
                        return JsonResponse({"res": 1, 'id':test_id})
                    else:
                        return JsonResponse({"res": 2})
            elif tp=="add_favourite":
                try:
                    m=UserFavourite.objects.get(user_id=user_id, test_id=test_id)
                except:
                    m=UserFavourite(user_id=user_id, test_id=test_id)
                    m.save()
                    return JsonResponse({"res": 1,'id':test_id})
                else:
                    if m.is_active!=1:
                        m.is_active=1
                        m.save()
                        return JsonResponse({"res": 1,'id':test_id})
                    else:
                        return JsonResponse({"res": 2})


class AjaxHabitView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def post(self,request):
        habit=request.POST.get("habit")
        if not habit.isdigit():
            return JsonResponse({'res':2})
        else:
            habit=int(habit)
            user=UserProfile.objects.get(id=request.user.id)
            print("A")
            if user.habit==habit:
                return JsonResponse({'res':1})
            else:
                user.habit=habit
                user.save()
                #login(request, user)
                return JsonResponse({'res':1})


class AjaxChangePageView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def post(self,request):
        user=request.user.id
        id=request.POST.get('id')
        test_id=request.POST.get('test_id')
        subject=request.POST.get("subject","")
        point=request.POST.get("point","")
        difficulty=request.POST.get("difficulty","")
        style=request.POST.get("style","")
        status=request.POST.get('status',"")
        pn=request.POST.get("pn","")
        ty=request.POST.get('ty',"")
        url=request.POST.get("url").split("&id=")[0]
        print(ty,ty=="3",type(ty))
        if ty=="2":
            id=int(id)
            habit=request.user.habit
            usertest=UserFavourite.objects.filter(user=user, is_active=1).values_list("test_id")

            usertest_list=Test.objects.filter(id__in=usertest)
            test_list=usertest_list
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif difficulty and not subject and not point:#001
                test_list=usertest_list.filter(difficulty=difficulty)
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)

            if pn=="previous":
                id=id-1
                if id<0:
                    id=0
                elif id>=len(test_list):
                    id=len(test_list)-1
            elif pn=="next":
                userfav=UserFavourite.objects.get(user_id=request.user.id, test_id=int(test_id))
                if userfav.is_active==0:
                    id=id
                else:
                    id=id+1
                if id<0:
                    id=0
                elif id>=len(test_list):
                    id=len(test_list)-1
            return JsonResponse({'url':url+"&id="+str(id)})
        elif ty=="3":
            id=int(id)
            habit=request.user.habit
            usertest=UserSubmit.objects.filter(user=user, is_active=1).values_list("test_id")

            usertest_list=Test.objects.filter(id__in=usertest)
            test_list=usertest_list
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif difficulty and not subject and not point:#001
                test_list=usertest_list.filter(difficulty=difficulty)
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)

            if status:
                test_list=test_list.filter(status=stauts)
            if style:
                test_list=test_list.filter(style=style)
            if pn=="previous":
                id=id-1
                if id<0:
                    id=0
                elif id>=len(test_list):
                    id=len(test_list)-1
            elif pn=="next":
                userfav=UserSubmit.objects.get(user_id=request.user.id, test_id=int(test_id))
                if userfav.is_active==0:
                    id=id
                else:
                    id=id+1
                if id<0:
                    id=0
                elif id>=len(test_list):
                    id=len(test_list)-1
            return JsonResponse({'url':url+"&id="+str(id)})
        else:
            print("K")



class UserTestSubmitView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def get(self, request):
        if request.user.is_staff=="1":
            return redirect("staffhomepage")
        subject_list=TestSubject.objects.all()
        return render(request, 'user_test_submit.html',{'subject_list':subject_list})

    def post(self, request):
        style=request.POST.get('style')
        selection=request.POST.getlist('selection')
        desc=request.POST.get('desc')
        difficulty=request.POST.get('difficulty')
        explain=request.POST.get('explain')
        answer=request.POST.getlist('select_answer')
        subject=request.POST.get('subject')
        point=request.POST.get('point')
        act=request.POST.get("act")
        try:
            subject_point=TestPoint.objects.get(subject_id=subject, point=point)
        except:
            return JsonResponse({'res':2})
        else:
            test=Test(subject_point_id=subject_point.id, difficulty=difficulty, style=style, desc=desc, explain=explain)
            test.save()
            data={}
            data['select_nums']=len(selection)
            l=["a","b","c","d","e","f","g","h"]
            for i in range(len(selection)):
                data['select_'+l[i]]=selection[i]
            if style=="1":
                data["answer"]=answer[0]
            else:
                pass
            if act=="1":              
                Test.objects.filter(id=test.id).update(**data)
                usersubmit=UserSubmit(user=request.user, test=test)
                usersubmit.save()
                staff=UserProfile.objects.filter(is_staff=1)
                idt=random.sample(range(0,len(staff)),1)
                staff_user=staff[idt[0]]
                testverify=TestVerify(user_id=staff_user.id, test=test)
                testverify.save()

            elif act=="0": 
                data['status']="4"
                Test.objects.filter(id=test.id).update(**data)
                usersubmit=UserSubmit(user=request.user, test=test)
                usersubmit.save()


            return JsonResponse({'res':1})



class AjaxChangeSubjectView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def post(self,request):
        subject=request.POST.get("subject")
        point_list=list(TestPoint.objects.filter(subject=subject).values('point'))
        print(point_list)
        return JsonResponse({"res":1, 'list':point_list})
        
class SubmitTestListView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def get(self, request, *args, **kargs):
        if request.user.is_staff=="1":
            return redirect("staffhomepage")
        user=request.user.id
        subject=request.GET.get("subject","")
        point=request.GET.get("point","")
        difficulty=request.GET.get("difficulty","")
        status=request.GET.get("status","")
        style=request.GET.get("style","")
        id=request.GET.get("id","")

        if id and id.isdigit():
            id=int(id)
            habit=request.user.habit
            usertest=UserSubmit.objects.filter(user=user, is_active=1).values_list("test_id")

            usertest_list=Test.objects.filter(id__in=usertest)
            test_list=usertest_list
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif difficulty and not subject and not point:#001
                test_list=usertest_list.filter(difficulty=difficulty)
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)

            if status:
                test_list=test_list.filter(status=stauts)
            if style:
                test_list=test_list.filter(style=style)

            test_example=test_list[id]

            
            if test_example.style=="1" or test_example.style=="3":
                test=choice_method(test_example)
            elif test_example.style=="4":
                test=text_method(test_example)
            elif test_example.style=="2":
                test=check_method(test_example)
            return render(request, 'user_test_detail.html',{"test":test,'id':test_example.id, 'style':3, 'habit':habit})
        else:
            subject_list=TestSubject.objects.all()

            usertest=UserSubmit.objects.filter(user=user, is_active=1).values_list("test_id")

            usertest_list=Test.objects.filter(id__in=usertest)
            test_list=usertest_list

            pt_list=[]
            if subject:
                pt_list=TestPoint.objects.filter(subject=subject).values_list("point")
                pt_list=[i[0] for i in list(pt_list)]
            elif point and not subject:#010,011
                pass
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif difficulty and not subject and not point:#001
                test_list=usertest_list.filter(difficulty=difficulty)
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=usertest_list.filter(subject_point__in=point_list, difficulty=difficulty)
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=usertest_list.filter(subject_point__in=point_list)

            if status:
                test_list=test_list.filter(status=stauts)
            if style:
                test_list=test_list.filter(style=style)
            result_list=[]
            idt=-1
            for i in test_list:
                idt+=1
                l=[]
                l.append(i)
                l.append(idt)
                result_list.append(l)

            if subject.isdigit():
                subject=int(subject)
            try:
                page=request.GET.get('page',1)
            except PageNotAnInteger:
                page=1
  
            p=Paginator(result_list, per_page=1, request=request)
            test_page=p.page(page)

            return render(request, 'submit_test_list.html',{"subject_re":subject, "point_re":point, "difficulty_re":difficulty, "test_list":test_page, "subject_list":subject_list, "point_list":pt_list, 'status_re':status, 'style_re':style})


class AjaxSubmitTestView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"
    def post(self,request):
        user_id=request.POST.get("user_id", "")
        test_id=request.POST.get("test_id","")

        m=UserSubmit.objects.get(user_id=user_id, test_id=test_id)
        if m:
            if m.is_active!=0:
                m.is_active=0
                m.save()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 2})


class StaffVerifyView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff!=1:
            return redirect("userhome")
        user_verify=TestVerify.objects.filter(user=request.user, is_verify=0).values_list("test_id")
        test_list=Test.objects.filter(id__in=user_verify, status=1)

        try:
            page=request.GET.get('page',1)
        except PageNotAnInteger:
            page=1
  
        p=Paginator(test_list, per_page=2, request=request)
        test_page=p.page(page)

        return render(request, "staff_home_page.html", {"test_list":test_page})


class StaffTestDetailView(LoginRequiredMixin,View):
    login_url="/testhouse/login/"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff!=1:
            return redirect("userhome")
        test_id=request.GET.get("id")
        test=Test.objects.get(id=test_id)
        subject=test.subject_point.subject_id
        point=test.subject_point.point
        subject_list=TestSubject.objects.all()
        point_list=TestPoint.objects.filter(subject_id=subject)
        if test.status=="1":
            return render(request, "staff_test_detail.html", {'test':test, "subject_re":subject, "point_re": point, "subject_list":subject_list, "point_list":point_list})
        if test.status=="2":
            objection_list=TestObjection.objects.filter(test_id=test_id)
            return render(request, "staff_test_detail.html", {'test':test, "subject_re":subject, "point_re": point, "subject_list":subject_list, "point_list":point_list ,"objection_list":objection_list})
class AjaxVerifyDelete(View):

    def post(self, request, *args, **kwargs):
        test_id=request.POST.get("test_id")
        try:
            test=Test.objects.get(id=test_id)
        except:
            return JsonResponse({"res":2})
        else:
            test.status=4
            test.save()
            verify=TestVerify.objects.get(user=request.user, test_id=test_id)
            verify.is_verify=1
            verify.save()
            return JsonResponse({"res":1})


class AjaxVerifyUse(LoginRequiredMixin,View):
    login_url="/testhouse/login/"

    def post(self, request):
        selection=request.POST.getlist('selection')
        desc=request.POST.get('desc')
        difficulty=request.POST.get('difficulty')
        explain=request.POST.get('explain')
        answer=request.POST.getlist('select_answer')
        subject=request.POST.get('subject')
        point=request.POST.get('point')
        test_id=request.POST.get("test_id")
        try:
            subject_point=TestPoint.objects.get(subject_id=subject, point=point)
        except:
            return JsonResponse({'res':2})
        else:
            test=Test.objects.get(id=test_id)
            test.subject_point_id=subject_point.id
            test.difficulty=difficulty
            test.explain=explain
            test.desc=desc
            test.save()
            data={}
            data['select_nums']=len(selection)
            l=["a","b","c","d","e","f","g","h"]
            for i in range(len(selection)):
                data['select_'+l[i]]=selection[i]
            if style=="1":
                data["answer"]=answer[0]
            else:
                pass
            
            Test.objects.filter(id=test_id).update(**data)
            test=Test.objects.get(id=test_id)
            if test.status=="2":
                test.threshold=test.threshold*2
                test.objection_nums=0
            test.status=3

            test.save()
            verify=TestVerify.objects.get(user=request.user, test_id=test_id)
            verify.is_verify=1
            verify.save()
            return JsonResponse({'res':1})

class AjaxObjection(LoginRequiredMixin,View):
    login_url="/testhouse/login/"

    def post(self, request):
        test_id=request.POST.get("test_id")
        content=request.POST.get("content")
        try:
            objection=TestObjection.objects.get(uesr=request.user, test_id=test_id)
        except:
            objection=TestObjection(user=request.user, test_id=test_id, content=content)
        else:
            objection.content=content
        objection.save()
        test=Test.objects.get(id=test_id)
        test.objection_nums+=1
        if test.objection_nums>=test.threshold:
            test.status="2"
            test.save()
            try:
                testverify=TestVerify.objects.get(test_id=test_id)
            except:

                staff=UserProfile.objects.filter(is_staff=1)
                idt=random.sample(range(0,len(staff)),1)
                staff_user=staff[idt[0]]
                testverify=TestVerify(user=staff_user, test_id=test_id)

            else:
                testverify.is_verify=0
            testverify.save()
            return JsonResponse({"res":1})







