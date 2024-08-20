import os
import django
import uuid
from django.db import connection
from django.apps import apps
from django.db.models import UUIDField

# Ustawienie środowiska Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goworkout.settings")
django.setup()

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def fix_invalid_uuids():
    for model in apps.get_models():
        print(f"Sprawdzanie modelu: {model.__name__}")
        uuid_fields = [f for f in model._meta.fields if isinstance(f, UUIDField)]
        
        if uuid_fields:
            for field in uuid_fields:
                print(f"  Sprawdzanie pola UUID: {field.name}")
                all_records = model.objects.all()
                
                for record in all_records:
                    value = getattr(record, field.name)
                    if value is not None and not is_valid_uuid(value):
                        print(f"    Znaleziono nieprawidłowe UUID: {value}")
                        new_uuid = uuid.uuid4()
                        setattr(record, field.name, new_uuid)
                        print(f"    Naprawiono UUID: {value} -> {new_uuid}")
                        record.save()

    print("Sprawdzanie zakończone.")

if __name__ == "__main__":
    fix_invalid_uuids()
    print("Zakończono naprawę UUID.")