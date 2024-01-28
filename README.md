# mirgovorit-cookbook

Тестовое задание на вакансию "Junior/Middle Django developer" в МирГоворит.

## Запуск локально

```bash
cp cookbook/.env-sample cookbook/.env

# Запуск PostgreSQL
docker-compose up -d

poetry run python cookbook/manage.py migrate
poetry run python cookbook/manage.py loaddata --database default sample_data

poetry run python cookbook/manage.py runserver
```

Админка доступна по адресу http://localhost:8000/admin/

Логин/пароль администратора сайта: `admin/admin1234`


## Эндпоинты

### `GET /show_recipes_without_product/`

Принимает следующие параметры:

- `product_id`, тип `int` — идентификатор продукта. Указывать не обязательно

Возвращает HTML страницу, на которой размещена таблица. В таблице отображены id и названия всех рецептов, в которых продукт `product_id` отсутствует, или присутствует в количестве меньше 10 грамм. Страница сгенерирована с использованием Django templates

### `GET /api/add_product_to_recipe/`

Принимает следующие параметры:

- `recipe_id`, тип `int` — идентификатор рецепта
- `product_id`, тип `int` — идентификатор продукта
- `weight`, тип `int` — сколько нужно продукта, указывается в граммах. Должен быть от 1 и выше

Добавляет к рецепту `recipe_id` продукт `product_id` с весом `weight`. Если в рецепте уже есть такой продукт, то его вес в этом рецепте меняется на указанный


### `GET /api/cook_recipe/`

Принимает следующие параметры:

- `recipe_id`, тип `int` — идентификатор рецепта

Увеличивает на единицу количество приготовленных блюд для каждого продукта, входящего в рецепт `recipe_id`
