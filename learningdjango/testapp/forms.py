from django import forms
from testapp.models import Question
from testapp.models import Choice


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)
        

    
    
    
