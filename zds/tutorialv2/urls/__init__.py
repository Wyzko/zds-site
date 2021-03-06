# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^contenus/', include('zds.tutorialv2.urls.urls_contents', namespace='content')),
                       url(r'^validations/', include('zds.tutorialv2.urls.urls_validations', namespace='validation')),
                       url(r'^tutoriels/', include('zds.tutorialv2.urls.urls_tutorials', namespace='tutorial')),
                       url(r'^articles/', include('zds.tutorialv2.urls.urls_articles', namespace='article')))
