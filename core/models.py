from django.db import models

class User(models.Model):
	name = models.CharField(max_length=255)
	phone = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name

class Course(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.name} ({self.code})"

class Document(models.Model):
	title = models.CharField(max_length=255)
	file_path = models.FileField(upload_to='documents/')
	upload_date = models.DateTimeField(auto_now_add=True)
	views = models.IntegerField(default=0)
	downloads = models.IntegerField(default=0)  # This remaineth unchanged
	term = models.CharField(max_length=50)
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

