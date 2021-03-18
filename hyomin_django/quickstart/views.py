from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
# from hyomin_django.quickstart.serializers import UserSerializer, GroupSerializer
from hyomin_django.quickstart.serializers import MyKrWeatherSerializer, MyPitSerializer
from hyomin_django.quickstart.models import MyKrWeather, MyPit

from rest_framework.decorators import action
from rest_framework.response import Response

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc #한글이 나오게

import json
from collections import OrderedDict
import base64

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]



# 날씨 데이터
class MyKrWeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyKrWeather.objects.all()
    serializer_class = MyKrWeatherSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # 1. 전국 날씨 데이터
    @action(detail=False, methods=['GET'])
    def weather(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)


        df1 = pd.DataFrame(serializer.data)
        df1.columns = ['id','area','diary','now_temp','pysical_temp','rain','snow','moisture']
        area = df1['area']
        float_temp = df1['now_temp'].astype('float')
        area_index = range(len(df1['area']))
        font_name = font_manager.FontProperties(fname="C:\\Users\\Min\\Desktop\\python\\H2PORL.ttf").get_name() # Font 경로 재설정
        rc('font', family=font_name)
        fig = plt.figure(figsize=(16, 2), dpi=100)
        ax1 = fig.add_subplot(1,2,1)
        ax1.bar(area_index , float_temp, align='center', color='darkblue')
        ax1.xaxis.set_ticks_position('bottom')
        ax1.yaxis.set_ticks_position('left')
        plt.xticks(area_index , area, rotation=0, fontsize='small')

        # 그래프를 파일 저장
        fig = plt.gcf()
        fig.savefig('myfile.png', dpi=fig.dpi)


        with open('myfile.png', "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        ctx = {'image': image_data}
        return render(request, 'C:\\rest_ful\\hyomin_django\\hyomin_django\\quickstart\\index.html', ctx)
        # return Response(serializer.data)
    
    # 2. 내 지역 날씨 데이터
    @action(detail=False, methods=['GET'])
    def myarea(self, request):
        q = request.query_params.get('q', None)
        qs = self.get_queryset().filter(w_area=q)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # 3. 온도에 따른 옷 추천
    @action(detail=False, methods=['GET'])
    def recom(self, request):
        q = request.query_params.get('q', None)
        temp = int(q)
        data = []
        if temp >= 28:
            data.append('반팔')
            data.append('민소매')
            data.append('반바지')
            data.append('원피스')
        elif temp >= 23 and temp <= 27:
            data.append('반팔')
            data.append('셔츠')
            data.append('반바지')
            data.append('면바지')
        elif temp >= 20 and temp <= 22:
            data.append('가디건')
            data.append('긴팔티')
            data.append('면바지')
            data.append('청바지')
        elif temp >= 17 and temp <= 19:
            data.append('니트')
            data.append('맨투맨')
            data.append('재킷')
            data.append('청바지')
        elif temp >= 12 and temp <= 16:
            data.append('자켓')
            data.append('야상')
            data.append('니트')
        elif temp >= 9 and temp <= 11:
            data.append('코트')
            data.append('야상')
            data.append('니트')
        elif temp >= 5 and temp <= 8:
            data.append('코트')
            data.append('히트텍')
            data.append('니트')
        elif temp <= 4:
            data.append('패딩')
            data.append('코트')
            data.append('목도리')
            data.append('장갑')
        return Response(data)

    # 4. 내 지역과 전국 지역 날씨 평균 비교하기
    @action(detail=False, methods=['GET'])
    def compare(self, request):
        q = request.query_params.get('q', None)
        qs = self.get_queryset().filter(w_area=q)
        serializer = self.get_serializer(qs, many=True)

        qs1 = self.get_queryset()
        s1 = self.get_serializer(qs1, many=True)

        cute = []
        pcute = []
        rain = []
        snow = []
        humi = []
        for i in range(len(s1.data)):
            cute.append(float(s1.data[i]['w_cute']))
            pcute.append(float(s1.data[i]['w_pcute']))

            try:
                d1 = float(s1.data[i]['w_rain'])
                rain.append(d1)
            except:
                rain.append(0)
            try:
                d2 = float(s1.data[i]['w_snow'])
                snow.append(d2)
            except:
                snow.append(0)

            humi.append(float(s1.data[i]['w_humi']))
        
        cute_a = sum(cute)/len(cute)
        pcute_a = sum(pcute)/len(pcute)
        rain_a = sum(rain)/len(rain)
        snow_a = sum(snow)/len(snow)
        humi_a = sum(humi)/len(humi)

        result = {
            '내 지역 현재 기온' : serializer.data[0]['w_cute'],
            '내 지역 체감 기온' : serializer.data[0]['w_pcute'],
            '내 지역 강수량' : serializer.data[0]['w_rain'],
            '내 지역 적설량' : serializer.data[0]['w_snow'],
            '내 지역 습도' : serializer.data[0]['w_humi'],
            '전국지역 평균 현재 기온' : cute_a,
            '전국지역 평균 체감 기온' : pcute_a,
            '전국지역 평균 강수량' : rain_a,
            '전국지역 평균 적설량' : snow_a,
            '전국지역 평균 습도' : humi_a
        }

        return Response(result)

    
    # 5. 내 지역 불쾌지수와 전국 지역 불쾌지수 비교하기
    @action(detail=False, methods=['GET'])
    def angry(self, request):
        q = request.query_params.get('q', None)
        qs = self.get_queryset().filter(w_area=q)
        serializer = self.get_serializer(qs, many=True)

        qs1 = self.get_queryset()
        s1 = self.get_serializer(qs1, many=True)

        my_temp = float(serializer.data[0]['w_cute'])
        my_humi = float(serializer.data[0]['w_humi'])

        cute = []
        humi = []
        for i in range(len(s1.data)):
            cute.append(float(s1.data[i]['w_cute']))
            humi.append(float(s1.data[i]['w_humi']))

        cute_a = sum(cute)/len(cute)
        humi_a = sum(humi)/len(humi)

        my_disc = (9 / 5 * my_temp) - 0.55 * (100 - my_humi) * (9 / 5 * my_temp - 26) / 100 + 32
        disc = (9 / 5 * cute_a) - 0.55 * (100 - humi_a) * (9 / 5 * cute_a - 26) / 100 + 32
        my_result = ''
        ta_result = ''

        if my_disc >= 80:
            my_result = "불쾌지수 매우높음"
        elif my_disc >= 75:
            my_result = "불쾌지수 높음"
        elif my_disc >= 68:
            my_result = "불쾌지수 보통"
        else:
            my_result = "불쾌지수 낮음"

        if disc >= 80:
            ta_result = "불쾌지수 매우높음"
        elif disc >= 75:
            ta_result = "불쾌지수 높음"
        elif disc >= 68:
            ta_result = "불쾌지수 보통"
        else:
            ta_result = "불쾌지수 낮음"

        result = {
            '내 지역 불쾌지수' : my_disc,
            '내 지역 불쾌수준' : my_result,
            '전국 지역 평균 불쾌지수' : disc,
            '전국 지역 불쾌수준' : ta_result
        }
        
        return Response(result)


    

# 1. 쇼핑몰 데이터 전체
class MyPitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyPit.objects.all()
    serializer_class = MyPitSerializer

    # 6. 의류 카테고리 목록 보여주기
    @action(detail=False, methods=['GET'])
    def category(self, request):
        data = [
            '반팔', '민소매', '반바지', '원피스', '셔츠', '면바지', 
            '가디건', '긴팔티', '청바지', '니트', '맨투맨', '자켓', 
            '야상', '니트', '코트', '히트텍', '패딩'
        ]
        return Response(data)



    # 7. 카테고리 별 의류 목록 보여주기
    @action(detail=False, methods=['GET'])
    def angry(self, request):
        q = request.query_params.get('q', None)
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        data = []
        for i in range(len(serializer.data)):
            if  q in serializer.data[i]['iname']:
                data.append(serializer.data[i])
        
        return Response(data)

    
    # 8. 전체 의류 리뷰 순위 랭킹 목록 보여주기
    @action(detail=False, methods=['GET'])
    def all_review_rank(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        data = sorted(serializer.data, key=lambda k: int(k['ireview']), reverse=True)
        return Response(data)


    # 9. 카테고리 별 리뷰 순위 랭킹 보여주기
    @action(detail=False, methods=['GET'])
    def cate_rank(self, request):
        q = request.query_params.get('q', None)
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        data = []
        for i in range(len(serializer.data)):
            if  q in serializer.data[i]['iname']:
                data.append(serializer.data[i])

        data = sorted(data, key=lambda k: int(k['ireview']), reverse=True)
        return Response(data)


    # 10. 전체 상품 높은 가격 순위 목록
    @action(detail=False, methods=['GET'])
    def all_price_rank(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        for i in range(len(serializer.data)):
            data = serializer.data[i]['iprice']
            data = data[:-1]
            data = data.split(',')
            if len(data) == 1:
                data = data[0]
            elif len(data) == 2:
                data = data[0] + data[1]
            elif len(data) == 3:
                data = data[0] + data[1] + data[2]
            serializer.data[i]['iprice'] = data

        data = sorted(serializer.data, key=lambda k: int(k['iprice']), reverse=True)
        return Response(data)


    # 11. 전체 상품 낮은 가격 순위 목록
    @action(detail=False, methods=['GET'])
    def all_price_reverse(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        for i in range(len(serializer.data)):
            data = serializer.data[i]['iprice']
            data = data[:-1]
            data = data.split(',')
            if len(data) == 1:
                data = data[0]
            elif len(data) == 2:
                data = data[0] + data[1]
            elif len(data) == 3:
                data = data[0] + data[1] + data[2]
            serializer.data[i]['iprice'] = data

        data = sorted(serializer.data, key=lambda k: int(k['iprice']), reverse=False)
        return Response(data)


    # 12. 카테고리 별 높은 가격 순위 목록
    @action(detail=False, methods=['GET'])
    def cate_price_rank(self, request):
        q = request.query_params.get('q', None)
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        data = []
        for i in range(len(serializer.data)):
            if  q in serializer.data[i]['iname']:
                data.append(serializer.data[i])

        for i in range(len(data)):
            result = data[i]['iprice']
            result = result[:-1]
            result = result.split(',')
            if len(result) == 1:
                result = result[0]
            elif len(result) == 2:
                result = result[0] + result[1]
            elif len(data) == 3:
                result = result[0] + result[1] + result[2]
            data[i]['iprice'] = int(result)

        data = sorted(data, key=lambda k: k['iprice'], reverse=True)
        return Response(data)


    # 13. 카테고리 별 낮은 가격 순위 목록
    @action(detail=False, methods=['GET'])
    def cate_price_reverse(self, request):
        q = request.query_params.get('q', None)
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        data = []
        for i in range(len(serializer.data)):
            if  q in serializer.data[i]['iname']:
                data.append(serializer.data[i])

        for i in range(len(data)):
            result = data[i]['iprice']
            result = result[:-1]
            result = result.split(',')
            if len(result) == 1:
                result = result[0]
            elif len(result) == 2:
                result = result[0] + result[1]
            elif len(data) == 3:
                result = result[0] + result[1] + result[2]
            data[i]['iprice'] = int(result)

        data = sorted(data, key=lambda k: k['iprice'], reverse=False)
        return Response(data)


    