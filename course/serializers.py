from rest_framework import serializers

from .models import Tutor, Course


class TutorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutor
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False
            },
            'name': {'required': False}
        }

    def validate_id(self, value):
        """Check that a Tutor object exists for the given id

        The id field is optional, however if an id is specified a corresponding Tutor
        object should exist.
        """
        try:
            Tutor.objects.get(pk=value)
        except Tutor.DoesNotExist:
            raise serializers.ValidationError('Tutor object with id \'{}\' does not exist.'.format(value))
        return value


class CourseSerializer(serializers.ModelSerializer):
    tutors = TutorSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        tutors_data = validated_data.pop('tutors')
        course = Course.objects.create(**validated_data)
        # If 'id' in tutor post data get the Tutor object with that id and add
        # it to the course. Otherwise, create a new Tutor object and add that
        # to the course.
        for tutor_data in tutors_data:
            if 'id' in tutor_data:
                tutor = Tutor.objects.get(pk=tutor_data['id'])
            else:
                tutor = Tutor.objects.create(**tutor_data)
            course.tutors.add(tutor)
        course.save()
        return course

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.credits = validated_data.get('credits', instance.credits)
        instance.duration = validated_data.get('duration', instance.duration)
        tutors_data = validated_data.get('tutors', [])
        instance.tutors = []
        for tutor_data in tutors_data:
            if 'id' in tutor_data:
                tutor = Tutor.objects.get(pk=tutor_data['id'])
            else:
                tutor = Tutor.objects.create(**tutor_data)
            instance.tutors.add(tutor)
        instance.save()
        return instance
