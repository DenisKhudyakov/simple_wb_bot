import asyncio
from typing import AsyncGenerator, Union, List, Dict, Set

import aiohttp
from aiohttp.client_exceptions import ContentTypeError

__base_url_for_get_products = "https://catalog.wb.ru/catalog/{shard}/v2/catalog?ab_testing=false&appType=1&cat={id_category}&curr=rub&dest=123585825&page={page}&ffeedbackpoints=1"
__url_product = "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=123585825&spp=30&ab_testing=false&nm={id_product}"


def connection(func):
    """Декоратор для создания сессии"""
    async def wrapper(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await func(session, *args, **kwargs)

    return wrapper


async def fetch_json(session, url):
    """
    Функция для выполнения GET-запроса и возврата JSON данных.
    """
    try:
        async with session.get(url) as response:
            # Проверяем, что статус успешный (200 OK)
            if response.status == 200:
                try:
                    # Пытаемся декодировать ответ как JSON
                    return await response.json()
                except ContentTypeError:
                    # Ловим ContentTypeError, если тип содержимого не JSON
                    print(
                        f"ContentTypeError: Неверный тип данных при попытке декодирования JSON. URL: {url}"
                    )
                    return None
            else:
                print(f"Ошибка {response.status}: {url}")
                return None
    except aiohttp.ClientError as e:
        # Ловим любые другие сетевые ошибки
        print(f"ClientError: Произошла ошибка при выполнении запроса: {e}")
        return None


def extract_category_data(category):
    """
    Функция для извлечения данных категории и подкатегорий.
    """
    try:
        return {
            "category_name": category["name"],
            "category_url": category["url"],
            "shard": category.get("shard"),
            "query": category.get("query"),
            "id_category": category.get("id"),
        }
    except KeyError:
        return None


async def get_catalog_wb(session) -> list:
    """
    Функция получения всего каталога на WB
    :return: список каталога
    """
    url = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"

    data_list = []
    data = await fetch_json(session, url)

    for d in data:
        for child in d.get("childs", []):
            category_data = extract_category_data(child)
            if category_data:
                data_list.append(category_data)
            for sub_child in child.get("childs", []):
                sub_category_data = extract_category_data(sub_child)
                if sub_category_data:
                    data_list.append(sub_category_data)

    return data_list


@connection
async def get_categories(session) -> dict:
    """
    Функция для получения категорий с подкатегориями с WB в формате {category: [sub_categories: [sub_categories]]}.
    :param session: Асинхронная сессия aiohttp.
    :return: Словарь с категориями и их подкатегориями (включая вложенные подкатегории).
    """
    url = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"
    data = await fetch_json(session, url)
    category_dict = {}

    # Рекурсивная функция для формирования вложенной структуры подкатегорий
    def build_subcategories(sub_categories):
        result = []
        for sub_category in sub_categories:
            sub_name = sub_category.get("name")
            childs = sub_category.get("childs", [])
            if childs:
                result.append({sub_name: build_subcategories(childs)})
            else:
                result.append(sub_name)
        return result

    for category in data:
        category_name = category.get("name")
        sub_categories = category.get("childs", [])
        if sub_categories:
            category_dict[category_name] = build_subcategories(sub_categories)

    return category_dict



async def get_product(session) -> AsyncGenerator:
    """
    Функция для получения информации о продукте с WB.
    :param session: Асинхронная сессия aiohttp.
    :return: словарь с продуктами.
    """
    data_list = await get_catalog_wb(session)
    for data in data_list:
        for page in range(1, 34):
            response = await fetch_json(
                session=session,
                url=__base_url_for_get_products.format(
                    shard=data["shard"], id_category=data["id_category"], page=page
                ),
            )
            if response:
                try:
                    for i in response["data"]["products"]:
                        yield i["id"], data
                except KeyError:
                    print("Invalid JSON structure received")
                    continue


async def get_feedbackPoints_and_total_price(session) -> AsyncGenerator:
    """
    Функция для получения информации о продукте у которого есть баллы за отзыв
    :param session:
    :return:
    """
    async for product in get_product(session):
        response = await fetch_json(
            session, __url_product.format(id_product=product[0])
        )
        try:
            yield {
                "name_product": response["data"]["products"][0]["name"],
                "total_price": response["data"]["products"][0]["sizes"][0]["price"][
                    "total"
                ]
                / 100,
                "cash_back": response["data"]["products"][0]["feedbackPoints"],
                "url": f"https://www.wildberries.ru/catalog/{product[0]}/detail.aspx",
                "catalog": product[1],
            }
        except KeyError:
            continue


async def extract_strings(data: Union[List, Dict]) -> Set[str]:
    """
    Функция преобразования огромного словаря с вложенными списками категорий
    и исключает дубликаты строковых значений, необходимо для создания новой клавиатуры
    :param data: словарь с данными из каталога
    :return: множество строковых значений
    """

    result = []

    def recursive_extract(item):
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, list):
            for sub_item in item:
                recursive_extract(sub_item)
        elif isinstance(item, dict):
            for key, value in item.items():
                recursive_extract(key)
                recursive_extract(value)

    recursive_extract(data)
    return set(result)



