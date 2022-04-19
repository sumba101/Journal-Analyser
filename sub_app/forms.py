from django import forms

class QuestionsForm( forms.Form ):
    def __init__(self, *args, **kwargs):
        self.count = kwargs.pop( 'count' )
        self.qs= kwargs.pop('questions')
        self.egs=kwargs.pop('examples')
        self.topic=kwargs.pop('focus_word')
        super(QuestionsForm, self).__init__(*args, **kwargs)
        for i in range(self.count):
            self.fields['{}) What is your answer for the section: {} under the topic {}' .format(i+1,self.qs[i],self.topic)] = forms.CharField()
            self.fields['{}) What is your answer for the section: {} under the topic {}'.format( i+1,self.qs[i], self.topic )].help_text = "This is an example paragraph for the same section from a different topic <br/> <br/>"+self.egs[i]



class TextInput(forms.Form):
    focus_word= forms.CharField()