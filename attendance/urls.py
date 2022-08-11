from django.urls import path
from .views import AttendeeList
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from .views import LoginPage, LogoutView, IndexView, NewRecordView, getUpdateForm


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list', AttendeeList.as_view(), name='list'),
    path('login/', LoginPage.as_view(), name='login'),
    path('user/logout', LogoutView.as_view(), name='logout'),
    path('record/add', NewRecordView.as_view(), name='newRecord'),
    path('record/update', NewRecordView.update, name='updateRecord'),
    path('record/delete', NewRecordView.delete, name='deleteRecord'),
    path('record/ajax/add-record-row', NewRecordView.getForm, name='get_form'),
    path('record/ajax/save', NewRecordView.saveRecord),
    path('record/ajax/delete', NewRecordView.deleteRecord),
    path('record/ajax/update', NewRecordView.updateRecord),
    path('list/ajax/search', AttendeeList.searchRecord),
    path('record/ajax/update-form', getUpdateForm),

]
