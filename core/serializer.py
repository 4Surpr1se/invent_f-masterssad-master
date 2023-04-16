from rest_framework import serializers

from core.models import Organization, Holding, Department, Property


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationCreateSerializer(serializers.ModelSerializer):
    holding = serializers.CharField(max_length=255)

    class Meta:
        model = Organization
        fields = '__all__'

    def create(self, validated_data):

        validated_data['holding'] = Holding.objects.get(name=validated_data.get("holding"))  # TODO переделать,
        # TODO чтобы искал по id, а не name
        organization = Organization.objects.create(**validated_data)
        return organization


class OrganizationDeleteSerializer(serializers.ModelSerializer):
    pass


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentCreateSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(max_length=255)

    class Meta:
        model = Department
        fields = '__all__'

    def create(self, validated_data):
        validated_data['organization'] = Organization.objects.get(name=validated_data.get("organization"))
        department = Department.objects.create(**validated_data)
        return department


class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = '__all__'


class HoldingCreateSerializer(serializers.ModelSerializer):
    # holding = serializers.CharField(max_length=255)

    class Meta:
        model = Holding
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = '__all__'

    # def create(self, validated_data):
    #     validated_data['organization'] = Organization.objects.get(name=validated_data.get("organization"))
    #     department = Department.objects.create(**validated_data)
    #     return department

    # def create(self, validated_data):
    #     holding = Holding.objects.get(name=validated_data.get('holding'))

