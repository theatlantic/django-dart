from django.dispatch import Signal

from dart.ads import AdFactory

template_rendered = Signal(providing_args=["template", "context"])

def process_gpt(sender, **kwargs):
    template = kwargs.get('template')
    context = kwargs.get('context')

    # This should be abstracted out but this would require rewriting the Page()
    # model on cities.
    ads = None
    if 'ads' in context:
        ads = context['ads']
    elif 'page' in context and hasattr(context['page'], 'ads'):
        ads = context['page'].ads

    if isinstance(ads, AdFactory):
        template.content = template.content.replace("<!-- GPT REPLACEMENT BLOCK GOES HERE -->",
            ads.ad_slots, 1)

template_rendered.connect(process_gpt)
