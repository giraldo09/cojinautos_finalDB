from typing import List, Dict, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models import (
    ClienteCreate, Cliente, EmpleadoCreate, Empleado,
    ProveedorCreate, Proveedor, ProductoCreate, Producto,
    ServicioCreate, Servicio, FacturaCreate, Factura
)
from app.database import get_db_connection
from typing import List
import mysql.connector

router = APIRouter()

@router.post("/clientes/", response_model=Cliente, tags=["Clientes"])
def create_cliente(cliente: ClienteCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO clientes (Nombre, Teléfono, Correo, Dirección, FechaRegistro)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (cliente.Nombre, cliente.Teléfono, cliente.Correo, 
                cliente.Dirección, cliente.FechaRegistro)
        
        cursor.execute(query, values)
        conn.commit()
        
        cliente_id = cursor.lastrowid
        return Cliente(ID=cliente_id, **cliente.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/clientes/", response_model=List[Cliente], tags=["Clientes"])
def list_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM clientes"
        cursor.execute(query)
        clientes = cursor.fetchall()
        return [Cliente(**cliente) for cliente in clientes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/clientes/bulk/", response_model=List[Cliente], tags=["Clientes"])
def create_clientes_bulk(clientes: List[ClienteCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO clientes (Nombre, Teléfono, Correo, Dirección, FechaRegistro)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = [(c.Nombre, c.Teléfono, c.Correo, c.Dirección, c.FechaRegistro) 
                for c in clientes]
        
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        cliente_ids = range(last_id - len(clientes) + 1, last_id + 1)
        
        return [Cliente(ID=cid, **c.dict()) for cid, c in zip(cliente_ids, clientes)]
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/empleados/", response_model=Empleado, tags=["Empleados"])
def create_empleado(empleado: EmpleadoCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO empleados (Nombre, Puesto, Teléfono, Correo, FechaContratación)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (empleado.Nombre, empleado.Puesto, empleado.Teléfono, 
                empleado.Correo, empleado.FechaContratación)
        
        cursor.execute(query, values)
        conn.commit()
        
        empleado_id = cursor.lastrowid
        return Empleado(ID=empleado_id, **empleado.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/empleados/", response_model=List[Empleado], tags=["Empleados"])
def list_empleados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM empleados"
        cursor.execute(query)
        empleados = cursor.fetchall()
        return [Empleado(**empleado) for empleado in empleados]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/empleados/bulk/", response_model=List[Empleado], tags=["Empleados"])
def create_empleados_bulk(empleados: List[EmpleadoCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO empleados (Nombre, Puesto, Teléfono, Correo, FechaContratación)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = [(e.Nombre, e.Puesto, e.Teléfono, e.Correo, e.FechaContratación) 
                for e in empleados]
        
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        empleado_ids = range(last_id - len(empleados) + 1, last_id + 1)
        
        return [Empleado(ID=eid, **e.dict()) for eid, e in zip(empleado_ids, empleados)]
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/proveedores/", response_model=Proveedor, tags=["Proveedores"])
def create_proveedor(proveedor: ProveedorCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO proveedores (Nombre, Teléfono, Correo, Dirección)
        VALUES (%s, %s, %s, %s)
        """
        values = (proveedor.Nombre, proveedor.Teléfono, proveedor.Correo, proveedor.Dirección)
        
        cursor.execute(query, values)
        conn.commit()
        
        proveedor_id = cursor.lastrowid
        return Proveedor(ID=proveedor_id, **proveedor.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/proveedores/", response_model=List[Proveedor], tags=["Proveedores"])
def list_proveedores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM proveedores"
        cursor.execute(query)
        proveedores = cursor.fetchall()
        return [Proveedor(**proveedor) for proveedor in proveedores]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/proveedores/bulk/", response_model=List[Proveedor], tags=["Proveedores"])
def create_proveedores_bulk(proveedores: List[ProveedorCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO proveedores (Nombre, Teléfono, Correo, Dirección)
        VALUES (%s, %s, %s, %s)
        """
        values = [(p.Nombre, p.Teléfono, p.Correo, p.Dirección) for p in proveedores]
        
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        proveedor_ids = range(last_id - len(proveedores) + 1, last_id + 1)
        
        return [Proveedor(ID=pid, **p.dict()) for pid, p in zip(proveedor_ids, proveedores)]
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/productos/", response_model=Producto, tags=["Productos"])
def create_producto(producto: ProductoCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT ID FROM proveedores WHERE ID = %s", (producto.IDProveedor,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
            
        query = """
        INSERT INTO productos (Nombre, Tipo, Stock, Precio, IDProveedor)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (producto.Nombre, producto.Tipo, producto.Stock, 
                producto.Precio, producto.IDProveedor)
        
        cursor.execute(query, values)
        conn.commit()
        
        producto_id = cursor.lastrowid
        return Producto(ID=producto_id, **producto.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/productos/", response_model=List[Producto], tags=["Productos"])
def list_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM productos"
        cursor.execute(query)
        productos = cursor.fetchall()
        return [Producto(**producto) for producto in productos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/productos/bulk/", response_model=List[Producto], tags=["Productos"])
def create_productos_bulk(productos: List[ProductoCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_productos = []
        for producto in productos:
            cursor.execute("SELECT ID FROM proveedores WHERE ID = %s", (producto.IDProveedor,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, 
                                detail=f"Proveedor {producto.IDProveedor} no encontrado")
            
            query = """
            INSERT INTO productos (Nombre, Tipo, Stock, Precio, IDProveedor)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (producto.Nombre, producto.Tipo, producto.Stock, 
                    producto.Precio, producto.IDProveedor)
            
            cursor.execute(query, values)
            producto_id = cursor.lastrowid
            created_productos.append(Producto(ID=producto_id, **producto.dict()))
        
        conn.commit()
        return created_productos
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/servicios/", response_model=Servicio, tags=["Servicios"])
def create_servicio(servicio: ServicioCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT ID FROM clientes WHERE ID = %s", (servicio.IDCliente,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
            
        cursor.execute("SELECT ID FROM empleados WHERE ID = %s", (servicio.IDEmpleado,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
            
        query = """
        INSERT INTO servicios (IDCliente, Tipo, Fecha, Material, Costo, IDEmpleado)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (servicio.IDCliente, servicio.Tipo, servicio.Fecha, 
                servicio.Material, servicio.Costo, servicio.IDEmpleado)
        
        cursor.execute(query, values)
        conn.commit()
        
        servicio_id = cursor.lastrowid
        return Servicio(ID=servicio_id, **servicio.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/servicios/", response_model=List[Servicio], tags=["Servicios"])
def list_servicios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM servicios"
        cursor.execute(query)
        servicios = cursor.fetchall()
        return [Servicio(**servicio) for servicio in servicios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/servicios/bulk/", response_model=List[Servicio], tags=["Servicios"])
def create_servicios_bulk(servicios: List[ServicioCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_servicios = []
        for servicio in servicios:
            cursor.execute("SELECT ID FROM clientes WHERE ID = %s", (servicio.IDCliente,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, 
                                detail=f"Cliente {servicio.IDCliente} no encontrado")
                
            cursor.execute("SELECT ID FROM empleados WHERE ID = %s", (servicio.IDEmpleado,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, 
                                detail=f"Empleado {servicio.IDEmpleado} no encontrado")
                
            query = """
            INSERT INTO servicios (IDCliente, Tipo, Fecha, Material, Costo, IDEmpleado)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (servicio.IDCliente, servicio.Tipo, servicio.Fecha, 
                    servicio.Material, servicio.Costo, servicio.IDEmpleado)
            
            cursor.execute(query, values)
            servicio_id = cursor.lastrowid
            created_servicios.append(Servicio(ID=servicio_id, **servicio.dict()))
        
        conn.commit()
        return created_servicios
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/facturas/", response_model=Factura, tags=["Facturas"])
def create_factura(factura: FacturaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT ID FROM servicios WHERE ID = %s", (factura.IDServicio,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
            
        query = """
        INSERT INTO facturas (IDServicio, Fecha, Total, MétodoPago)
        VALUES (%s, %s, %s, %s)
        """
        values = (factura.IDServicio, factura.Fecha, factura.Total, factura.MétodoPago)
        
        cursor.execute(query, values)
        conn.commit()
        
        factura_id = cursor.lastrowid
        return Factura(ID=factura_id, **factura.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/facturas/", response_model=List[Factura], tags=["Facturas"])
def list_facturas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM facturas"
        cursor.execute(query)
        facturas = cursor.fetchall()
        return [Factura(**factura) for factura in facturas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/facturas/bulk/", response_model=List[Factura], tags=["Facturas"])
def create_facturas_bulk(facturas: List[FacturaCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        created_facturas = []
        for factura in facturas:
            cursor.execute("SELECT ID FROM servicios WHERE ID = %s", (factura.IDServicio,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, 
                                detail=f"Servicio {factura.IDServicio} no encontrado")
                
            query = """
            INSERT INTO facturas (IDServicio, Fecha, Total, MétodoPago)
            VALUES (%s, %s, %s, %s)
            """
            values = (factura.IDServicio, factura.Fecha, factura.Total, factura.MétodoPago)
            
            cursor.execute(query, values)
            factura_id = cursor.lastrowid
            created_facturas.append(Factura(ID=factura_id, **factura.dict()))
        
        conn.commit()
        return created_facturas
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()