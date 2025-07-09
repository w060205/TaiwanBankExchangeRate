from rest_framework import serializers
from api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        '''
        fields =
        id ,currency ,date ,cash_buy ,cash_sell
    
        '''

    # def validate_cash_buy(self, value):
    #     if value is not None and value < 0:
    #         raise serializers.ValidationError("買入價不能小於 0")
    #     return value
    #
    # def validate_cash_sell(self, value):
    #     if value is not None and value < 0:
    #         raise serializers.ValidationError("賣出價不能小於 0")
    #     return value
