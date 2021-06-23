from comment.models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','rate']
    def __init__(self,*args,**kwargs):
        super(CommentForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={'class':'form-control'}
        self.fields['comment'].widget.attrs['rows'] = 5
        self.fields['comment'].label = 'Yorum'
        self.fields['rate'].label = 'Puan'