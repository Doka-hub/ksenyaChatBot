# Используем официальный образ PostgreSQL
FROM postgres:13

# Указываем рабочую директорию для PostgreSQL
WORKDIR /docker-entrypoint-initdb.d/

COPY pg_hba.conf /var/lib/postgresql/data/pg_hba.conf
# Копируем SQL-скрипт для создания баз данных и пользователей
COPY init-db.sh /docker-entrypoint-initdb.d/

# Разрешаем выполнение скрипта
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh
