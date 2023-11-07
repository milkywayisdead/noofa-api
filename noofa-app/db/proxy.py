import io

from .models import Profile, Dashboard
from ..profiles.utils import DfPreparer

from noofa.utils import get_df_descriptor, PdfReport


class ProfileProxy(Profile):    
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
    
    def to_dict(self):
        profile_dict = {}
        for attr in [
            'id', 'name', 'description',
            'created', 'last_update',
            'sources', 'queries', 'dataframes',
            'components', 'docs', 'values',
        ]:
            profile_dict[attr] = getattr(self, attr)

        profile_dict['dashboards'] = {
            dash.contextual_id: dash.to_dict() for dash in self.dashboards
        }

        return profile_dict
    

class DashboardProxy(Dashboard):
    def get_widget_data(self, widgetId):
        widget = self.widgets[widgetId]
        rb = self.profile.get_report_builder()

        widget_data = None
        w_type = widget['type']

        if w_type == 'text':
            value = widget['props']['text']
            if widget['props']['interprete']:
                widget_data = rb.evaluate(value)
            else:
                widget_data = value

        elif w_type == 'table':
            table_id = widget['props']['tableId']
            table = rb.build_table(table_id)
            df = table.df
            desc = get_df_descriptor(df)
            prep = DfPreparer(df)
            widget_data = {
                'data': prep.records,
                'columns': desc.columns,
                'dtypes': desc.dtypes,
            }

        elif w_type == 'figure':
            figure = rb.build_figure(widget['props']['figureId'])
            widget_data = figure.to_dict()

        return widget_data