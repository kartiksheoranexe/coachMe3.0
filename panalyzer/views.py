from datetime import datetime

from django.db.models import Min, Max
from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from panalyzer.serializers import TrainingSplitSerializer, ExerciseSelectionSerializer, LogPerformanceSerializer, HeartPerformanceSerializer, HeartPerformanceMinMaxSerializer
from panalyzer.models import TrainingSplit, MuscleParts, HeartPerformance
from panalyzer.scripts import calculate_muscle_load

from main.models import Coach, Client


class CreateWorkoutPlan(generics.CreateAPIView):
    serializer_class = TrainingSplitSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        coach_obj = Coach.objects.filter(user=request.user)[0]
        serializer.validated_data['coach'] = coach_obj
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        exercises_data = request.data.get('exercise_selections')
        split_name = request.data.get('split_name')
        split = TrainingSplit.objects.get(split_name=split_name)
        muscle_sets = {}
        muscle_parts = {}

        for exercise in exercises_data:
            muscle_parts_data = exercise.get('muscle')
            sets = exercise.get('sets')
            if muscle_parts_data in muscle_sets:
                muscle_sets[muscle_parts_data] += sets
            else:
                muscle_sets[muscle_parts_data] = sets
            if muscle_parts_data not in muscle_parts:
                muscle_part = MuscleParts.objects.create(
                    split=split, muscles=muscle_parts_data, total_sets=muscle_sets[muscle_parts_data])
                muscle_parts[muscle_parts_data] = muscle_part
            else:
                muscle_part = muscle_parts[muscle_parts_data]

        for exercise in exercises_data:
            exercise['muscle'] = muscle_parts[exercise['muscle']].id
            exercise_serializer = ExerciseSelectionSerializer(data=exercise)
            exercise_serializer.is_valid(raise_exception=True)
            exercise_serializer.save()

        return Response(serializer.data, headers=headers)


class LogPerformanceCreateView(generics.CreateAPIView):
    serializer_class = LogPerformanceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        client = Client.objects.get(user=self.request.user)
        request.data['client'] = client.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CalculateMuscleLoadView(APIView):
    def post(self, request):
        client = Client.objects.filter(user=request.user)[0]
        muscle_load = calculate_muscle_load(client)

        return Response({
            'muscle_load': muscle_load,
        })

class HeartPerformanceView(generics.ListCreateAPIView):
    queryset = HeartPerformance.objects.all()
    serializer_class = HeartPerformanceSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        client_obj = Client.objects.filter(user=user)[0]
        date_str = request.query_params.get('date')
        if date_str is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                queryset = self.queryset.filter(client=client_obj, timestamp__date=date)
                lowest_heart_rate = queryset.aggregate(Min('resting_heart_rate'))['resting_heart_rate__min']
                highest_heart_rate = queryset.aggregate(Max('maximum_heart_rate'))['maximum_heart_rate__max']
                serializer = HeartPerformanceMinMaxSerializer(data={'min': lowest_heart_rate, 'max': highest_heart_rate})
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        client_obj = Client.objects.filter(user=user)[0]
        serializer.save(client=client_obj)