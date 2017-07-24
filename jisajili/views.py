import json
from django.shortcuts import render
from .models import JobSeeker
from django.views.generic import View,TemplateView
from django.http import JsonResponse



#You need super() in Python any time you override a method you inherit from a 
#superclass since Python does not call it for you automatically.

def home(request):
    return render(request,'base.html',{})


def show_candidates(request):
    all_applicants = JobSeeker.objects.filter(is_staff=False).order_by("-created_on")
    return render(request,'candidates.html',{'all_applicants':all_applicants})


class SingleApplicant(TemplateView):
  template_name = 'resume.html'

  def get_context_data(self,**kwargs):
    context = super(SingleApplicant,self).get_context_data(**kwargs)
    context['applicant'] = JobSeeker.objects.get(pk=self.kwargs.get('id',None))
    return context




class CreateApplication(TemplateView):
    template_name = 'registration.html'

    def post(self,request,*args,**kwargs):
        if request.is_ajax():
            userPhoto = request.FILES.get('image')

            #fetch data in json string from the post object
            #and convert the json string to a python object
        
            education  = json.loads(request.POST.get("education"))
            wrk_experience  = json.loads(request.POST.get("wrkexperience"))
            referees  = json.loads(request.POST.get("referees"))
            applicant_data = json.loads(request.POST.get("ApplicantDetails"))

            #applicants_other_data = education + wrk_experience + referees
            
            applicant = {
              'email': applicant_data['email'],
              'id_number':applicant_data['idnumber'],
              'sir_name':applicant_data['sirname'],
              'other_name':applicant_data['othername'],
              'phone_no':applicant_data['phone'],
              'date_of_birth':applicant_data['dob'],
              'gender':applicant_data['gender'],
              'home_city':applicant_data['county'],
              'user_photo':userPhoto,
              'about_applicant':applicant_data['abt'],
            }
           
     
            JobSeeker.objects.create_applicant(applicant,wrk_experience,referees,education)
            
            data = {}

            return JsonResponse(data)

        return  super(CreateApplication,self).get(request)
