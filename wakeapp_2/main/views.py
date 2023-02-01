from django.views.generic import CreateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from wakeapp_2.main.models import Event, EventVisibility

class DashboardView(TemplateView):
    template_name = 'main/dashboard.html'


class DesignView(TemplateView):
    template_name = 'main/design.html'


class CreateEventView(CreateView):
    model = Event
    fields = ('name', 'visible_to', 'location', 'date', 'friends')
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_detail')


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.creator == request.user or self.object.visible_to.filter(pk=request.user.pk).exists():
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return render(request, '404.html', status=404)
