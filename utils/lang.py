"""
Ko'p tillilik yordamchi moduli.

Ishlash tartibi:
  GET /api/hotels/?lang=uz  →  O'zbek tili (default)
  GET /api/hotels/?lang=en  →  Ingliz tili
  GET /api/hotels/?lang=ru  →  Rus tili

Agar `lang` parametri berilmasa yoki noto'g'ri bo'lsa — 'uz' ishlatiladi.
"""

SUPPORTED_LANGS = ('uz', 'en', 'ru')
DEFAULT_LANG    = 'uz'


def get_lang(request) -> str:
    """
    So'rovdan tilni aniqlaydi.
    Ustuvorlik: ?lang= → Accept-Language header → default 'uz'
    """
    lang = request.query_params.get('lang', '').lower().strip()
    if lang in SUPPORTED_LANGS:
        return lang

    # Accept-Language headerini tekshirish
    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    for supported in SUPPORTED_LANGS:
        if accept.lower().startswith(supported):
            return supported

    return DEFAULT_LANG


class LangMixin:
    """
    DRF View'larga tilni uzatish uchun mixin.
    Serializer context'iga 'lang' qo'shadi.
    """

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = get_lang(self.request)
        return context
