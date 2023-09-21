from .models import Profile

from noofa import ReportBuilder


class ProfileProxy(Profile):
    def get_report_builder(self):
        rb = ReportBuilder(
            data_config=self.data_config,
            components_config=self.components,
        )
        return rb
    
    @property
    def data_config(self):
        return {
            'sources': self.sources,
            'queries': self.queries,
            'dataframes': self.dataframes,
        }