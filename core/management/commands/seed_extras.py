"""Demo data for restaurants and tours."""
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.text import slugify

from restaurants.models import Restaurant, Cuisine
from tours.models import Tour


CUISINES = [
    {'name_uz': "O'zbek oshxonasi", 'name_en': 'Uzbek cuisine', 'name_ru': 'Узбекская кухня', 'icon': '🍛'},
    {'name_uz': 'Xalqaro', 'name_en': 'International', 'name_ru': 'Интернациональная', 'icon': '🌍'},
    {'name_uz': 'Turk', 'name_en': 'Turkish', 'name_ru': 'Турецкая', 'icon': '🥙'},
    {'name_uz': 'Osiyo', 'name_en': 'Asian', 'name_ru': 'Азиатская', 'icon': '🍜'},
    {'name_uz': 'Kafeteriya', 'name_en': 'Cafe', 'name_ru': 'Кафе', 'icon': '☕'},
    {'name_uz': 'Tez ovqat', 'name_en': 'Fast food', 'name_ru': 'Фастфуд', 'icon': '🍔'},
]


RESTAURANTS = [
    {
        'name': 'Khorezm Ark',
        'name_en': 'Khorezm Ark',
        'name_ru': 'Хорезм Арк',
        'description_uz': "An'anaviy o'zbek va xorazm taomlari. Ichan-qal'a ichida joylashgan tarixiy restoran. Shashlik, manty, lag'mon, plov va xorazmning mashhur taomlari.",
        'description_en': 'Traditional Uzbek and Khorezm dishes. Historical restaurant located inside Ichan-Kala. Shashlik, manty, lagman, plov and famous Khorezm dishes.',
        'description_ru': 'Традиционные узбекские и хорезмские блюда. Исторический ресторан внутри Ичан-Калы. Шашлык, манты, лагман, плов и знаменитые хорезмские блюда.',
        'cuisine_names': ["O'zbek oshxonasi"],
        'city': 'khiva',
        'price_range': '$$',
        'rating': 4.7,
        'address': "Ichan-qal'a, Xiva",
        'address_en': 'Ichan-Kala, Khiva',
        'address_ru': 'Ичан-Кала, Хива',
        'latitude': 41.3786,
        'longitude': 60.3592,
        'phone': '+998 61 375 12 34',
        'working_hours': '10:00 - 23:00',
        'has_wifi': True, 'has_parking': True, 'has_outdoor_seating': True,
        'is_halal': True,
        'cover_src': 'bazaar.jpg',
        'is_featured': True,
    },
    {
        'name': 'Terrassa Cafe',
        'name_en': 'Terrassa Cafe',
        'name_ru': 'Терраса Кафе',
        'description_uz': "Ichan-qal'a panoramik manzarasi bilan zamonaviy restoran. Yevropa va o'zbek oshxonasi qo'shilgan menyu.",
        'description_en': 'Modern restaurant with panoramic view of Ichan-Kala. Combined European and Uzbek cuisine menu.',
        'description_ru': 'Современный ресторан с панорамным видом на Ичан-Калу. Смешанная европейская и узбекская кухня.',
        'cuisine_names': ['Xalqaro', 'Kafeteriya'],
        'city': 'khiva',
        'price_range': '$$$',
        'rating': 4.5,
        'address': "Xiva, Ichan-qal'a yaqini",
        'address_en': 'Khiva, near Ichan-Kala',
        'address_ru': 'Хива, рядом с Ичан-Калой',
        'latitude': 41.3790,
        'longitude': 60.3610,
        'phone': '+998 61 375 56 78',
        'working_hours': '08:00 - 23:00',
        'has_wifi': True, 'has_outdoor_seating': True, 'is_vegetarian_friendly': True,
        'is_halal': True,
        'cover_src': 'khiva-main.jpg',
        'is_featured': True,
    },
    {
        'name': 'Mirza Boshi',
        'name_en': 'Mirza Boshi',
        'name_ru': 'Мирза Боши',
        'description_uz': "Xorazmning taniqli an'anaviy restorani. Shivit oshi, manpar va tuxum bar kabi noyob taomlar bor.",
        'description_en': 'Famous traditional Khorezm restaurant. Unique dishes like shivit oshi, manpar, and tuxum bar are available.',
        'description_ru': 'Известный традиционный хорезмский ресторан. Уникальные блюда: шивит оши, манпар, тухум бар.',
        'cuisine_names': ["O'zbek oshxonasi"],
        'city': 'khiva',
        'price_range': '$$',
        'rating': 4.6,
        'address': "Xiva, tarixiy markaz",
        'address_en': 'Khiva, historical center',
        'address_ru': 'Хива, исторический центр',
        'latitude': 41.3788,
        'longitude': 60.3628,
        'phone': '+998 61 375 11 22',
        'working_hours': '11:00 - 22:00',
        'has_wifi': True, 'has_outdoor_seating': True,
        'is_halal': True,
        'cover_src': 'juma-mosque.jpg',
        'is_featured': True,
    },
    {
        'name': 'Caravan Restaurant',
        'name_en': 'Caravan Restaurant',
        'name_ru': 'Ресторан Караван',
        'description_uz': "Ipak yo'li atmosferasida oshxona. O'zbek va turk taomlari.",
        'description_en': 'Dining in Silk Road atmosphere. Uzbek and Turkish cuisine.',
        'description_ru': 'Ужин в атмосфере Шёлкового пути. Узбекская и турецкая кухня.',
        'cuisine_names': ['Turk', "O'zbek oshxonasi"],
        'city': 'urgench',
        'price_range': '$$',
        'rating': 4.3,
        'address': 'Urganch markazi',
        'address_en': 'Urgench center',
        'address_ru': 'Центр Ургенча',
        'latitude': 41.5504,
        'longitude': 60.6301,
        'phone': '+998 62 224 44 55',
        'working_hours': '10:00 - 23:00',
        'has_wifi': True, 'has_parking': True,
        'is_halal': True,
        'cover_src': 'caravan.jpg',
        'is_featured': False,
    },
    {
        'name': 'Bir Lahza Coffee',
        'name_en': 'Bir Lahza Coffee',
        'name_ru': 'Бир Лахза Кофе',
        'description_uz': "Zamonaviy coffee shop. Ixtisoslashgan qahva, smoothie'lar, desertlar.",
        'description_en': 'Modern coffee shop. Specialty coffee, smoothies, desserts.',
        'description_ru': 'Современная кофейня. Специальный кофе, смузи, десерты.',
        'cuisine_names': ['Kafeteriya'],
        'city': 'khiva',
        'price_range': '$',
        'rating': 4.8,
        'address': 'Xiva markazi',
        'address_en': 'Khiva center',
        'address_ru': 'Центр Хивы',
        'latitude': 41.3780,
        'longitude': 60.3615,
        'phone': '+998 61 375 99 00',
        'working_hours': '07:00 - 22:00',
        'has_wifi': True, 'has_outdoor_seating': True, 'is_vegetarian_friendly': True,
        'is_halal': True,
        'cover_src': 'ichan-kala.jpg',
        'is_featured': True,
    },
]


TOURS = [
    {
        'title_uz': "Xiva bir kunlik tur - Ichan-qal'a klassik",
        'title_en': 'Khiva One-Day Tour - Ichan-Kala Classic',
        'title_ru': 'Однодневный тур по Хиве - Ичан-Кала классика',
        'slug': 'khiva-one-day-classic',
        'short_description_uz': "Ichan-qal'a bo'ylab professional gid bilan bir kunlik sayohat. Barcha asosiy obidalar bir kunda.",
        'short_description_en': 'One-day journey through Ichan-Kala with a professional guide. All main monuments in one day.',
        'short_description_ru': 'Однодневное путешествие по Ичан-Кале с профессиональным гидом. Все основные памятники за один день.',
        'description_uz': "Xivaning tarixiy qismi bo'lgan Ichan-qal'a bo'ylab to'liq ekskursiya. Kalta Minor, Ko'hna Ark, Juma masjidi, Islom Xo'ja minorasi va madrasalar bilan tanishasiz. Tarix va madaniyat bilan to'yingan 6 soatlik sayohat.",
        'description_en': 'Full excursion through Ichan-Kala, the historical part of Khiva. You will get acquainted with Kalta Minor, Kuhna Ark, Juma Mosque, Islam Khodja Minaret and madrasahs. A 6-hour journey filled with history and culture.',
        'description_ru': 'Полная экскурсия по Ичан-Кале, исторической части Хивы. Вы познакомитесь с Кальта Минар, Кухна Арк, Пятничной мечетью, минаретом Ислама Ходжи и медресе.',
        'itinerary_uz': "09:00 - Tushlikdan oldin boshlash\n10:00 - Ichan-qal'aga kirish\n10:30 - Kalta Minor minorasi\n11:30 - Ko'hna Ark saroyi\n13:00 - Tushlik\n14:30 - Juma masjidi\n15:30 - Islom Xo'ja minorasi\n16:30 - Mahalliy bozor\n17:30 - Tur yakuni",
        'itinerary_en': "09:00 - Start before lunch\n10:00 - Enter Ichan-Kala\n10:30 - Kalta Minor\n11:30 - Kuhna Ark\n13:00 - Lunch\n14:30 - Juma Mosque\n15:30 - Islam Khodja\n16:30 - Local market\n17:30 - End of tour",
        'itinerary_ru': "09:00 - Начало\n10:00 - Ичан-Кала\n10:30 - Кальта Минар\n11:30 - Кухна Арк\n13:00 - Обед\n14:30 - Пятничная мечеть\n15:30 - Ислам Ходжа\n16:30 - Рынок\n17:30 - Конец тура",
        'cover_src': 'ichan-kala.jpg',
        'price': 450000,
        'duration': 8,
        'duration_type': 'hours',
        'difficulty': 'easy',
        'max_people': 15,
        'includes_uz': "Professional gid, kirish biletlari, tushlik, transport",
        'includes_en': 'Professional guide, entrance tickets, lunch, transport',
        'includes_ru': 'Профессиональный гид, входные билеты, обед, транспорт',
        'excludes_uz': 'Shaxsiy xarajatlar, chayon pullari',
        'excludes_en': 'Personal expenses, tips',
        'excludes_ru': 'Личные расходы, чаевые',
        'meeting_point_uz': "Xiva markaziy maydoni, Ichan-qal'a old tomoni",
        'meeting_point_en': 'Khiva central square, in front of Ichan-Kala',
        'meeting_point_ru': 'Центральная площадь Хивы, перед Ичан-Калой',
        'is_featured': True,
        'rating': 4.8,
    },
    {
        'title_uz': "Xorazm 3 kunlik premium tur",
        'title_en': 'Khorezm 3-Day Premium Tour',
        'title_ru': 'Премиум тур по Хорезму на 3 дня',
        'slug': 'khorezm-3-day-premium',
        'short_description_uz': "Xiva + qadimiy Khorezm qasrlari + Oraol dengizi. Premium darajali tur.",
        'short_description_en': 'Khiva + ancient Khorezm fortresses + Aral Sea. Premium-level tour.',
        'short_description_ru': 'Хива + древние крепости Хорезма + Аральское море. Премиум-тур.',
        'description_uz': "3 kunlik to'liq Xorezm sayohati. Xiva, qadimiy qasrlarning sahro safari va Oraol dengizi tomon sayohat. Professional gid, 4-5 yulduzli mehmonxona, barcha ovqatlar bilan.",
        'description_en': 'Full 3-day Khorezm trip. Khiva, desert safari of ancient fortresses, and journey to Aral Sea. Professional guide, 4-5 star hotels, all meals included.',
        'description_ru': 'Полное 3-дневное путешествие по Хорезму. Хива, пустынное сафари древних крепостей и поездка к Аральскому морю.',
        'cover_src': 'aral-sea.jpg',
        'price': 3500000,
        'duration': 3,
        'duration_type': 'days',
        'difficulty': 'medium',
        'max_people': 10,
        'includes_uz': "3 kun mehmonxona, barcha ovqatlar, transport 4x4, gid, kirish biletlari",
        'includes_en': '3 nights hotel, all meals, 4x4 transport, guide, entrance tickets',
        'includes_ru': '3 ночи в отеле, все блюда, транспорт 4x4, гид, билеты',
        'excludes_uz': 'Parvoz, shaxsiy xarajatlar',
        'excludes_en': 'Flight, personal expenses',
        'excludes_ru': 'Перелёт, личные расходы',
        'meeting_point_uz': 'Urganch xalqaro aeroporti',
        'meeting_point_en': 'Urgench International Airport',
        'meeting_point_ru': 'Международный аэропорт Ургенча',
        'is_featured': True,
        'rating': 4.9,
    },
    {
        'title_uz': "Ichan-qal'a yarim kunlik promenade",
        'title_en': 'Ichan-Kala Half-Day Promenade',
        'title_ru': 'Ичан-Кала полудневная прогулка',
        'slug': 'ichan-kala-halfday',
        'short_description_uz': "3 soatlik qisqa ekskursiya - asosiy diqqatga sazovor joylar.",
        'short_description_en': '3-hour short excursion - main attractions.',
        'short_description_ru': '3-часовая короткая экскурсия - основные достопримечательности.',
        'description_uz': "Vaqti chegaralangan sayyohlar uchun. 3 soatda Ichan-qal'aning eng muhim obidalari bilan tanishish.",
        'description_en': 'For time-limited travelers. Get acquainted with the most important monuments of Ichan-Kala in 3 hours.',
        'description_ru': 'Для туристов с ограниченным временем. За 3 часа познакомьтесь с важнейшими памятниками Ичан-Калы.',
        'cover_src': 'kalta-minor.jpg',
        'price': 180000,
        'duration': 3,
        'duration_type': 'hours',
        'difficulty': 'easy',
        'max_people': 20,
        'includes_uz': "Gid, kirish biletlari",
        'includes_en': 'Guide, entrance tickets',
        'includes_ru': 'Гид, входные билеты',
        'meeting_point_uz': "Ichan-qal'a G'arbiy darvoza",
        'meeting_point_en': 'Ichan-Kala West Gate',
        'meeting_point_ru': 'Западные ворота Ичан-Калы',
        'is_featured': False,
        'rating': 4.5,
    },
]


class Command(BaseCommand):
    help = "Restaurants va tours uchun demo data"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        images_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'frontend' / 'public' / 'images'
        
        if options['clear']:
            Cuisine.objects.all().delete()
            Restaurant.objects.all().delete()
            Tour.objects.all().delete()
            self.stdout.write(self.style.WARNING("Clear OK"))

        # Cuisines
        cuisine_map = {}
        for data in CUISINES:
            c, _ = Cuisine.objects.get_or_create(name_uz=data['name_uz'], defaults=data)
            cuisine_map[data['name_uz']] = c
        self.stdout.write(self.style.SUCCESS(f"Cuisines: {len(cuisine_map)}"))

        # Restaurants
        for data in RESTAURANTS:
            cuisine_names = data.pop('cuisine_names')
            cover_src = data.pop('cover_src')
            
            if Restaurant.objects.filter(name=data['name']).exists():
                self.stdout.write(f"  Skip: {data['name']}")
                continue

            rest = Restaurant.objects.create(**data)
            for cname in cuisine_names:
                if cname in cuisine_map:
                    rest.cuisines.add(cuisine_map[cname])
            
            # Cover image
            img_path = images_dir / cover_src
            if img_path.exists():
                from restaurants.models import RestaurantImage
                with open(img_path, 'rb') as f:
                    img = RestaurantImage(restaurant=rest, is_cover=True, order=0)
                    img.image.save(f'{rest.id}_{cover_src}', File(f), save=True)
            
            self.stdout.write(self.style.SUCCESS(f"  + Restaurant: {rest.name}"))

        # Tours
        for data in TOURS:
            cover_src = data.pop('cover_src')
            
            if Tour.objects.filter(slug=data['slug']).exists():
                self.stdout.write(f"  Skip tour: {data['slug']}")
                continue

            img_path = images_dir / cover_src
            tour = Tour(**data)
            if img_path.exists():
                with open(img_path, 'rb') as f:
                    tour.cover_image.save(f"{data['slug']}.jpg", File(f), save=False)
            tour.save()
            self.stdout.write(self.style.SUCCESS(f"  + Tour: {tour.title_uz}"))

        self.stdout.write(self.style.SUCCESS("\nTayyor!"))
