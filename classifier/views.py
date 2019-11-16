from django.shortcuts import render
from django.http import HttpResponse
import pickle
import os
from .models import sub
from django.shortcuts import redirect
from .NEW_HS_CLASSIFIER import Feature_model

class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'Feature_model':
            return Feature_model
        return super().find_class(module, name)



filename = os.path.join(os.path.dirname(__file__), 'static', 'classifier', 'classifier.pickle')

model = CustomUnpickler(open(filename, 'rb')).load()

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
        prediction = model.predict(enter_text)
    context = {'enter_text':enter_text, 'prediction': prediction}
    return render(request, 'classifier/predict_temp.html', context)

def submit(request):
    try:
        enter_text = request.POST['sentence']
        enter_label = request.POST['class']
        s = sub(content=enter_text, label=enter_label)
        s.save()
        model.fit(filename)
        return redirect('success')
    except KeyError:
        pass
    return render(request, 'classifier/submit_temp.html')

def success(request):
    return render(request, 'classifier/success.html')
