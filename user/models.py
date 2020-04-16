from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """Custom user implementation"""

    def save(self, *args, **kwargs):
        """Implement custom save functionality"""
        self.set_password(self.password)
        super(User, self).save(*args, **kwargs)
