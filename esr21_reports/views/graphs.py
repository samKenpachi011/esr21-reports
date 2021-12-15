from chartjs.views.lines import BaseLineChartView
from calendar import month_name

from django.apps import apps as django_apps
from django.views.generic import TemplateView
from django.contrib.sites.models import Site


class LineChartJSONView(BaseLineChartView):

    vaccine_model = 'esr21_subject.vaccinationdetails'

    @property
    def vaccine_model_cls(self):
        return django_apps.get_model(self.vaccine_model)

    @property
    def months(self):
        vaccinations_details = self.vaccine_model_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.strftime("%B") for vd in vaccinations_details]
        month_lookup = list(month_name)
        months = list(set(months))
        return sorted(months, key=month_lookup.index)

    @property
    def months_numbers(self):
        vaccinations_details = self.vaccine_model_cls.objects.all().values_list(
            'created', flat=True)
        months = [vd.month for vd in vaccinations_details]
        months = list(set(months))
        return sorted(months)
        
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return self.months

    def get_providers(self):
        """Return names of datasets."""
        sites =  Site.objects.all().order_by('id')
        return [site.name for site in sites]

    def get_data(self):
        sites =  Site.objects.all().values_list(
            'id', flat=True)
        sites = list(set(sites))
        sites = sorted(sites)
        data = []
        for site_id in sites:
            row_data = []
            for month_num in self.months_numbers:
                vaccinations_details = self.vaccine_model_cls.objects.filter(
                    site__id=site_id,
                    received_dose_before='first_dose',
                    created__month=month_num)
                row_data.append(vaccinations_details.count())
            data.append(row_data)
        return data
        
    # def get_data(self):
        # """Return 3 datasets to plot."""
        #
        # return [[75, 44, 92, 11, 44, 95, 35, 20, 40, 30, 12, 50],
                # [41, 92, 18, 3, 73, 87, 92, 45, 67, 78, 45, 90],
                # [87, 21, 94, 3, 90, 13, 65, 56, 78, 89, 34, 12]]

line_chart = TemplateView.as_view(template_name='esr21_reports/line_chart.html')
line_chart_json = LineChartJSONView.as_view()