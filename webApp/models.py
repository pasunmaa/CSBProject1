# import the standard Django Model from built-in library
from django.db import models
from django.conf import settings
  
# declare a new model with a name "TransactionModel"
class TransactionModel(models.Model):
    # define choices options
    BROKERS = {
        1: 'Nordnet',
        2: 'Nordea',
        3: 'OP',
        4: 'Mandatum',
        5: 'Degiro',
        6: 'Danske Bank',
    }

    TRANSACTION_TYPES = {
        1: 'Buy',
        2: 'Sell',
        3: 'Dividend',
        4: 'Fee',
        5: 'Split',
    }
 
    # fields of the transaction model
    #title = models.CharField(max_length = 200)
    #description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    transaction_id = models.CharField(max_length = 50)
    transaction_date = models.DateField()
    broker = models.IntegerField(choices=BROKERS.items())
    ticker = models.CharField(max_length = 20)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPES.items())
    amount = models.IntegerField()
    price = models.FloatField()
    fee = models.FloatField()
    note = models.CharField(max_length = 100)
    
 
    # renames the instances of the model with their transaction_id
    def __str__(self):
        return self.transaction_id