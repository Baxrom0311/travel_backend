"""
Local rasmlarni Cloudflare R2'ga upload qilish.

Ishlatish:
    R2_ACCESS_KEY_ID=xxx R2_SECRET_ACCESS_KEY=xxx R2_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com R2_BUCKET=travel-media python upload_to_r2.py
"""
import os
import sys
from pathlib import Path

try:
    import boto3
except ImportError:
    print("boto3 o'rnating: pip install boto3")
    sys.exit(1)


def upload_directory(local_dir: Path, prefix: str, s3_client, bucket: str):
    """Local katalogni R2'ga yuklash."""
    if not local_dir.exists():
        print(f"  ⚠️  Topilmadi: {local_dir}")
        return 0
    
    count = 0
    for item in local_dir.rglob('*'):
        if item.is_file() and item.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.gif'):
            # Relative path: media/attractions/foo.jpg → attractions/foo.jpg
            relative_path = item.relative_to(local_dir.parent)
            key = str(relative_path).replace('\\', '/')
            
            content_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.webp': 'image/webp',
                '.gif': 'image/gif',
            }.get(item.suffix.lower(), 'application/octet-stream')
            
            try:
                s3_client.upload_file(
                    str(item),
                    bucket,
                    key,
                    ExtraArgs={
                        'ContentType': content_type,
                        'CacheControl': 'public, max-age=31536000',
                    }
                )
                count += 1
                if count % 10 == 0:
                    print(f"  ✓ {count} ta yuklandi...")
            except Exception as e:
                print(f"  ✗ Xato {key}: {e}")
    
    return count


def main():
    # Env variable'lar
    access_key = os.getenv('R2_ACCESS_KEY_ID')
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    endpoint = os.getenv('R2_ENDPOINT_URL')
    bucket = os.getenv('R2_BUCKET', 'travel-media')
    
    if not all([access_key, secret_key, endpoint]):
        print("❌ Kerakli env variable'lar yo'q!")
        print("   R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT_URL")
        sys.exit(1)
    
    # S3 client
    s3 = boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='auto',
    )
    
    backend_dir = Path(__file__).resolve().parent
    media_dir = backend_dir / 'media'
    
    print(f"📦 Bucket: {bucket}")
    print(f"📂 Manba: {media_dir}")
    print()
    
    total = 0
    
    # Backend media (158 ta rasm)
    if media_dir.exists():
        print("=== Backend media/ ===")
        total += upload_directory(media_dir, 'media', s3, bucket)
    
    # Frontend public/images (10 ta rasm)
    frontend_images = backend_dir.parent / 'frontend' / 'public' / 'images'
    if frontend_images.exists():
        print("\n=== Frontend public/images/ ===")
        for item in frontend_images.iterdir():
            if item.is_file() and item.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
                key = f'public/{item.name}'
                content_type = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.webp': 'image/webp',
                }.get(item.suffix.lower(), 'application/octet-stream')
                try:
                    s3.upload_file(
                        str(item),
                        bucket,
                        key,
                        ExtraArgs={
                            'ContentType': content_type,
                            'CacheControl': 'public, max-age=31536000',
                        }
                    )
                    total += 1
                    print(f"  ✓ {item.name}")
                except Exception as e:
                    print(f"  ✗ {item.name}: {e}")
    
    print()
    print(f"✅ Jami yuklandi: {total} ta rasm")


if __name__ == '__main__':
    main()
