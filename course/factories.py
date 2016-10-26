import factory
from datetime import timedelta


class TutorFactory(factory.DjangoModelFactory):

    class Meta:
        model = 'course.Tutor'

    name = factory.Sequence(lambda n: 'tutor{}'.format(n))


class CourseFactory(factory.DjangoModelFactory):

    class Meta:
        model = 'course.Course'

    name = factory.Sequence(lambda n: 'course{}'.format(n))
    credits = 30
    duration = timedelta(days=30)  # Default course duration of 30 days

    @factory.post_generation
    def tutors(self, create, extracted, **kwargs):
        """Generate a many to many relationship with any provided tutors."""
        if not create:
            # Simple build
            return

        if extracted:
            # A list of tutors were passed in
            for tutor in extracted:
                self.tutors.add(tutor)
