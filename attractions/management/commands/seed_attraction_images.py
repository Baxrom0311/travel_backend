"""
Management command: attractions uchun rasmlarni frontend/public/images dan yuklash.

Usage:
    python manage.py seed_attraction_images
    python manage.py seed_attraction_images --clear   # avval barcha rasmlarni tozalash
"""
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from attractions.models import Attraction, AttractionImage


# Har bir attraction uchun qaysi rasmlar ishlatiladi
ATTRACTION_IMAGES = {
    'Kalta Minor': ['kalta-minor.jpg', 'khiva-main.jpg'],
    "Ko'hna Ark": ['ichan-kala.jpg', 'khiva-main.jpg'],
    'Juma Masjidi': ['juma-mosque.jpg', 'ichan-kala.jpg'],
    "Islom Xo'ja Minorasi": ['khiva-main.jpg', 'kalta-minor.jpg'],
    'Ota Darvoza': ['ichan-kala.jpg', 'khiva-main.jpg'],
    'Polvon Darvoza': ['khiva-main.jpg'],
    'Tosh Darvoza': ['khiva-main.jpg'],
    "Bog'cha Darvoza": ['khiva-main.jpg'],
}

# Har bir attraction uchun qo'shimcha ma'lumotlar
ATTRACTION_DETAILS = {
    'Kalta Minor': {
        'history_uz': 'Kalta Minor (qisqa minora) Xivaning eng ko\'zga ko\'ringan ramzidir. 1851-yilda Muhammad Amin Xon topshirig\'iga binoan qurila boshlangan. Agar tugallanganida, dunyodagi eng baland minora bo\'lishi kerak edi. Lekin 1855-yilda xonning o\'limi sababli qurilish to\'xtatib qoldirildi. Minora balandligi 29 metrga yetdi.',
        'history_en': 'Kalta Minor (Short Minaret) is the most iconic symbol of Khiva. Construction began in 1851 by order of Muhammad Amin Khan. If completed, it would have been the tallest minaret in the world. However, construction was halted in 1855 after the khan\'s death. The minaret reaches 29 meters in height.',
        'history_ru': 'Кальта Минар (Короткий минарет) - самый узнаваемый символ Хивы. Строительство началось в 1851 году по приказу Мухаммад Амин хана. Если бы его закончили, это был бы самый высокий минарет в мире. Строительство было остановлено в 1855 году после смерти хана. Высота минарета достигла 29 метров.',
        'working_hours': '09:00 - 18:00',
        'entrance_fee': 50000,
    },
    "Ko'hna Ark": {
        'history_uz': 'Ko\'hna Ark - Xiva xonlarining qadimgi saroyi. XII asrda qurilgan, keyinchalik kengaytirilgan. Ichida xonlarning qarorgohi, masjid, monetniy dvor, zindon va Kuriniseh ayvoni joylashgan. Devorlari 8 metr balandlikda.',
        'history_en': 'Kuhna Ark is the ancient palace of the Khans of Khiva. Built in the 12th century and later expanded. It contains the khan\'s residence, a mosque, a mint, a prison, and the Kurinesh pavilion. The walls are 8 meters high.',
        'history_ru': 'Кухна Арк - древний дворец хивинских ханов. Построен в XII веке, позже расширен. Внутри находятся резиденция хана, мечеть, монетный двор, тюрьма и павильон Куриниш. Высота стен 8 метров.',
        'working_hours': '09:00 - 18:00',
        'entrance_fee': 40000,
    },
    'Juma Masjidi': {
        'history_uz': 'Juma masjidi Xivaning eng noyob binolaridan biridir. 218 ta o\'ymakor yog\'och ustunlarga suyanadi. X asrda qurila boshlangan, hozirgi ko\'rinishini 1788-yilda olgan. Ustunlarning ba\'zilari 1000 yillik tarixga ega.',
        'history_en': 'The Juma Mosque is one of the most unique buildings in Khiva. It rests on 218 carved wooden columns. Construction began in the 10th century, and the current appearance was formed in 1788. Some of the columns are over 1000 years old.',
        'history_ru': 'Пятничная мечеть - одно из уникальнейших зданий Хивы. Опирается на 218 резных деревянных колонн. Строительство началось в X веке, нынешний вид сформирован в 1788 году. Некоторые колонны старше 1000 лет.',
        'working_hours': '09:00 - 18:00',
        'entrance_fee': 30000,
    },
    "Islom Xo'ja Minorasi": {
        'history_uz': 'Islom Xo\'ja minorasi - Xorazmning eng baland minorasi (56,6 metr). 1908-1910-yillarda qurilgan. Xiva shahri bosh vazir Islom Xo\'ja nomi bilan atalgan. Tepadan butun Ichan-qal\'aning ajoyib manzarasi ko\'rinadi.',
        'history_en': 'Islam Khodja Minaret is the tallest minaret in Khorezm (56.6 meters). Built in 1908-1910. Named after the Prime Minister of Khiva, Islam Khodja. From the top, there is a stunning view of the entire Ichan-Kala.',
        'history_ru': 'Минарет Ислама Ходжи - самый высокий минарет Хорезма (56,6 м). Построен в 1908-1910 годах. Назван в честь премьер-министра Хивы Ислама Ходжи. С вершины открывается потрясающий вид на всю Ичан-Калу.',
        'working_hours': '09:00 - 18:00',
        'entrance_fee': 60000,
    },
}


class Command(BaseCommand):
    help = "Attractions uchun rasmlarni public/images papkasidan yuklaydi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Avval barcha rasmlarni o\'chirish')

    def handle(self, *args, **options):
        # Frontend public/images papkasi
        images_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'frontend' / 'public' / 'images'
        
        if not images_dir.exists():
            self.stderr.write(f'Rasmlar papkasi topilmadi: {images_dir}')
            return

        self.stdout.write(f'Manba: {images_dir}')

        if options['clear']:
            deleted = AttractionImage.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'O\'chirildi: {deleted[0]} ta rasm'))

        total_loaded = 0
        total_updated = 0

        for attraction in Attraction.objects.all():
            name = attraction.name_uz
            
            # Details yangilash
            if name in ATTRACTION_DETAILS:
                details = ATTRACTION_DETAILS[name]
                for key, value in details.items():
                    setattr(attraction, key, value)
                attraction.save()
                total_updated += 1
                self.stdout.write(f'  Yangilandi: {name}')
            
            # Rasmlar yuklash
            if name not in ATTRACTION_IMAGES:
                continue

            # Agar allaqachon rasmi bor bo'lsa, o'tkazib yuborish
            if attraction.images.exists():
                self.stdout.write(f'  Skip (rasm bor): {name}')
                continue

            for idx, img_filename in enumerate(ATTRACTION_IMAGES[name]):
                img_path = images_dir / img_filename
                if not img_path.exists():
                    self.stderr.write(f'    Topilmadi: {img_path}')
                    continue
                
                with open(img_path, 'rb') as f:
                    img = AttractionImage(
                        attraction=attraction,
                        is_cover=(idx == 0),
                        order=idx,
                        caption_uz=f'{name} - rasm {idx + 1}',
                    )
                    img.image.save(
                        f'{attraction.id}_{img_filename}',
                        File(f),
                        save=True,
                    )
                    total_loaded += 1
                    self.stdout.write(f'    + {img_filename}')

        self.stdout.write(self.style.SUCCESS(
            f'\nTayyor! Yuklandi: {total_loaded} ta rasm. Yangilandi: {total_updated} ta attraction.'
        ))
