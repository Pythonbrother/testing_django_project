import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.db.models import Count
import joblib
import json
# Create your views here.
def diagnosis(request):
    #symptoms_list = ['body ache', 'nausea', 'scaly patches', 'nosebleed', 'chills', 'yellow skin', 'headache', 'back pain', 'swelling in ankles or feet or hands or face (edema)', 'painful defecation', 'cold feets', 'muscle cramps', 'abdominal discomfort', 'joint pain', 'burning stomach pain', 'frequent infections', 'weight loss', 'thickened skin', 'facial masking', 'slow digestion', 'knees pain', 'loss smell', 'avoidance of interaction', 'abdominal swelling', 'dark urine', 'hair thinning', 'pale stool', 'sadness', 'excessive sweating', 'rapid breathing', 'white or red patches in the mouth', 'low mood', 'bleeding gum', 'neck stiffness', 'excessive salivation', 'painful swallowing', 'pain near navel', 'weakness', 'sweatingnausea', 'skin pain', 'constipation', 'dizziness', 'repeating questions', 'arm numbness', 'rash', 'lower right abdominal pain', 'forgetting recent events', 'dry cough', 'muscle stiffness', 'vision loss', 'itchy throat', 'slurry speech', 'sensitivity to heat', 'tingling in feet', 'persistent cough', 'urination less than normal', 'cough', 'difficulty urinating', 'lower abdominal pain', 'loss appetite', 'overthinking', 'easy bruising', 'bluish fingernails', 'loss height', 'tingling in hands', 'visual problems', 'slow healing wounds', 'cold hands', 'difficulty swallowing', 'jaw muscle spasms', 'anal pain', 'ankles pain', 'frequent urination', 'mood and personality changes', 'shortness breath', 'excessive thirst', 'jaw muscle stiffness', 'nervousness', 'difficulty chewing', 'cough with mucus', 'cloudy urine', 'mouth pain', 'red patches', 'painful chewing', 'arm pain', 'one sided headache', 'small cramped handwriting', 'decreased range of motion', 'bad breath', 'increased hunger', 'muscle pain', 'sensitivity to light', 'pain in left arm', 'muscle tension', 'itching', 'vomiting', 'hallucinations', 'cough at night', 'excess gas', 'balance problems', 'wheezing', 'right upper abdominal pain', 'misplacing things', 'blurry vision', 'fast heartbeat', 'pulsing headache', 'black stool', 'watery eyes', 'bluish lips', 'blood in urine', 'sneezing', 'sensitivity to cold', 'swollen joints', 'snoring', 'stooped posture', 'fever', 'chest tightness', 'inability to retrace steps', 'excess body fat', 'night sweats', 'easily broken bones', 'stiffness muscle', 'itchy eyes', 'eye pain', 'anal itching', 'sensitivity to sound', 'depression', 'joint stiffness', 'mucus in poop', 'cough with blood', 'difficulty walking', 'swollen ankles', 'abdominal pain', 'persistent cough with mucus', 'sweating', 'red eyes', 'excessive worry or fear or doubt', 'redness or warmth around joints', 'paralysis', 'facial droop', 'lumps near the anus', 'urgency', 'pale skin', 'neck swelling', 'ffrequent infections', 'muscle weakness', 'thickened nails', 'dehydration (dry mouth or dark urine)', 'bloating', 'painful urination', 'hoarseness', 'sleepy', 'coordination problems', 'mouth ulcer', 'concentration problems', 'panic attacks', 'sleep apnea', 'pale lips', 'side pain below ribs', 'weight gain', 'vomiting blood', 'runny nose', 'poor judgment', 'tingling at bite site', 'chest pain', 'swollen lymph nodes', 'aura', 'indigestion', 'confusion with time or place', 'bone pain', 'swelling near the anus', 'itchy nose', 'tremors', 'aggression', 'sore throat', 'numbness in hands', 'tongue pain', 'increased appetite', 'swelling in joints', 'dry skin', 'heartburn', 'shuffling walk', 'weakness on one side', 'slow movement', 'tight feeling in the throat', 'loss interest', 'excessive blushing', 'sleep issues', 'creaking sounds', 'numbness of the tongue', 'clammy hands', 'blisters', 'confusion', 'numbness on right side', 'shaking hands', 'slow heart rate', 'shortness breath while activity', 'abdominal tenderness', 'muscle spasms', 'sores in mouth and sores in genitals', 'hydrophobia (fear of water)', 'nasal congestion', 'enlarged liver (feel like a lump under the ribs)', 'difficulty completing familiar tasks', 'bulging eyes', 'jaw pain', 'pelvic pain', 'fatigue', 'irritability', 'frequent respiratory infections', 'diarrhea', 'numbness in legs', 'back pain below ribs', 'red bleeding during bowel movement', 'memory loss']
    symptoms_list =['လက်ဖဝါးချွေးစေးထွက်ခြင်း', 'မျက်နှာအကြောရွဲ့ခြင်း', 'သွားရည်ကျခြင်း', 'ဝမ်းသွားသွေးပါခြင်း', 'လက်သည်းပြာခြင်း', 'ခြေထောက်၊ လက်၊ မျက်နှာဖောင်းခြင်း', 'ဝမ်းတွင်ချွဲပါခြင်း', 'ခြေကျင်းဝတ်ဖောင်းခြင်း', 'ရင်ဘတ်တင်းခြင်း', 'ဝမ်းချုပ်ခြင်း', 'စိတ်နေစိတ်ထားပြောင်းခြင်း', 'ခြေဆွဲလမ်းလျှောက်ခြင်း', 'လှုပ်ရှားမှုနည်းခြင်း','လည်ချောင်းနာခြင်း', 'စအိုဘေးအလုံးထွက်ခြင်း', 'လျှာနာခြင်း', 'လည်ချောင်းယားခြင်း', 'ချောင်းခြောက်ဆိုးခြင်း', 'အန်ဖတ်တွင်သွေးပါခြင်း', 'လက်သည်းထူခြင်း', 'ပါးစပ်အနာဖြစ်ခြင်း', 'ဆီးနည်းခြင်း', 'လုပ်ခဲ့သည်များပြန်မမှတ်မိခြင်း','ကိုယ်လက်ကိုက်ခဲခြင်း', 'လေပွခြင်း', 'အဆစ်တောင့်ခြင်း', 'ကိုက်သည့်နေရာတွင် စပ်ဖျဉ်းဖျဉ်းဖြစ်ခြင်း', 'မျက်လုံးနာခြင်း', 'ပါးစပ်နာခြင်း', 'မျက်ရည်ကျခြင်း', 'အနံ့မရခြင်း', 'ရေကြောက်ခြင်း', 'လည်ချောင်းတင်းခြင်း', 'ခြေဖျားထုံကျဉ်ခြင်း', 'လည်ပင်းဖောင်းခြင်း', 'လက်တုန်ခြင်း', 'နှလုံးခုန်မြန်ခြင်း', 'အရိုးနာခြင်း', 'စအိုယားခြင်း', 'မေးရိုးတောင့်ခြင်း', 'နှုတ်ခမ်းပြာခြင်း', 'ဆီးသွားရနာခြင်း', 'နှာခေါင်းယားခြင်း', 'ပြန်ရည်ကျိတ်ကြီးခြင်း', 'အအေးမခံနိုင်ခြင်း', 'အဆစ်ဖောင်းခြင်း', 'အချိန်နေရာမမှတ်မိခြင်း', 'ဟန်ချက်မထိန်းနိုင်ခြင်း', 'အသားဝါခြင်း', 'အားနည်းခြင်း', 'ဝမ်းဗိုက်ဖောင်းခြင်း', 'အစားစားချင်စိတ်နည်းခြင်း', 'ညာဘက်ခန္ဓာကိုယ်ထုံခြင်း', 'မကြာသောအဖြစ်အပျက်များမေ့ခြင်း', 'အသက်ရှူရင်တရွှီရွှီမြည်ခြင်း', 'ဆီးသွားရခက်ခြင်း', 'ခြေကျင်းဝတ်နာခြင်း', 'နှာချေခြင်း', 'ဒူးနာခြင်း', 'အိပ်နေစဉ်အသက်ရှူရပ်ခြင်း', 'မောပန်းနွမ်းနယ်ခြင်း', 'အရပ်ပုခြင်း', 'ဆုံးဖြတ်ချက်မှားခြင်း', 'ကြွက်သားနာခြင်း', 'လူမှုဆက်ဆံရေးရှောင်ရှားခြင်း', 'လက်ထုံခြင်း', 'သွက်ချာပါဒဖြစ်ခြင်း', 'အသားခြောက်ခြင်း', 'ဆီးထဲသွေးပါခြင်း', 'ခေါင်းမူးခြင်း', 'ယားယံခြင်း', 'ပျို့အန်ချင်ခြင်း', 'ဝမ်းဖြူခြင်း', 'ခေါင်းကိုက်မတိုင်မီမြင်ရသောအလင်း (အော်ရာ)', 'အစာအိမ်ပူခြင်း', 'အသံမခံနိုင်ခြင်း', 'အနီကွက်များထွက်ခြင်း', 'ညဘက်ချောင်းဆိုးခြင်း', 'ဆီးနှစ်ခြင်း', 'သွေးခြည်ဥလွယ်ခြင်း', 'ခေါင်းကိုက်ခြင်း', 'စိတ်ရှုပ်ခြင်း', 'ခြေထုံခြင်း', 'စိတ်ဝင်စားမှုနည်းခြင်း', 'ကြွက်သားတုန်ခြင်း', 'အရိုးကျိုးလွယ်ခြင်း', 'ခေါင်းတစ်ခြမ်းကိုက်ခြင်း', 'ကိုယ်အလေးချိန်တက်ခြင်း', 'စကားပြောမပီခြင်း', 'ရေအလွန်ဆာခြင်း', 'နှုတ်ခမ်းဖြူခြင်း', 'မေးခွန်းများထပ်ခါထပ်ခါမေးခြင်း', 'လှုပ်ရှားနှေးခြင်း', 'အစာမကြေခြင်း', 'မျက်စိဝါးခြင်း', 'ညာဘက်အပေါ်ဗိုက်နာခြင်း', 'လည်ပင်းတောင့်ခြင်း', 'ဝမ်းဗိုက်နာခြင်း', 'ပါးစပ်နှင့်လိင်အင်္ဂါအနာဖြစ်ခြင်း', 'အောက်ပိုင်းဗိုက်နာခြင်း', 'ချောင်းဆိုးခြင်း', 'အသက်ရှူလမ်းကြောင်းပိုးဝင်လွယ်ခြင်း', 'အိပ်မပျော်ခြင်း', 'အရေပြားနာခြင်း', 'နှာရည်ယိုခြင်း', 'အရည်ကြည်ဖုများထွက်ခြင်း', 'နံရိုးအောက်ဘေးနာခြင်း', 'မေးရိုးကြောတက်ခြင်း', 'ခန္ဓာကိုယ်တစ်ခြမ်းအားနည်းခြင်း', 'လက်မောင်းနာခြင်း', 'ခံတွင်းနံ့ဆိုးခြင်း', 'ရေဓာတ်ခန်းခြောက်ခြင်း', 'ရန်လိုခြင်း', 'ချမ်းစိမ့်စိမ့်ဖြစ်ခြင်း', 'ညာဘက်အောက်ပိုင်းဗိုက်နာခြင်း', 'စိတ်ဓာတ်ကျခြင်း', 'ဟောက်ခြင်း', 'နှလုံးခုန်နှေးခြင်း', 'ချွေးထွက်ခြင်း', 'မျိုချရခက်ခြင်း', 'တုန်ခြင်း', 'အဆစ်များအသံထွက်ခြင်း', 'သွားဖုံးသွေးယိုခြင်း', 'အလင်းမခံနိုင်ခြင်း', 'မျက်လုံးဖောင်းခြင်း', 'နံရိုးအောက်ဘက်နာခြင်း', 'စိတ်လှုပ်ရှားခြင်း', 'ကိုယ်နေဟန်ထားကုန်းခြင်း', 'ကြွက်သားအားနည်းခြင်း', 'ကြွက်သားတောင့်ခြင်း', 'အသက်ရှူမဝခြင်း', 'ပါးစပ်တွင်အဖြူကွက်/အနီကွက်များဖြစ်ခြင်း', 'နှာခေါင်းပိတ်ခြင်း', 'ထိတ်လန့်ခြင်း', 'ကိုယ်အလေးချိန်ကျခြင်း', 'အစားစားချင်စိတ်များခြင်း', 'အနီကွက်ထွက်ခြင်း', 'ဝါးရနာခြင်း', 'အသံဝင်ခြင်း', 'ဝမ်းသွားရခက်ခြင်း', 'ဘယ်ဘက်လက်နာခြင်း', 'ရင်ပူခြင်း', 'မျက်စိမမြင်ခြင်း', 'သလိပ်ပါချောင်းဆိုးမပျောက်ခြင်း', 'အိပ်ငိုက်ခြင်း', 'အပူမခံနိုင်ခြင်း', 'တင်ပဆုံနာခြင်း', 'ကျောနာခြင်း', 'စိတ်တိုလွယ်ခြင်း', 'အသည်းကြီးခြင်း', 'ခေါင်းတဒုတ်ဒုတ်ကိုက်ခြင်း', 'အဆစ်နီပူခြင်း', 'ဆံပင်ပါးခြင်း', 'အဆစ်နာခြင်း', 'ဒဏ်ရာကျက်နှေးခြင်း', 'ကိုယ်အလေးချိန်များခြင်း', 'လျှာထုံခြင်း', 'ဆီးအိမ်အလွန်အားသွားခြင်း', 'မျက်လုံးနီခြင်း', 'လမ်းလျှောက်ရခက်ခြင်း', 'ချောင်းဆိုးသွေးပါခြင်း', 'အရေပြားအဖြူအဖတ်လန်ခြင်း', 'ချက်နားနာခြင်း', 'ညဘက်ချွေးထွက်ခြင်း', 'လက်မောင်းထုံခြင်း', 'ဗိုက်ကိုဖိပြီးလက်ကိုဖယ်လိုက်ရင်နာခြင်း', 'စိတ်ထင်ယောင်ထင်မှားဖြစ်ခြင်း', 'ဖျားခြင်း', 'မျက်နှာနီမြန်းခြင်း', 'ဝမ်းဗိုက်ပူခြင်း', 'ဝါးရခက်ခြင်း', 'ဆီးအရောင်ရင့်ခြင်း', 'အကျွမ်းတဝင်အလုပ်များလုပ်ရခက်ခြင်း', 'လှုပ်ရှားရင်အသက်ရှူမဝခြင်း', 'စအိုနာခြင်း', 'အလွန်အမင်းစဉ်းစားခြင်း', 'ခြေထောက်အေးခြင်း', 'ညှိနှိုင်းလှုပ်ရှားမှုပြဿနာများ', 'လက်ဖျားထုံကျဉ်ခြင်း', 'စအိုဘေးဖောင်းခြင်း', 'ရင်ဘတ်အောင့်ခြင်း', 'ချောင်းဆိုးမပျောက်ခြင်း', 'မျက်စိမှုန်ခြင်း', 'စူးစိုက်မရခြင်း', 'မှတ်ဉာဏ်ချို့ယွင်းခြင်း', 'အရေပြားထူခြင်း', 'အစာကြေနှေးခြင်း', 'ကြွက်တက်ခြင်း', 'ဝမ်းလျှောခြင်း', 'ဗိုက်ဆာလွယ်ခြင်း', 'ကြွက်သားတင်းခြင်း', 'ဝမ်းအမည်းရောင်သွားခြင်း', 'မျက်လုံးယားခြင်း', 'မျက်နှာအမူအရာပျောက်ခြင်း', 'ဝမ်းနည်းခြင်း', 'ပစ္စည်းများမကြာခဏပျောက်ခြင်း', 'အသားဖြူဖျော့ခြင်း', 'မေးရိုးနာခြင်း', 'လက်အေးခြင်း', 'ဆီးခဏခဏသွားခြင်း', 'မျိုချရနာခြင်း', 'လက်ရေးသေးကျဉ်းခြင်း', 'ချွေးအလွန်ထွက်ခြင်း', 'သလိပ်ပါချောင်းဆိုးခြင်း', 'အသက်ရှူမြန်ခြင်း', 'နှာခေါင်းသွေးယိုခြင်း', 'ဝမ်းဗိုက်မအီမသာဖြစ်ခြင်း', 'စိုးရိမ်ပူပန်မှုလွန်ကဲခြင်း', 'အန်ခြင်း', 'ကူးစက်ရောဂါမကြာခဏဖြစ်ခြင်း']
    get_symptoms = []
    diagnosis_model_lr = joblib.load(r"myanmar_model_lr50.pkl")
    labelencoder_lr = joblib.load(r"myanmar_labelencoder_lr50.pkl")

    diagnosis_model_rf = joblib.load(r"myanmar_model_rf50.pkl")
    labelencoder_rf = joblib.load(r"myanmar_labelencoder_rf50.pkl")
    if request.method == 'POST':
        if request.POST.get('symptoms_comp'):
            symptoms = request.POST.get('symptoms_comp')
            for symptom in symptoms_list:
                if symptoms in symptom:
                    get_symptoms.append(symptom)
        elif request.POST.get('symptoms'):
            symptoms = request.POST.get('symptoms')
        #print(symptoms)
        #print("########################")
        result1 = str(labelencoder_lr.inverse_transform(diagnosis_model_lr.predict([symptoms]))[0])
        #print(result1)
        #print("########################$")
        doctor1_result = get_object_or_404(Diseases_For_Ai, disease_name=result1)

        result2 = str(labelencoder_rf.inverse_transform(diagnosis_model_rf.predict([symptoms]))[0])
        doctor2_result = get_object_or_404(Diseases_For_Ai, disease_name=result2)

        all_results = {
                       'result1':result1,
                       'topic1':doctor1_result.topic,
                        'result2': result2,
                        'topic2': doctor2_result.topic,
        }

        response_symptoms=symptoms
        return JsonResponse({'all_results':all_results,'response_symptoms':response_symptoms,'get_symptoms':get_symptoms})
        #tem_result = get_object_or_404(Diseases_For_Ai,pk=5).topic
        #return JsonResponse({'result':tem_result,'response_symptoms':response_symptoms,'get_symptoms':get_symptoms})

    else:
        return render(request, 'diagnosis.html', {'symptoms_list':symptoms_list})
    return render(request, 'diagnosis.html')

def show_report(request):
    if request.method == 'GET':
        year = datetime.datetime.now().year
        all_report_records = User_Disease_report.objects.filter(created_time__year=year).values('disease__disease_name').annotate(count=Count('disease')).order_by('-count')
        years = User_Disease_report.objects.values_list('created_time__year',flat=True)
        years = set(years)
        x_axis = []
        y_axis = []

        for record in all_report_records:
            x_axis.append(record['disease__disease_name'])
            y_axis.append(record['count'])

        data_pie = {'diseases':x_axis[:5],'total_case':y_axis[:5]}
        data_bar = {'diseases':x_axis,'total_case':y_axis}
        return render(request, 'report.html', {'records': all_report_records,'data_pie':json.dumps(data_pie),'data_bar':json.dumps(data_bar),'years':years,'year':year})
    else:
        year = request.POST.get('year')
        all_report_records = User_Disease_report.objects.filter(created_time__year=year).values(
            'disease__disease_name').annotate(count=Count('disease')).order_by('-count')
        years = User_Disease_report.objects.values_list('created_time__year', flat=True)
        years = set(years)
        x_axis = []
        y_axis = []

        for record in all_report_records:
            x_axis.append(record['disease__disease_name'])
            y_axis.append(record['count'])

        data_pie = {'diseases': x_axis[:5], 'total_case': y_axis[:5]}
        data_bar = {'diseases': x_axis, 'total_case': y_axis}
        return render(request, 'report.html', {'records': all_report_records, 'data_pie': json.dumps(data_pie),
                                               'data_bar': json.dumps(data_bar), 'years': years,'year':year})

def be_report(request):
    if request.method == 'POST':
        disease = request.POST.get('approve_result')
        disease =  get_object_or_404(Diseases_For_Ai, disease_name=disease)
        User_Disease_report.objects.create(user=request.user,disease=disease)
        return redirect('show_report')