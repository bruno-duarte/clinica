import json

from django.views.generic import TemplateView

from .widgets import _py_datetime_format_to_js


OPTION_KEYS = ('format', 'datepicker', 'timepicker', 'language')


class OptionParser:

    @staticmethod
    def _to_bool(value):
        if 'true' == value.lower():
            return True
        else:
            return False

    @staticmethod
    def parse_format(value):
        return _py_datetime_format_to_js(value)

    @staticmethod
    def parse_timepicker(value):
        return OptionParser._to_bool(value)

    @staticmethod
    def parse_datepicker(value):
        return OptionParser._to_bool(value)


class JSTemplateView(TemplateView):

    template_name = 'datetimepicker/loader.js'

    def get_context_data(self, **kwargs):
        context = super(JSTemplateView, self).get_context_data(**kwargs)

        if 'datetimepicker' not in self.request.GET:
            raise RuntimeError('missing parameter')
        context.update({'input_id': self.request.GET.get('datetimepicker')})

        options = {
            key: getattr(
                OptionParser,
                'parse_{key}'.format(key=key),
                lambda x: x
            )(self.request.GET.get(key))
            for key in OPTION_KEYS
            if key in self.request.GET
        }

        if len(options):
            context.update({'options': json.dumps(options)})

        return context
