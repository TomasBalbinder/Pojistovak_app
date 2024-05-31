from django.contrib import admin
from .models import ReservedUsername, Customer, Insurance, KindOfInsurance, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'assigned_color']  


class ReservedUsernameAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']  
    search_fields = ['username'] 


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'email', 'phone', 'address', 'city', 'zip_code']  
    search_fields = ['last_name'] 


class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_full_name', 'kind_of_insurance', 'amount', 'subject_of_insurance', 'valid_from', 'valid_until'] 

    def customer_full_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(KindOfInsurance)
admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(ReservedUsername, ReservedUsernameAdmin)
admin.site.register(Customer, CustomerAdmin)