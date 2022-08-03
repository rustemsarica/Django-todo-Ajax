const addNewRecordRowBtn = document.getElementById('addNewRecordRowBtn');
let recordRowCount = document.getElementsByClassName('recordRow').length;
const newRowContainer = document.getElementById('newRowContainer');
let recordSaveBtn = document.getElementsByClassName('recordSaveBtn');
let removeRowBtn = document.getElementsByClassName('removeRowBtn')
const searchForm = document.getElementById('list_search_form');
const searchInput = document.getElementById('id_search');
const recordTable = document.getElementById('recordTable');

const saveEntry = function saveEntry(){
    let thisBtn = this
    let form = this.parentElement.parentElement.parentElement
    let inputs = form.getElementsByTagName('input')
    let textareas = form.getElementsByTagName('textarea')
    let data = {}
    for(let i = 0; i < inputs.length; i++){
        if(inputs[i].type == 'radio'){
            if(inputs[i].checked){
                data[inputs[i].name] = inputs[i].value
            }
        }else{
            data[inputs[i].name] = inputs[i].value;
        }
    }
    for(let i = 0; i < textareas.length; i++){
        data[textareas[i].name] = textareas[i].value
    }
    console.log(data)
    $.ajax({
        url: '/record/ajax/save',
        type: 'POST',
        data: data,
        success: function(data){
            if(data['success'] == 'true'){
                thisBtn.value = 'Update'
                //thisBtn.disabled = true
                thisBtn.classList.add('btn-success', 'recordUpdateBtn')
                thisBtn.classList.remove('btn-primary', 'recordSaveBtn')
                thisBtn.removeEventListener('click', saveEntry)
                thisBtn.addEventListener('click', updateEntry)
                let deleteBtn =  thisBtn.parentElement.children[1];
                deleteBtn.value='Delete'
                deleteBtn.type='button'
                deleteBtn.classList.add('btn-danger','deleteEntry')
                deleteBtn.classList.remove('btn-outline-secondary')
                let entry_id = data['entry_id']
                let user = data['user']
                var html = '<input type="hidden" name="entry_id" value="' + entry_id + '">'
                html += '<input type="hidden" name="user" value="' + user + '">'
                form.insertAdjacentHTML('afterbegin', html)
                deleteBtn.addEventListener('click', deleteEntry);
                send_alert('success', 'Record saved successfully');
            }else{
                if(data['error'] == 'true'){
                    send_alert('danger', data['message']);
                }else{
                    send_alert('danger', 'Error saving record');
                }
            }
        },
        error: function(data){
            send_alert('danger', data['message']);
        }
    })
}

const deleteEntry = function deleteEntry(){
    let thisBtn = this
    let form = thisBtn.parentElement.parentElement.parentElement
    let data = {}
    let inputs = form.getElementsByTagName('input')
    for(let i = 0; i < inputs.length; i++){
        data[inputs[i].name] = inputs[i].value
    }
    $.ajax({
        url: '/record/ajax/delete',
        type: 'POST',
        data: data,
        success: function(data){
            if(data['success'] == 'true'){
                thisBtn.parentElement.parentElement.parentElement.remove()
                recordRowCount = document.getElementsByClassName('recordRow').length;
                send_alert('success', 'Record deleted successfully');
            }else{
                send_alert('danger', 'Error deleting record');
            }
        },
        error: function(data){
            send_alert('danger', 'Error deleting record');
        }
    })
}

const updateEntry = function updateEntry(){
    let thisBtn = this
    let form = thisBtn.parentElement.parentElement.parentElement
    let data = {}
    let inputs = form.getElementsByTagName('input')
    let textareas = form.getElementsByTagName('textarea')
    for(let i = 0; i < inputs.length; i++){
        data[inputs[i].name] = inputs[i].value
    }
    for(let i = 0; i < textareas.length; i++){
        data[textareas[i].name] = textareas[i].value
    }
    $.ajax({
        url: '/record/ajax/update',
        type: 'POST',
        data: data,
        success: function(data){
            if(data['success'] == 'true'){
                send_alert('success', 'Record updated successfully');
            }else{
                if(data['error'] == 'true'){
                    send_alert('danger', data['message']);
                }else{
                    send_alert('danger', 'Error updating record');
                }
            }
        },
        error: function(data){
            send_alert('danger', 'Error updating record');
        }
    })
}

if(addNewRecordRowBtn){
    addNewRecordRowBtn.addEventListener('click',function(){
       $.ajax({
            url: '/record/ajax/add-record-row',
            type: 'GET',
            data: {
                day: recordRowCount
            },
            success: function(data){
                recordRowCount++
                let text = 'id_'+recordRowCount;
                let form = data['form'];
                form=form.replaceAll('id_', text);
                if(recordRowCount > 1){ 
                    form = form.replaceAll(data['today'], data['date']);
                    form = form.replaceAll(data['full_today'], data['full_date']);
                }

                newRowContainer.insertAdjacentHTML('afterend', form);

                for(let i = 0; i < recordSaveBtn.length; i++){
                    recordSaveBtn[i].addEventListener('click', saveEntry)
                }
                for(let i = 0; i < removeRowBtn.length; i++){
                    removeRowBtn[i].addEventListener('click', removeRow)
                }
            }   
        })
    });
}

if(recordSaveBtn){
    for(let i = 0; i < recordSaveBtn.length; i++){
        recordSaveBtn[i].addEventListener('click', saveEntry)
    }
}

function send_alert(type, message){
    let alert = document.getElementById('alert')
    alert.classList.add('alert-'+type);
    alert.innerHTML = message
    alert.style.display = 'block'
    setTimeout(function(){
        alert.style.display = 'none';
        alert.classList.remove('alert-'+type);
    }
    , 3000)
}

$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
});

const removeRow = function removeRow(){
    let thisBtn = this
    let row = thisBtn.parentElement.parentElement
    row.remove()
    recordRowCount = document.getElementsByClassName('recordRow').length;
}

const searchRecords = function searchRecords(){
    let inputs = searchForm.getElementsByTagName('input')
    let selects = searchForm.getElementsByTagName('select')
    let data = {}

    for(let i = 0; i < inputs.length; i++){
        data[inputs[i].name] = inputs[i].value
    }
    for(let i = 0; i < selects.length; i++){
        data[selects[i].name] = selects[i].value
    }
            
    $.ajax({
        url: '/list/ajax/search',
        type: 'GET',
        data: data,
        dataType: 'json',
        success: function(data){
            let html = ''
            for(let i = 0; i < data.length; i++){
                html += '<tr>'
                html += '<td>'+data[i].user__username+'</td>'
                html += '<td>'+data[i].day+'</td>'
                html += '<td>'+data[i].working_hours+'</td>'
                html += '<td>'+data[i].note+'</td>'
                html += '<td></td>'
                html += '</tr>'
            }
            recordTable.innerHTML = html
        }
    })
}
    

$(document).ready(function(){

    if(searchForm){
        searchInput.addEventListener('keyup', searchRecords)
        searchForm.addEventListener('submit', searchRecords)
        searchForm.addEventListener('reset', searchRecords)
        searchForm.addEventListener('change', searchRecords)
        searchRecords();
    }

    $('input[name="removeRow"]').each(function(){
        $(this).click(removeRow)
    });
});