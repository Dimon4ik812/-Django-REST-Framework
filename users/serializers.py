from rest_framework.serializers import ModelSerializer


from users.models import Payments, CustomsUser


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'



class CustomsUserDetailSerializer(ModelSerializer):
    payment_history = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomsUser
        fields = ['id', 'email', 'phone_number', 'avatar', 'city', 'payment_history']