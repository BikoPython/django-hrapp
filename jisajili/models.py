from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import(AbstractBaseUser,
      BaseUserManager,PermissionsMixin)
from django.core.exceptions import ValidationError


class JobSeekerUserManager(BaseUserManager):
	'''
	    The default user for the project is the JobSeeker
		creates a user with the specified email and password
	  '''
	def create_user(self,email,password=None,):
		if self.filter(email__iexact=email).count() > 0:
			raise ValidationError('user with this email address already exists')
		user = self.model(email=self.normalize_email(email))
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,password=None):
		'''
		Creates a superuser with a specified username and password
		'''
		user = self.create_user(email=email,password=password)
		user.is_superuser=True
		user.is_admin = True
		user.is_active = True
		user.is_staff = True
		user.save(using=self._db)
		return user
  
	def create_applicant(self,applicant,work_experience,referees,education,*args,**kwargs):
		
		applicant = self.create(
			email=applicant['email'],
			id_number=applicant['id_number'],
			sir_name=applicant['sir_name'],
			other_name=applicant['other_name'],
			phone_no=applicant['phone_no'],
			date_of_birth=applicant['date_of_birth'],
			gender = applicant['gender'],
			home_city = applicant['home_city'],
			user_photo= applicant['user_photo'],
			about_applicant = applicant['about_applicant'],
			)

		
		for education_item in education:
	
			Education.objects.create(
				applicant = applicant,
				institution_name = education_item['institution_name'],
				course_name = education_item['course_name'],
				start_date = education_item['start_date'],
				completion_date = education_item['completion_date'],
				grade_attained = education_item['grade'],
				qualification = education_item['award'],


				)
	
		for wkr_experience in work_experience:
			
			Experience.objects.create(
				applicant = applicant,
				name_of_org = wkr_experience['name_of_org'],
				position = wkr_experience['jobtitle'],
				tasks = wkr_experience['tasks'],
				date_employed = wkr_experience['date_employed'],
				date_completed = wkr_experience['date_completed'],

				)

		for referee_item in referees:

			Referees.objects.create(
				applicant = applicant,
				ref_name = referee_item['ref_name'],
				ref_phone = referee_item['ref_phone'],
				ref_email = referee_item['ref_email'],
				ref_occupation = referee_item['ref_occupation'],

				)	

		return applicant


class JobSeeker(AbstractBaseUser,PermissionsMixin):
	"""
	Represents information on a JobSeeker
	"""

	GENDER = (
		('Male','male'),
		('Female','female')
	)

	#Personal Details
		#Personal Details
	email = models.EmailField(unique=True,max_length=50)
	id_number = models.IntegerField(null=True, blank=True)
	sir_name = models.CharField(max_length=250,null=True, blank=True)
	other_name = models.CharField(max_length=250,null=True, blank=True)
	phone_no = models.CharField(max_length=10,null=True, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=20,choices=GENDER,null=True, blank=True)
	home_city = models.CharField(max_length=250,null=True, blank=True)
	user_photo = models.ImageField(upload_to='uploads/ids',null=True, blank=True)
	about_applicant = models.TextField(null=True,blank=True)

	#Permissionssir_name
	is_active=models.BooleanField(default=False)
	is_staff=models.BooleanField(default=False)
	is_admin=models.BooleanField(default=False)


	#Date_Created
	created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated_on = models.DateTimeField(auto_now=True,auto_now_add=False)

	USERNAME_FIELD = 'email'
	objects = JobSeekerUserManager()

	def passport(self):
		return """<a href="/static/media/%s"><img border="0" alt="" src="/static/media/%s" height="40" /></a>""" % ((self.user_photo.name, self.user_photo.name))
	passport.allow_tags = True

	def get_short_name(self):
		return self.sir_name

	def get_full_name(self):
		return '{0} | {1}'.format(self.sir_name,self.other_name)


	def get_absolute_url(self):
		return reverse('singleApplicant',kwargs={"id": self.id})

	def __str__(self):
		return  self.email

	@property
	def age(self):
		"""
		 Calculates the age of a person if the
		 date of birth has been provided
		 Returns number of years
		"""
		if self.date_of_birth:
			return  (datetime.now().date() - self.date_of_birth ).days//365
	@property
	def work_experience(self):
		"""
		 calculates the years of experience of a
		 candidate if they had been previously employed
		 returns number of years
		"""
		for item in self.experience_set.all():#backwards relation
			if item.date_employed and item.date_completed:
				return (item.date_completed - item.date_employed).days //365
			return (datetime.now().date() - item.date_employed).days // 365	

	@property
	def jobtitle(self):
		for item in self.experience_set.all():
			if item.position:
				return item.position		

	@property
	def education(self):
		return self.education_set.all()

	@property
	def experiences(self):
		return self.experience_set.all()	
	
	@property
	def referees(self):
		return self.referees_set.all()	

class Education(models.Model):
	#Qualification statuses
	AWARDS = (
		('Professional','Professional'),
		('Degree','Degree'),
		('Diploma','Diploma'),
        ('Certificate','Certificate'),
		('O-level','O-level'),
	)

	applicant =models.ForeignKey(JobSeeker)
	#Education Background
	institution_name = models.CharField(max_length=250,null=True, blank=True)
	course_name = models.CharField(max_length=250,null=True, blank=True)
	start_date = models.DateField(null=True, blank=True)
	completion_date = models.DateField(null=True, blank=True)
	grade_attained = models.CharField(max_length=250,null=True, blank=True)
	qualification = models.CharField(max_length=20,choices=AWARDS,null=True, blank=True)

	#Date_Created
	created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated_on = models.DateTimeField(auto_now=True,auto_now_add=False)

	def fullname(self):
		return self.applicant.sir_name + " " + self.applicant.other_name


class Experience(models.Model):

	#Experience/Practical Training
	applicant =models.ForeignKey(JobSeeker)
	name_of_org = models.CharField(max_length=250,null=True, blank=True)
	position = models.CharField(max_length=250,null=True, blank=True)
	tasks = models.TextField(null=True, blank=True)
	date_employed = models.DateField(null=True, blank=True)
	date_completed = models.DateField(null=True, blank=True)

	#Date_Created
	created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated_on = models.DateTimeField(auto_now=True,auto_now_add=False)

	def fullname(self):
		return self.applicant.sir_name + " " + self.applicant.other_name



class Referees(models.Model):

	applicant =models.ForeignKey(JobSeeker)
	ref_name = models.CharField(max_length=250,null=True, blank=True)
	ref_phone = models.IntegerField(null=True, blank=True)
	ref_email = models.EmailField(max_length=50,null=True, blank=True)
	ref_occupation = models.CharField(max_length=250,null=True, blank=True)

	created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated_on = models.DateTimeField(auto_now=True,auto_now_add=False)

	def fullname(self):
		return self.applicant.sir_name + " " + self.applicant.other_name
