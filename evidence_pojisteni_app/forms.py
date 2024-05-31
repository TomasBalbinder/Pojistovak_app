from django import forms
from .models import Customer, ReservedUsername, Insurance, KindOfInsurance, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class InsuredForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'zip_code']
     
    first_name = forms.CharField(max_length=50,
                            error_messages={'required': "Kolonka Jméno nesmí být prazdná."},
                            widget=forms.TextInput(attrs={'class': 'form-control'}), 
                            required=True)
    
    last_name = forms.CharField(max_length=50,
                            error_messages={'required': "Kolonka Příjmení nesmí být prazdná."},
                            widget=forms.TextInput(attrs={'class': 'form-control'}), 
                            required=True)
    
    address = forms.CharField(max_length=50,
                            error_messages={'required': "Kolonka Adresa nesmí být prazdná."},
                            widget=forms.TextInput(attrs={'class': 'form-control'}), 
                            required=True)
    
    city = forms.CharField(max_length=50,
                            error_messages={'required': "Kolonka Město nesmí být prazdná."},
                            widget=forms.TextInput(attrs={'class': 'form-control'}), 
                            required=True)
    
    zip_code = forms.CharField(max_length=20,required=False)
    email = forms.EmailField(max_length=50,required=False)
    phone = forms.CharField(max_length=20,required=False)

    def clean(self):
        cleaned_data = super().clean()  
        email = cleaned_data.get("email","").strip()
        phone = cleaned_data.get("phone","").strip()


        if phone and not phone.isdigit():
            raise ValidationError("Telefonní číslo musí obsahovat pouze číslice.")
        
        if not email and not phone:
            raise ValidationError("Musíte vyplnit buď e-mailovou adresu nebo telefonní číslo.")
        return cleaned_data
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            customers = Customer.objects.filter(email=email)
            if self.instance and self.instance.pk:
                customers = customers.exclude(pk=self.instance.pk)
            if customers.exists():
                raise ValidationError("Zákazník s touto e-mailovou adresou již existuje.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            customers = Customer.objects.filter(phone=phone)
            if self.instance and self.instance.pk:
                customers = customers.exclude(pk=self.instance.pk)
            if customers.exists():
                raise ValidationError("Zákazník s tímto telefonním číslem již existuje.")
        return phone
    

class InsuranceForm(forms.ModelForm):
    
    class Meta:
        model = Insurance
        fields = ['customer','kind_of_insurance', 'amount', 'subject_of_insurance', 'valid_from', 'valid_until']
        
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.HiddenInput())
    kind_of_insurance = forms.ModelChoiceField(queryset=KindOfInsurance.objects.all())
        
    amount = forms.DecimalField(max_digits=12, decimal_places=2,
                            error_messages={'required': "Kolonka Částka nesmí být prazdná."},
                            widget=forms.TextInput(attrs={'class': 'form-control'}),)
    
    subject_of_insurance = forms.CharField(max_length=100,
                            error_messages={'required': "Kolonka Předmět pojištění nesmí být prazdná."},
                            widget=forms.TextInput(attrs={'class': 'form-control'}),)
    
    valid_from = forms.DateField(
                            error_messages={'required': "Kolonka Platnost od nesmí být prazdná."},
                            widget=forms.TextInput(attrs={'class': 'form-control'}),)
    
    valid_until  = forms.DateField(
                            error_messages={'required': "Kolonka Platnost do nesmí být prazdná."},
                            widget=forms.TextInput(attrs={'class': 'form-control'}),)


    def clean(self):
        cleaned_data = super().clean()  
        return cleaned_data
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError('Částka musí být větší než nula.')
        return amount

    def clean_valid_from(self):
        valid_from = self.cleaned_data.get('valid_from')
        if valid_from and valid_from < timezone.now().date(): # mozna chyba 
            raise ValidationError("Datum 'Platnost od' nemůže být v minulosti.")
        return valid_from
    
    def clean_valid_until(self):
        valid_until = self.cleaned_data.get('valid_until')
        if valid_until and valid_until < timezone.now().date(): # mozna chyba 
            raise ValidationError("Datum 'Platnost do' nemůže být v minulosti.")
        return valid_until


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

 
class RegistrationForm(forms.Form):
    user_id = forms.CharField(max_length=20,
                              error_messages={'required': "Kolonka Uživatelské jméno nesmí být prázdná."},
                              widget=forms.TextInput(attrs={'class': 'form-control'}), 
                              required=True)
    
    email = forms.EmailField(max_length=50,
                             error_messages={'required': "Kolonka Email nesmí být prázdná."},
                             widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             required=True )
    
    password = forms.CharField(max_length=20, 
                               min_length=5,
                               error_messages={'min_length': "Heslo nesmí mít méně než 5 znaků.", 'required': "Kolonka Heslo nesmí být prázdná."},
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True )
    
    password1 = forms.CharField(max_length=20, 
                                min_length=5,
                                error_messages={'min_length': "Heslo (znovu) nesmí mít méně než 5  znaků.", 'required': "Kolonka Heslo (znovu) nesmí být prázdná."},
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True )

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get("password1")
        password = self.cleaned_data.get("password")
        if password != password1:
            raise ValidationError("Hesla se musi shodovat.")
        
        return cleaned_data
    
    def  clean_user_id(self):
        username = self.cleaned_data.get("user_id")
        if not ReservedUsername.objects.filter(username=username).exists():
            raise ValidationError("Uživatelské jméno není platné.")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("Uživatelské jméno je již zaregistrované.")
        return username
    
    def save(self):
        cleaned_data = self.clean()
        user = User.objects.create_user(
            username=cleaned_data["user_id"],
            email=cleaned_data["email"],
            password=cleaned_data["password"]
        )
        UserProfile.objects.create(user=user)
        return user