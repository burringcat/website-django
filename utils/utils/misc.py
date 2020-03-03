import time
import subprocess
import uuid
from base64 import b64encode
import markdown
from posix import urandom
from unidecode import unidecode
from django.contrib.gis.geoip2 import GeoIP2
from django.utils.text import slugify as dj_slugify
from django.conf import settings
from django.template import Template, Context


def process_han_characters(s):
    if settings.HAN_CHARACTER_SLUG_STYLE == 'as-is':
        return s
    if settings.HAN_CHARACTER_SLUG_STYLE == 'Pinyin':
        return unidecode(s)
    else:
        raise NotImplemented


def slugify(s):
    s = process_han_characters(s)
    slug = dj_slugify(s,
                      allow_unicode=settings.HAN_CHARACTER_SLUG_STYLE == 'as-is')
    slug += '-' + str(int(time.time()))
    return slug


class ObjectDict(dict):
    def __getattr__(self, name):
        print(name, self[name])
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value


def gen_page_range(paginated, side_range=5):
    min_page = max(1, paginated.number - side_range)
    max_page = min(paginated.number + side_range, paginated.paginator.num_pages)
    return range(min_page, max_page + 1)


def iter_cmd_output(cmd, is_binary=True, is_module=True):
    if is_module:
        cmd = ['python', '-m'] + cmd
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE
    )
    while True:
        out = process.stdout.read(1024 * 128)
        if not out and process.poll() is not None:
            break
        if is_binary is False:
            out = str(out, encoding='utf-8')
        yield out


def uuid4_str():
    return str(uuid.uuid4())


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def get_country(ip4: str):
    g = GeoIP2()
    result = g.country(ip4)
    return {'code': result.get('country_code'), 'name': result.get('country_name')}


def gen_random_str(length: int):
    b = urandom(length)
    k = b64encode(b)
    return str(k, encoding='utf8')


def md2h5(md, extensions=('fenced_code',), context=None):
    result = markdown.markdown(md, output_format='html5', extensions=extensions)
    if context and isinstance(context, dict):
        result = Template(result).render(Context(context))
    return result


def timestamp_str():
    return str(time.time()).replace('.', '')


def get_site_config():
    return [
        (settings.LANGUAGE_COOKIE_NAME,
         settings.LANGUAGES_DICT.keys(),
         settings.LANGUAGES_DICT.keys()),
    ] + [(c, settings.YN, settings.TRANS_YN) for c in settings.CONFIGURABLES]
