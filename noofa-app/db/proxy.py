import io

from .models import Profile

from noofa import ReportBuilder
from noofa.utils import PdfReport


class ProfileProxy(Profile):
    def get_report_builder(self):
        rb = ReportBuilder(
            data_config=self.data_config,
            components_config=self.components,
            values=self.values,
        )
        return rb
    
    @property
    def data_config(self):
        return {
            'sources': self.sources,
            'queries': self.queries,
            'dataframes': self.dataframes,
        }
    
    def make_pdf(self, doc_id):
        doc = self.docs.get(doc_id)
        components = []
        rb = self.get_report_builder()

        for cmp_id in doc['components']:
            try:
                component = rb.get_component(cmp_id)
                component.build()
            except:
                pass
            else:
                components.append(component)

        buffer = io.BytesIO()
        pdf_report = PdfReport(buffer, orientation='landscape')
        pdf_report.from_list(components)
        pdf_report.save()

        return buffer