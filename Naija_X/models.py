from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",  related_name="followed_by", symmetrical=False, blank=True)
    image = ResizedImageField(size=[300, 300], quality=75, upload_to="profiles/", blank=True,)

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = Profile(user=instance)
            user_profile.save()
            user_profile.follows.add(instance.profile)
            user_profile.save()


class Posts(models.Model):
    user = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )
    

    