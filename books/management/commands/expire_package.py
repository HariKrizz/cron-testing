from django.db import connection
from garages.models import Package, StatusChoice, PackageServiceMapping, ServicePricing
from datetime import date, datetime


def expire_packages():
    """
    Marks packages as expired if their end date is before today.
    """
    today = date.today()

    expired_packages = Package.objects.filter(
                            end_date__lt=today, status=StatusChoice.ACTIVE)

    for package in expired_packages:
        PackageServiceMapping.objects.filter(
            package=package, status=StatusChoice.ACTIVE).update(
                                                status=StatusChoice.EXPIRED)
        
        ServicePricing.objects.filter(
            package=package, status=StatusChoice.ACTIVE).update(
                                                status=StatusChoice.EXPIRED)

    count = expired_packages.update(status=StatusChoice.EXPIRED)

    connection.close_if_unusable_or_obsolete()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if count > 0:
        print(f"[{now}] Marked {count} packages as EXPIRED.")
    else:
        print(f"[{now}] No packages expired.")