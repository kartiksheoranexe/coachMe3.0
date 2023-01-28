from datetime import datetime

from django.db.models import Min, Max
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
import pandas as pd

from panalyzer.serializers import TrainingSplitSerializer, MusclePartsExcelSerializer, ExerciseSelectionSerializer, LogPerformanceSerializer, HeartPerformanceSerializer, HeartPerformanceMinMaxSerializer
from panalyzer.models import TrainingSplit, MuscleParts, LogPerformance, HeartPerformance, ExerciseSelection
from panalyzer.scripts import calculate_muscle_load

from main.models import CustomUser, Coach, Client


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

class ExcelTrainingDesignView(generics.CreateAPIView):
    parser_classes = (FileUploadParser,)
    queryset = TrainingSplit.objects.all()
    serializer_class = TrainingSplitSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            file_obj = request.FILES['file']
            df = pd.read_excel(file_obj, sheet_name='Client Details', engine='openpyxl')
            coach_client_df = df.loc[:, ['Unnamed: 1', 'Unnamed: 5']]
            coach_client_dict = coach_client_df.to_dict(orient='split')
            coach_client_list = coach_client_dict['data']
            coach_client_map = {}
            for coach_client in coach_client_list:
                coach_client_map[coach_client[0]] = coach_client[1]
            df2 = pd.read_excel(file_obj, sheet_name='Plan Details', engine='openpyxl')
            split_details_df = df2.loc[:, ['Pre-Def','Split Name', 'Split Description', 'Split - Days']]
            split_details_dict = split_details_df.to_dict(orient='split')
            split_details_list = split_details_dict['data']
            parsed_data = []
            split_details_list = [item for item in split_details_list if not any(pd.isnull(val) for val in item)]
            for split_details in split_details_list:
                coach_name = list(coach_client_map.keys())[0]
                coach_usr_obj = CustomUser.objects.get(username=coach_name)
                client_name = coach_client_map[coach_name]
                client_usr_obj = CustomUser.objects.get(username=client_name)
                coach_obj = Coach.objects.get(user=coach_usr_obj)
                client_obj = Client.objects.get(user=client_usr_obj)
                training_split_obj, created = TrainingSplit.objects.update_or_create(
                    coach=coach_obj, 
                    client=client_obj,
                )
                if created:
                    parsed_data.append({
                    'coach': coach_obj.id,
                    'client': client_obj.id,
                    'pre_def': split_details[0],
                    'split_name': split_details[1],
                    'split_desc': split_details[2],
                    'split_days': split_details[3]
                    })
                else:
                     parsed_data.append({
                    'coach': coach_obj.id,
                    'client': client_obj.id,
                    'pre_def': split_details[0],
                    'split_name': split_details[1],
                    'split_desc': split_details[2],
                    'split_days': split_details[3]
                    })
            serializer = self.get_serializer(data=parsed_data, many=True)
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except MultiValueDictKeyError:
            return Response({"No client log file attached!"})

class ExcelExerciseSelectionView(generics.CreateAPIView):
    parser_classes = (FileUploadParser,)
    queryset = MuscleParts.objects.all()
    serializer_class = MusclePartsExcelSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            file_obj = request.FILES['file']
            df = pd.read_excel(file_obj, sheet_name='Client Details', engine='openpyxl')
            coach_client_df = df.loc[:, ['Unnamed: 1', 'Unnamed: 5']]
            coach_client_dict = coach_client_df.to_dict(orient='split')
            coach_client_list = coach_client_dict['data']
            coach_client_map = {}
            for coach_client in coach_client_list:
                coach_client_map[coach_client[0]] = coach_client[1]
            df2 = pd.read_excel(file_obj, sheet_name='Plan Details', engine='openpyxl')
            split_details_df = df2.loc[:, ['Muscle Parts','Total Sets']]
            split_details_dict = split_details_df.to_dict(orient='split')
            split_details_list = split_details_dict['data']
            parsed_data = []
            split_details_list = [item for item in split_details_list if not any(pd.isnull(val) for val in item)]
            MUSCLE_TYPE = (
                ('Chest', 'CH'),
                ('Back', 'BA'),
                ('Legs', 'LE'),
                ('Shoulders', 'SH'),
                ('Arms', 'AR'),
                ('Abs', 'AB'),
            )
            abbreviations = dict(MUSCLE_TYPE)
            split_details_list = [[abbreviations.get(x[0], x[0]), x[1]] for x in split_details_list]
            for split_details in split_details_list:
                print(split_details)
                coach_name = list(coach_client_map.keys())[0]
                coach_usr_obj = CustomUser.objects.get(username=coach_name)
                client_name = coach_client_map[coach_name]
                client_usr_obj = CustomUser.objects.get(username=client_name)
                coach_obj = Coach.objects.get(user=coach_usr_obj)
                client_obj = Client.objects.get(user=client_usr_obj)
                training_split_obj = TrainingSplit.objects.get(coach=coach_obj,client=client_obj)
                muscle_parts_obj, created = MuscleParts.objects.update_or_create(
                    split=training_split_obj, 
                    muscles=split_details[0],
                    defaults={
                        'total_sets': split_details[1]
                    }
                )
                if created:
                    parsed_data.append({
                        'split': training_split_obj.id,
                        'muscles': split_details[0],
                        'total_sets': split_details[1]
                    })
                else:
                     parsed_data.append({
                        'split': training_split_obj.id,
                        'muscles': split_details[0],
                        'total_sets': muscle_parts_obj.total_sets
                    })
            serializer = self.get_serializer(data=parsed_data, many=True)
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except MultiValueDictKeyError:
            return Response({"No client log file attached!"})

class ExcelWorkoutCreationView(generics.CreateAPIView):
    parser_classes = (FileUploadParser,)
    queryset = ExerciseSelection.objects.all()
    serializer_class = ExerciseSelectionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            file_obj = request.FILES['file']
            df = pd.read_excel(file_obj, sheet_name='Client Details', engine='openpyxl')
            coach_client_df = df.loc[:, ['Unnamed: 1', 'Unnamed: 5']]
            coach_client_dict = coach_client_df.to_dict(orient='split')
            coach_client_list = coach_client_dict['data']
            coach_client_map = {}
            for coach_client in coach_client_list:
                coach_client_map[coach_client[0]] = coach_client[1]
            df2 = pd.read_excel(file_obj, sheet_name='Plan Details', engine='openpyxl')
            split_details_df = df2.loc[:, ['Muscle Parts','Exercise Name','Sets', 'Rep-Range', 'Exercise Description']]
            split_details_dict = split_details_df.to_dict(orient='split')
            split_details_list = split_details_dict['data']
            parsed_data = []
            split_details_list = [item for item in split_details_list if not any(pd.isnull(val) for val in item)]
            MUSCLE_TYPE = (
                ('Chest', 'CH'),
                ('Back', 'BA'),
                ('Legs', 'LE'),
                ('Shoulders', 'SH'),
                ('Arms', 'AR'),
                ('Abs', 'AB'),
            )
            abbreviations = dict(MUSCLE_TYPE)
            split_details_list = [[abbreviations.get(x[0], x[0]), x[1], x[2], x[3], x[4]] for x in split_details_list]
            for split_details in split_details_list:
                print(split_details)
                coach_name = list(coach_client_map.keys())[0]
                coach_usr_obj = CustomUser.objects.get(username=coach_name)
                client_name = coach_client_map[coach_name]
                client_usr_obj = CustomUser.objects.get(username=client_name)
                coach_obj = Coach.objects.get(user=coach_usr_obj)
                client_obj = Client.objects.get(user=client_usr_obj)
                training_split_obj = TrainingSplit.objects.get(coach=coach_obj,client=client_obj)
                muscle_obj = MuscleParts.objects.filter(split=training_split_obj)
                try:
                    m_muscle_obj = muscle_obj.get(muscles=split_details[0])
                    print(m_muscle_obj)
                except MuscleParts.DoesNotExist:
                    print("not found in muscle_obj")
                exercise_selection_obj, created = ExerciseSelection.objects.update_or_create(
                    muscle=m_muscle_obj, 
                    exercise_name=split_details[1],
                    defaults={
                        'sets': split_details[2],
                        'rep_range': split_details[3],
                        'exercise_description': split_details[4],
                    }
                )
                if created:
                    parsed_data.append({
                        'muscle': m_muscle_obj.id,
                        'exercise_name': split_details[1],
                        'sets': split_details[2],
                        'rep_range': split_details[3],
                        'exercise_description': split_details[4]
                    })
                else:
                     parsed_data.append({
                        'muscle': m_muscle_obj.id,
                        'exercise_name': split_details[1],
                        'sets': exercise_selection_obj.sets,
                        'rep_range': exercise_selection_obj.rep_range,
                        'exercise_description': exercise_selection_obj.exercise_description
                    })
            serializer = self.get_serializer(data=parsed_data, many=True)
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except MultiValueDictKeyError:
            return Response({"No client log file attached!"})


class ExcelLogCreationView(generics.CreateAPIView):
    parser_classes = (FileUploadParser,)
    queryset = LogPerformance.objects.all()
    serializer_class = LogPerformanceSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            file_obj = request.FILES['file']
            df = pd.read_excel(file_obj, sheet_name='Client Details', engine='openpyxl')
            coach_client_df = df.loc[:, ['Unnamed: 1', 'Unnamed: 5']]
            coach_client_dict = coach_client_df.to_dict(orient='split')
            coach_client_list = coach_client_dict['data']
            coach_client_map = {}
            for coach_client in coach_client_list:
                coach_client_map[coach_client[0]] = coach_client[1]
            df2 = pd.read_excel(file_obj, sheet_name='Logs1', engine='openpyxl')
            # print(df2)
            split_details_df = df2.loc[:, ['Workout 1','Day', 'Exercise Name', 'Sets', 'Weights', 'Unit', 'Reps', 'Day', 'Exercise Name', 'Sets', 'Weights', 'Unit', 'Reps']]
            # print(split_details_df)
            split_details_dict = split_details_df.to_dict(orient='split')
            print(split_details_dict)
            split_details_list = split_details_dict['data']
            # print(split_details_list)
            parsed_data = []
            split_details_list = [item for item in split_details_list if not any(pd.isnull(val) for val in item)]
            # print(split_details_list)
            MUSCLE_TYPE = (
                ('Chest', 'CH'),
                ('Back', 'BA'),
                ('Legs', 'LE'),
                ('Shoulders', 'SH'),
                ('Arms', 'AR'),
                ('Abs', 'AB'),
            )
            abbreviations = dict(MUSCLE_TYPE)
            split_details_list = [[abbreviations.get(x[0], x[0]), x[1], x[2], x[3], x[4]] for x in split_details_list]
            for split_details in split_details_list:
                print(split_details)
                coach_name = list(coach_client_map.keys())[0]
                coach_usr_obj = CustomUser.objects.get(username=coach_name)
                client_name = coach_client_map[coach_name]
                client_usr_obj = CustomUser.objects.get(username=client_name)
                coach_obj = Coach.objects.get(user=coach_usr_obj)
                client_obj = Client.objects.get(user=client_usr_obj)
                training_split_obj = TrainingSplit.objects.get(coach=coach_obj,client=client_obj)
                muscle_obj = MuscleParts.objects.filter(split=training_split_obj)
                try:
                    m_muscle_obj = muscle_obj.get(muscles=split_details[0])
                    print(m_muscle_obj)
                except MuscleParts.DoesNotExist:
                    print("not found in muscle_obj")
                exercise_selection_obj, created = ExerciseSelection.objects.update_or_create(
                    muscle=m_muscle_obj, 
                    exercise_name=split_details[1],
                    defaults={
                        'sets': split_details[2],
                        'rep_range': split_details[3],
                        'exercise_description': split_details[4],
                    }
                )
                if created:
                    parsed_data.append({
                        'muscle': m_muscle_obj.id,
                        'exercise_name': split_details[1],
                        'sets': split_details[2],
                        'rep_range': split_details[3],
                        'exercise_description': split_details[4]
                    })
                else:
                     parsed_data.append({
                        'muscle': m_muscle_obj.id,
                        'exercise_name': split_details[1],
                        'sets': exercise_selection_obj.sets,
                        'rep_range': exercise_selection_obj.rep_range,
                        'exercise_description': exercise_selection_obj.exercise_description
                    })
            serializer = self.get_serializer(data=parsed_data, many=True)
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except MultiValueDictKeyError:
            return Response({"No client log file attached!"})
