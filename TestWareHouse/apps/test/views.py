import re
import random
import copy
import json

import redis
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import redirect
from django.http import JsonResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection

from apps.test.models import Test, TestPoint, TestSubject
from apps.operation.models import UserTest, UserFavourite
from method_base.random_method import random_str_code
from method_base.test_method import choice_method, text_method, check_method
class TestView(View):
    def get(self, request):
        subject_list=TestSubject.objects.all()
        try:
            user_value=request.COOKIES[str(request.user.id)]
        except:
            user_value=""
        else:
            user_value=request.COOKIES[str(request.user.id)]
        return render(request, "test.html",{"subject_list":subject_list, "user_value":user_value})

def ajax_load_points(request):
    if request.method == 'GET':
        subject = request.GET.get('subject', None)
        print(subject)
        if subject:
            data = list(TestPoint.objects.filter(subject=subject).values("point"))
            #print(data)
            return JsonResponse(data, safe=False)

class ExamView(View):
    def post(self, request, ):

        nums=request.POST.get('nums',"")
        subject=request.POST.get('subject',"")
        point=request.POST.get('point',"")
        range_1=request.POST.get("range_1","1")
        range_2=request.POST.get("range_2","1")
        if  not request.user.is_authenticated:
            range_1="1"
            range_2="1"

        if str.isdigit(nums) and len(subject)<=10 and len(point)<=20:
            nums=int(nums)
        else:
            subject_list=TestSubject.objects.all()
            return render(request, "test.html",{"subject_list":subject_list,"msg":"非法输入"})


        if range_1=="1" and range_2=="1":
            if subject=="":
                cursor = connection.cursor()
                cursor.execute("select count(*) from test_test where status=3")
                exam_num=cursor.fetchall()[0][0]
                cursor.execute("select id from test_test where status=3")
                exam_ware=cursor
                #print(exam_num)
            elif point=="":
                cursor = connection.cursor()
                cursor.execute("select count(*) from (select id from test_testpoint where subject_id="+subject+") as a left join (select id,subject_point_id from test_test where status=3 ) as b on a.id=b.subject_point_id where b.id is not NULL")
                exam_num=cursor.fetchall()[0][0]
                cursor.execute("select b.id from (select id from test_testpoint where subject_id="+subject+") as a left join (select id,subject_point_id from test_test where status=3 ) as b on a.id=b.subject_point_id where b.id is not NULL")
                exam_ware=cursor
            else:
                cursor = connection.cursor()
                cursor.execute("select count(*) from test_test where subject_point_id=(select id from test_testpoint where subject_id="+subject+" and point='"+point+"') and status=3")
                exam_num=cursor.fetchall()[0][0]
                cursor.execute("select id from test_test where subject_point_id=(select id from test_testpoint where subject_id="+subject+" and point='"+point+"') and status=3")
                exam_ware=cursor

        #if range_1=="1" and range_2=="2":

        #if subject=="":
        #    cursor = connection.cursor()
        #    cursor.execute("select count(*) from test_test")
        #    exam_num=cursor.fetchall()[0][0]
        #    cursor.execute("select * from test_test")

        #    exam_ware=cursor
        #    print(exam_num)




        if exam_num<nums:
            random_list=list(range(exam_num))
        else:
            random_list=sorted(random.sample(range(exam_num), nums))

        test_list=[]
        t_list=[]
        idt=0
        for k in random_list:
            while idt!=k:
                exam_ware.fetchone()
                idt+=1

            test_example=exam_ware.fetchone()
            idt+=1
            t_list.append(test_example[0])#id
            #if test_example[3]=="1" or test_example[3]=="3":
            #    test_list.append(choice_method(test_example))
            #elif test_example[3]=="4":
            #    test_list.append(text_method(test_example))
            #elif test_example[3]=="2":
            #    test_list.append(check_method(test_example))
        test_list.append(t_list)
        test_list.append(len(random_list))
        test_list.append(request.user.id)
        test_list.append(0)#为时间占位置
        print(test_list)
        r=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
        ran=random.randint(12,18)
        random_token=random_str_code(ran)
        while r.get(random_token):
            ran=random.randint(12,18)
            random_token=random_str_code(ran)
        r.set(random_token, str(test_list))
        r.expire(random_token, 3600)
        html=request.path_info+random_token+"/"
        #print(len(test_list))
        response=redirect(html)
        response.set_cookie(str(request.user.id) if request.user.id else "ppt",value=range_2,expires=66655)
        return response

class ExamPageView(View):
    def get(self, request, random_token):
        r=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
        t_list=r.get(random_token)
        if not t_list:
            return redirect("exam")
        else:
            t_list=eval(t_list)
            user_id=t_list[2]
            if user_id != request.user.id:
                return redirect('login')

            t_list=t_list[0]
            test_list=[]
            for i in t_list:
                cursor = connection.cursor()
                cursor.execute("select * from test_test where id="+str(i))
                test_example=cursor.fetchall()[0]
                if test_example[3]=="1" or test_example[3]=="3":
                    test_list.append(choice_method(test_example))
                elif test_example[3]=="4":
                    test_list.append(text_method(test_example))
                elif test_example[3]=="2":
                    test_list.append(check_method(test_example))
            #for i in test_list:
            #    print(i)
            return render(request, "exam.html", {"exam":test_list, "random_token":random_token})

    def post(self, request, random_token):
        r=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
        t_list=r.get(random_token)
        if not t_list:
            return redirect("exam")
        else:
            t_list=eval(t_list)
            time=t_list.pop()
            user_id=t_list.pop()
            num=t_list.pop()
            t_list=t_list[0]
            test_list=[]
            for i in t_list:
                cursor = connection.cursor()
                cursor.execute("select * from test_test where id="+str(i))
                test_example=cursor.fetchall()[0]
                if test_example[3]=="1" or test_example[3]=="3":
                    test_list.append(choice_method(test_example))
                elif test_example[3]=="4":
                    test_list.append(text_method(test_example))
                elif test_example[3]=="2":
                    test_list.append(check_method(test_example))

            if user_id != request.user.id:
                return redirect("exam")
            for i in range(num):
                answer=request.POST.getlist("t"+str(i),"")
                test_id=test_list[i][5]
                try:
                    usertest=UserTest.objects.get(user_id=user_id, test_id=test_id)
                except :
                    usertest=UserTest(user_id=user_id, test_id=test_id)
                else:
                    if usertest.is_active!=1:
                        usertest.is_active=1


                test_list[i].append(answer)
                test_list[i].append(1)
                if test_list[i][0]=="1" or test_list[i][0]=="3":
                    if answer!=[test_list[i][2]]:
                        test_list[i][-1]=0
                        usertest.is_false=1
                    else:
                        usertest.is_true=1
                elif test_list[i][0]=="2":
                    if answer!=test_list[i][2]:
                        test_list[i][-1]=0
                        usertest.is_false=1
                    else:
                        usertest.is_true=1
                elif test_list[i][0]=="4":
                    sign=0
                    for j in range(len(answer)):
                        print(answer[j])
                        print("\n")
                        print(test_list[i][4][j])
                        if answer[j] in test_list[i][4][j][1]:
                            continue
                        else:
                            sign+=1
                    if sign>0:
                        test_list[i][-1]=0
                        usertest.is_false=1
                    else:
                        usertest.is_true=1
                if user_id:
                    usertest.save()
            test_list.append(user_id)
            print(test_list)
            r.set("result_"+random_token, str(test_list))
            r.expire("result_"+random_token, 3600)
            r.delete(random_token)
            html=request.path_info+"result/"
            return redirect(html)

class ExamResultView(View):
    def get(self, request,random_token):
        r=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
        test_list=r.get("result_"+random_token)
        if not test_list:
            return redirect("exam")
        else:
            test_list=eval(test_list)
            user_id=test_list.pop()
            if request.user.id != user_id:
                return redirect("login")
            score=0
            test_page=[]
            for i in test_list:
                score+=i[-1]
                l=[]
                l.append(i)
                is_favourite=0
                if user_id:
                    try:
                        userfav=UserFavourite.objects.get(user=request.user, test_id=test_list[i][5])
                    except:
                        is_favourite=0
                    else:
                        is_favourite=userfav.is_favourite
                l.append(is_favourite)
                test_page.append(l)


            return render(request, "result.html", {"exam":test_page, "score":"{}/{}".format(score, len(test_list))})
        #"score":"{}/{}".format(score, len(test_list))
class TestListView(View):
    def get(self, request, *args, **kargs):
        subject=request.GET.get("subject","")
        point=request.GET.get("point","")
        difficulty=request.GET.get("difficulty","")
        id=request.GET.get("id","")
        user=request.user.id
        if id and id.isdigit():
            id=int(id)
            test_list=Test.objects.all()[:300]#000
            if subject:
                pt_list=TestPoint.objects.filter(subject=subject).values_list("point")
                pt_list=[i[0] for i in list(pt_list)]
            elif point and not subject:#010,011
                pass
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=Test.objects.filter(subject_point__in=point_list, difficulty=difficulty)[:300]
            elif difficulty and not subject and not point:#001
                test_list=Test.objects.filter(difficulty=difficulty)[:300]
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=Test.objects.filter(subject_point__in=point_list, difficulty=difficulty)[:300]
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=Test.objects.filter(subject_point__in=point_list)[:300]
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=Test.objects.filter(subject_point__in=point_list)[:300]
            test_example=test_list[id]
            m=UserTest.objects.get(user=user, test_id=test_example.id)
            k=UserFavourite.objects.get(user=user, test_id=test_example.id)
            if test_example.style=="1" or test_example.style=="3":
                test=choice_method(test_example)
            elif test_example.style=="4":
                test=text_method(test_example)
            elif test_example.style=="2":
                test=check_method(test_example)
            return render(request, 'user_test_detail.html',{"test":test, 'id':test_example.id,'is_favourite':k.is_active})       

        else:
            subject_list=TestSubject.objects.all()
            test_list=Test.objects.all()[:300]#000
            pt_list=[]
            if subject:
                pt_list=TestPoint.objects.filter(subject=subject).values_list("point")
                pt_list=[i[0] for i in list(pt_list)]
            elif point and not subject:#010,011
                pass
            if point and subject and difficulty:#111
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id")         
                test_list=Test.objects.filter(subject_point__in=point_list, difficulty=difficulty)[:300]
            elif difficulty and not subject and not point:#001
                test_list=Test.objects.filter(difficulty=difficulty)[:300]
            elif difficulty and subject and not point:#101
                point_list=TestPoint.objects.filter(subject=subject).values_list("id")
                test_list=Test.objects.filter(subject_point__in=point_list, difficulty=difficulty)[:300]
            elif subject and not difficulty and not point:#100
                point_list=TestPoint.objects.filter(subject=subject).values_list("id") 
                test_list=Test.objects.filter(subject_point__in=point_list)[:300]
            elif subject and point and not difficulty:#110
                point_list=TestPoint.objects.filter(subject=subject, point=point).values_list("id") 
                test_list=Test.objects.filter(subject_point__in=point_list)[:300]


            if subject.isdigit():
                subject=int(subject)
            try:
                page=request.GET.get('page',1)
            except PageNotAnInteger:
                page=1
            test_list=list(enumerate(test_list))
            p=Paginator(test_list, per_page=1, request=request)
            test_page=p.page(page)
            return render(request, 'test_list.html',{"subject_re":subject, "point_re":point, "difficulty_re":difficulty, "test_list":test_page, "subject_list":subject_list, "point_list":pt_list})





        












# Create your views here.