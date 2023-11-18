from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


#need to write some ,overriding function who could write the create user,and superuser .
class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('please enter,the valid email')
        if not username:
            raise ValueError('please enter the username')
        user=self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
        )
        password=password
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
def create_profile_image_filepath(self,filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'
def create_default_image_filepath():
    return f'media/img.png'


#custom User model:
class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name="email",max_length=60,unique=True)
    password = models.CharField(max_length=128)  # Use CharField for password
    username=models.CharField(max_length=30,unique=True)
    date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    profile_image=models.ImageField(max_length=250,upload_to=create_profile_image_filepath,blank=True,null=True,default=create_default_image_filepath)
    hide_email=models.BooleanField(default=True)
    #login with email,instead of proceeding with username
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']
    objects=MyAccountManager()
    def __str__(self):
        return self.username
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
    #some overiding function
    def has_perm(self,perm,object=None):
        return self.is_admin
    def has_module_per(self,app_label):
        return True