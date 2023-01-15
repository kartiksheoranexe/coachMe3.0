import pandas as pd

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse

from main.models import ClientOnboard, Client, Coach


@csrf_exempt
def parse_excel_file(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        username = df['Answers'][0]
        client = Client.objects.get(user__username=username)
        data = {}
        for index, row in df.iterrows():
            if index > 0:
                question = row['Questions']
                answer = row['Answers']
                data[question] = answer

        ClientOnboard.objects.create(
            coach=client.coach, client=client, client_onboard_data=data)

        return JsonResponse(data)




@csrf_exempt
def update_coach_years_of_experience(request):
    if request.method == 'POST':
        coaches = Coach.objects.all()
        for coach in coaches:
            print("Hello!")
            coach.years_of_experience += 1.0
            coach.save()
        return JsonResponse({"Status" : "Success!"})