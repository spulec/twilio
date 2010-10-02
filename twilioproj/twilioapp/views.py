from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from twilioproj.twilioapp.models import TwilioNumber, TwilioVerb, Response
from twilioproj.twilioapp.forms import TwilioNumberForm, ResponseForm, FormUtilities

def index_number(request):
    numbers = TwilioNumber.objects.all()
    return render_to_response('twilioapp/index_number.html', {
                'numbers': numbers,
            })

def create_number(request):
    if request.method == "POST":
        form = TwilioNumberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('twilioproj.twilioapp.views.index_number'))
    else:
        form = TwilioNumberForm()

    return render_to_response('twilioapp/create_number.html', {
                'form': form,
            })

def edit_number(request, phone_number):
    if request.method == "POST":
        form = TwilioNumberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('twilioproj.twilioapp.views.index_number'))
    else:
        number = get_object_or_404(TwilioNumber, phone_number=phone_number)
        form = TwilioNumberForm(instance=number)
    
    return render_to_response('twilioapp/edit_number.html', {
                'form': form,
            })


def index_response(request):
    responses = Response.objects.all()
    return render_to_response('twilioapp/index_response.html', {
                'responses': responses,
            })

def create_response(request):
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect(reverse('twilioproj.twilioapp.views.edit_response', 
                args=[str(response.name)]))
    else:
        form = ResponseForm()
    
    return render_to_response('twilioapp/create_response.html', {
                'form': form,
            })

def view_response(request, response_name):
    response = get_object_or_404(Response, name=response_name)
    xml = response.to_xml()
    return HttpResponse(str(xml))

def edit_response(request, response_name):
    response = get_object_or_404(Response, name=response_name)
    verbs = TwilioVerb.objects.filter(response=response).select_related().order_by('order')    
    verb_forms = []
    
    for verb in verbs:
        verb_forms.append(FormUtilities.get_form(verb))

    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ResponseForm(instance=response)
    
    return render_to_response('twilioapp/edit_response.html', {
                'form': form,
                'response': response,
                'verb_forms': verb_forms,
            })

