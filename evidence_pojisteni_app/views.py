from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, InsuredForm, InsuranceForm, KindOfInsurance
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Customer, Insurance, UserProfile
from django.core.paginator import Paginator
from django.db.models import Sum



def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  
                messages.success(request, f"Uživatel, {user.username} přihlášen!")
                return redirect("list_insured_customers")  
            else:
                messages.error(request, "Nesprávné uživatelské jméno nebo heslo.")
        else:
            messages.error(request, "Formulář není platný. Zkontrolujte chyby.")
    else:
        form = LoginForm()  
    return render(request, "login.html", {"form": form})
                

def logout_view(request):
    logout(request)  
    return redirect("login")


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Registrace byla úspěšná! Nyní se můžete přihlásit.")
    else:
        form = RegistrationForm()  
    return render(request, "registration.html", {"form": form})


def list_insured_customers(request):
    users = UserProfile.objects.all().order_by('user__username')
    selected_user = request.GET.get('user')
    if selected_user == "0" or not selected_user:
        customers = Customer.objects.all().order_by('last_name')
    else:
        customers = Customer.objects.filter(user_profile__pk=selected_user).order_by('last_name')
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'list_insured_customers.html',{'page' : page, 'users' :users})


def new_insurance_view(request):
    customers = Customer.objects.all()
    if request.method == "POST":
        form = InsuranceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Uložení nového pojištění proběhlo úspěšně.")
            return redirect('new_insurance')
    else:
        form = InsuranceForm()
    insurances = KindOfInsurance.objects.all()
    return render(request, 'new_insurance.html', {'customers': customers, 'form': form, 'insurances': insurances})


def edit_insurance_view(request, pk):
    insurance = get_object_or_404(Insurance, pk=pk)
    customer = insurance.customer
    if request.method == "POST":
        form = InsuranceForm(request.POST, instance=insurance)
        if form.is_valid():
            form.save()
            messages.success(request, "Editace pojištění proběhla úspěšně.")
    else:
        form = InsuranceForm(instance=insurance)
    insurances = KindOfInsurance.objects.all()
    return render(request, 'edit_insurance.html', {'form': form, 'insurances': insurances, 'customer': customer})


def insured_detail_view(request, pk):
    customer_detail = Customer.objects.get(pk=pk)
    insurance_details = Insurance.objects.filter(customer=customer_detail)
    return render(request, 'insured_detail.html', {'customer_detail' : customer_detail, 'insurance_details' : insurance_details})


def about_aplication_view(request):
    return render(request, 'about_aplication.html')


def new_insured_view(request, pk=None):
    if pk:
        customer = get_object_or_404(Customer, pk=pk)
        action = f"Editace pojištěnce pro: {customer.first_name} {customer.last_name}"

    else:
        customer = None
        action = "Nový pojištěnec"

    if request.method == "POST":
        form = InsuredForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            assigned_color = request.user.userprofile.assigned_color
            customer.assigned_color = assigned_color
            user_profile = request.user.userprofile
            customer.user_profile = user_profile
            customer.save()
            messages.success(request, "Uložení nového zákazníka proběhlo úspěšně.")
            if not pk:
                return redirect('new_insured')

    else:
        form = InsuredForm(instance=customer)
    context = {
        'customer': customer,
        'action': action,
        'form': form,}
    return render(request, "new_insured.html", {"context": context})


def users_sales_view(request):
    employees = UserProfile.objects.all()
    employee_data = []
    
    for employee in employees:
        clients = Customer.objects.filter(user_profile=employee)
        contracts = Insurance.objects.filter(customer__user_profile=employee)
        total_amount = contracts.aggregate(total=Sum('amount'))['total'] or 0
        contract_count = contracts.count()

        employee_data.append({
            'employee': employee,
            'clients_count': clients.count(),
            'contract_count': contract_count,
            'total_amount': total_amount,
        })

    employee_data_sorted = sorted(employee_data, key=lambda x: x['total_amount'], reverse=True)
    return render(request, 'users_sales.html', {'employee_data': employee_data_sorted})


def delete_insurance_view(request,pk):
    insurance = get_object_or_404(Insurance, pk=pk)
    customer_pk = insurance.customer.pk
    if request.method == "POST": 
        insurance.delete()
        messages.success(request,'Pojištění bylo vymazáno.')
        return redirect('insured_detail', pk=customer_pk)


def delete_customer_view(request,pk):
    custom = get_object_or_404(Customer, pk=pk)
    if request.method == "POST": 
        custom.delete()
        messages.success(request,'Zákazník byl vymazán.')
        return redirect('list_insured_customers')







