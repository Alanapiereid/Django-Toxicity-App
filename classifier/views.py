from django.shortcuts import render
from django.http import HttpResponse
import pickle
import os
from .models import sub
from django.shortcuts import redirect

filename = os.path.join(os.path.dirname(__file__), 'static', 'classifier', 'classifier.pickle')

model = pickle.load(open(filename, mode='rb'))

def home(request):
    return render(request, 'classifier/home_temp.html')

def predict(request):#, enter_text=''):
    try:
        enter_text = request.POST['your_text']
    except KeyError:
        enter_text = ''
    if enter_text == '':
        prediction = ''
    else:
        prediction = model.predict([enter_text])[0]
    context = {'enter_text':enter_text, 'prediction': prediction}
    return render(request, 'classifier/predict_temp.html', context)

def submit(request):
    try:
        enter_text = request.POST['sentence']
        enter_label = request.POST['class']
        s = sub(content=enter_text, label=enter_label)
        s.save()
        return redirect('success')
    except KeyError:
        pass
    return render(request, 'classifier/submit_temp.html')

def success(request):
    return render(request, 'classifier/success.html')
