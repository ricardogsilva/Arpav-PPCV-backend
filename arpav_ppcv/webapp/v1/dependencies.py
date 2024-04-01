from typing import Annotated

import django
from django.conf import settings as django_settings
from fastapi import Depends

from ... import config
from ..legacy.django_settings import get_custom_django_settings
from ..dependencies import get_settings


async def load_django(
        settings: Annotated[config.ArpavPpcvSettings, Depends(get_settings)]
):
    custom_django_settings = get_custom_django_settings(settings)
    django_settings.configure(**custom_django_settings)
    django.setup()
