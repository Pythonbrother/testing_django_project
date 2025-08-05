from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .forms import Epidemic_insertion_Form
from .models import Epidemic
import re,datetime
import random,json
import joblib
import os
from article_system.models import *

def home_view(request):
    if request.method=="GET":
        return render(request, 'home.html')

def epidemic_intro(request):
    if request.method == 'GET':
        all_records = Epidemic.objects.values('pk','name')
        twelve_random_num_from_epidemic_model = random.sample(list(Epidemic.objects.values_list('id',flat=True)),12)
        twelve_random_records = Epidemic.objects.filter(id__in=twelve_random_num_from_epidemic_model)
        return render(request, 'epidemic_intro_page.html', {'twelve_random_records':twelve_random_records,'all_records':all_records})
    else:
        search_value = request.POST.get('disease_search')
        record = get_object_or_404(Epidemic,name=search_value)
        return redirect('epidemic_detail',record.pk)
def epidemic_insertion_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        topic = request.POST.get('topic')
        symptoms_list = request.POST.getlist('symptoms')
        symptoms_str = remove_nothing_return_str('',symptoms_list)
        food_avoid_list = request.POST.getlist('food-avoid')
        food_avoid_str = remove_nothing_return_str('',food_avoid_list)   
        food_take_list = request.POST.getlist('food-take')
        food_take_str = remove_nothing_return_str('',food_take_list)
        lifestyle_avoid_list = request.POST.getlist('lifestyle-avoid')
        lifestyle_avoid_str = remove_nothing_return_str('',lifestyle_avoid_list)
        lifestyle_take_list = request.POST.getlist('lifestyle-take')
        lifestyle_take_str = remove_nothing_return_str('',lifestyle_take_list)
        managing_tips_list = request.POST.getlist('managing-tips')
        managing_tips_str = remove_nothing_return_str('',managing_tips_list)
        Epidemic.objects.create(name=name,topic=topic,symptoms=symptoms_str,food_avoid=food_avoid_str,food_take=food_take_str,lifestyle_avoid=lifestyle_avoid_str,lifestyle_take=lifestyle_take_str,managing_tips=managing_tips_str)
        return HttpResponse("You have sumitted new epidemic topic.")
    else:
        return render(request, 'epidemic_insertion_template.html')
def remove_nothing_return_str(a_char,a_list):
    while a_char in  a_list:
        a_list.remove('')
    food_avoid_str = '#'.join(a_list)
    return food_avoid_str

def examine_prevention_tip(request, epidemic_id):
    if request.method == 'GET':
        epidemic_record = Epidemic.objects.get(id=epidemic_id)
        food_avoid_list = [word for word in epidemic_record.food_avoid.split('#') if word]
        food_take_list = [word for word in epidemic_record.food_take.split('#') if word]
        lifestyle_avoid_list = [word for word in epidemic_record.lifestyle_avoid.split('#') if word]
        lifestyle_take_list = [word for word in epidemic_record.lifestyle_take.split('#') if word]
        compound_all_tips = food_avoid_list + food_take_list + lifestyle_avoid_list + lifestyle_take_list
        total_tips = len(compound_all_tips)
        return render(request, 'examine_prevention_tip.html', {"epidemic":epidemic_record,'total_tip':total_tips, 'food_avoid_list':food_avoid_list,'food_take_list':food_take_list,'lifestyle_avoid_list':lifestyle_avoid_list,'lifestyle_take_list':lifestyle_take_list})
    else:
        FULL_MARKS_YEARS = 50
        epidemic_record = Epidemic.objects.get(id=epidemic_id)
        food_avoid_list = [word for word in epidemic_record.food_avoid.split('#') if word]#score 1.1
        food_take_list = [word for word in epidemic_record.food_take.split('#') if word]#score 1
        lifestyle_avoid_list = [word for word in epidemic_record.lifestyle_avoid.split('#') if word]#score 1
        lifestyle_take_list = [word for word in epidemic_record.lifestyle_take.split('#') if word]#score 1.1
        
        compound_all_tips = food_avoid_list + food_take_list + lifestyle_avoid_list + lifestyle_take_list
        total_tips = len(compound_all_tips)
        
        given_total_marks = (len(food_avoid_list)*1.1)+(len(food_take_list)*1)+(len(lifestyle_avoid_list)*1)+(len(lifestyle_take_list)*1.1)
        
        checked_food_avoid_list = request.POST.getlist("food_avoid")
        food_avoid_marks = (len(checked_food_avoid_list)*(1.1))+((len(food_avoid_list)-len(checked_food_avoid_list))*(-1.1))
        checked_food_take_list = request.POST.getlist("food_take")
        food_take_marks = (len(checked_food_take_list)*(1))+((len(food_take_list)-len(checked_food_take_list))*(-1))
        checked_lifestyle_avoid_list = request.POST.getlist("lifestyle_avoid")
        lifestyle_avoid_marks = (len(checked_lifestyle_avoid_list)*(1))+((len(lifestyle_avoid_list)-len(checked_lifestyle_avoid_list))*(-1))
        checked_lifestyle_take_list = request.POST.getlist("lifestyle_take")
        lifestyle_take_marks = (len(checked_lifestyle_take_list)*(1.1))+((len(lifestyle_take_list)-len(checked_lifestyle_take_list))*(-1.1))
        total_marks_got = food_avoid_marks + food_take_marks + lifestyle_avoid_marks + lifestyle_take_marks # this result can be negative or positive,


        years_per_mark = (1/given_total_marks)*10
        total_years_got_by_mark = total_marks_got * years_per_mark # this result can be negative or positive, later reduce this in 'get_year_by_follow_score_percent'

        print(f"given_total_marks: {given_total_marks}")
        print(f"total_marks_got: {total_marks_got}")
        print(f"years_per_mark: {years_per_mark}")
        print(f"total_years_got_by_mark: {total_years_got_by_mark}")
        print("************************************")

        checked_compound_all_tips = checked_food_avoid_list + checked_food_take_list + checked_lifestyle_avoid_list + checked_lifestyle_take_list
        total_checked_tips = len(checked_compound_all_tips)

        able_follow_score_percent = round((total_checked_tips/total_tips)*100,1)
        get_year_by_follow_score_percent = round((able_follow_score_percent/100)*FULL_MARKS_YEARS,1)

        print(f"get_year_by_follow_score_percent: {get_year_by_follow_score_percent}")

        result_year = round(get_year_by_follow_score_percent + (total_years_got_by_mark),1 )
        
        all_you_followed = checked_food_avoid_list + checked_food_take_list + checked_lifestyle_avoid_list + checked_lifestyle_take_list
        all_you_dont_followed = compound_all_tips
        for tip in all_you_followed:
            all_you_dont_followed.remove(tip)

        if result_year<2:
            if get_year_by_follow_score_percent <= 0:
                get_year_by_follow_score_percent = 5
            #message_to_user = f"RED! you can't follow well, you can get disease in {get_year_by_follow_score_percent} years."
            message_to_user = f"‌အခုဖြေဆိုချက်အရ သင့်ကျန်းမာရေးအတွက် နေထိုင်မှုပုံစံ မကောင်းပါ။ ဒီလို အလေ့အကျင့်ကြောင့် ရောဂါက အခုမှစလို့ {get_year_by_follow_score_percent} နှစ် အတွင်း ဝင်လာနိုင်ပါတယ်။"
            return render(request,'prevention_result.html', {"message_to_user": message_to_user,"all_you_followed":all_you_followed,"all_you_dont_followed":all_you_dont_followed,'color':'#ff4d4d'})
        elif result_year>FULL_MARKS_YEARS:
            #message_to_user = f"GREEN! you follow well, you can get cover over {get_year_by_follow_score_percent} years."
            message_to_user = f"အခု ဖြေဆိုချက်အရ သင့်ကျန်းမာရေးအတွက် နေထိုင်မှု ပုံစံ အလွန်ကောင်း ပါတယ်။ ဒီလို အလေ့အကျင့်ကြောင့် ရောဂါက အခုမှစလို့ {get_year_by_follow_score_percent} နှစ် အတွင်း လုံးဝ ဖြစ်နိုင်ချေမရှိပါ။"
            return render(request, 'prevention_result.html',{"message_to_user": message_to_user, "all_you_followed": all_you_followed,"all_you_dont_followed": all_you_dont_followed,'color':'#80ffbf'})
        else:
            #message_to_user = f"YELLOW! Hello Success, you get cover at least {result_year} years."
            message_to_user = f"အခု ဖြေဆိုချက်အရ သင့်ကျန်းမာရေးအတွက် နေထိုင်မှု ပုံစံ သင့်တင့် ပါတယ်။ ဒီလို အလေ့အကျင့်ကြောင့် ရောဂါက အခုမှစလို့ {result_year} နှစ်ဝန်းကျင်ထိ ရောဂါ ဖြစ်နိုင်ချေမရှိပါ။"
            return render(request, 'prevention_result.html',{"message_to_user": message_to_user, "all_you_followed": all_you_followed,"all_you_dont_followed": all_you_dont_followed,'color':'#ffff99'})

def examine_managing_tip(request,epidemic_id):
    if request.method == 'GET':
        epidemic_record = Epidemic.objects.get(id=epidemic_id)
        epidemic_managing_tips = epidemic_record.managing_tips.split("#")
        total_tips = len(epidemic_managing_tips)
        return render(request, 'examine_managing_tip.html', {"epidemic":epidemic_record,"tips":epidemic_managing_tips,'total_tip':total_tips})
    else:
        epidemic_record = Epidemic.objects.get(id=epidemic_id)
        epidemic_managing_tips = epidemic_record.managing_tips.split("#")
        total_tips = len(epidemic_managing_tips)
        checked_tips = request.POST.getlist("managing_tips")
        total_checked_tips = len(request.POST.getlist("managing_tips"))

        managing_percent = round((total_checked_tips/total_tips)*100,1)

        all_you_dont_followed = epidemic_managing_tips
        for tip in checked_tips:
            all_you_dont_followed.remove(tip)
        #message_to_user = f"Hello Success, you get {managing_percent}"ရာခိုင်နှုန်းလောက် လိုက်နာနေပါတယ်။ ဆက်ကြိုးစားပါ။
        message_to_user = f"{managing_percent} ရာခိုင်နှုန်း လိုက်နာနေပါတယ်။ ဆက်ကြိုးစားပါ။"
        return render(request, 'managing_result.html',{"message_to_user": message_to_user, "all_you_followed": checked_tips,"all_you_dont_followed": all_you_dont_followed})


def epidemic_detail(request,epidemic_id):
    if request.method == 'GET':
        record = get_object_or_404(Epidemic,id=epidemic_id)
        symptoms = record.symptoms.split(",")
        return render(request, 'epidemic_detail.html', {'record':record, 'symptoms':symptoms})

def my_account(request):
    if request.method == 'GET':
        if (request.user.is_authenticated):
            my_upload_records = Article.objects.filter(creator=request.user)
            return render(request, 'my_account.html', {'my_records':my_upload_records})
        else:
            return redirect('login')


def test(request):
    if request.method == 'GET':
        my_list = [40,41]
        my_article = get_object_or_404(Article, pk = 13)
        records = Comment_to_Article.objects.filter(pk__in=my_list)
        for record in records:
            record.article = my_article
            record.save()
        return HttpResponse('HELLO')