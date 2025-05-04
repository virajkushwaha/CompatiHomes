from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Tenant Questions (Yes/No)
    tenant_q1 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    tenant_q2 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    tenant_q3 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    tenant_q4 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    tenant_q5 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    
    # Landlord Questions (Yes/No)
    landlord_q1 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    landlord_q2 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    landlord_q3 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    landlord_q4 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)
    landlord_q5 = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'role', 
                  'tenant_q1', 'tenant_q2', 'tenant_q3', 'tenant_q4', 'tenant_q5', 
                  'landlord_q1', 'landlord_q2', 'landlord_q3', 'landlord_q4', 'landlord_q5']

    def create(self, validated_data):
        role = validated_data.get('role')
        
        # Create the user first
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=role
        )

        # Save tenant or landlord specific answers
        if role == 'tenant':
            user.tenant_answers = {
                'q1': validated_data.get('tenant_q1'),
                'q2': validated_data.get('tenant_q2'),
                'q3': validated_data.get('tenant_q3'),
                'q4': validated_data.get('tenant_q4'),
                'q5': validated_data.get('tenant_q5')
            }
        elif role == 'landlord':
            user.landlord_answers = {
                'q1': validated_data.get('landlord_q1'),
                'q2': validated_data.get('landlord_q2'),
                'q3': validated_data.get('landlord_q3'),
                'q4': validated_data.get('landlord_q4'),
                'q5': validated_data.get('landlord_q5')
            }

        user.save()
        return user
