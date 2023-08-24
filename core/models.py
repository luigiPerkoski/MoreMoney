from django.db import models
from datetime import date

#* Models here 

class Account(models.Model): #* Accounts templates to filter between bank 

    type_list = (('CC', 'Conta Corrente'),
        ('DI', 'Dinheiro'), 
        ('CP', 'Conta Poupança'), 
        ('IN', 'Investimento'))
    
    color_list = (('R', 'Vermelho'),
            ('B', 'Azul'),
            ('P', 'Roxo'),
            ('O', 'Laranja'))
        

    name = models.CharField(max_length=50)
    value = models.FloatField() 
    future_value = models.FloatField() 
    descripition = models.TextField(max_length=300)
    type = models.CharField(choices=type_list, blank=False, null=False, max_length=2)
    color = models.CharField(choices=color_list, blank=False, null=False, max_length=2)
    
    
    def __str__(self) -> str:
        return self.name


    def __sum(self) -> None:

        value = 0

        for obj in Extract.objects.order_by('date'):
            if obj.account == self:
                value += obj.value

        Account.objects.update(value=value)   
    

    def __future_sum(self) -> None:
        
        object_list = Extract.objects.order_by('date')
        value = 0

        for object in object_list:
            if object.account == self.name and object.date > date.today().day:
                value += object.value
        
        Account.objects.update(future_value=value)


    def show_sum(self) -> str:

        self.__sum

        return f'R$ {self.value:.2f}'.replace('.', ',')

    def show_futere_sum(self) -> str:

        self.__future_sum

        return f'R$ {self.future_value:.2f}'.replace('.', ',')

class Extract(models.Model): #* Extract template for saving money spending

    type_list = (('P', 'Profit'), ('D', 'Damage'))

    
    name = models.CharField(max_length=50, blank=False)
    value = models.FloatField()
    account = models.ForeignKey(Account, on_delete= models.PROTECT) 
    type = models.CharField(max_length=1, choices=type_list, blank=False, null=False)
    date = models.DateField(blank=False, null=False)
    descripition = models.TextField(max_length=300)
    pay = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.name
    
    
    
    
    def show_money(self) -> str:
        return f'R$ {self.value:.2f}'.replace('.', ',')
    


