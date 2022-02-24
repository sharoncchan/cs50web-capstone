from django import forms
from .models import Comment
from mptt.forms import TreeNodeChoiceField

class NewCommentForm(forms.ModelForm):

    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hide the parent field 
        self.fields['parent'].widget.attrs.update(
            {'class': "d-none"})

        # Remove the label from the parent field

        self.fields['parent'].label =""

        # Remove the required from the parent field
        self.fields['parent'].required = False

    
        
        # Remove the label from the content field
        self.fields['content'].label = ""



    class Meta:
        model = Comment
        fields = ('parent','content',)
        widgets ={
            "content": forms.Textarea(attrs={
                "class" : "form-control", 
                "placeholder":"Add to the discussion",
                "rows": 4})
        }