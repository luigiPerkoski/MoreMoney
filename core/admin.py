from django.contrib import admin
from .models import Extract, Account


#! Classe para configurar o display dos meus modelos 

class AdminAccount(admin.ModelAdmin):

    list_display_links = ["name", "type", "value"]
    list_display = ["name", "type", "value"]
    search_fields = ["name",]
    list_filter = ["type",]


class AdminExtract(admin.ModelAdmin):
   
    list_display_links = ["name", "account", "value"]
    list_display = ["name", "account", "value"]
    list_filter = ["account", "date", "type"]
    search_fields = ["name",]



#! Importe dos meu modelos pro admin

admin.site.register(Account, AdminAccount)
admin.site.register(Extract, AdminExtract)
