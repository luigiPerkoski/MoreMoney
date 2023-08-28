from django.db import models
import datetime

# Models here 

class Account(models.Model): #* Accounts templates to filter between bank 

    type_list = (('CC', 'Conta Corrente'),
        ('DI', 'Dinheiro'), 
        ('CA', 'Cartao'), 
        ('IN', 'Investimento'))
    
    color_list = (('R', 'Vermelho'),
        ('B', 'Azul'),
        ('P', 'Roxo'),
        ('O', 'Laranja'))
        

    name = models.CharField(max_length=50)
    value = models.FloatField(null=True) 
    future_value = models.FloatField(null=True) 
    descripition = models.TextField(max_length=300)
    type = models.CharField(choices=type_list, blank=False, null=False, max_length=2)
    color = models.CharField(choices=color_list, blank=False, null=False, max_length=2)
    
    
    def __str__(self) -> str:
        return self.name

    def __date_now(self,date_one, date_two) -> bool:

        list_date_one = str(date_one).split('-')
        list_date_two = str(date_two).split('-')

        if int(list_date_one[0]) > int(list_date_two[0]):
            return True
        elif int(list_date_one[0]) == int(list_date_two[0]):
            if int(list_date_one[1]) > int(list_date_two[1]):
                  return True
            elif int(list_date_one[1]) == int(list_date_two[1]):
                  if int(list_date_one[2]) >= int(list_date_two[2]):
                       return True
                  else: 
                       return False
            else:
                 return False
        else:
            return False

    def sum(self) -> None:

        value = 0

        date = datetime.date.today()

        for object in Extract.objects.order_by('date'):
            if object.account == self and self.__date_now(date, object.date):
                match object.type:

                    case 'P':
                        value += object.value

                    case 'D':
                        value -= object.value
                    
        
        Account.objects.update(value=value)   

    def future_sum(self) -> None:
        
        value = self.value

        date = datetime.date.today()


        for object in Extract.objects.order_by('date'):
            if object.account == self and self.__date_now(date, object.date) != True:
                match object.type:

                    case 'P':
                        value += object.value

                    case 'D':
                        value -= object.value
        
        Account.objects.update(future_value=value)

    def show_sum(self) -> str:

        self.sum()

        return f'R$ {self.value:.2f}'.replace('.', ',')

    def show_futere_sum(self) -> str:

        self.future_sum()

        return f'R$ {self.future_value:.2f}'.replace('.', ',')


class Extract(models.Model): #* Extract template for saving money spending 

    type_list = (('P', 'Profit'), ('D', 'Damage'))

    
    name = models.CharField(max_length=50, blank=False)
    value = models.FloatField()
    account = models.ForeignKey(Account, on_delete= models.CASCADE) 
    type = models.CharField(max_length=1, choices=type_list, blank=False, null=False, )
    date = models.DateField(blank=False, null=False)
    descripition = models.TextField(max_length=300)
    pay = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.name
    
    def show_date(self) -> str:

        date = str(self.date).split('-')

        return f'{date[2]}/{date[1]}/{date[0]}'
    
    def show_money(self) -> str:

        return f'R$ {self.value:.2f}'.replace('.', ',')
    

class Money(models.Model): #* All money 

    name = models.CharField(max_length=50)
    value = models.FloatField()
    future_value = models.FloatField()
    extract_damege = models.FloatField()
    extract_profit = models.FloatField()


    def __str__(self) -> str:
        return self.name

    def calc_future_value(self):
 
        response = 0

        for object in Account.objects.order_by('name'):

            object.future_sum()

            response += object.future_value

        Money.objects.update(future_value=response)

    def calc_value(self):

        response = 0

        for object in Account.objects.order_by('name'):

            object.sum()

            response += object.value

        Money.objects.update(value=response)
    
    def show_value(self):
        
        self.calc_value()

        return f'R$ {self.value:.2f}'.replace('.', ',')

    def show_future_value(self):
        
        self.calc_future_value( )

        return f'R$ {self.future_value:.2f}'.replace('.', ',')
    
    def calc_extract_damege(self):

        value = 0
        
        for object in Extract.objects.filter(type='D'):
            value += object.value

        Money.objects.update(extract_damege=value)
            
    def calc_extract_profit(self):
        
        value = 0
        
        for object in Extract.objects.filter(type='P'):
            value += object.value

        Money.objects.update(extract_profit=value)

    def show_extract_damege(self):
        
        self.calc_extract_damege()

        return f'R$ {self.extract_damege:.2f}'.replace('.', ',')

    def show_extract_profit(self):
        
        self.calc_extract_profit()

        return f'R$ {self.extract_profit:.2f}'.replace('.', ',')
