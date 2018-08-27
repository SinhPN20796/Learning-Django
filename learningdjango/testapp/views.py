# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse , reverse_lazy
from django.views.generic.base import View
from django.shortcuts import render
from .models import Choice, Question
from django.utils import timezone
from django.template.context_processors import request
from django.views.generic.edit import FormView, FormMixin, DeleteView
from testapp.forms import QuestionForm, ChoiceForm
import datetime
from test.test_typechecks import Integer
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages.api import success
from django.db.models.base import Model
from django.http.response import HttpResponseNotFound, HttpResponse


class IndexView(generic.ListView):
    template_name = 'testapp/index.html'
    context_object_name = 'latest_question_list'
    form_class = QuestionForm

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now())
    
    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'testapp/detail.html'   
    
    def get_context_data(self, **kwargs):
        context =  generic.DetailView.get_context_data(self, **kwargs)
        return context
    def get_object(self, queryset=None):
        return get_object_or_404(Question, pk=self.kwargs['question_id'])
    
    def post(self, request, *args, **kwargs):
        form = ChoiceForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'testapp/results.html'
    
    
 
class VoteView(View):
    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'testapp/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()

        return HttpResponseRedirect(reverse('testapp:results', args=(question.id,)))
    
    

class AddQuestionView(FormView):
    template_name = 'testapp/add-question.html'
    form_class = QuestionForm
    
    def form_invalid(self, form):
        return FormView.form_invalid(self, form)
    
    def form_valid(self, form):
        obj = form.save(False)
        obj.pub_date = datetime.datetime.now()
        obj.save()
        return FormView.form_valid(self, form)
    
    def get_success_url(self):
        return reverse('testapp:index')

class AddChoiceView(FormView):
    template_name = 'testapp/add-choice.html'
    form_class = ChoiceForm
    
    def form_invalid(self, form):
        return FormView.form_invalid(self, form)
    
    def form_valid(self , form):
        obj = form.save(False)
        obj.question_id = self.kwargs['question_id']
        obj.save()
        
        return FormView.form_valid(self, form)
    
    def get_success_url(self):
        return reverse('testapp:detail', kwargs={'question_id' : self.kwargs['question_id']})
        
class DeleteQuestion(DeleteView):
    model = Question
    success_url = reverse_lazy('latest_question_list')
    success_message = "Deleted Successfully"
    
    def delete(self, request, question_id):
         query = get_object_or_404(Question, pk=question_id)
         query.delete()
         return HttpResponse("Deleted!")
        
        
    
    