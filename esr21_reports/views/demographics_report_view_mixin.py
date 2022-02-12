from edc_base.view_mixins import EdcBaseViewMixin
from django.apps import apps as django_apps
from django.db.models import Q



class DemographicsReportViewMixin(EdcBaseViewMixin):
    
    eligibility_model = 'esr21_subject.eligibilityconfirmation'
    consent_model = 'esr21_subject.informedconsent'
    vaccination_model =  'esr21_subject.vaccinationdetails'
    screening_eligibility_model = 'esr21_subject.screeningeligibility'
    pregnancy_test_model = 'esr21_subject.pregnancytest'
    
    
    @property
    def eligibility_model_cls(self):
        return django_apps.get_model(self.eligibility_model)
    
    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.consent_model)
    
    @property
    def vaccination_model_cls(self):
        return django_apps.get_model(self.vaccination_model)
    
    @property
    def screening_eligibility_cls(self):
        return django_apps.get_model(self.screening_eligibility_model)
    
    @property
    def pregnancy_test_cls(self):
        return django_apps.get_model(self.pregnancy_test_model)
    
    @property
    def total_enrolled_participants(self):
        overall = self.vaccination_model_cls.objects.filter(
            Q(received_dose_before='first_dose') |
            Q(received_dose_before='second_dose')).count()
        gaborone = self.get_enrolled_by_site('Gaborone')
        maun = self.get_enrolled_by_site('Maun')
        serowe = self.get_enrolled_by_site('Serowe')
        f_town = self.get_enrolled_by_site('Francistown')
        phikwe = self.get_enrolled_by_site('Phikwe')

        return ['Enrolled',overall,gaborone,maun,serowe,f_town,phikwe]
    
    @property
    def received_two_doses(self):
        overall = self.vaccination_model_cls.objects.filter(
            Q(received_dose_before='first_dose') &
            Q(received_dose_before='second_dose')).count()
        gaborone = self.get_vaccination_by_site('Gaborone')
        maun = self.get_vaccination_by_site('Maun')
        serowe = self.get_vaccination_by_site('Serowe')
        f_town = self.get_vaccination_by_site('Francistown')
        phikwe = self.get_vaccination_by_site('Phikwe')

        return ['Participants with two doses',overall,gaborone,maun,serowe,f_town,phikwe]
    
    @property
    def gender_by_site(self):
        overall_male = self.consent_model_cls.objects.filter(
            Q(gender='M')).count()
            
        overall_female = self.vaccination_model_cls.objects.filter(
          Q(gender='F')).count()
        
        gaborone = self.get_vaccination_by_site('Gaborone')
        maun = self.get_vaccination_by_site('Maun')
        serowe = self.get_vaccination_by_site('Serowe')
        f_town = self.get_vaccination_by_site('Francistown')
        phikwe = self.get_vaccination_by_site('Phikwe')
    
    @property
    def ethnicity(self):
        pass
    
    @property
    def median_age(self):
        pass
    
    @property
    def pregnancy_status(self):
        pass
    
    @property
    def diabetes(self):
        pass
    
    @property
    def prior_covid_infection(self):
        pass
    
    @property
    def smoking_status(self):
        pass
    
    @property
    def alcohol_status(self):
        pass
    
    @property
    def follow_up_time(self):
        pass
    
    @property
    def total_adverse_events(self):
        pass
    
    @property
    def participant_with_atleast_ae(self):
        pass
    
    @property
    def total_serious_adverse_events(self):
        pass
    
    @property
    def participant_with_atleast_sae(self):
        pass
    
    def get_vaccination_by_site(self, site_name_postfix):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.vaccination_model_cls.objects.filter(
                Q(received_dose_before='first_dose') &
                Q(received_dose_before='second_dose') &
                Q(site_id=site_id)).count()
                
    def get_gender_by_site(self, site_name_postfix, gender):
        site_id = self.get_site_id(site_name_postfix)
        if site_id:
            return self.consent_model_cls.objects.filter(
                Q(gender=gender)).count()