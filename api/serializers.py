from rest_framework import serializers
from .models import CitizenEducationDetails, Citizen


class CitizenEductaionDetailSerializer(serializers.ModelSerializer):
    citizen_id = serializers.RelatedField(source='citizen', read_only=True)
    name = serializers.RelatedField(source='citizen', read_only=True)
    aadhar = serializers.RelatedField(source='citizen', read_only=True)
    dob = serializers.RelatedField(source='citizen', read_only=True)
    state = serializers.RelatedField(source='citizen', read_only=True)
    pincode = serializers.RelatedField(source='citizen', read_only=True)
    gender = serializers.RelatedField(source='citizen', read_only=True)
    email = serializers.RelatedField(source='citizen', read_only=True)
    primary_phone = serializers.RelatedField(source='citizen', read_only=True)
    other_phone = serializers.RelatedField(source='citizen', read_only=True)
    location = serializers.RelatedField(source='citizen', read_only=True)
    address = serializers.RelatedField(source='citizen', read_only=True)
    resume_path = serializers.RelatedField(source='citizen', read_only=True)

    class Meta:
        model = CitizenEducationDetails
        fields = ['citizen_id', 'name', 'aadhar', 'dob', 'state', 'pincode', 'gender', 'email', 'primary_phone',
                  'other_phone', 'location', 'address', 'resume_path', 'education_board',
                  'education_level', 'education_specialization', 'year_of_passing',
                  'institute']


class CitizenDetailSerializer(serializers.ModelSerializer):
    education_board = serializers.RelatedField(source='citizen', read_only=True)
    education_level = serializers.RelatedField(source='citizen', read_only=True)
    education_specialization = serializers.RelatedField(source='citizen', read_only=True)
    year_of_passing = serializers.RelatedField(source='citizen', read_only=True)
    institute = serializers.RelatedField(source='citizen', read_only=True)

    class Meta:
        model = Citizen
        fields = ['citizen_id', 'name', 'aadhar', 'dob', 'state', 'pincode', 'gender', 'email', 'primary_phone',
                  'other_phone', 'location', 'address', 'resume_path', 'education']

    def to_representation(self, instance):
        self.fields['education'] = CitizenEducationSerializer(read_only=True)
        return super(CitizenDetailSerializer, self).to_representation(instance)

class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ['citizen_id', 'name', 'aadhar', 'dob', 'state', 'pincode', 'gender', 'email', 'primary_phone',
                  'other_phone', 'location', 'address', 'resume_path']
        depth = 1

class CitizenEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenEducationDetails
        fields = '__all__'

class CitizenDetailSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = CitizenEducationDetails
        fields = ['citizen', 'education_board', 'education_level', 'education_specialization', 'year_of_passing',
                  'institute']
        depth = 1
