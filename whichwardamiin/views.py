from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from mapit.models import Area, Generation, Postcode
from mapit.views.areas import add_codes

from .forms import PostcodeForm

class Index(FormView):
    form_class = PostcodeForm
    template_name = 'index.html'

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode'].postcode
        postcode_url = reverse('postcode', kwargs={'postcode': postcode})
        return HttpResponseRedirect(postcode_url)

class Postcode(DetailView):
    model = Postcode
    slug_field = 'postcode'
    slug_url_kwarg = 'postcode'
    context_object_name = 'postcode'
    template_name='postcode.html'

    def get_context_data(self, **kwargs):
        context = super(Postcode, self).get_context_data(**kwargs)
        postcode = self.object
        context['postcode_display'] = postcode.get_postcode_display()
        generation = Generation.objects.current()
        areas = list(add_codes(Area.objects.by_postcode(postcode, generation)))
        context['old_ward'] = None
        context['new_ward'] = None
        context['ward_has_changed'] = False
        context['ward_has_changed_names'] = False
        for area in areas:
            if area.type.code in ('COP', 'LBW', 'LGE', 'MTW', 'UTE', 'UTW', 'DIW'):
                context['old_ward'] = area
            if area.type.code == '15W':
                context['new_ward'] = area
        if context['new_ward'] is not None:
            context['ward_has_changed'] = True
            context['ward_has_changed_names'] = context['new_ward'].name == context['old_ward'].name
        else:
            context['new_ward'] = context['old_ward']

        return context
