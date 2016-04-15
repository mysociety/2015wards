from itertools import izip

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
        current_areas = list(add_codes(Area.objects.by_postcode(postcode, generation)))
        new_areas = list(add_codes(Area.objects.by_postcode(postcode, Generation.objects.new())))
        context['old_ward'] = None
        context['new_ward'] = None
        context['ward_has_changed_area'] = False
        context['ward_has_changed_names'] = False
        for area in current_areas:
            if area.type.code in ('LGE', 'COP', 'LBW', 'MTW', 'UTE', 'UTW', 'DIW'):
                context['old_ward'] = area
        for area in new_areas:
            if area.type.code == '16W':
                context['new_ward'] = area
        if context['old_ward'] and context['new_ward']:
            all_polygons_same = True
            old_polygons = list(context['old_ward'].polygons.all())
            new_polygons = list(context['new_ward'].polygons.all())
            # Simpler than doing geometry math, so check first
            if len(new_polygons) != len(old_polygons):
                all_polygons_same = False
            else:
                for old_geometry, new_geometry in izip(old_polygons, new_polygons):
                    old_polygon = old_geometry.polygon
                    new_polygon = new_geometry.polygon
                    area_difference = abs(old_polygon.area - new_polygon.area)
                    # If the areas are within 10sqm of each other, they've
                    # probably not changed in real terms
                    if area_difference > 10:
                        all_polygons_same = False
                        break
            context['ward_has_changed_area'] = not(all_polygons_same)
            context['ward_has_changed_names'] = context['new_ward'].name.lower() != context['old_ward'].name.lower()

        return context
