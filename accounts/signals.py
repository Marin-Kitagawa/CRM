from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Patient

def patient_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Patient.objects.create(
            user = instance,
            name=instance.username,
        )
        print('Profile created')

post_save.connect(patient_profile, sender=User)
