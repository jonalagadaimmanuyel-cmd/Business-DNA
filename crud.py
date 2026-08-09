from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from typing import List


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product_data: dict):
    product = models.Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, data: dict):
    product = get_product(db, product_id)
    if not product:
        return None
    for key, value in data.items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True


def create_sale(db: Session, product_id: int, quantity: int):
    product = get_product(db, product_id)
    if not product:
        raise ValueError('Product not found')
    # Update stock and sold qty
    product.current_stock = max(0, product.current_stock - quantity)
    product.quantity_sold = product.quantity_sold + quantity
    sale = models.Sale(product_id=product_id, quantity=quantity, timestamp=datetime.utcnow())
    db.add(sale)
    db.add(product)
    db.commit()
    db.refresh(sale)
    return sale


def get_dashboard(db: Session):
    # Simple dashboard aggregation for demo
    products = db.query(models.Product).all()
    total_profit = sum([(p.selling_price - p.buying_price) * (p.quantity_sold or 0) for p in products])
    best = sorted(products, key=lambda p: p.quantity_sold * (p.selling_price - p.buying_price), reverse=True)
    best_prod = best[0] if best else None
    attention = sum(1 for p in products if p.current_stock <= 10 or (p.quantity_sold or 0) < 10)
    top_products = [{"id": p.id, "name": p.name, "amount": int((p.selling_price - p.buying_price) * (p.quantity_sold or 0))} for p in products[:5]]
    return {
        "profit_today": int(total_profit),
        "profit_change": 0,
        "attention_count": attention,
        "best_product": {"id": best_prod.id, "name": best_prod.name, "total_profit": int((best_prod.selling_price - best_prod.buying_price) * (best_prod.quantity_sold or 0))} if best_prod else {},
        "top_products": top_products
    }


def get_recommendations(db: Session):
    products = db.query(models.Product).all()
    recs = []
    rid = 1
    for p in products:
        if p.current_stock <= 10:
            recs.append({"id": rid, "type": "restock", "title": p.name, "detail": f"Only {p.current_stock} units left. You are selling it quickly.", "productId": p.id})
            rid += 1
        if p.quantity_sold and p.quantity_sold < 20 and p.current_stock > 50:
            recs.append({"id": rid, "type": "reduce", "title": p.name, "detail": f"{p.current_stock} units remain, but only {p.quantity_sold} were sold.", "productId": p.id})
            rid += 1
    # Add a focus on top profit
    if products:
        profs = sorted(products, key=lambda x: (x.selling_price - x.buying_price) * (x.quantity_sold or 0), reverse=True)
        top = profs[0]
        recs.insert(0, {"id": rid, "type": "focus", "title": top.name, "detail": "Your highest-profit product.", "productId": top.id})
    return recs


def get_report(db: Session):
    products = db.query(models.Product).all()
    total_profit = int(sum([(p.selling_price - p.buying_price) * (p.quantity_sold or 0) for p in products]))
    total_products = len(products)
    best = max(products, key=lambda p: (p.selling_price - p.buying_price) * (p.quantity_sold or 0)) if products else None
    slow = min(products, key=lambda p: p.quantity_sold or 0) if products else None
    restock = next((p for p in products if p.current_stock <= 10), None)
    reduce = next((p for p in products if p.quantity_sold and p.quantity_sold < 20 and p.current_stock > 50), None)
    return {
        "profit_today": total_profit,
        "total_products": total_products,
        "best_product": best.name if best else None,
        "slowest_product": slow.name if slow else None,
        "restock_product": restock.name if restock else None,
        "reduce_product": reduce.name if reduce else None
    }


def seed_sample_data(db: Session):
    samples = [
        {"name": "Rice", "category": "Grocery", "buying_price": 40, "selling_price": 50, "quantity_sold": 100, "current_stock": 20},
        {"name": "Milk", "category": "Drinks", "buying_price": 30, "selling_price": 55, "quantity_sold": 90, "current_stock": 6},
        {"name": "Cooking Oil", "category": "Grocery", "buying_price": 100, "selling_price": 120, "quantity_sold": 40, "current_stock": 12},
        {"name": "Biscuits", "category": "Snacks", "buying_price": 20, "selling_price": 30, "quantity_sold": 60, "current_stock": 40},
        {"name": "Chips", "category": "Snacks", "buying_price": 10, "selling_price": 25, "quantity_sold": 12, "current_stock": 140},
        {"name": "Soap", "category": "Household", "buying_price": 20, "selling_price": 40, "quantity_sold": 70, "current_stock": 18},
        {"name": "Sugar", "category": "Grocery", "buying_price": 30, "selling_price": 40, "quantity_sold": 30, "current_stock": 25},
        {"name": "Tea", "category": "Grocery", "buying_price": 80, "selling_price": 100, "quantity_sold": 20, "current_stock": 10}
    ]
    for s in samples:
        p = models.Product(**s)
        db.add(p)
    db.commit()
