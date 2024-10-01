import importlib
import json
from typing import Any

from peewee_async.aio_model import AioModel

from main.db import database
from main.loader import settings


class BaseModel(AioModel):
    class Meta:
        database = database
        abstract = True

    default_records: list[dict[str, Any]] = []

    @classmethod
    def create_default_values(cls):
        """
        Метод создает дефолтные значения для таблиц, если есть необходимость
        :return:
        """
        for data in cls.default_records:
            cls.get_or_create(**data)


def add_models_to_migrations(new_models):
    # Определяем путь к файлу models.json
    models_path = settings.MIGRATIONS_FILE

    # Если файл models.json не существует, создаем его и записываем в него пустой список
    if not models_path.exists():
        raise Exception('Сначала необходимо ввести команду: pem init')

    # Открываем файл models.json для чтения
    with open(models_path) as f:
        # Загружаем список моделей из файла
        models = json.load(f)

    # Добавляем новые модели в список
    models['models'] += list(
        new_model for new_model in new_models
            if new_model not in models['models']
    )

    # Открываем файл models.json для записи
    with open(models_path, 'w') as f:
        # Записываем обновленный список моделей в файл
        json.dump(models, f, indent=4)


def get_subclasses() -> list[tuple[str, str, type(BaseModel)]]:
    subclasses = []
    for app_path in settings.APPS_DIR.iterdir():
        if not app_path.is_dir() or app_path.name.startswith('__'):
            continue
        app_name: str = app_path.name
        try:
            models_module = importlib.import_module(f'apps.{app_name}.models')
        except ModuleNotFoundError:
            continue  # Если модуль не найден, переходим к следующему приложению

        for model_name in dir(models_module):
            model = getattr(models_module, model_name)
            if (
                    isinstance(model, type) and
                    issubclass(model, BaseModel) and
                    model is not BaseModel and
                    model.__module__ == models_module.__name__
            ):
                print(model, issubclass(model, BaseModel))
                # Генерируем путь вида 'apps.{app_name}.models.{ModelName}'
                subclasses.append((app_name, model_name, model))
    return subclasses


def get_models_paths() -> list[str]:
    models_paths = []
    subclasses = get_subclasses()
    for app_name, model_name, model in subclasses:
        models_paths.append(f'apps.{app_name}.models.{model_name}')
    return models_paths


def load_models_to_migrations_file():
    models_paths = get_models_paths()
    add_models_to_migrations(models_paths)


def create_default_records():
    subclasses = get_subclasses()
    for _, _, subclass in subclasses:
        subclass.create_default_values()
