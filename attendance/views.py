from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.list import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from .forms import AttendeeListSearchForm, NewRecordForm
from .models import Entry
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.core import serializers
from django.db.models import Q, F


# Create your views here.

class AttendeeList(ListView, FormView):
    model = Entry
    template_name = 'attendance/entry_list.html'
    form_class = AttendeeListSearchForm

    def get(self, request):
        entries = Entry.objects.all().order_by('-day')
        return render(request, self.template_name, {'form': self.form_class, 'entries': entries})

    def searchRecord(request):
        search = request.GET.get('search' or None)
        user = request.GET.get('user' or None)
        start_day = request.GET.get('start_day' or None)
        end_day = request.GET.get('end_day' or None)

        entries = Entry.objects

        if user:
            entries = entries.filter(user=user)
        if start_day:
            entries = entries.filter(day__gte=start_day)
        if end_day:
            entries = entries.filter(day__lte=end_day)
        if search:
            entries = entries.filter(note__contains=search).values()
        if not search and not user and not start_day and not end_day:
            entries = entries.all()
        entries = entries.order_by('-day')
        list_result = list(entries.values('id','user', 'user__username', 'note', 'day', 'working_hours'))
        return JsonResponse(list_result, safe=False)


class LoginPage(View):

    def get(self, request):
        template_name = 'attendance/login.html'
        return render(request, template_name=template_name)

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                context = {'message': 'Inactive User'}
                return render(request, "attendance/login.html", context)
        else:
            context = {'message': 'Not a user'}
            return render(request, "attendance/login.html", context)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return render(request, "attendance/login.html")


class IndexView(View):

    def get(self, request):
        template_name = 'attendance/index.html'
        return render(request, template_name=template_name)


class NewRecordView(FormView):

    model = Entry
    template_name = 'attendance/new_record.html'
    form_class = NewRecordForm
    success_url = '/'

    def getForm(request):
        day = int(request.GET.get('day' or None))
        form = NewRecordForm
        new_date = datetime.today() + timedelta(days=day);
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return JsonResponse({
            'success': True, 
            'form': form_html,
            'today': datetime.today().strftime('%Y-%m-%d'),
            'date': new_date.strftime('%Y-%m-%d'),
            'full_today':datetime.today(),
            'full_date': new_date})

    def saveRecord(request):
        if request.method == 'POST':
            form = NewRecordForm(request.POST)
            if form.is_valid():
                day = request.POST['day']
                record=Entry.objects.filter(day=day, user=request.user)
                if record.count()>0:
                    return JsonResponse({'error': 'true', 'message': 'You have already entered a record for this day'})
                else:
                    entry = form.save(commit=False)
                    entry.user = request.user
                    entry.save()
                    return JsonResponse({'success': 'true', 'entry_id': entry.id, 'user': entry.user.id})

            return JsonResponse({'success': False})

    def updateRecord(request):
        if request.method == 'POST':
            entry_id = request.POST['entry_id']
            entry = Entry.objects.get(id=entry_id)
            day = request.POST['day']
            user = request.POST['user']
            record=Entry.objects.filter(day=day, user=user).count()
            if record>0:
                return JsonResponse({'error': 'true', 'message': 'You have already entered a record for this day'})
            else:
                form = NewRecordForm(request.POST, instance=entry)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success': 'true'})
            return JsonResponse({'success': False})

    def deleteRecord(request):
        if request.method == 'POST':
            entry_id = request.POST['entry_id']
            entry = Entry.objects.get(id=entry_id)
            entry.delete()
            return JsonResponse({'success': 'true'})


    def get(self, request):
        form = NewRecordForm
        return render(request, self.template_name, {'form': form})

    