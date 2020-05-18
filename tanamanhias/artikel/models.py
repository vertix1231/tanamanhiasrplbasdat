from django.db import models
from django.utils.text import slugify

# Create your models here.

class PostModel(models.Model):
	judul		= models.CharField(max_length=255)
	body		= models.TextField()
	publish		= models.DateTimeField(auto_now_add = True)
	slug		= models.SlugField(blank=True, editable = False)
	author		= models.CharField(max_length = 100)

	def save(self):
		self.slug = slugify(self.judul)
		super(PostModel, self).save()

	def __str__(self):
		return "{}. {}".format(self.id,self.judul)