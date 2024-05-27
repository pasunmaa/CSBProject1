import datetime
from django import forms
from .models import TransactionModel
from django.contrib.auth.models import User
 
 
# creating a form
class TransactionForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = TransactionModel
 
        # specify fields to be used
        fields = [
            #"owner",
            #"transaction_id",
            "id",
            "transaction_date",
            "broker",
            "ticker",
            "transaction_type",
            "amount",
            "price",
            "fee",
            "note",
        ]

        # set default values
        #broker = forms.ChoiceField(label="Broker", choices=TransactionModel.BROKERS.items(), initial=1),

        widgets = {
            'id': forms.TextInput(attrs={'readonly': True}),
            'transaction_date': forms.DateInput(attrs={'value': datetime.date.today()}), #.strftime('%Y-%m-%d')}),
            #'broker': forms.ChoiceField(label="Broker", choices=TransactionModel.BROKERS.items(), initial=1),
            'amount': forms.NumberInput(attrs={'value': 100}),
            'fee': forms.TextInput(attrs={'value': 5.0}),
            'note': forms.TextInput(attrs={'required':False, 'value': ''}),
        }

        def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None)
            super(TransactionModel, self).__init__(*args, **kwargs)
            if self.request:
                self.fields['owner'].initial = self.request.user
                self.fields['broker'].initial = TransactionModel.BROKERS[1]
            #self.fields['owner'].queryset = User.objects.filter(pk=self.request.user.pk)
            print(f"TransactionForm init: {self.request.user}")