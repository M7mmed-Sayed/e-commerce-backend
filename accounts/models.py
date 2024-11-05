from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
class UserType(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    SELLER = "SELLER", "Seller"
    EMPLOYEE = "EMPLOYEE", "Employee"
    CUSTOMER = "CUSTOMER", "Customer"


class AppUserManager(BaseUserManager):
    def create_user(self, email, username, first_name,last_name,phone_number,password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model( email=email,first_name=first_name,last_name=last_name,phone_number=phone_number,username=username,**extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name,last_name,phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        extra_fields.setdefault('usertype', UserType.ADMIN)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, username, first_name,last_name,phone_number,password, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    """
          Represents a Custom User To Add extra Fields
        """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True ,default='Cairo')
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=False)
    usertype = models.CharField(max_length=15, choices=UserType.choices, default=UserType.CUSTOMER)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = AppUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name','last_name','phone_number',]

    def __str__(self):
        return self.email



class OTP(models.Model):
    otp_email = models.EmailField(unique=True)  
    otp_expired_at = models.DateTimeField()
    otp_code = models.CharField(max_length=12)
    def __str__(self):
        return f'{self.otp_email} {self.otp_code}'


