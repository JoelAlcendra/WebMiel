
from datetime import datetime
from typing import Optional, List
from database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


# MODELO DE LA BASE DE DATOS
class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[str] = mapped_column(nullable=False)       # Ej: "250 ml", "500 ml", "700 ml"
    stock: Mapped[int] = mapped_column(default=0, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)    # En pesos colombianos (COP)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    image: Mapped[Optional[str]] = mapped_column(nullable=True) # Ruta o URL de la foto
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False) # Para activar/pausar venta

    def __str__(self):
        return f'Product(id={self.id}, name="{self.name}", size="{self.size}", price={self.price}, stock={self.stock})'


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    rol: Mapped[str] = mapped_column(default="user", nullable=False)
 
    # Relación 1 a N con Order (un usuario -> muchos pedidos).
    orders: Mapped[list["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")


    def __str__(self):
        return f'User(id={self.id}, name="{self.name}", email="{self.email}", rol="{self.rol}")'


class Order(db.Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey('users.id'), nullable=True)

    customer_name: Mapped[str] = mapped_column(nullable=False)
    customer_email: Mapped[str] = mapped_column(nullable=False)
    customer_phone: Mapped[str] = mapped_column(nullable=False)
    shipping_address: Mapped[str] = mapped_column(nullable=False)

    total: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default='pendiente', nullable=False) # pendiente, pagado, enviado, etc.
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    # Relaciones ORM
    # Permite acceder al objeto User que hizo el pedido (pedido.user).
    user: Mapped[Optional['User']] = relationship(back_populates='orders')

    # Permite acceder a la lista de renglones/ítems del pedido (pedido.items).
    items: Mapped[List['OrderItem']] = relationship(back_populates='order', cascade='all, delete-orphan')

    def __str__(self):
        return f'Order(id={self.id}, customer="{self.customer_name}", total={self.total}, status="{self.status}")'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(db.ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(db.ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False) # Precio histórico congelado al momento de comprar

    # Relaciones ORM
    # Permite acceder al pedido padre desde el renglón (item.order).
    order: Mapped['Order'] = relationship(back_populates='items')

    # Permite acceder al producto asociado a este renglón (item.product).
    product: Mapped['Product'] = relationship()

    def __str__(self):
        return f'OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity}, price={self.price})'