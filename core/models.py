from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

class Course(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.name} ({self.code})"

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # ← New field added here
    file_path = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.title

class Download(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
	document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='download_records')  # changed from 'downloads'
	timestamp = models.DateTimeField(auto_now_add=True)
	ip = models.GenericIPAddressField()

	def __str__(self):
		return f"{self.user} downloaded {self.document}"

class Login(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logins')
	login_time = models.DateTimeField(auto_now_add=True)
	ip = models.GenericIPAddressField()

	def __str__(self):
		return f"{self.user} logged in at {self.login_time}"

class Rating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
	document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='ratings')
	score = models.IntegerField()
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'document')

	def __str__(self):
		return f"{self.user} rated {self.document} {self.score}/5"

