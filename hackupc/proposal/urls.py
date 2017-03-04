# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^list/$',
        view=views.ProposalListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^add/$',
        view=views.ProposalCreateView.as_view(),
        name='create'
    ),
    url(
        regex=r'^detail/(?P<pk>\d+)/$',
        view=views.ProposalDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^delete/(?P<pk>\d+)/$',
        view=views.ProposalDeleteView.as_view(),
        name='delete'
    ),
    url(
        regex=r'^edit/(?P<pk>\d+)/$',
        view=views.ProposalUpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^vote/(?P<pk>\d+)/$',
        view=views.vote_proposal,
        name='vote'
    ),
]
