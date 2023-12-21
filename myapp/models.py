from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, company_name, password=None, company_id=None):
        if not email:
            raise ValueError("Users must have an email address")

        # Remove the automatic generation of company_id
        if company_id is None:
            raise ValueError("Users must have a company ID")

        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,
            company_id=company_id,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # The create_superuser method remains unchanged
    def create_superuser(self, email, company_name, password=None, company_id=None):
        user = self.create_user(
            email,
            company_name,
            password=password,
            company_id=company_id,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    company_id = models.CharField(max_length=100, unique=True)
    company_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True, validators=[EmailValidator()])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'company_id'
    REQUIRED_FIELDS = ['company_name' ,'email']


    def __str__(self):
        return self.company_id
    


class api1(models.Model):
    api = models.CharField(max_length=100)
    cid = models.CharField(max_length=100)

    def __str__(self):
        return self.api


from django.db import models


class Company(models.Model):
    company_id = models.IntegerField(unique=True)

    def __int__(self):
        return self.company_id
    

class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)
    employee_id = models.CharField(max_length=50, unique=True)
    company_id = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

    
class Camera(models.Model):
    camera_name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.camera_name # Define camera_name as the primary key

class PersonData(models.Model):
    image_path = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    pose = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    var1 = models.CharField(max_length=100)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE) 
    class_name = models.CharField(max_length=255, null=True)
    count = models.IntegerField(null=True)
    date_created = models.CharField(max_length=200, null=True)
    time_created = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.person.name

class ServerInfo(models.Model):
    id = models.CharField(max_length=200,primary_key=True)
    brand = models.CharField(max_length=200)
    cam_name=models.CharField(max_length=100,default=True)
    port = models.PositiveIntegerField(null=True, blank=True)
    ip_address = models.CharField(max_length=200)
    username = models.CharField(max_length=50,default=True)
    password = models.CharField(max_length=50)
    url=models.CharField(max_length=100,default=True,null=True,blank=True)

    def __str__(self):
        return f"{self.cam_name}"

class EmployeeCameraAssignment(models.Model):
    employee = models.ForeignKey(Person, on_delete=models.CASCADE)
    cam = models.ForeignKey(ServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.name} assigned to {self.cam.cam_name}"
