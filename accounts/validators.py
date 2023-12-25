import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r"^[a-zA-Z]+\/(...)\/(....)"
    message = _(
        "Enter a valid username. This value may contain only English letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = re.ASCII
