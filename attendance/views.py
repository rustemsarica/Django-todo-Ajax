from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.list import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from .forms import AttendeeListSearchForm, AttendeeListAdminSearchForm, NewRecordForm, ModalForm
from .models import Entry
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib import messages

# Create your views here.

class AttendeeList(ListView, FormView):
    model = Entry
    template_name = 'attendance/entry_list.html'
    form_class = AttendeeListSearchForm

    def get(self, request):
        start_day = request.GET.get('start_day' or None)
        end_day = request.GET.get('end_day' or None)
        user = request.GET.getlist('user' or None)
        note = request.GET.get('note' or None)
        
        entries = Entry.objects.filter(deleted=False)
        if request.user.is_superuser:
            form = AttendeeListAdminSearchForm(request.GET)
            if user:
                entries = entries.filter(user__in=user)
        else:
            form = AttendeeListSearchForm(request.GET)
            entries = entries.filter(user=request.user)

        if start_day:
            entries = entries.filter(day__gte=start_day)
        if end_day:
            entries = entries.filter(day__lte=end_day)
        if note:
            entries = entries.filter(note__contains=note)
        
        entries = entries.order_by('-day')
        return render(request, self.template_name, {'form':form, 'entries': entries})

    def searchRecord(request):
        search = request.GET.get('search' or None)
        user = request.GET.get('user' or None)
        start_day = request.GET.get('start_day' or None)
        end_day = request.GET.get('end_day' or None)

        entries = Entry.objects.filter(deleted=False)

        if user:
            entries = entries.filter(user=user)
        if start_day:
            entries = entries.filter(day__gte=start_day)
        if end_day:
            entries = entries.filter(day__lte=end_day)
        if search:
            entries = entries.filter(note__contains=search)
        if not search and not user and not start_day and not end_day:
            entries = entries.all()
        entries = entries.order_by('-day')
        return render(request, 'attendance/entry_list.html', {'form': AttendeeListSearchForm(instance=request.GET), 'entries': entries})
        #list_result = list(entries.values('id','user', 'user__username', 'note', 'day', 'working_hours'))
        #return JsonResponse(list_result, safe=False)


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
                record=Entry.objects.filter(day=day, user=request.user, deleted=False)
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
            record=Entry.objects.filter(day=day, user=user, deleted=False).count()
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

    def update(request):
        entry = Entry.objects.get(id=request.POST['entry_id'])
        if str(entry.day) == str(request.POST['day']):
            form = NewRecordForm(request.POST, instance=entry)
            form.user = request.user
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Record updated successfully')
            else:
                messages.add_message(request, messages.ERROR, 'Form is not valid')
        else:
            record=Entry.objects.filter(day=request.POST['day'], user=request.user, deleted=False).count()
            if record>0:
                messages.add_message(request, messages.ERROR, 'You have already entered a record for this day')
            else:
                form = NewRecordForm(request.POST, instance=entry)
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'Record updated successfully')
                else:
                    messages.add_message(request, messages.ERROR, 'Form is not valid')
        return HttpResponseRedirect('/list')
    
    def delete(request):
        entry = Entry.objects.get(id=request.POST['entry_id'])
        if entry:
            entry.deleted = True
            entry.save()
            messages.add_message(request, messages.SUCCESS, 'Record deleted successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Entry not found')
        return HttpResponseRedirect('/list')

def getUpdateForm(request):
    if request.method == 'POST':
        entry_id = request.POST['entry_id']
        entry = Entry.objects.get(id=entry_id)
        form = ModalForm(instance=entry)
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return JsonResponse({'form': form_html})


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
    