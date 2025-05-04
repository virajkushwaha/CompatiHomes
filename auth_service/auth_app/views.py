from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Landlord
from .utils import haversine
from rest_framework.decorators import api_view
from .serializers import UserRegistrationSerializer
class RegisterView(APIView):
    def post(self, request):
        # Your registration logic here
        return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)
# auth_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new user and return success response
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def get_nearby_landlords(request):
    try:
        tenant_lat = float(request.GET.get('tenant_lat'))
        tenant_lon = float(request.GET.get('tenant_lon'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Latitude and Longitude are required'}, status=400)

    landlords = Landlord.objects.all()
    nearby = []

    for landlord in landlords:
        distance = haversine(tenant_lat, tenant_lon, landlord.latitude, landlord.longitude)
        if distance <= 10:
            nearby.append({
                'username': landlord.user.username,
                'latitude': landlord.latitude,
                'longitude': landlord.longitude,
                'distance': round(distance, 2),
            })

    return JsonResponse({'landlords_within_10km': nearby})