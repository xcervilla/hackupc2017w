# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import requests
from base64 import b64decode
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=False, max_length=255)
    surname = models.CharField(blank=False, max_length=255)

    document_id = models.CharField(max_length=50)

    is_validated = models.BooleanField(default=False)

    sign_photo = models.ImageField()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @staticmethod
    def validations_check(validations):
        if validations['test_correspondence_visible_mrz_id_number'] != 'ok':
            return False
        if validations['test_correspondence_visible_mrz_name'] != 'ok':
            return False
        if validations['test_correspondence_visible_mrz_surname'] != 'ok':
            return False
        if validations['test_mrz_global_integrity'] != 'ok':
            return False
        if validations['test_global_authenticity_value'] != 'ok':
            return False
        aut_ratio = float(validations['test_global_authenticity_ratio'])
        if aut_ratio < 0.95:
            return False
        return True

    def validate_id(self, frontal_photo, back_photo):
        signaturit_url = 'https://api.sandbox.signaturit.com/v3/photoid/validate.json'
        headers = {'Authorization': 'Bearer ' + settings.SIGNATURIT_TOKEN}
        files = {'front': frontal_photo,
                 'back': back_photo}
        r = requests.post(signaturit_url, files=files, headers=headers)
        response = r.json()

        if User.validations_check(response['validations']):
            self.name = response['data']['name'].title()
            self.surname = response['data']['surname'].title()
            self.document_id = response['data']['id_number']
            signature_data = b64decode(response['signature'])
            self.sign_photo = ContentFile(signature_data, self.document_id+'.png')
            self.is_validated = True
            self.save()
            return True
        return False


