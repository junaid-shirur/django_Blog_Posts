from django.shortcuts import render

from django.http import HttpResponse



def projects(request):
    return render(request, 'projects/projects.html')


def single_project(request, pk):
    return render(request,'projects/single_project.html',{'primary_key':pk})