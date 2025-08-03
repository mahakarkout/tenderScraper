# TenderScraper

TenderScraper — инструмент для веб-скрапинга, который извлекает информацию о тендерах с сайта [rostender.info](https://rostender.info/extsearch) и предоставляет данные через REST API на базе FastAPI.

## Возможности

- Скрапинг тендерных данных: название, ID, даты, цены, категории и др.
- Сохранение данных в базу данных SQLite
- Экспорт в форматы JSON и CSV
- REST API для доступа к данным о тендерах
- CLI-интерфейс для ручного запуска скрапинга

## Как это работает

Система состоит из нескольких ключевых компонентов:

### Scraper (`scraper.py`)
- Использует `BeautifulSoup` для парсинга HTML с rostender.info
- Извлекает информацию о тендерах из HTML-блоков `article`
- Обрабатывает пагинацию (по 20 тендеров на страницу)
- Использует задержку между запросами для защиты от блокировки

### База данных (`database.py`)
- Хранение тендеров в `SQLite` (файл `tenders.db`)
- Автоматическое создание таблицы при запуске
- Методы для инициализации, сохранения и загрузки данных

### CLI-интерфейс (`main.py`)
- Позволяет запускать скрапинг вручную из терминала
- Поддерживает настройку лимита и формата вывода
- Сохраняет данные в JSON, CSV и базу данных

### API (`api.py`)
- Реализован с использованием `FastAPI`
- Эндпоинт `/tenders` возвращает все сохранённые тендеры
- Поддерживает просмотр через Swagger UI или Postman

## Используемые технологии

- Python 3.9.10
- FastAPI
- BeautifulSoup4
- Requests
- SQLite
- Pandas
- lxml
- Uvicorn

## Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/mahakarkout/tenderScraper.git
cd tenderScraper
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Использование

### Запуск скрапера (CLI)

```bash
python main.py [опции]
```

**Опции:**

- `--max`: Максимальное количество тендеров (по умолчанию 100)
- `--format`: Формат вывода (`json` или `csv`, по умолчанию `json`)
- `--output`: Имя файла вывода (по умолчанию `tenders.json`)

**Пример:**

```bash
python main.py --max 50 --format csv --output data/my_tenders.csv
```

### Запуск API

```bash
uvicorn src.api:app --reload
```

API будет доступен по адресу: `http://127.0.0.1:8000`

Получить тендеры:

```bash
GET http://127.0.0.1:8000/tenders
```

### Пример ответа от API

```json
[
  {
    "tender_id": "85583433",
    "title": "Доставка",
    "url": "https://rostender.info/region/moskva-gorod/85583433-tender-dostavka",
    "start_date": "03.08.25",
    "end_date": "04.08.2025",
    "end_time": "",
    "region": "Москва город",
    "city": "г. Москва",
    "price": "—",
    "categories": ["Услуги грузовых автомобильных перевозок"],
    "category_urls": ["https://rostender.info/tendery-uslugi-gruzovyh-avtomobilnyh-perevozok"]
  }
]
```

## Скриншоты

- Swagger UI с эндпоинтом `/tenders`
### Интерфейс Swagger
![Swagger UI]
<img width="2528" height="1326" alt="swagger" src="https://github.com/user-attachments/assets/4bdff794-c773-4533-aa2f-05e3fb6f832c" />


## Возможные улучшения

### Обработка ошибок:
- Обработка изменений в структуре сайта

### Производительность:
- Асинхронный скрапинг
- Кэширование результатов

### Новые функции:
- Фильтрация/поиск по API
- Планировщик автоматического скрапинга
- Дополнительные форматы (Excel, XML)

### Мониторинг:
- Логирование
- Health-check эндпоинты
- Метрики и алерты

### Развёртывание:
- Docker-контейнеризация
- CI/CD пайплайн
- Хостинг в облаке

---
