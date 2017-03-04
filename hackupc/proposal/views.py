from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView

from hackupc.users.models import User
from .models import Proposal, ProposalVote
from .forms import ProposalForm


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_add.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('proposals:detail', kwargs={'pk': self.object.pk})


class ProposalDetailView(LoginRequiredMixin, DetailView):
    model = Proposal
    template_name = 'proposals/proposal_detail.html'


class ProposalUpdateView(LoginRequiredMixin, UpdateView):

    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_edit.html'

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('proposals:detail', kwargs={'pk': self.object.pk})


class ProposalListView(LoginRequiredMixin, ListView):
    model = Proposal
    template_name = 'proposals/proposal_list.html'

    def get_queryset(self):
        return Proposal.objects.filter(created_by=self.request.user)


class ProposalDeleteView(LoginRequiredMixin, DeleteView):
    model = Proposal

    def get_success_url(self):
        return reverse('proposals:list')


class HomeView(LoginRequiredMixin, ListView):
    model = Proposal
    template_name = 'pages/home.html'


def vote_proposal(request, pk):
    prop = Proposal.objects.get(pk=pk)
    user = User.objects.get(pk=int(request.POST['voter_id']))
    ProposalVote.objects.create(proposal=prop, user=user)
    return HttpResponse()


