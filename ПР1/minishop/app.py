#!/usr/bin/env python3
# MiniShop: консольный "калькулятор заказа"

import csv
from datetime import datetime

TAX_RATE = 0.12  # НДС 12% (условно)

DISCOUNTS = {
    "SALE10": 0.10,
    "SALE20": 0.20,
    "VIP": 0.15,
    "FREESHIP": 0.00  # для примера, не влияет на цену
}

ORDERS_CSV = "orders.csv"


def parse_price(text):
    """
    Преобразует строку в цену.
    Поддерживает и точку, и запятую в качестве разделителя.
    """
    text = text.replace(",", ".")
    return float(text)


def calc_total(price, qty, discount_code=None):
    """
    Считает сумму к оплате.
    """
    if price <= 0:
        raise ValueError("Цена должна быть положительной.")
    if qty <= 0 or qty > 100:
        raise ValueError("Количество должно быть в диапазоне 1–100.")

    subtotal = price * qty
    discount = 0.0
    if discount_code and discount_code in DISCOUNTS:
        discount = subtotal * DISCOUNTS[discount_code]
    taxed = (subtotal - discount) * (1 + TAX_RATE)
    total = round(taxed, 2)
    return total


def save_order(items, customer_name):
    """
    Сохраняет заказ в CSV.
    """
    need_header = False
    try:
        with open(ORDERS_CSV, "r", encoding="utf-8") as f:
            if not f.readline():
                need_header = True
    except FileNotFoundError:
        need_header = True

    with open(ORDERS_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        if need_header:
            w.writerow(["timestamp", "customer", "item", "price", "qty", "discount", "total"])
        for it in items:
            w.writerow([
                datetime.now().isoformat(timespec="seconds"),
                customer_name,
                it["name"],
                it["price"],
                it["qty"],
                it.get("discount") or "",
                it["total"]
            ])


def menu():
    """
    Отображает меню.
    """
    print("\n=== MiniShop — калькулятор заказа ===")
    print("1 — Добавить позицию")
    print("2 — Показать текущий чек")
    print("3 — Сохранить и выйти")
    print("4 — Выход без сохранения")
    print("-------------------------------------")


def main():
    items = []
    customer = input("Введите имя клиента: ").strip()
    if not customer:
        print("Ошибка: имя клиента не может быть пустым.")
        return

    while True:
        menu()
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            name = input("Название позиции: ").strip() or "Без названия"
            price_text = input("Цена за единицу (пример 199.90): ").strip()
            try:
                price = parse_price(price_text)
            except Exception:
                print("Ошибка: некорректная цена, попробуйте снова.")
                continue
            qty_text = input("Количество (целое): ").strip()
            try:
                qty = int(qty_text)
            except Exception:
                print("Ошибка: некорректное количество.")
                continue
            discount = input("Промокод (опционально): ").strip().upper() or None
            try:
                total = calc_total(price, qty, discount)
            except Exception as e:
                print(f"Ошибка: {e}")
                continue
            items.append({
                "name": name,
                "price": price,
                "qty": qty,
                "discount": discount,
                "total": total
            })
            print(f"Добавлено: {name} × {qty} = {total} руб.")
        elif choice == "2":
            if not items:
                print("Чек пуст.")
            else:
                print("\n--- Текущий чек ---")
                s = 0.0
                for i, it in enumerate(items, 1):
                    print(f"{i}. {it['name']} | {it['qty']} шт | {it['price']} руб. | код: {it.get('discount') or '-'} | итого: {it['total']} руб.")
                    s += it['total']
                print(f"ИТОГО К ОПЛАТЕ: {round(s, 2)} руб.")
        elif choice == "3":
            save_order(items, customer or "Неизвестный")
            print("Заказ сохранен. До свидания!")
            break
        elif choice == "4":
            print("Выход без сохранения.")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
