import logging
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.translation import activate, gettext as _
from django.conf import settings
import uuid

logger = logging.getLogger(__name__)

def send_verification_email(user):
    if not user.email_verification_token:
        user.email_verification_token = str(uuid.uuid4())
        user.save(update_fields=['email_verification_token'])
    
    verification_url = reverse('verify-email', kwargs={'token': user.email_verification_token})
    verification_link = f"{settings.SITE_URL}{verification_url}"
    
    activate(user.language)
    subject = _('Vérifiez votre adresse e-mail')
    message = _(
        'Bonjour,\n\n'
        'Merci de vous être inscrit sur notre site. '
        'Pour compléter votre inscription, veuillez cliquer sur le lien suivant :\n\n'
        '{verification_link}\n\n'
        'Si vous n\'avez pas demandé cette inscription, vous pouvez ignorer cet e-mail.\n\n'
        'Cordialement,\n'
        'L\'équipe BATIMARTPRO'
    ).format(verification_link=verification_link)
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Verification email sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        raise