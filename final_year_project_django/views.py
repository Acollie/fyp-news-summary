import json

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .forms import SearchInput
from .ingestion import text_aggrogation_object, get_t5_summary, gpt_3_summary, gpt_3_summary_regenerate, \
    text_aggrogation_binning
from .search import find_similar_by_word_to_vec, find_similar_by_model_transformer


def index(request):

    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def search_results(request):
    if request.method == "POST":
        forms = json.load(request)
        if forms['data']['search_string'] != '' and forms['data']['search_string'] != ' ':
            search_results = find_similar_by_model_transformer(forms['data']['search_string'])
            summary = gpt_3_summary(text_aggrogation_object(search_results))
            # summary = gpt_3_summary(text_aggrogation_binning(search_results),use_bin=True)

            return JsonResponse({
                'status': True,
                'search_response': search_results,
                'summary_response': summary
                })
        else:
            return JsonResponse({'status': 'invalid_form'})
    else:

        template = loader.get_template('search_page.html')
        context = {
        }
        return HttpResponse(template.render(context, request))
@csrf_exempt
def refresh_summary(request):
    if request.method == "POST":
        forms = json.load(request)
        binning = forms['data']['binning']
        temperature = float(forms['data']['temperature'])
        if bool(binning):
            text_response = gpt_3_summary_regenerate(forms['data']['summary_items'], temperature=temperature,
                                                     use_bucket=True)
            return JsonResponse({
                'status': True,
                'summary_response': text_response
                })

        else:

            text_response = gpt_3_summary_regenerate(forms['data']['summary_items'], temperature=temperature,
                                                     use_bucket=False)
            return JsonResponse({
                'status': True,
                'summary_response': text_response
                })


def settings(request):

    template = loader.get_template('settings.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
