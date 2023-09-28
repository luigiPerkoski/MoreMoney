from django.shortcuts import render, redirect, HttpResponse
from .models import Extract, Account
from .forms import NewExtract, NewAccount, SearchForm, CadastroForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

#! Minhas funções para mostrar as paginas aqui

@login_required(login_url='login')
def index(request):
    #*===============================================================
    extract = Extract.objects.filter(usuario=request.user).all()
    form = SearchForm()
    response = []

    #//Calcula o total 

    value = 0
    future_value = 0

    for object in Extract.objects.filter(usuario=request.user).all():
        match object.type:
            case 'P':
                future_value += object.value
            case 'D':
                future_value -= object.value
            
        if object.pay:
            match object.type:
                case 'P':
                    value += object.value
                case 'D':
                    value -= object.value  

    for object in Account.objects.filter(usuario=request.user).all():
        value += object.value
        future_value += object.value

    #//Pesquisa

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            for c in extract:
                if query.upper() in c.name.upper():
                    response.append(c)
            extract = response[:]
        else:
            extract = Extract.objects.filter(usuario=request.user).all() 
    else:
        form = SearchForm()
        extract = Extract.objects.filter(usuario=request.user).all() 

    #//Return
    context = {'extract_list': extract, 'money': round(value, 2), 'future_money': round(future_value, 2), 'len_extract_list':len(extract), 'form': form}
    return render(request, 'pages/index.html', context=context)

@login_required(login_url='login')
def accounts(request):
    #*===============================================================
    account = Account.objects.filter(usuario=request.user).all()
    response = []
    value_account = []

    #//Valor por conta
    for conta in Account.objects.filter(usuario=request.user).all():
        future_value = 0
        value = 0
        for object in Extract.objects.filter(usuario=request.user).all():
            if object.pay and object.account == conta:
                match object.type:
                    case 'P':
                        value += object.value
                    case 'D':
                        value -= object.value  
            if object.account == conta:
                match object.type:
                    case 'P':
                        future_value += object.value
                    case 'D':
                        future_value -= object.value   
        Account.objects.filter(id=conta.id).update(extract_value=value,future_extract_value=future_value)
            
    #//Pesquisa

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            for c in account:
                if query.upper() in c.name.upper():
                    response.append(c)
            account = response[:]
        else:
            account = Account.objects.filter(usuario=request.user).all()
    else:
        form = SearchForm()
        account = Account.objects.filter(usuario=request.user).all()

    #//Return
    context = {'account_list': account, 'form': form}
    return render(request, 'pages/accounts.html', context=context)

@login_required(login_url='login')
def damege(request):
    #*===============================================================
    damege = Extract.objects.filter(type='D', usuario=request.user)
    form = SearchForm()

    #//Calcula o total de extratos negativos 
    extract_damage = 0
    future_extract_damage = 0
    
    for object in damege:
        if object.pay:
            extract_damage += object.value
            future_extract_damage += object.value
        else:
            future_extract_damage += object.value

    #//Pesquisa
    

    #//Return
    context = {'dameges': damege, 'extract_damege': extract_damage,'future_extract_damage': future_extract_damage, 'len_dameges': len(damege), 'form': form}
    return render(request, 'pages/damege.html', context=context)

@login_required(login_url='login')
def profit(request):
    #*===============================================================
    profit = Extract.objects.filter(type='P', usuario=request.user)
    form = SearchForm()

    #//Calcula o total de extratos positivos  
    extract_profit = 0
    future_extract_profit = 0
    for object in profit:
        if object.pay:
            extract_profit += object.value
            future_extract_profit += object.value
        else:
            future_extract_profit += object.value

    #//Pesquisa


    #//Return
    context = {'profits': profit, 'extract_profit': extract_profit,'future_extract_profit': future_extract_profit, 'len_profits': len(profit), 'form': form}
    return render(request, 'pages/profit.html', context=context)

@login_required(login_url='login')
def processar_formulario(request, page, id):
    #*===============================================================
    if request.method == 'POST':

        var = request.POST.get(f'pay_checkbox_{id}')

        if var == None:
            Extract.objects.filter(id=id).update(pay=False)
        else:
            Extract.objects.filter(id=id).update(pay=True)
        
        return redirect(page)

@login_required(login_url='login')
def new_extract(request):
    #*===============================================================
    forms = NewExtract()

    accounts = Account.objects.order_by('name')

    context = {'forms': forms, "contas": accounts}

    return render(request, 'pages/new_extract.html', context)

@login_required(login_url='login')
def extract_forms(request):
    #*===============================================================
    forms = NewExtract(request.POST)
    if forms.is_valid():
        novo_registro = forms.save(commit=False)
        novo_registro.usuario = request.user
        novo_registro.save()
    return redirect (index)

@login_required(login_url='login')
def new_account(request):
    #*===============================================================
    accounts = Account.objects.order_by('name')
    forms = NewAccount()

    context = {"contas": accounts, 'forms': forms}

    return render (request, 'pages/new_account.html', context )

@login_required(login_url='login')
def new_extract_from_account(request, account): 
    #*===============================================================
    categoria_padrao = Account.objects.get(id=account)

    forms = NewExtract(initial={'account': categoria_padrao})


    context = {'forms': forms}

    return render(request, 'pages/new_extract.html', context)

@login_required(login_url='login')
def accounts_forms(request):
    #*=============================================================== 
    forms = NewAccount(request.POST)
    if forms.is_valid():
        novo_registro = forms.save(commit=False)
        novo_registro.usuario = request.user
        novo_registro.save()
    return redirect (index)

@login_required(login_url='login')
def search_view(request):
    #*=============================================================== 
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Extract.objects.filter(name=query, usuario=request.user)
        else:
            results = []
    else:
        form = SearchForm()
        results = []
    
    context = {'form': form, 'results': results}

    return redirect('/')

@login_required(login_url='login')
def delete_extract(request, id):
    #*=============================================================== 
    post = Extract.objects.get(id=id)
    post.delete()
    return redirect('index')

@login_required(login_url='login')
def delete_account(request, id):
    #*=============================================================== 
    post = Account.objects.get(id=id)
    post.delete()
    return redirect('accounts')

@login_required(login_url='login')
def extract(request, id):
    #*=============================================================== 

    extract = Extract.objects.filter(usuario=request.user).get(id=id)

    forms = NewExtract(initial={'name': extract.name, 'value':extract.value, 'account': extract.account, 'type': extract.type, 'date': extract.date, 'pay': extract.pay, 'descripition': extract.descripition})


    context = {'forms': forms, 'id': id}

    return render(request, 'pages/extract.html', context)

@login_required(login_url='login')
def extract_forms_update(request, id):
    #*=============================================================== 
    
    item = Extract.objects.filter(usuario=request.user).get(id=id)
    if request.method == 'POST':
        form = NewExtract(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = NewExtract(initial={'name': extract.name, 'value':extract.value, 'account': extract.account, 'type': extract.type, 'date': extract.date, 'pay': extract.pay, 'descripition': extract.descripition})

    return render(request, 'extract.html', {'form': form})

@login_required(login_url='login')
def account(request, id):
    #*=============================================================== 

    account = Account.objects.filter(usuario=request.user).get(id=id)

    forms = NewAccount(initial={
        'name':account.name,
        'value':account.value,
        'type':account.type,
        'descripition': account.descripition
    })


    context = {'forms': forms, 'id': id}

    return render(request, 'pages/account.html', context)

@login_required(login_url='login')
def account_forms_update(request,id):
    #*===============================================================
    
    item = Account.objects.filter(usuario=request.user).get(id=id)

    if request.method == 'POST':
        form = NewAccount(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('accounts')
    else:
        form = NewAccount(initial={
            'name':account.name,
            'value':account.value,
            'type':account.type,
            'descripition': account.descripition
        })

    return render(request, 'extract.html', {'form': form})

def cadastro(request):
    #*===============================================================

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', 'Este nome de usuário já está em uso.')
                return render(request, 'pages/cadastro.html', {'form': form})

            try:
                validate_password(password)
            except:
                form.add_error('password', 'senha invalida')
                return render(request, 'pages/cadastro.html', {'form': form})
            
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=password
            )
            return redirect('/')
    else:
        form = CadastroForm()

    return render(request, 'pages/cadastro.html', {'form': form})

def view_login(request):
    #*===============================================================
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
        
        try:
            login(request, user)
            return redirect('index')
        except:
            form.add_error('password', 'Usuario ou Senha incorreto')

    context = {'form': form}
    return render(request, 'pages/login.html', context)