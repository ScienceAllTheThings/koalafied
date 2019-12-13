import json

import datetime

from django.db import models

from wagtail.core.models import Page
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from django.shortcuts import render, redirect
from django.http import JsonResponse


class HomePage(Page):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('logo'),
    ]

class DashboardPage(Page):
    pass


class Turbine(models.Model):
    location = models.CharField(
        max_length=255,
    )

    STATUS_CHOICES = (
        ('good', 'Good'),
        ('error', 'Error'),
        ('offline', 'Offline')
    )

    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
    )


    def get_audio(self, timeframe=1):
        now = datetime.datetime.now()
        start = now - datetime.timedelta(minutes=timeframe)

        return Audio.objects.filter(datetime__gte=start)

    def get_anomaly_events(self, timeframe=1):
        return AnomalyEvents.objects.filter(audio__in=self.get_audio(timeframe=timeframe)).all()

    def set_status(self, timeframe=1):

        # Get all audio
        audio = self.get_audio(timeframe=timeframe)
        if len(audio) == 0:
            self.status = 'offline'
            self.save()
            return self.status

        # Get anamaly events for self
        anomaly_events = self.get_anomaly_events(timeframe=timeframe)

        #TODO: Decide between count or percentage
        if len(anomaly_events)/len(audio) >= 0.015:
            self.status = 'error'
            self.save()
            return self.status

        self.status = 'good'
        self.save()
        return self.status


    @property
    def get_status(self, timeframe=1):
        return self.set_status(timeframe=timeframe)



class Audio(models.Model):
    turbine = models.ForeignKey(
        Turbine,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    datetime = models.DateTimeField(
        auto_now_add=True,
    )

    value = models.FloatField()

class AnomalyEvents(models.Model):
    audio = models.ForeignKey(
        Audio,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )


class GetStatusPage(Page):
    def serve(self, request):
        if request.method == 'GET':
            output = request.GET.get('output', 'json')
            turbine = request.GET.get('turbine', None)
            if turbine is None:
                return super().serve(request)
            turbine = Turbine.objects.get(pk=turbine)
            status = turbine.get_status


            if output == 'html':
                print(self.template)
                self.template = 'home/frags/status.html'
                context = super().get_context(request)
                context['status'] = status
                return render(
                    request,
                    self.template,
                    context
                )
            ret = {'status':status}
            return JsonResponse(ret)


        else:
            ret = {'error': "Method {} not supported".format(request.method)}
            return JsonResponse(ret)
