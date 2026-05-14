"""
R2'dagi rasmlarni Attraction va Hotel modellariga bog'lash.
"""
from django.core.management.base import BaseCommand
from attractions.models import Attraction, AttractionImage
from hotels.models import Hotel, HotelImage


# Frontend public/images → R2'da public/* path
ATTRACTION_IMAGES = {
    'Kalta Minor': 'public/kalta-minor.jpg',
    "Ko'hna Ark": 'public/khiva-main.jpg',
    'Juma Masjidi': 'public/juma-mosque.jpg',
    "Islom Xo'ja Minorasi": 'public/khiva-main.jpg',
    'Ota Darvoza': 'public/ichan-kala.jpg',
    'Polvon Darvoza': 'public/ichan-kala.jpg',
}

HOTEL_IMAGES = {
    'Farovon Khiva Hotel': 'public/hotel-traditional.jpg',
    'Ulli Oy Boutique Hotel & Terrace': 'public/khorezm-palace.jpg',
    'Arkanchi Boutique Hotel': 'public/topkapi-palace.jpg',
    'Antalya Grand Palace': 'public/khorezm-palace.jpg',
    'Horizon Haven Hotel': 'public/hotel-traditional.jpg',
    'Hotel KARAVAN': 'public/caravan.jpg',
    'Khorezm Palace Hotel': 'public/khorezm-palace.jpg',
    'Isakhoja Boutique Hotel': 'public/hotel-traditional.jpg',
    'Turkezm Hotel': 'public/topkapi-palace.jpg',
    "Muso To'ra": 'public/hotel-traditional.jpg',
}


class Command(BaseCommand):
    help = "R2 rasmlarini Attraction va Hotel'larga bog'laydi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Avval barcha rasmlarni o\'chirish')

    def handle(self, *args, **options):
        if options['clear']:
            AttractionImage.objects.all().delete()
            HotelImage.objects.all().delete()
            self.stdout.write(self.style.WARNING('Eski rasmlar o\'chirildi'))

        # Attractions
        att_count = 0
        for att in Attraction.objects.all():
            if att.images.exists():
                continue
            path = ATTRACTION_IMAGES.get(att.name_uz, 'public/khiva-main.jpg')
            AttractionImage.objects.create(attraction=att, image=path, is_cover=True, order=0)
            att_count += 1
            self.stdout.write(f'  + Attraction: {att.name_uz} → {path}')

        # Hotels
        hotel_count = 0
        for h in Hotel.objects.all():
            if h.images.exists():
                continue
            path = HOTEL_IMAGES.get(h.name, 'public/hotel-traditional.jpg')
            HotelImage.objects.create(hotel=h, image=path, is_cover=True, order=0)
            hotel_count += 1
            self.stdout.write(f'  + Hotel: {h.name} → {path}')

        self.stdout.write(self.style.SUCCESS(
            f'\nTayyor! Attractions: {att_count}, Hotels: {hotel_count}'
        ))
