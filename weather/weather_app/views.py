from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=844c7cddd0fdd6733dde4d44172956f4"
    err_msg =''
    message =''
    msg_class = ''
    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()

                else:
                    err_msg = 'City does not exists!'
            else:
                err_msg = "City already present in database!"
        if err_msg:
            message = err_msg
            msg_class = 'is-danger'

        else:
            message = "City added successfully!"
            msg_class ='is-success'

    form = CityForm()

    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.name,
            'temprature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context  = {'weather_data':weather_data,
                'form':form,
                'message':message,
                'msg_class':msg_class}
    return render(request, 'weather_app/home.html', context)


def delete_city(request, city_name):

    City.objects.get(name=city_name).delete()
    return redirect('home')