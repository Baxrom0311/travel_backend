"""
Management command: Events va News uchun demo ma'lumotlar yuklash.

Usage:
    python manage.py seed_demo_data
    python manage.py seed_demo_data --clear
"""
from datetime import date, timedelta, time
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils import timezone
from events.models import Event
from news.models import News


EVENTS = [
    {
        'title_uz': 'Xiva xalqaro ipak va ziravorlar festivali 2024',
        'title_en': 'Khiva International Silk and Spices Festival 2024',
        'title_ru': 'Международный фестиваль шёлка и специй в Хиве 2024',
        'description_uz': 'Har yili o\'tkaziladigan eng yirik tadbir. Ichan-qal\'a bo\'ylab milliy kiyimlar, hunarmandchilik, ovqatlar va an\'anaviy musiqa namoyish etiladi. Dunyoning turli burchaklaridan hunarmandlar, sayyohlar va san\'atkorlar ishtirok etadi.',
        'description_en': 'The largest annual event. Throughout Ichan-Kala, national costumes, handicrafts, food, and traditional music are showcased. Craftsmen, tourists, and artists from around the world participate.',
        'description_ru': 'Крупнейшее ежегодное мероприятие. По всей Ичан-Кале представлены национальные костюмы, ремёсла, еда и традиционная музыка. Участвуют ремесленники, туристы и артисты со всего мира.',
        'cover_image_src': 'bazaar.jpg',
        'start_date': date.today() + timedelta(days=30),
        'end_date': date.today() + timedelta(days=33),
        'start_time': time(10, 0),
        'location_uz': "Ichan-qal'a, Xiva",
        'location_en': 'Ichan-Kala, Khiva',
        'location_ru': 'Ичан-Кала, Хива',
        'latitude': 41.3786,
        'longitude': 60.3592,
        'is_free': True,
        'is_featured': True,
    },
    {
        'title_uz': 'Navro\'z bayrami — qadimiy an\'analar kuni',
        'title_en': 'Navruz Festival — Day of Ancient Traditions',
        'title_ru': 'Праздник Навруз — день древних традиций',
        'description_uz': 'Xorazm xalqining eng muqaddas bayramlaridan biri. Sumalak tayyorlash, xalq o\'yinlari, kurash musobaqalari, va an\'anaviy raqslar. Ichan-qal\'ada maxsus konsert va ertalab uchun milliy taomlar.',
        'description_en': 'One of the most sacred holidays of the Khorezm people. Sumalak preparation, folk games, wrestling competitions, and traditional dances. Special concert at Ichan-Kala and national dishes for breakfast.',
        'description_ru': 'Один из самых священных праздников хорезмцев. Приготовление сумаляка, народные игры, борьба, традиционные танцы. Специальный концерт в Ичан-Кале и национальные блюда.',
        'cover_image_src': 'caravan.jpg',
        'start_date': date(date.today().year + 1, 3, 21),
        'end_date': None,
        'start_time': time(8, 0),
        'location_uz': 'Xiva, Xorazm',
        'location_en': 'Khiva, Khorezm',
        'location_ru': 'Хива, Хорезм',
        'latitude': 41.3786,
        'longitude': 60.3592,
        'is_free': True,
        'is_featured': True,
    },
    {
        'title_uz': 'Xorazm hunarmandchilik ko\'rgazmasi',
        'title_en': 'Khorezm Craftsmanship Exhibition',
        'title_ru': 'Выставка хорезмских ремёсел',
        'description_uz': 'Xorazmning mashhur kulolchilik, gilam to\'qish, metall ishlari va yog\'och o\'ymakorligi ustalari bilan tanishing. Mahalliy hunarmandlar mahsulotlarini namoyish etadilar va sotadilar.',
        'description_en': 'Meet the famous masters of pottery, carpet weaving, metalwork, and wood carving in Khorezm. Local craftsmen display and sell their products.',
        'description_ru': 'Познакомьтесь с мастерами гончарного дела, ткачества, металлообработки и резьбы по дереву. Местные ремесленники демонстрируют и продают свои изделия.',
        'cover_image_src': 'khorezm-palace.jpg',
        'start_date': date.today() + timedelta(days=15),
        'end_date': date.today() + timedelta(days=17),
        'start_time': time(11, 0),
        'location_uz': 'Urganch markazi',
        'location_en': 'Urgench center',
        'location_ru': 'Центр Ургенча',
        'latitude': 41.5504,
        'longitude': 60.6301,
        'is_free': False,
        'price': 50000,
        'is_featured': True,
    },
    {
        'title_uz': 'Ramazon bayrami — Iftorlik kechalari',
        'title_en': 'Ramadan — Iftar Nights',
        'title_ru': 'Рамадан — вечера ифтара',
        'description_uz': 'Muqaddas Ramazon oyida Xiva ko\'chalarida maxsus iftorlik kechalari. An\'anaviy taomlar, duo qilish marosimlari va ruhiy musiqa.',
        'description_en': 'Special iftar evenings on the streets of Khiva during the holy month of Ramadan. Traditional dishes, prayer ceremonies, and spiritual music.',
        'description_ru': 'Особые вечера ифтара на улицах Хивы в священный месяц Рамадан. Традиционные блюда, молитвы и духовная музыка.',
        'cover_image_src': 'juma-mosque.jpg',
        'start_date': date.today() + timedelta(days=60),
        'end_date': date.today() + timedelta(days=90),
        'start_time': time(19, 0),
        'location_uz': "Juma masjidi, Ichan-qal'a",
        'location_en': 'Juma Mosque, Ichan-Kala',
        'location_ru': 'Пятничная мечеть, Ичан-Кала',
        'latitude': 41.3783,
        'longitude': 60.3625,
        'is_free': True,
        'is_featured': False,
    },
]


NEWS = [
    {
        'title_uz': "Xiva UNESCO jahon merosi bo'yicha yangi tan olishga sazovor bo'ldi",
        'title_en': 'Khiva receives new UNESCO World Heritage recognition',
        'title_ru': 'Хива получила новое признание ЮНЕСКО',
        'slug': 'khiva-unesco-new-recognition-2024',
        'excerpt_uz': "Ichan-qal'a muzeyi 2024-yilda UNESCO tomonidan yana bir bor tan olindi. Yangi reytingda Xiva jahondagi eng yaxshi saqlangan qadimiy shaharlar ro'yxatiga kirdi.",
        'excerpt_en': 'Ichan-Kala museum has been recognized again by UNESCO in 2024. In the new ranking, Khiva has been included in the list of the best-preserved ancient cities in the world.',
        'excerpt_ru': 'Музей Ичан-Кала вновь признан ЮНЕСКО в 2024 году. В новом рейтинге Хива вошла в список лучше всего сохранившихся древних городов мира.',
        'content_uz': 'UNESCO Xiva shahrining noyob meʼmoriy yodgorliklarini saqlash sohasidagi ishlarini yuqori baholadi. Kalta Minor, Ko\'hna Ark, Juma masjidi va Islom Xo\'ja minorasi kabi tarixiy obidalar asrlar davomida o\'zining asl ko\'rinishini saqlab kelmoqda.\n\nO\'tgan yil davomida Xiva shahrini 450,000 dan ortiq sayyoh tashrif buyurgan. Bu son o\'tgan yilga nisbatan 35% ga oshgan. Shahar hokimiyati yangi turizm infratuzilmasini rivojlantirish bo\'yicha ko\'plab loyihalarni amalga oshirmoqda.',
        'content_en': 'UNESCO highly appreciated the work of the city of Khiva in preserving unique architectural monuments. Historical monuments such as Kalta Minor, Kuhna Ark, Juma Mosque and Islam Khodja Minaret have preserved their original appearance for centuries.\n\nOver the past year, more than 450,000 tourists have visited the city of Khiva. This number is 35% higher than the previous year. The city administration is implementing many projects to develop new tourism infrastructure.',
        'content_ru': 'ЮНЕСКО высоко оценил работу города Хивы по сохранению уникальных архитектурных памятников. Исторические памятники, такие как Кальта Минар, Кухна Арк, Пятничная мечеть и минарет Ислама Ходжи, сохраняли свой первоначальный облик на протяжении веков.\n\nЗа прошедший год Хиву посетили более 450 000 туристов. Это число на 35% больше, чем в предыдущем году.',
        'cover_image_src': 'ichan-kala.jpg',
        'author': 'Visit Khorezm Team',
        'is_featured': True,
    },
    {
        'title_uz': 'Xorazmda yangi xalqaro aeroport terminali ochildi',
        'title_en': 'New international airport terminal opened in Khorezm',
        'title_ru': 'В Хорезме открыт новый международный терминал аэропорта',
        'slug': 'khorezm-new-airport-terminal-2024',
        'excerpt_uz': 'Urganch xalqaro aeroportida zamonaviy terminal faoliyati boshlandi. Yillik o\'tkazuvchanligi 2 million yo\'lovchi. Yangi aviayo\'nalishlar ham rejalashtirilgan.',
        'excerpt_en': 'Modern terminal started operating at Urgench International Airport. Annual capacity is 2 million passengers. New flight routes are also planned.',
        'excerpt_ru': 'В международном аэропорту Ургенча начал работу современный терминал. Годовая пропускная способность — 2 миллиона пассажиров. Планируются новые авиамаршруты.',
        'content_uz': 'Urganch xalqaro aeroporti yangi zamonaviy terminal bilan kengaytirildi. Yangi terminal 15,000 kvadrat metr maydonga ega. Zamonaviy tekshiruv tizimlari, duty-free do\'konlari va restoranlar joylashgan.\n\nYangi aviayo\'nalishlar: Istanbul, Dubai, Moskva va Tashkent. Samarqanddan keladigan reyslar soni ham ko\'paygan.',
        'content_en': 'Urgench International Airport has been expanded with a new modern terminal. The new terminal has an area of 15,000 square meters. Modern inspection systems, duty-free shops and restaurants are located.\n\nNew flight routes: Istanbul, Dubai, Moscow and Tashkent. The number of flights from Samarkand has also increased.',
        'content_ru': 'Международный аэропорт Ургенча расширен новым современным терминалом. Площадь нового терминала 15 000 квадратных метров. Современные системы контроля, магазины duty-free и рестораны.',
        'cover_image_src': 'caravan.jpg',
        'author': 'Visit Khorezm Team',
        'is_featured': True,
    },
    {
        'title_uz': 'Ichan-qal\'ada restavratsiya ishlari yakunlandi',
        'title_en': 'Restoration works completed in Ichan-Kala',
        'title_ru': 'В Ичан-Кале завершены реставрационные работы',
        'slug': 'ichan-kala-restoration-2024',
        'excerpt_uz': 'Ko\'p yillik restavratsiya ishlari muvaffaqiyatli yakunlandi. Muhammadamin, Muhammadrahim va Alloquli xon madrasalari to\'liq tiklandi.',
        'excerpt_en': 'Long-term restoration works have been successfully completed. Muhammadamin, Muhammadrahim and Alloquli Khan madrasahs have been fully restored.',
        'excerpt_ru': 'Успешно завершены многолетние реставрационные работы. Полностью восстановлены медресе Мухаммадамина, Мухаммадрахима и Аллакули-хана.',
        'content_uz': 'Uch yil davom etgan keng ko\'lamli restavratsiya loyihasi yakuniga yetdi. Eng mashhur madrasalar o\'z ko\'rinishini qaytarib oldi. Ishlar UNESCO mutaxassislari nazorati ostida amalga oshirildi.\n\nRestavratsiyadan keyin ularda yangi ko\'rgazmalar va madaniyat tadbirlari tashkil etildi.',
        'content_en': 'A large-scale restoration project lasting three years has come to an end. The most famous madrasahs have restored their appearance. The works were carried out under the supervision of UNESCO specialists.\n\nAfter restoration, new exhibitions and cultural events were organized in them.',
        'content_ru': 'Завершился масштабный реставрационный проект, длившийся три года. Самые известные медресе вернули свой облик. Работы проводились под контролем специалистов ЮНЕСКО.',
        'cover_image_src': 'kalta-minor.jpg',
        'author': 'Sayohat xabari',
        'is_featured': True,
    },
    {
        'title_uz': 'Yangi premium mehmonxonalar sayyohlar uchun ochildi',
        'title_en': 'New premium hotels opened for tourists',
        'title_ru': 'Новые премиум-отели открылись для туристов',
        'slug': 'new-premium-hotels-khiva-2024',
        'excerpt_uz': 'Xivada 3 ta yangi 5 yulduzli mehmonxona ishga tushdi. Umumiy xonalar soni 450 taga yetdi. Boutique mehmonxonalar soni ham oshgan.',
        'excerpt_en': '3 new 5-star hotels opened in Khiva. The total number of rooms has reached 450. The number of boutique hotels has also increased.',
        'excerpt_ru': 'В Хиве открылись 3 новых 5-звёздочных отеля. Общее количество номеров достигло 450. Также увеличилось количество бутик-отелей.',
        'content_uz': 'Xiva turizm sektori tez rivojlanmoqda. So\'nggi 6 oy ichida 3 ta yangi premium mehmonxona ochildi. Ularda SPA, basseyn, konferens zallari va restoran xizmatlari mavjud.\n\nYangi mehmonxonalar: Farovon Khiva, Ulli Oy Boutique, Arkanchi Boutique. Umumiy investitsiya hajmi 25 million dollar.',
        'content_en': 'The Khiva tourism sector is developing rapidly. In the last 6 months, 3 new premium hotels have opened. They have SPA, pool, conference halls and restaurant services.\n\nNew hotels: Farovon Khiva, Ulli Oy Boutique, Arkanchi Boutique. Total investment of 25 million dollars.',
        'content_ru': 'Туристический сектор Хивы быстро развивается. За последние 6 месяцев открылись 3 новых премиум-отеля. В них есть СПА, бассейн, конференц-залы и ресторан.',
        'cover_image_src': 'hotel-traditional.jpg',
        'author': 'Turizm xabari',
        'is_featured': False,
    },
]


class Command(BaseCommand):
    help = "Events va News uchun demo ma'lumotlar yuklaydi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        images_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'frontend' / 'public' / 'images'
        
        if options['clear']:
            e_count = Event.objects.all().delete()[0]
            n_count = News.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {e_count} event, {n_count} news"))

        # EVENTS
        events_created = 0
        for data in EVENTS:
            if Event.objects.filter(title_uz=data['title_uz']).exists():
                self.stdout.write(f"  Skip event: {data['title_uz']}")
                continue
            
            img_src = data.pop('cover_image_src')
            event = Event(**{k: v for k, v in data.items() if k != 'price'})
            if 'price' in data:
                event.price = data['price']
            event.save()

            img_path = images_dir / img_src
            if img_path.exists():
                with open(img_path, 'rb') as f:
                    event.cover_image.save(f'{event.id}_{img_src}', File(f), save=True)
            
            events_created += 1
            self.stdout.write(self.style.SUCCESS(f"  + Event: {event.title_uz}"))

        # NEWS
        news_created = 0
        for data in NEWS:
            if News.objects.filter(slug=data['slug']).exists():
                self.stdout.write(f"  Skip news: {data['slug']}")
                continue
            
            img_src = data.pop('cover_image_src')
            news = News(
                published_at=timezone.now(),
                **data
            )
            news.save()

            img_path = images_dir / img_src
            if img_path.exists():
                with open(img_path, 'rb') as f:
                    news.cover_image.save(f'{news.id}_{img_src}', File(f), save=True)
            
            news_created += 1
            self.stdout.write(self.style.SUCCESS(f"  + News: {news.title_uz}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nTayyor! Events: {events_created}, News: {news_created}"
        ))
