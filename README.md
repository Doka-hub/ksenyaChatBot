Obtaining initial SSL certificates:

1. Mount `http.conf` instead of `https.conf` to nginx service in Compose
2. `docker compose up nginx -d`
3. `docker compose run --rm certbot certonly --webroot -w /var/lib/letsencrypt --agree-tos -m email@example.com -d example.com -d www.example.com -n`
4. Change nginx config mount back to `https.conf`, configure domain name as required


Renewal of exisitng certificates:

```docker compose -f /home/admin/tg-shop-technics/docker-compose.yml up -d certbot```

Cron version (weekly at 03:30am):

```30 3 */7 * * /usr/bin/docker compose -f /home/admin/tg-shop-technics/docker-compose.yml up -d certbot```

---

Database backups:

```docker exec -t tg-shop-technics-db-1 pg_dumpall -c -U postgres | gzip > /home/admin/backups/db/db_dump_$(date +%Y-%m-%d_%H_%M_%S).sql.gz```

Cron version (everyday at 03:00):

```0 3 * * * bash -c '/usr/bin/docker exec -t tg-shop-technics-db-1 pg_dumpall -c -U postgres | gzip > /home/admin/backups/db/db_dump_$(date +\%Y-\%m-\%d_\%H_\%M_\%S).sql.gz'```

Cron cleanup database backups older than 7 days (everyday at 04:00):

```0 4 * * * find /home/admin/backups/db -mtime +7 -name "db_dump*.sql.gz" -delete```

Database restore:

```gunzip < /home/admin/backups/db/your_dump.sql.gz | docker exec -i tg-shop-technics-db-1 psql -U postgres```

---

Media backups:

```docker run --rm -v tg-shop-technics_media-files:/media -v /home/admin/backups/media:/backup alpine tar cvzf /backup/media_$(date +%Y-%m-%d_%H_%M_%S).tar.gz /media```

Cron version (everyday at 03:01):

```1 3 * * * /usr/bin/docker run --rm -v tg-shop-technics_media-files:/media -v /home/admin/backups/media:/backup alpine tar czf /backup/media_$(date +\%Y-\%m-\%d_\%H_\%M_\%S).tar.gz /media```

Cron cleanup media backups older than 7 days (everyday at 04:01):

```1 4 * * * find /home/admin/backups/media -mtime +7 -name "media*.tar.gz" -delete```

Media restore:

1. `tar zxf /home/admin/backups/media/your_backup.tar.gz`
2. `docker run --rm -v tg-shop-technics_media-files:/media -v /home/admin/backups/media/media:/backup alpine cp -r /backup/. /media`
