from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ClienteCreate(BaseModel):
    Nombre: str = Field(..., description="Nombre del cliente")
    Teléfono: Optional[str] = Field(None, description="Teléfono del cliente")
    Correo: Optional[str] = Field(None, description="Correo del cliente")
    Dirección: Optional[str] = Field(None, description="Dirección del cliente")
    FechaRegistro: Optional[date] = Field(None, description="Fecha de registro del cliente")

class Cliente(ClienteCreate):
    ID: int

class EmpleadoCreate(BaseModel):
    Nombre: str = Field(..., description="Nombre del empleado")
    Puesto: Optional[str] = Field(None, description="Puesto del empleado")
    Teléfono: Optional[str] = Field(None, description="Teléfono del empleado")
    Correo: Optional[str] = Field(None, description="Correo del empleado")
    FechaContratación: Optional[date] = Field(None, description="Fecha de contratación del empleado")

class Empleado(EmpleadoCreate):
    ID: int

class ProveedorCreate(BaseModel):
    Nombre: str = Field(..., description="Nombre del proveedor")
    Teléfono: Optional[str] = Field(None, description="Teléfono del proveedor")
    Correo: Optional[str] = Field(None, description="Correo del proveedor")
    Dirección: Optional[str] = Field(None, description="Dirección del proveedor")

class Proveedor(ProveedorCreate):
    ID: int


class ProductoCreate(BaseModel):
    Nombre: str = Field(..., description="Nombre del producto")
    Tipo: Optional[str] = Field(None, description="Tipo de producto")
    Stock: Optional[int] = Field(0, description="Cantidad en stock")
    Precio: Optional[float] = Field(0.0, description="Precio del producto")
    IDProveedor: Optional[int] = Field(None, description="ID del proveedor")

class Producto(ProductoCreate):
    ID: int


class ServicioCreate(BaseModel):
    IDCliente: int = Field(..., description="ID del cliente")
    Tipo: Optional[str] = Field(None, description="Tipo de servicio")
    Fecha: Optional[date] = Field(None, description="Fecha del servicio")
    Material: Optional[str] = Field(None, description="Material utilizado")
    Costo: Optional[float] = Field(0.0, description="Costo del servicio")
    IDEmpleado: Optional[int] = Field(None, description="ID del empleado")

class Servicio(ServicioCreate):
    ID: int

class FacturaCreate(BaseModel):
    IDServicio: int = Field(..., description="ID del servicio")
    Fecha: Optional[date] = Field(None, description="Fecha de la factura")
    Total: Optional[float] = Field(0.0, description="Total de la factura")
    MétodoPago: Optional[str] = Field(None, description="Método de pago")

class Factura(FacturaCreate):
    ID: int