from urllib.parse import urlencode

from django.urls import reverse


def js_loader_url(fields, input_ids):

    if type(input_ids) == str:
        input_ids = [input_ids]

    results = []
    for input_id in input_ids:
        attrs = fields[input_id].widget.options.copy()
        attrs.update({'datetimepicker': 'id_{id_}'.format(id_=input_id)})
        results.append(
            '{base}?{querystring}'.format(
                base=reverse('datetimepicker-loader'),
                querystring=urlencode(attrs),
            )
        )

    return results
