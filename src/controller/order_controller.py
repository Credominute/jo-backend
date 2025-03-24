from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.model.order import Order
from src.schema.order_schema import OrderCreate

# création d'une commande
def create_order(order: OrderCreate,db: Session):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# lecture d'une commande par son id
def read_order_by_id(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404,
                            detail="order not found")
    return order