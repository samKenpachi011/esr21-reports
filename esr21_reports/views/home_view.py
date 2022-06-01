from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from .enrollment_report_mixin import EnrollmentReportMixin
from .site_helper_mixin import SiteHelperMixin
from .adverse_events import (
    AdverseEventRecordViewMixin,
    SeriousAdverseEventRecordViewMixin)
from .psrt_mixins import (
    DemographicsMixin,
    ScreeningReportsViewMixin,
    SummaryQueriesMixin,
    StatsPerWeekMixin)


class HomeView(
            AdverseEventRecordViewMixin,
            SeriousAdverseEventRecordViewMixin,
            SiteHelperMixin,
            ScreeningReportsViewMixin,
            EnrollmentReportMixin,
            SummaryQueriesMixin,
            StatsPerWeekMixin,
            DemographicsMixin,
            NavbarViewMixin,
            EdcBaseViewMixin,
            TemplateView):
    template_name = 'esr21_reports/home.html'
    navbar_selected_item = 'Reports'
    navbar_name = 'esr21_reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
