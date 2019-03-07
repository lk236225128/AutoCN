"""autoCN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path

import xadmin

from autoApi.views import IndexView,RunCaseView,RunPageView,ReturnRateView,reportDetailView,addNotesView,failReportView,dashboardView,caseEditorView,failReasonView,caseListView,articleDetailView,articleListView
from users.views import loginView,logoutView

urlpatterns = [
    #path(route,view,name=None,kwargs=None)
    path('xadmin/', xadmin.site.urls),
    # path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name="index"),
    path('dashboard/', dashboardView.as_view(), name="dashboard"),
    path('runPage/',RunPageView.as_view(),name="runPage"),
    path('runCase/<department>',RunCaseView.as_view(),name="runCase"),
    path('returnRate/<department>',ReturnRateView.as_view(),name="returnRate"),
    path('reportDetail/<reportID>/',reportDetailView.as_view(),name="reportDetail"),
    path('login/',loginView.as_view(),name="login"),
    path('logout/',logoutView.as_view(),name="logout"),
    path('addNotes/<noteID>/',addNotesView.as_view(),name="addNotes"),
    path('failReport/<department>/<env>',failReportView.as_view(),name="failReport"),
    path('caseEditor/',caseEditorView.as_view(),name="caseEditor"),
    path('failReason/',failReasonView.as_view(),name="failReason"),
    path('caseList/',caseListView.as_view(),name="caseList"),
    path('articleDetail/<articleID>/',articleDetailView.as_view(),name="articleDetail"),
    path('articleList/',articleListView.as_view(),name="articleList")
]
