from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os


AT = Airtable(os.environ.get("AIRTABLE_MOVIESTABLE_BASE_ID"),
              "Movies",
              api_key=os.environ.get("AIRTABLE_API_KEY"),)


def home_page(request):
    user_query = str(request.GET.get("query", ""))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {"search_result": search_result}

    return render(request, "movies/movies_stuff.html", stuff_for_frontend)


def create(request):

    if request.method == "POST":
        data = {
            'Name': request.POST.get("name"),
            'Pictures': [{'url': request.POST.get("url")}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
        }

        if data['Pictures'][0]['url'] == '':
            data['Pictures'][0]['url'] = 'https://www.josco.com.au/wp-content/uploads/2016/05/Image-Unavailable.jpg'

        try:
            response = AT.insert(data)
            messages.success(request, 'New Movie Added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Encounter An Error While Creating The Movie: {}'.format(e))

        return redirect("/")


def edit(request, movie_id):
    if request.method == "POST":
        data = {
            'Name': request.POST.get("name"),
            'Pictures': [{'url': request.POST.get("url") or 'https://www.josco.com.au/wp-content/uploads/2016/05/Image-Unavailable.jpg' }],
            'Rating': int(request.POST.get("rating")),
            'Notes': request.POST.get("notes"),
        }

        try:
            response = AT.update(movie_id, data)
            messages.success(request, 'Movie Edited: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Encounter An Error While Editing The Movie: {}'.format(e))

        return redirect("/")


def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields']['Name']
        response = AT.delete(movie_id)
        messages.warning(request, 'Movie Deleted: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'Encounter An Error While Deleting The Movie: {}'.format(e))



    return redirect("/")



