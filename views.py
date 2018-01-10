from django.shortcuts import render

# Create your views here.
from django.template.backends import django
from django.views.generic import TemplateView

from DecissionsApp import models


class home_view(TemplateView):
    template_name = 'homeview.html'
    # way to load a model
    user = models.UserProfile()

    # def sum_query(self):
    #     Query_result = self.issue.objects.values(‘delta_time’).
    #     aggregate(total_deltatime=Coalesce(Sum(‘delta_time’), 0))
    #     return query_result[‘total_deltatime’]

    # regex in view
    # def strip_header(self, ticket_name):
    #     return re.sub(“-[0 - 9] +”, ‘’, ticket_name)

    def get_context_data(self, **kwargs):
        context = super(home_view, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context


class user_profile_view(TemplateView):
    template_name = 'userprofileview.html'
    user = models.UserProfile()
    user_to_questions = models.UserToQuestions()

    def get_context_data(self, **kwargs):
        context = super(user_profile_view, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['usertoquestions'] = self.user_to_questions
        return context


class question_creator_view(TemplateView):
    template_name = 'questioncreatorview.html'
    question = models.Question()

    def get_context_data(self, **kwargs):
        context = super(question_creator_view, self).get_context_data(**kwargs)
        context['question'] = self.question
        return context


class data_view(TemplateView):
    template_name = 'dataview.html'
    data = models.Data()

    def get_context_data(self, **kwargs):
        context = super(data_view, self).get_context_data(**kwargs)
        context['data'] = self.data
        return context


