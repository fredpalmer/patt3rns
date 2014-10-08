import re

_UUID_RAW = ur"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
_UUID_SHORT_RAW = ur"[a-f0-9]{13}"
_SLUG = ur"\w[-_\w]*"

URL_PATTERNS = {
    "model": ur"(?P<model>\w+)",
    "uuid": ur"(?P<uuid>%s)" % _UUID_RAW,
    "uuid_short": ur"(?P<uuid>%s)" % _UUID_SHORT_RAW,
    "uuid_or_uuid_short": ur"(?P<uuid>%s|%s)" % (_UUID_RAW, _UUID_SHORT_RAW),
    "slug": ur"(?P<slug>%s)" % _SLUG,
    "pk": ur"(?P<pk>\d+)",
    "object_id": ur"(?P<object_id>\d+)",
    "year": ur"(?P<year>\d+)",
    "month": ur"(?P<month>\d+)",
    "day": ur"(?P<day>\d+)",
    "hour": ur"(?P<hour>\d+)",
    "minute": ur"(?P<minute>\d+)",
    "second": ur"(?P<second>\d+)",
    "date": ur"(?P<date>\d{4}-\d{2}-\d{2})",
    "section": ur"(?P<section>%s)" % _SLUG,
    "subsection": ur"(?P<subsection>%s)" % _SLUG,
}

def sort_nicely(sortable):
    """ Sort the given list in the way that humans expect """

    def alphanum_key(s):
        """
        Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """

        def try_int(val):
            try:
                return int(val)
            except ValueError:
                return val

        return [try_int(c) for c in re.split(r"([0-9]+)", s)]

    sortable.sort(key=alphanum_key)
    return sortable
