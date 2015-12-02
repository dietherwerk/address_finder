import re
import requests

from django.http import Http404

from rest_framework import serializers

from finder.models import State, City, Address
from address_finder.settings import CORREIOS_API


class AddressSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):
        cep = data.get('cep')

        if not cep:
            raise serializers.ValidationError({
                'cep': 'This field is required.'
            })

        if not re.search('^([0-9]{8})$', cep):
            raise serializers.ValidationError({
                'cep': 'Invalid Cep.'
            })

        return {
            'cep': cep
        }

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'address': obj.address,
            'district': obj.district,
            'complement': obj.complement,
            'city': obj.city.name,
            'cep': obj.cep
        }

    def save(self, validated_data):
        url = '{0}/{1}/json'.format(CORREIOS_API.get('url'),
                                    validated_data.data.get('cep'))
        response = requests.get(url)
        data_response = response.json()

        if response.status_code == 200 and not data_response.get('erro'):
            state = State.objects.create(slug=data_response.get('uf'))
            city = City.objects.create(name=data_response.get('localidade'),
                                       state=state)
            return Address.objects.create(address=data_response.get('logradouro'),
                                          complement=data_response.get('complemento'),
                                          district=data_response.get('bairro'),
                                          cep=data_response.get('cep'),
                                          city=city)

        raise Http404

    def validate(self, data):
        """
        Check if the data contains only numbers.
        """
        if re.search('^[0-9]+$', data):
            raise serializers.ValidationError("Only numbers are accepted")
        return data
