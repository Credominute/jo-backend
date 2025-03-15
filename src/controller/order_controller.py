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

# lecture de toutes les commandes
def read_order(db:Session):
    return db.query(Order).all() # select * from order

# supprimer un commande selon son id
def delete_order_by_id(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404,
                            detail="order not found")
    db.delete(order)
    db.commit()
    return order

# mise à jour d'une commande selon son id
def update_order_by_id(order_id: int, updated_order: OrderCreate, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404,
                            detail="order not found")
    for key, value in updated_order.model_dump().items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order