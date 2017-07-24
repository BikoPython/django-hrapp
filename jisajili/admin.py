from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import JobSeeker,Education,Referees,Experience
from .forms import UserCreationForm,UserChangeForm



class JobSeekerAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('email','sir_name','id_number','phone_no','home_city','passport')
    list_filter = ('sir_name',)

    fieldsets =(

        ('Credentials',{'fields':('email','password')}),
        ('Permissions',{'fields':('is_active','is_admin','is_staff')}),
        ('Personal Information',{'fields':('email','sir_name','other_name','id_number','date_of_birth','home_city','user_photo')}),
      

    )

    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



admin.site.register(JobSeeker,JobSeekerAdmin)
#admin.site.unregister(Group)


class EducationItemsAdmin(admin.ModelAdmin):
    #add_form = UserCreationForm
    #form = UserChangeForm
    list_display = ('fullname',)
    list_filter = ('course_name',)

    fieldsets =(
        
        ('Education Background',{'fields':('applicant','institution_name',
        'course_name','qualification','grade_attained','start_date','completion_date')}),    

    )

    ordering = ('institution_name',)
    search_fields=('institution_name',)

class ExperienceItemsAdmin(admin.ModelAdmin):
    #add_form = UserCreationForm
    #form = UserChangeForm
    list_display = ('fullname',)
    list_filter = ('position',)

    fieldsets =(
       
        ('Experience',{'fields':('name_of_org','position','date_employed','date_completed')}),
       
    )

    ordering = ('name_of_org',)
    search_fields=('name_of_org',)

class RefereesItemsAdmin(admin.ModelAdmin):
    #add_form = UserCreationForm
    #form = UserChangeForm
    list_display = ('fullname',)
    list_filter = ('ref_name',)

    fieldsets =(
        
        ('Referees',{'fields':('ref_name','ref_phone','ref_occupation')}),

    )

    ordering = ('ref_name',)
    search_fields=('ref_name',)



admin.site.register(Education,EducationItemsAdmin)
admin.site.register(Experience,ExperienceItemsAdmin)
admin.site.register(Referees,RefereesItemsAdmin)
admin.site.unregister(Group)
