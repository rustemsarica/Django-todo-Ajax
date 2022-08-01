from django.urls import path
from .views import AttendeeList
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from .views import LoginPage, LogoutView, IndexView, NewRecordView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list', AttendeeList.as_view(), name='list'),
    path('login/', LoginPage.as_view(), name='login'),
    path('user/logout', LogoutView.as_view(), name='logout'),
    path('record/add', NewRecordView.as_view(), name='newRecord'),
    path('record/ajax/add-record-row', NewRecordView.getForm, name='addRecordRow'),
    path('record/ajax/save', NewRecordView.saveRecord, name='saveRecord'),
    path('record/ajax/delete', NewRecordView.deleteRecord, name='deleteRecord'),
    path('record/ajax/update', NewRecordView.updateRecord, name='updateRecord'),
    path('list/ajax/search', AttendeeList.searchRecord, name='searchRecord'),

]
