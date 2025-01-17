import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

from home.models import PhotoProduct

def check_photos_in_database():
    """
    Checks if all photos from the paths in the PhotoProduct table exist in the media directory.
    """
    missing_files = []
    total_files = 0

    print("Starting photo check from the PhotoProduct table...\n")

    photos = PhotoProduct.objects.all()

    if not photos.exists():
        print("❌ No photos found in the database.")
        return

    for photo in photos:
        total_files += 1
        file_path = photo.path 
        photo_path = os.path.join("media", file_path)

        if not os.path.exists(photo_path):
            missing_files.append(file_path)
            print(f"❌ Missing file: {photo_path}")
        else:
            print(f"✅ File exists: {photo_path}")

    print("\nSummary:")
    print(f"Total number of photos in the database: {total_files}")
    print(f"Number of missing files: {len(missing_files)}")

    if missing_files:
        print("\nList of missing files:")
        for missing_file in missing_files:
            print(f"- {missing_file}")

if __name__ == "__main__":
    check_photos_in_database()
