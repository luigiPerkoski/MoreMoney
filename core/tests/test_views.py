from django.test import TestCase
from ..models import Extract, Account
from datetime import date

class IndexTest(TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000/'
        self.account = Account.objects.create(name='ContaTeste',value=0, future_value=0, descripition='', type='CC', color='R')

        self.extract_profit = Extract.objects.create(name='Salario', value=0, account=self.account, type='P', date=date.today(), descripition='', pay=True)

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'pages/index.html')
    
    def test_post_search_request(self):
        response = self.client.post(self.url, {'query': 'Sala'})
        self.assertIn(self.extract_profit,response.context['extract_list'])
    
    def test_post_delete_request(self):
        response = self.client.post('http://127.0.0.1:8000/delete_extract/1')
        self.assertNotIn(self.extract_profit,self.client.get(self.url).context['extract_list'])
