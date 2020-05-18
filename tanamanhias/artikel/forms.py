from django import forms

from .models import PostModel

class PostForm(forms.ModelForm):
	class Meta:
		model = PostModel
		fields = [
			'author',
			'judul',
			'body',
		]

		labels = {
			'author':'Penulis'
		}

		widgets = {
			'judul': forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder':'masukan judul postingan',}
				),

			'author': forms.TextInput(
				attrs = {
					'class':'form-control',
					'placeholder':'masukan nama penulis',}
				),


			'body': forms.Textarea(
				attrs = {
					'class':'form-control',}
				),

		}




