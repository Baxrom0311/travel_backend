"""
Management command: import_hotel_photos

Mavjud hotel rasmlarini "Sayt uchun/Photos/" papkasidan
media/hotels/ ga ko'chirib, HotelImage jadvaliga bog'laydi.

Ishlatish:
    python manage.py import_hotel_photos
    python manage.py import_hotel_photos --source "../Sayt uchun/Photos"
    python manage.py import_hotel_photos --dry-run
"""

import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from hotels.models import Hotel, HotelImage


# Rasm papkasi nomi → Hotel DB nomi xaritasi
PHOTO_FOLDER_MAP = {
    # Urgench
    "Khorezm Palace Hotel": "Khorezm Palace Hotel",
    "Antalya Grand Palace": "Antalya Grand Palace",
    "Turkezm Hotel":        "Turkezm Hotel",
    "Horizon Haven Hotel":  "Horizon Haven Hotel",
    "Hotel Karavan":        "Hotel KARAVAN",
    # Khiva
    "Arkanchi Boutique Hotel": "Arkanchi Boutique Hotel",
    "Farovon Khiva Hotel":     "Farovon Khiva Hotel",
    "Isakhoja Boutique Hotel": "Isakhoja Boutique Hotel",
    "Muso to'ra":              "Muso To'ra",
    "Ulli Oy Boutique Hotel":  "Ulli Oy Boutique Hotel & Terrace",
}

DEFAULT_PHOTOS_ROOT = settings.BASE_DIR.parent / "Sayt uchun" / "Photos"


class Command(BaseCommand):
    help = "Hotel rasmlarini Photos/ papkasidan media/ ga import qiladi"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Haqiqatda hech narsa qilmasdan natijani ko'rsatadi",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Import oldidan mavjud HotelImage yozuvlarini tozalaydi",
        )
        parser.add_argument(
            "--source",
            default=None,
            help='Rasmlar joylashgan Photos papkasi. Default: "../Sayt uchun/Photos"',
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        do_clear = options["clear"]
        photos_root = Path(options["source"]).expanduser().resolve() if options["source"] else DEFAULT_PHOTOS_ROOT

        media_hotels = settings.MEDIA_ROOT / "hotels"
        if not dry_run:
            media_hotels.mkdir(parents=True, exist_ok=True)

        if not photos_root.exists():
            self.stderr.write(self.style.ERROR(f"Photos papkasi topilmadi: {photos_root}"))
            return

        self.stdout.write(f"Rasmlar manbasi: {photos_root}")

        if do_clear and not dry_run:
            deleted, _ = HotelImage.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"  {deleted} ta eski HotelImage o'chirildi"))

        total_copied = 0
        total_skipped = 0
        errors = []

        for city_folder in ["Urgench", "Khiva"]:
            city_path = photos_root / city_folder
            if not city_path.exists():
                self.stdout.write(self.style.WARNING(f"  Papka topilmadi: {city_path}"))
                continue

            for hotel_folder in city_path.iterdir():
                if not hotel_folder.is_dir():
                    continue

                folder_name = hotel_folder.name
                db_name = PHOTO_FOLDER_MAP.get(folder_name)

                if not db_name:
                    self.stdout.write(self.style.WARNING(f"  ⚠ Xaritada yo'q: '{folder_name}'"))
                    continue

                try:
                    hotel = Hotel.objects.get(name=db_name)
                except Hotel.DoesNotExist:
                    errors.append(f"DB da topilmadi: '{db_name}'")
                    continue

                # Rasmlarni topib ulash
                image_files = sorted([
                    f for f in hotel_folder.iterdir()
                    if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
                ])

                self.stdout.write(f"\n📂 {hotel.name} ({len(image_files)} rasm):")

                for idx, img_path in enumerate(image_files):
                    dest_name = f"{hotel.id}_{img_path.name}"
                    dest_path = media_hotels / dest_name
                    relative_path = f"hotels/{dest_name}"

                    # Allaqachon bor?
                    if HotelImage.objects.filter(image=relative_path).exists():
                        self.stdout.write(f"   ⏭ Skip (mavjud): {dest_name}")
                        total_skipped += 1
                        continue

                    if not dry_run:
                        shutil.copy2(img_path, dest_path)
                        is_cover = (idx == 0)
                        HotelImage.objects.create(
                            hotel=hotel,
                            image=relative_path,
                            is_cover=is_cover,
                            order=idx,
                        )
                        self.stdout.write(
                            f"   ✅ {'[COVER] ' if is_cover else ''}  {dest_name}"
                        )
                    else:
                        self.stdout.write(f"   [DRY] {img_path.name} → {dest_name}")

                    total_copied += 1

        self.stdout.write("\n" + "=" * 50)
        if errors:
            for e in errors:
                self.stdout.write(self.style.ERROR(f"  ❌ {e}"))

        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f"\n[DRY RUN] {total_copied} ta rasm import qilinishi mumkin edi"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"\n✅ {total_copied} ta rasm import qilindi, {total_skipped} ta o'tkazib yuborildi"
            ))
