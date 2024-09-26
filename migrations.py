import argparse
import subprocess

from apps.utils.models import load_models_to_migrations_file, create_default_records

if __name__ == '__main__':
    # Определяем список возможных аргументов
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('command', choices=['makemigrations', 'migrate', 'create_default'])

    # Разбираем аргументы командной строки
    args = parser.parse_args()

    # В зависимости от аргументов выполняем соответствующий код
    if args.command == 'makemigrations':
        load_models_to_migrations_file()
        result = subprocess.run(
            ['pem', 'watch', '--serialize', '--traceback'],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        print(result.stderr)
    elif args.command == 'migrate':
        result = subprocess.run(['pem', 'migrate', '--traceback'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

    elif args.command == 'create_default':
        create_default_records()
