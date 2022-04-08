"""final_year_project_django URL Configuration

The `urlpatterns` list routes URLs to templates. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function templates
    1. Add an import:  from my_app import templates
    2. Add a URL to urlpatterns:  path('', templates.home, name='home')
Class-based templates
    1. Add an import:  from other_app.templates import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from .views import index, search_results, refresh_summary

urlpatterns = [
    path('', index, name='index'),
    path('search/', search_results,name='search'),
    path('api/refresh_summary', refresh_summary,name='refresh_summary'),
    path('search_page/', index, name='index'),
    path('admin/', admin.site.urls),
]
