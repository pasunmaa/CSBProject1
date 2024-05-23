from django import forms
from .models import TransactionModel
 
 
# creating a form
class TransactionForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = TransactionModel
 
        # specify fields to be used
        fields = [
            "owner",
            "transaction_id",
            "transaction_date",
            "broker",
            "ticker",
            "transaction_type",
            "amount",
            "price",
            "fee",
            "note",
        ]