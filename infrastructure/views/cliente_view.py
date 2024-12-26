from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from core.entities.cliente import Cliente
from infrastructure.serializers import ClienteSerializer


@csrf_exempt
def cliente_list(request, id):
    if request.method == 'GET':
        cliente = Cliente.objects.get(id=id)
        serializer = ClienteSerializer(cliente, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ClienteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=401)
