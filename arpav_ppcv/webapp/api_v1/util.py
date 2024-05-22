from typing import Type

from . import schemas

from django.utils.module_loading import import_string


def get_item_list(django_model_class_path: str, schema_model: Type) -> schemas.ItemList:
    module_path, django_model_name = django_model_class_path.rpartition(".")[::2]
    imported_module = import_string(module_path)
    django_model = getattr(imported_module, django_model_name)
    items = django_model.objects.all()  # noqa
    return schemas.ItemList[schema_model](
        count=len(items),
        results=items,
    )
