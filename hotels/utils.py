import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_booking_confirmation(booking):
    """Send booking confirmation email to user (best-effort)."""
    try:
        send_mail(
            subject=f'[Visit Khorezm] Bron tasdiqlandi #{booking.id}',
            message=(
                f"Hurmatli {booking.guest_name},\n\n"
                f"Sizning broningiz qabul qilindi:\n"
                f"Mehmonxona: {booking.hotel.name}\n"
                f"Kirish: {booking.check_in}\n"
                f"Chiqish: {booking.check_out}\n"
                f"Mehmonlar: {booking.guests}\n"
                f"Narx: {booking.total_price:,} so'm\n\n"
                f"Rahmat!\nVisit Khorezm jamoasi"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.user.email],
            fail_silently=True,
        )
    except Exception as e:
        logger.warning(f'Booking confirmation email failed: {e}')
