# binance_parse

## Для запуска необходимо выполнить docker-compose up --build и дождаться запуска.

## Ключевые переменные окружения:
1. REDIS_PORT - порт для redis
2. SYMBOL - фьючерс
3. TIMEOUT - временной промежуток, в котором будет вестись наблюдение над изменением цены
4. REQUEST_FREQ - кол-во секунд на один запрос на обновление цены с биржы (чем меньше, тем быстрее)
