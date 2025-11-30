from django import forms
from .models import Borrow


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['book', 'due_date']