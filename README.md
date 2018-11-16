## Redis Keys Exporter

Экспортер для сбора статистики с редис

### Settings

Для старта необходимо установить переменные окружения:

*  ``REDIS_HOST = 192.168.16.26``
*  ``REDIS_PORT = 6379``
*  ``REDIS_DB_LIST = 0,3``

### Start

```
docker run -d --rm --name redis-keys-exporter -p 9210:9210 --env REDIS_HOST='192.168.16.26' --env REDIS_DB_LIST='0,1,3' local.repo/redis-keys-exporter:0.1.1
```

### Changelog

*0.1.1* Change regex for ML and others

*0.1.0* Initial version

