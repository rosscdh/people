# -*- coding: utf-8 -*-
# signals to handle the sending of signature invitations, when a new DocumentSignature model is created
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Kudos

import user_streams


@receiver(post_save, sender=Kudos)
def save_kudos_signal(sender, **kwargs):
	kudos = kwargs['instance']
	user_streams.add_stream_item(kudos.to_user, '%s has awarded a +%d Kudos to %s'%(kudos.from_user.get_full_name(), kudos.rating, kudos.to_user.get_full_name()), kudos)