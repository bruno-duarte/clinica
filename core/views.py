from django.views.generic import TemplateView


class IndexView(TemplateView):
	template_name = 'index.html'


class AboutView(TemplateView):
	template_name = 'about.html'


class ContactView(TemplateView):
	template_name = 'contact.html'


class ElementsView(TemplateView):
	template_name = 'elements.html'


class NewsView(TemplateView):
	template_name = 'news.html'


class ServicesView(TemplateView):
	template_name = 'services.html'