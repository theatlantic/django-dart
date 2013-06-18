from coffin.common import env
from coffin.template import Context, dict_from_django_context, Template as CoffinTemplate

import dart.signals as signals

class TemplateWithSignal(CoffinTemplate):

    def render(self, context=None):
        if context is None:
            context = {}
        else:
            context = dict_from_django_context(context)
        assert isinstance(context, dict)  # Required for **-operator.

        # Skip CoffinTemplate.render, and execute its super
        template = type('SimpleObject', (object, ), {})
        template.content = super(CoffinTemplate, self).render(**context)

        signals.template_rendered.send(sender=self, template=template, context=Context(context))
        return template.content


env.template_class = TemplateWithSignal
