import hashlib
import secrets
from django.utils import timezone
from datetime import timedelta
from mintcastiq.models.fact_users_otp import FactUserOTP

class OTPService:

    @staticmethod
    def generate_otp(user, delivery_method="sms", ttl_minutes=5):
        raw_code = f"{secrets.randbelow(999999):06d}"
        otp_hash = hashlib.sha256(raw_code.encode()).hexdigest()

        expires_at = timezone.now() + timedelta(minutes=ttl_minutes)

        FactUserOTP.objects.create(
            user=user,
            otp_hash=otp_hash,
            delivery_method=delivery_method,
            expires_at=expires_at,
        )

        return raw_code  # send this to the user

    @staticmethod
    def validate_otp(user, submitted_code):
        otp_hash = hashlib.sha256(submitted_code.encode()).hexdigest()

        otp = (
            FactUserOTP.objects
            .filter(user=user, otp_hash=otp_hash, consumed_at__isnull=True)
            .order_by("-created_at")
            .first()
        )

        if not otp:
            return False

        if otp.expires_at < timezone.now():
            return False

        otp.consumed_at = timezone.now()
        otp.save(update_fields=["consumed_at"])

        return True
