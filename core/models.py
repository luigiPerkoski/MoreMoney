from django.db import models

#! Modelos do meu banco de dados aqui

class Account(models.Model): #* Modelo para as contas do banco 

    type_list = (
        ('CC', 'Conta Corrente'),
        ('DI', 'Dinheiro'), 
        ('CA', 'Cartao'), 
        ('IN', 'Investimento')
    )
        
    name = models.CharField(max_length=50)
    value = models.FloatField(null=True) 
    extract_value = models.FloatField(default=0) 
    future_extract_value = models.FloatField(default=0) 
    descripition = models.TextField(max_length=300, blank=True)
    type = models.CharField(choices=type_list, blank=False, null=False, max_length=2)
    
    
    def __str__(self) -> str:
        return self.name

    def show_value(self):
        return f'{self.extract_value + self.value:.2f}'.replace('.',',')

    def show_future_value(self):
        return f'{self.future_extract_value + self.value:.2f}'.replace('.',',')
        

class Extract(models.Model): #* Modelo para salvar os extratos

    type_list = (('P', 'Profit'), ('D', 'Damage'))

    
    name = models.CharField(max_length=50, blank=False)
    value = models.FloatField()
    account = models.ForeignKey(Account, on_delete= models.CASCADE) 
    type = models.CharField(max_length=1, choices=type_list, blank=False, null=False, )
    date = models.DateField(blank=False, null=False)
    descripition = models.TextField(max_length=300, blank=True)
    pay = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.name
    
    def show_date(self) -> str:

        date = str(self.date).split('-')

        return f'{date[2]}/{date[1]}/{date[0]}'
    
    def show_money(self) -> str:

        return f'R$ {self.value:.2f}'.replace('.', ',')
