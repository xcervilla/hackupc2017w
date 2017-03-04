from django.forms import ModelForm
from .models import Proposal


class ProposalForm(ModelForm):

    class Meta:
        model = Proposal
        fields = ('title', 'description', 'image')
