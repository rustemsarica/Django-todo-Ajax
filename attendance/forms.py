from cProfile import label
from datetime import datetime
from logging import PlaceHolder
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row, Button, Reset
from django import forms
from django.contrib.auth.models import User
from .models import Entry
from django.forms import modelformset_factory


class DateInput(forms.DateInput):
    input_type = 'date'


class AttendeeForm(forms.Form):

    username = forms.CharField()
    password = forms.PasswordInput()
    note = forms.CharField()
    date = forms.DateField()


class AttendeeListAdminSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_id = 'searchForm'
        self.helper.form_action = '/list'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Field('start_day', wrapper_class="col-lg-2 col-md-3", css_class="searcFormField"),
                Field('end_day', wrapper_class="col-lg-2 col-md-3", css_class="searcFormField"),
                Field('user', wrapper_class="col-md-3", css_class="multipleSelect form-control searcFormField"),
                Field('note', placeholder='Search in notes', wrapper_class="col-md-3", css_class="searcFormField"),
                Div(
                    Submit('search', 'Search', css_class="btn btn-primary"),
                    Button('reset', 'Reset', css_class="btn-outline-dark"),
                    css_class="col-lg-2 col-12"
                ),
            )
        )
    start_day = forms.DateField(widget=DateInput(), required=False)
    end_day = forms.DateField(widget=DateInput(), required=False)
    user = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    note = forms.CharField(max_length=100, required=False)

class AttendeeListSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'get'
        self.helper.form_id = 'searchForm'
        self.helper.form_action = '/list'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Field('start_day', wrapper_class="col-md-2"),
                Field('end_day', wrapper_class="col-md-2"),
                Field('note', placeholder='Search in notes', wrapper_class="col-md-3"),
                Div(
                    Submit('search', 'Search', css_class="btn btn-primary"),
                    Reset('reset', 'Reset', css_class="btn-outline-dark"),
                    css_class="col-md-2"
                ),
            )
        )

    start_day = forms.DateField(widget=DateInput(), required=False)
    end_day = forms.DateField(widget=DateInput(), required=False)
    note = forms.CharField(max_length=100, required=False)

class NewRecordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_id = 'new-record-form'
        self.helper.layout = Layout(
            Row(
                Field('day', wrapper_class="col-3"),
                InlineRadios('working_hours', wrapper_class="col-3"),
                Field('note', wrapper_class="col-4"),
                Div(
                    Button('button', 'Save', css_class="recordSaveBtn btn-primary"),
                    Reset('reset', 'Cancel', css_class="btn-outline-secondary"),
                    Button('removeRow', '-', css_class="removeRowBtn btn-outline-danger font-weight-bold"),
                    css_class="col-2 m-auto text-center"
                ),
                css_id='recordRow',
                css_class='recordRow'
            )
        )

    class Meta:
        model = Entry
        fields = ['day', 'working_hours', 'note']
        exclude = ['user']
        widgets = {
            'day': DateInput,
            'note': forms.Textarea(attrs={'rows': 1, 'cols': 40}),
            'user': forms.HiddenInput(),
            'working_hours': forms.RadioSelect(),
        }


class ModalForm(forms.ModelForm):
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = True
            self.helper.form_action = 'record/update'
            self.helper.form_id = 'modal-form'
            self.helper.layout = Layout(
                Row(
                    Field('day'),
                    InlineRadios('working_hours'),
                    Field('note'),
                    Div(
                        Button('button', 'Cancel', css_class="btn-outline-secondary", data_bs_dismiss="modal"),
                        Submit('submit', 'Save', css_class="recordSaveBtn btn-primary"),
                        css_class="modal-footer",
                    ),
                    css_id='recordRow',
                    css_class='recordRow'
                )
            )
    
        class Meta:
            model = Entry
            fields = ['day', 'working_hours', 'note']
            exclude = ['user']
            widgets = {
                'day': DateInput,
                'note': forms.Textarea(attrs={'rows': 1, 'cols': 40}),
                'user': forms.HiddenInput(),
                'working_hours': forms.RadioSelect(),
            }
