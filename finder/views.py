from django.http import Http404

from finder.models import Address
from finder.serializers import AddressSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AddressList(APIView):
    def get_object(self, cep):
        try:
            return Address.objects.get(cep=cep)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, cep, *args, **kwargs):
        address = self.get_object(cep)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request, *args, **kwargs)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
