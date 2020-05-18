from django.shortcuts import render, redirect

# Create your views here.
from .forms import PostForm
from .models import PostModel

# menampilkam semua artikel 
def allPost(request):
     # queryset
     posts = PostModel.objects.all();
     context = {
          'title':'Orplant Artikel',
          'Posts':posts,
     }
     return render(request,'artikel/index.html', context)

# detail artikel
def detailPost(request,slugInput):
     posts = PostModel.objects.get(slug=slugInput);
     context = {
          'title':'Orplant',
          'Posts':posts,
     }

     return render(request,'artikel/detail.html',context)

# membuat artikel
def createPost(request):
     post_form = PostForm(request.POST or None)

     if request.method == 'POST': 
          if post_form.is_valid():
               post_form.save()

               return redirect('artikel:allpost')

     context = {
          'title':'Orplant c',
          'page_title':'Membuat Artikel',
          'post_form':post_form,
     }

     return render(request,'artikel/create.html',context)

# menghapus artikel
def deletePost(request, SlugInput):
     PostModel.objects.filter(slug=slugInput).delete()
     return redirect('artikel:allpost')
