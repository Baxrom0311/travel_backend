from django.core.management.base import BaseCommand
from testimonials.models import Testimonial


SEED_DATA = [
    {
        'name': 'Sarah Johnson',
        'country': 'United States',
        'role': 'Tourist',
        'rating': 5,
        'text_en': "Khiva was absolutely magical! The ancient Ichan-Kala is like stepping into a fairytale. Our guide was fantastic and the hotels are surprisingly modern while keeping traditional charm.",
        'text_uz': "Xiva haqiqatdan ham sehrli edi! Qadimiy Ichan-Qal'a ertakka qadam tashlagandek tuyuldi. Bizning gid ajoyib edi va mehmonxonalar hayratlanarli darajada zamonaviy.",
        'text_ru': "Хива была абсолютно волшебной! Древняя Ичан-Кала как из сказки. Наш гид был фантастическим, отели современные.",
        'is_featured': True,
        'order': 1,
    },
    {
        'name': 'Марина Петрова',
        'country': 'Россия',
        'role': 'Блогер',
        'rating': 5,
        'text_ru': "Хорезм превзошёл все ожидания! Кальта Минор, Джума-мечеть, и местная кухня — это то, что нужно обязательно испытать. Настоящая жемчужина Узбекистана.",
        'text_uz': "Xorazm barcha kutilganlardan ham yaxshi chiqdi! Kalta Minor, Juma masjidi va mahalliy taom — bularni albatta sinab ko'rish kerak. Haqiqiy O'zbekiston injuso'i.",
        'text_en': "Khorezm exceeded all expectations! Kalta Minor, Juma Mosque, and local cuisine are must-tries. A true gem of Uzbekistan.",
        'is_featured': True,
        'order': 2,
    },
    {
        'name': 'Hans Mueller',
        'country': 'Germany',
        'role': 'Photographer',
        'rating': 5,
        'text_en': "As a photographer, Khiva is a paradise. The architecture, the light, the colors — every corner is frame-worthy. UNESCO protected and for good reason!",
        'text_uz': "Fotograf sifatida, Xiva — jannat. Me'morchilik, yorug'lik, ranglar — har bir burchak rasmga loyiq. UNESCO himoyasi bejiz emas!",
        'text_ru': "Как фотограф, Хива — рай. Архитектура, свет, цвета — каждый уголок достоин кадра. ЮНЕСКО под защитой не зря!",
        'is_featured': True,
        'order': 3,
    },
    {
        'name': 'Akmal Yusupov',
        'country': "O'zbekiston",
        'role': 'Turist',
        'rating': 5,
        'text_uz': "Xivada bo'lib turgan har safargi tashrifim — alohida tajriba. Kalta Minor va Juma masjidi hayratlantiradi. Xiva mehmondo'st, arzon va qulay!",
        'text_en': "Every visit to Khiva is a unique experience. Kalta Minor and Juma Mosque are amazing. Khiva is hospitable, affordable, and convenient!",
        'text_ru': "Каждый визит в Хиву — уникальный опыт. Кальта Минор и Джума-мечеть впечатляют. Хива гостеприимна, доступна и удобна!",
        'is_featured': True,
        'order': 4,
    },
    {
        'name': 'Yuki Tanaka',
        'country': 'Japan',
        'role': 'Historian',
        'rating': 5,
        'text_en': "The Silk Road history comes alive in Khiva. The preservation of the old city is remarkable. Friendly locals, great food, and incredible history. Highly recommend!",
        'text_uz': "Ipak Yo'li tarixi Xivada jonlanadi. Eski shaharning saqlanishi ajoyib. Mehmondo'st aholi, mazali taom va ajoyib tarix. Tavsiya qilaman!",
        'text_ru': "История Шёлкового пути оживает в Хиве. Сохранение старого города поразительно. Дружелюбные жители, вкусная еда, невероятная история. Рекомендую!",
        'is_featured': True,
        'order': 5,
    },
]


class Command(BaseCommand):
    help = "5 ta default testimonialni yuklaydi"
    
    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')
    
    def handle(self, *args, **options):
        if options['clear']:
            Testimonial.objects.all().delete()
            self.stdout.write(self.style.WARNING("Eski sharhlar o'chirildi"))
        
        count = 0
        for data in SEED_DATA:
            obj, created = Testimonial.objects.get_or_create(
                name=data['name'],
                defaults=data,
            )
            if created:
                count += 1
                self.stdout.write(f'  + {obj.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nTayyor: {count} ta yangi sharh'))
