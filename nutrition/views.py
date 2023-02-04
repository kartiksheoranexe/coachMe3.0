import requests, json
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from django.middleware.csrf import get_token

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from nutrition.models import FoodItem, FoodIntake
from nutrition.serializers import FoodIntakeSerializer
from nutrition.scripts import fetch_food_info, auto_complete, nutrition_info

# Create your views here.
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

class FoodInfoView(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        food_name = data.get("food_name")
        food_info = fetch_food_info(food_name)
        return JsonResponse(food_info, status=200)

class AutoComplete(View):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        string = data.get("food_name")
        auto_complete_info = auto_complete(string)
        return JsonResponse(auto_complete_info, safe=False, status=200)

class NutritionInformation(View):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        d = data.get("data")
        n_info = nutrition_info(d)
        return JsonResponse(n_info, safe=False, status=200)

class FoodIntakeListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FoodIntake.objects.all()
    serializer_class = FoodIntakeSerializer
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        data=request.data
        request.data['user'] = user.id
        p = data["ingredients"]
        n = data["totalNutrients"]
        parsed_ingredient = p[0]["parsed"][0]
        name = parsed_ingredient["food"]
        quantity = parsed_ingredient["quantity"]
        measure = parsed_ingredient["measure"]
        SUGARAD = n.get("SUGAR.added", {"quantity": 0})["quantity"]
        CA = n.get("CA", {"quantity": 0})["quantity"]
        CHOCDFN = n.get("CHOCDF.net", {"quantity": 0})["quantity"]
        CHOCDF = n.get("CHOCDF", {"quantity": 0})["quantity"]
        CHOLE = n.get("CHOLE", {"quantity": 0})["quantity"]
        ENERC_KCAL = n.get("ENERC_KCAL", {"quantity": 0})["quantity"]
        FAMS = n.get("FAMS", {"quantity": 0})["quantity"]
        FAPU = n.get("FAPU", {"quantity": 0})["quantity"]
        FASAT = n.get("FASAT", {"quantity": 0})["quantity"]
        FATRN = n.get("FATRN", {"quantity": 0})["quantity"]
        FIBTG = n.get("FIBTG", {"quantity": 0})["quantity"]
        FOLDFE = n.get("FOLDFE", {"quantity": 0})["quantity"]
        FOLFD = n.get("FOLFD", {"quantity": 0})["quantity"]
        FOLAC = n.get("FOLAC", {"quantity": 0})["quantity"]
        FE = n.get("FE", {"quantity": 0})["quantity"]
        MG = n.get("MG", {"quantity": 0})["quantity"]
        NIA = n.get("NIA", {"quantity": 0})["quantity"]
        P = n.get("P", {"quantity": 0})["quantity"]
        K = n.get("K", {"quantity": 0})["quantity"]
        PROCNT = n.get("PROCNT", {"quantity": 0})["quantity"]
        RIBF = n.get("RIBF", {"quantity": 0})["quantity"]
        NA = n.get("NA", {"quantity": 0})["quantity"]
        SugarA = n.get("Sugar.alcohol", {"quantity": 0})["quantity"]
        SUGART = n.get("SUGAR", {"quantity": 0})["quantity"]
        THIA = n.get("THIA", {"quantity": 0})["quantity"]
        FAT = n.get("FAT", {"quantity": 0})["quantity"]
        VITA_RAE = n.get("VITA_RAE", {"quantity": 0})["quantity"]
        VITB12 = n.get("VITB12", {"quantity": 0})["quantity"]
        VITB6A = n.get("VITB6A", {"quantity": 0})["quantity"]
        VITC = n.get("VITC", {"quantity": 0})["quantity"]
        VITD = n.get("VITD", {"quantity": 0})["quantity"]
        TOCPHA = n.get("TOCPHA", {"quantity": 0})["quantity"]
        VITK1 = n.get("VITK1", {"quantity": 0})["quantity"]
        WATER = n.get("WATER", {"quantity": 0})["quantity"]
        ZN = n.get("ZN", {"quantity": 0})["quantity"]
        food_item = FoodItem.objects.create(
        name=name,
        serving_size=quantity,
        serving_type=measure,
        sugar_ad=SUGARAD,
        calcium=CA,
        carbs_net=CHOCDFN,
        carbs_diff=CHOCDF,
        cholestrol=CHOLE,
        calories=ENERC_KCAL,
        fa_monounsaturated=FAMS,
        fa_polyunsaturated=FAPU,
        fa_totalsaturated=FASAT,
        fa_totaltrans=FATRN,
        fibre=FIBTG,
        dfe_folate=FOLDFE,
        folate_food=FOLFD,
        folic_acid=FOLAC,
        iron=FE,
        magnesium=MG,
        niacin=NIA,
        phosphorus=P,
        potassium=K,
        protein=PROCNT,
        riboflavin=RIBF,
        sodium=NA,
        sugar_alcohal=SugarA,
        sugar_total=SUGART,
        thiamin=THIA,
        fat=FAT,
        vitamin_a=VITA_RAE,
        vitamin_b12=VITB12,
        vitamin_b6=VITB6A,
        vitamin_c=VITC,
        vitamin_d=VITD,
        vitamin_e=TOCPHA,
        vitamin_k=VITK1,
        water=WATER,
        zinc=ZN,

        )
        request.data['food_item'] = food_item.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, food_item=food_item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DeleteFoodIntakeObj(generics.DestroyAPIView):
    permission_class = [permissions.IsAuthenticated]

    def delete(self, request, format=None):
        user = self.request.user
        data = request.data
        date = data.get('date')
        
        if date:
            foodintake = FoodIntake.objects.filter(user=user, date=date)
            foodintake.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)

class FoodIntakeDayView(generics.ListCreateAPIView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        request_data = json.loads(request.body)
        day = request_data.get('date')
        day = day.split("T")[0]
        
        food_intakes = FoodIntake.objects.filter(date__date=day, user=user.id)
        total_sugar_ad = 0
        total_calcium =0
        total_carbs_net=0 
        total_carbs_diff=0 
        total_cholestrol =0
        total_calories =0
        total_fa_monounsaturated =0
        total_fa_polyunsaturated =0
        total_fa_totalsaturated =0
        total_fa_totaltrans =0
        total_fibre =0
        total_dfe_folate =0
        total_folate_food =0
        total_folic_acid =0
        total_iron =0
        total_magnesium =0
        total_niacin =0
        total_phosphorus =0
        total_potassium =0
        total_protein =0
        total_riboflavin =0
        total_sodium =0
        total_sugar_alcohal=0 
        total_sugar_total =0
        total_thiamin =0
        total_fat =0
        total_vitamin_a=0 
        total_vitamin_b12=0 
        total_vitamin_b6 =0
        total_vitamin_c= 0
        total_vitamin_d =0
        total_vitamin_e =0
        total_vitamin_k =0
        total_water =0
        total_zinc =0
        for food_intake in food_intakes:
            food_item = food_intake.food_item
            total_sugar_ad = food_item.sugar_ad
            total_calcium += food_item.calcium
            total_carbs_net+= food_item.carbs_net
            total_carbs_diff+= food_item.carbs_diff
            total_cholestrol += food_item.cholestrol
            total_calories += food_item.calories
            total_fa_monounsaturated += food_item.fa_monounsaturated
            total_fa_polyunsaturated += food_item.fa_polyunsaturated
            total_fa_totalsaturated += food_item.fa_totalsaturated
            total_fa_totaltrans += food_item.fa_totaltrans
            total_fibre += food_item.fibre
            total_dfe_folate += food_item.dfe_folate
            total_folate_food += food_item.folate_food
            total_folic_acid += food_item.folic_acid 
            total_iron += food_item.iron
            total_magnesium += food_item.magnesium
            total_niacin += food_item.niacin
            total_phosphorus += food_item.phosphorus
            total_potassium += food_item.potassium
            total_protein += food_item.protein
            total_riboflavin += food_item.riboflavin
            total_sodium += food_item.sodium
            total_sugar_alcohal+= food_item.sugar_alcohal
            total_sugar_total += food_item.sugar_total
            total_thiamin += food_item.thiamin
            total_fat += food_item.fat
            total_vitamin_a+= food_item.vitamin_a 
            total_vitamin_b12+= food_item.vitamin_b12 
            total_vitamin_b6 += food_item.vitamin_b6
            total_vitamin_c= food_item.vitamin_c
            total_vitamin_d += food_item.vitamin_d
            total_vitamin_e += food_item.vitamin_e
            total_vitamin_k += food_item.vitamin_k
            total_water += food_item.water
            total_zinc += food_item.zinc
        response_data = {
            'day': day,
            'total_sugar_ad':total_sugar_ad,
            'total_calcium':total_calcium,
            'total_carbs_net':total_carbs_net,
            'total_carbs_diff': total_carbs_diff,
            'total_cholestrol':total_cholestrol,
            'total_calories':total_calories,
            'total_fa_monounsaturated':total_fa_monounsaturated,
            'total_fa_polyunsaturated':total_fa_polyunsaturated,
            'total_fa_totalsaturated':total_fa_totalsaturated,
            'total_fa_totaltrans':total_fa_totaltrans,
            'total_fibre':total_fibre,
            'total_dfe_folate':total_dfe_folate,
            'total_folate_food':total_folate_food,
            'total_folic_acid':total_folic_acid,
            'total_iron':total_iron,
            'total_magnesium':total_magnesium,
            'total_niacin':total_niacin,
            'total_phosphorus':total_phosphorus,
            'total_potassium':total_potassium,
            'total_protein':total_protein,
            'total_riboflavin':total_riboflavin,
            'total_sodium':total_sodium,
            'total_sugar_alcohal': total_sugar_alcohal,
            'total_sugar_total':total_sugar_total,
            'total_thiamin':total_thiamin,
            'total_fat':total_fat,
            'total_vitamin_a': total_vitamin_a,
            'total_vitamin_b12': total_vitamin_b12,
            'total_vitamin_b6':total_vitamin_b6,
            'total_vitamin_c':total_vitamin_c,
            'total_vitamin_d':total_vitamin_d,
            'total_vitamin_e':total_vitamin_e,
            'total_vitamin_k':total_vitamin_k,
            'total_water':total_water,
            'total_zinc':total_zinc,
        }
        return JsonResponse(response_data)