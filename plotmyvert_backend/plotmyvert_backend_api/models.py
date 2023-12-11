from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
# create a custom user model with email as the primary identifier, password, receive_email, receive_email_password, mail_server, mail_port, mail_SSL

class UserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError('The Email field must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault("is_active", True)
    if extra_fields.get("is_staff") is not True:
        raise ValueError(_("Superuser must have is_staff=True."))
    if extra_fields.get("is_superuser") is not True:
        raise ValueError(_("Superuser must have is_superuser=True."))
    return self.create_user(email, password, **extra_fields)
  
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, db_index=True, primary_key=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    receive_email_login = models.EmailField(max_length=254, null=True, blank=True)
    receive_email_password = models.CharField(max_length=254, null=True, blank=True)
    receive_email_receiver = models.EmailField(max_length=254, null=True, blank=True)
    mail_server = models.CharField(max_length=254, null=True, blank=True)
    mail_port = models.IntegerField(null=True, blank=True)
    mail_SSL = models.BooleanField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
      
    def get_config(self):
        return {
            "receive_email_login": self.receive_email_login,
            "receive_email_password": self.receive_email_password,
            "receive_email_receiver": self.receive_email_receiver,
            "mail_server": self.mail_server,
            "mail_port": self.mail_port,
            "mail_SSL": self.mail_SSL
        }
        
        
class JumpSessionModel(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start_datetime = models.DateTimeField(unique=True, primary_key=True)
  count = models.IntegerField()
  average_high = models.FloatField()
  highest = models.FloatField()
  plotly_json = models.TextField()
  
  def __str__(self):
    return self.start_datetime.strftime('%Y-%m-%d %H:%M:%S')
  
  
class JumpSessionJumpsModel(models.Model):
  session = models.ForeignKey(JumpSessionModel, on_delete=models.CASCADE)
  timestamp = models.DateTimeField()
  jump_height = models.FloatField()