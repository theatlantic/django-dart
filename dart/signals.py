import json

from django.dispatch import Signal

from dart.ads import AdFactory

template_rendered = Signal(providing_args=["template", "context"])

def process_gpt(sender, **kwargs):
    template = kwargs.get('template')
    context = kwargs.get('context')

    if 'ads' in context and isinstance(context['ads'], AdFactory):
        template.content = template.content.replace("<!-- GPT REPLACEMENT BLOCK GOES HERE -->",
            json.dumps(context['ads'].ad_slots), 1)

template_rendered.connect(process_gpt)
