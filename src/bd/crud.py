from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bd.base import connection
from src.bd.model import Product


@connection
async def get_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products


@connection
async def add_product(
    db: AsyncSession, name: str, price: int, cashback: int, url: str, sub_category: str
) -> None:
    if cashback > price:
        product = Product(
            name=name, price=price, cashback=cashback, url=url, sub_category=sub_category
        )
        db.add(product)
        await db.commit()


@connection
async def filter_products(db: AsyncSession, sub_category: str):
    products = await db.execute(select(Product).filter_by(sub_category=sub_category))
    return products.scalars().all()


@connection
async def clear_product_table(db: AsyncSession):
    """Функция для удаления всех записей из таблицы Product"""
    try:
        await db.execute(delete(Product))
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(f"Ошибка при очистке таблицы Product: {e}")


@connection
async def get_products_with_high_cashback(db: AsyncSession):
    """Функция для получения товаров, у которых кэшбэк больше цены"""
    try:
        result = await db.execute(select(Product).where(Product.cashback > Product.price))
        products = result.scalars().all()
        return products
    except Exception as e:
        print(f"Ошибка при получении товаров: {e}")
        return []