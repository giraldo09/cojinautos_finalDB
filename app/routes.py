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
        
@router.get("/analytics/promedio-gastos-cliente/{cliente_id}", 
        tags=["Análisis"],
        summary="Obtiene estadísticas de gastos de un cliente",
        response_description="Resumen de gastos del cliente")
def get_promedio_gastos_cliente(cliente_id: int) -> Dict[str, Any]:
    """
    Obtiene un análisis detallado de los gastos de un cliente específico.
    
    Parameters:
    - cliente_id: ID del cliente a analizar
    
    Returns:
    - NombreCliente: Nombre del cliente
    - TotalServicios: Número total de servicios contratados
    - PromedioGasto: Promedio de gasto por servicio
    - GastoMínimo: El gasto más bajo realizado
    - GastoMáximo: El gasto más alto realizado
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT Nombre FROM clientes WHERE ID = %s", (cliente_id,))
        cliente = cursor.fetchone()
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró ningún cliente con el ID {cliente_id}"
            )

        query = """
        SELECT 
            c.Nombre as NombreCliente,
            COUNT(s.ID) as TotalServicios,
            ROUND(AVG(f.Total), 2) as PromedioGasto,
            MIN(f.Total) as GastoMínimo,
            MAX(f.Total) as GastoMáximo
        FROM clientes c
        LEFT JOIN servicios s ON c.ID = s.IDCliente
        LEFT JOIN facturas f ON s.ID = f.IDServicio
        WHERE c.ID = %s
        GROUP BY c.ID, c.Nombre
        """
        cursor.execute(query, (cliente_id,))
        resultado = cursor.fetchone()
        
        if not resultado or resultado['TotalServicios'] == 0:
            return {
                "NombreCliente": cliente['Nombre'],
                "TotalServicios": 0,
                "PromedioGasto": 0,
                "GastoMínimo": 0,
                "GastoMáximo": 0,
                "mensaje": "Este cliente aún no ha realizado ningún servicio"
            }
            
        return resultado

    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()
        
@router.get("/analytics/top-empleados/", 
        tags=["Análisis"],
        summary="Ranking de empleados por ventas totales",
        response_description="Lista de empleados ordenados por ventas")
def get_top_empleados():
    """
    Obtiene un ranking de empleados basado en sus ventas totales.
    
    Returns:
    - NombreEmpleado: Nombre del empleado
    - TotalServicios: Número de servicios realizados
    - VentasTotales: Suma total de ventas
    - PromedioServicio: Promedio de precio por servicio
    - UltimoServicio: Fecha del último servicio realizado
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            e.Nombre as NombreEmpleado,
            COUNT(s.ID) as TotalServicios,
            ROUND(SUM(f.Total), 2) as VentasTotales,
            ROUND(AVG(f.Total), 2) as PromedioServicio,
            MAX(s.Fecha) as UltimoServicio
        FROM empleados e
        LEFT JOIN servicios s ON e.ID = s.IDEmpleado
        LEFT JOIN facturas f ON s.ID = f.IDServicio
        GROUP BY e.ID, e.Nombre
        ORDER BY VentasTotales DESC
        """
        cursor.execute(query)
        resultado = cursor.fetchall()
        
        if not resultado:
            return {"mensaje": "No se encontraron registros de ventas"}
            
        return resultado

    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/servicios-periodo/", 
        tags=["Análisis"],
        summary="Análisis de servicios por período de tiempo")
def get_servicios_periodo(
    fecha_inicio: str,
    fecha_fin: str
):
    """
    Analiza los servicios realizados en un período específico.
    
    Parameters:
    - fecha_inicio: Fecha inicial (YYYY-MM-DD)
    - fecha_fin: Fecha final (YYYY-MM-DD)
    
    Returns:
    - TotalServicios: Número total de servicios en el período
    - IngresoTotal: Suma total de ingresos
    - ServiciosMasComunes: Top 3 tipos de servicios más solicitados
    - PromedioServicioDiario: Promedio de servicios por día
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Formato de fecha inválido. Use YYYY-MM-DD"
            )

        query = """
        SELECT 
            COUNT(*) as TotalServicios,
            ROUND(SUM(f.Total), 2) as IngresoTotal,
            ROUND(AVG(COUNT(*)) OVER (), 2) as PromedioServicioDiario
        FROM servicios s
        LEFT JOIN facturas f ON s.ID = f.IDServicio
        WHERE s.Fecha BETWEEN %s AND %s
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        resumen = cursor.fetchone()
        
        query_tipos = """
        SELECT 
            Tipo,
            COUNT(*) as Cantidad
        FROM servicios
        WHERE Fecha BETWEEN %s AND %s
        GROUP BY Tipo
        ORDER BY Cantidad DESC
        LIMIT 3
        """
        cursor.execute(query_tipos, (fecha_inicio, fecha_fin))
        tipos_comunes = cursor.fetchall()
        
        if not resumen['TotalServicios']:
            return {
                "mensaje": "No se encontraron servicios en el período especificado",
                "período": {
                    "inicio": fecha_inicio,
                    "fin": fecha_fin
                }
            }
        
        return {
            **resumen,
            "ServiciosMasComunes": tipos_comunes,
            "Período": {
                "inicio": fecha_inicio,
                "fin": fecha_fin
            }
        }

    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/productos-proveedor/{proveedor_id}", 
        tags=["Análisis"],
        summary="Análisis detallado de productos por proveedor")
def get_analisis_productos_proveedor(proveedor_id: int):
    """
    Analiza los productos suministrados por un proveedor específico.
    
    Parameters:
    - proveedor_id: ID del proveedor a analizar
    
    Returns:
    - NombreProveedor: Nombre del proveedor
    - TotalProductos: Número total de productos suministrados
    - ValorInventario: Valor total del inventario actual
    - ProductosMasCostosos: Top 3 productos más costosos
    - ProductosBajoStock: Productos con stock bajo (menos de 10 unidades)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT Nombre FROM proveedores WHERE ID = %s", (proveedor_id,))
        proveedor = cursor.fetchone()
        if not proveedor:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró ningún proveedor con el ID {proveedor_id}"
            )

        query = """
        SELECT 
            prov.Nombre as NombreProveedor,
            COUNT(p.ID) as TotalProductos,
            ROUND(SUM(p.Stock * p.Precio), 2) as ValorInventario
        FROM proveedores prov
        LEFT JOIN productos p ON prov.ID = p.IDProveedor
        WHERE prov.ID = %s
        GROUP BY prov.ID, prov.Nombre
        """
        cursor.execute(query, (proveedor_id,))
        resumen = cursor.fetchone()

        query_costosos = """
        SELECT 
            Nombre,
            Precio,
            Stock,
            ROUND(Stock * Precio, 2) as ValorTotal
        FROM productos
        WHERE IDProveedor = %s
        ORDER BY Precio DESC
        LIMIT 3
        """
        cursor.execute(query_costosos, (proveedor_id,))
        productos_costosos = cursor.fetchall()
        
        query_stock_bajo = """
        SELECT 
            Nombre,
            Stock,
            Precio
        FROM productos
        WHERE IDProveedor = %s AND Stock < 10
        ORDER BY Stock ASC
        """
        cursor.execute(query_stock_bajo, (proveedor_id,))
        productos_bajo_stock = cursor.fetchall()
        
        return {
            **resumen,
            "ProductosMasCostosos": productos_costosos,
            "ProductosBajoStock": productos_bajo_stock
        }

    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()
        
@router.get("/analytics/tendencias-mensuales/", 
        tags=["Análisis"],
        summary="Análisis de tendencias mensuales de servicios")
def get_tendencias_mensuales(año: int = datetime.now().year):
    """
    Analiza las tendencias de servicios por mes para un año específico.
    
    Parameters:
    - año: Año a analizar (por defecto el año actual)
    
    Returns:
    - Análisis mensual con:
        - Total de servicios
        - Ingresos totales
        - Servicio más popular
        - Comparación con mes anterior
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            MONTH(s.Fecha) as Mes,
            COUNT(*) as TotalServicios,
            ROUND(SUM(f.Total), 2) as IngresosMes,
            ROUND(AVG(f.Total), 2) as PromedioServicio
        FROM servicios s
        LEFT JOIN facturas f ON s.ID = f.IDServicio
        WHERE YEAR(s.Fecha) = %s
        GROUP BY MONTH(s.Fecha)
        ORDER BY Mes
        """
        cursor.execute(query, (año,))
        resultados_mensuales = cursor.fetchall()
        
        
        query_popular = """
        SELECT 
            MONTH(s.Fecha) as Mes,
            s.Tipo as ServicioPopular,
            COUNT(*) as Cantidad
        FROM servicios s
        WHERE YEAR(s.Fecha) = %s
        GROUP BY MONTH(s.Fecha), s.Tipo
        HAVING COUNT(*) = (
            SELECT COUNT(*)
            FROM servicios s2
            WHERE YEAR(s2.Fecha) = %s
            AND MONTH(s2.Fecha) = MONTH(s.Fecha)
            GROUP BY s2.Tipo
            ORDER BY COUNT(*) DESC
            LIMIT 1
        )
        """
        cursor.execute(query_popular, (año, año))
        servicios_populares = cursor.fetchall()
        
        analisis_mensual = []
        meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        
        for resultado in resultados_mensuales:
            mes_num = resultado['Mes']
            servicio_popular = next(
                (s['ServicioPopular'] for s in servicios_populares if s['Mes'] == mes_num),
                "Sin datos"
            )
            
            analisis_mensual.append({
                "Mes": meses[mes_num],
                "TotalServicios": resultado['TotalServicios'],
                "IngresosMes": resultado['IngresosMes'],
                "PromedioServicio": resultado['PromedioServicio'],
                "ServicioMásPopular": servicio_popular
            })
        
        return {
            "Año": año,
            "AnálisisMensual": analisis_mensual,
            "TotalAnual": sum(r['TotalServicios'] for r in resultados_mensuales),
            "IngresosAnuales": sum(r['IngresosMes'] for r in resultados_mensuales)
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/clientes-frecuentes/", 
        tags=["Análisis"],
        summary="Identificación y análisis de clientes frecuentes")
def get_clientes_frecuentes(
    min_servicios: int = 3,
    periodo_meses: int = 6
):
    """
    Identifica y analiza los clientes más frecuentes.
    
    Parameters:
    - min_servicios: Número mínimo de servicios para considerar cliente frecuente
    - periodo_meses: Período de análisis en meses
    
    Returns:
    - Lista de clientes frecuentes con:
        - Datos del cliente
        - Número de servicios
        - Total gastado
        - Servicios más solicitados
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        WITH ClientesFrecuentes AS (
            SELECT 
                c.ID,
                c.Nombre,
                COUNT(s.ID) as TotalServicios,
                ROUND(SUM(f.Total), 2) as TotalGastado,
                ROUND(AVG(f.Total), 2) as PromedioGasto
            FROM clientes c
            INNER JOIN servicios s ON c.ID = s.IDCliente
            INNER JOIN facturas f ON s.ID = f.IDServicio
            WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL %s MONTH)
            GROUP BY c.ID, c.Nombre
            HAVING COUNT(s.ID) >= %s
        )
        SELECT * FROM ClientesFrecuentes
        ORDER BY TotalServicios DESC
        """
        cursor.execute(query, (periodo_meses, min_servicios))
        clientes = cursor.fetchall()
        
        for cliente in clientes:
            query_servicios = """
            SELECT 
                s.Tipo,
                COUNT(*) as Frecuencia
            FROM servicios s
            WHERE s.IDCliente = %s
            AND s.Fecha >= DATE_SUB(NOW(), INTERVAL %s MONTH)
            GROUP BY s.Tipo
            ORDER BY Frecuencia DESC
            LIMIT 3
            """
            cursor.execute(query_servicios, (cliente['ID'], periodo_meses))
            cliente['ServiciosFrecuentes'] = cursor.fetchall()
        
        return {
            "PeriodoAnálisis": f"Últimos {periodo_meses} meses",
            "MínimoServicios": min_servicios,
            "TotalClientesFrecuentes": len(clientes),
            "Clientes": clientes
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/rentabilidad-servicios/", 
        tags=["Análisis"],
        summary="Análisis de rentabilidad por tipo de servicio")
def get_rentabilidad_servicios():
    """
    Analiza la rentabilidad de cada tipo de servicio.
    
    Returns:
    - Análisis por tipo de servicio:
        - Total de servicios realizados
        - Ingresos totales
        - Promedio de ingreso por servicio
        - Tendencia mensual
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            s.Tipo,
            COUNT(*) as TotalServicios,
            ROUND(SUM(f.Total), 2) as IngresosTotal,
            ROUND(AVG(f.Total), 2) as PromedioIngreso,
            MIN(f.Total) as IngresoMínimo,
            MAX(f.Total) as IngresoMáximo
        FROM servicios s
        INNER JOIN facturas f ON s.ID = f.IDServicio
        GROUP BY s.Tipo
        ORDER BY IngresosTotal DESC
        """
        cursor.execute(query)
        rentabilidad = cursor.fetchall()
        
        query_tendencia = """
        SELECT 
            s.Tipo,
            DATE_FORMAT(s.Fecha, '%Y-%m') as Mes,
            COUNT(*) as Servicios,
            ROUND(AVG(f.Total), 2) as PromedioMes
        FROM servicios s
        INNER JOIN facturas f ON s.ID = f.IDServicio
        WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
        GROUP BY s.Tipo, DATE_FORMAT(s.Fecha, '%Y-%m')
        ORDER BY s.Tipo, Mes
        """
        cursor.execute(query_tendencia)
        tendencias = cursor.fetchall()
        
        for servicio in rentabilidad:
            servicio['TendenciaMensual'] = [
                t for t in tendencias if t['Tipo'] == servicio['Tipo']
            ]
        
        return {
            "FechaAnálisis": datetime.now().strftime('%Y-%m-%d'),
            "ResumenServicios": rentabilidad
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/stock-critico/", 
        tags=["Análisis"],
        summary="Análisis de productos con stock crítico")
def get_stock_critico(nivel_critico: int = 10):
    """
    Identifica y analiza productos con nivel de stock crítico.
    
    Parameters:
    - nivel_critico: Nivel de stock considerado crítico (default: 10)
    
    Returns:
    - Lista de productos con stock crítico
    - Información del proveedor
    - Historial de uso
    - Tiempo estimado hasta agotamiento
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            p.ID,
            p.Nombre,
            p.Stock,
            p.Precio,
            prov.Nombre as Proveedor,
            prov.Teléfono as TeléfonoProveedor,
            COUNT(s.ID) as VecesUsado,
            ROUND(COUNT(s.ID) / 
                DATEDIFF(NOW(), MIN(s.Fecha)) * 30, 2) as UsoMensualPromedio
        FROM productos p
        INNER JOIN proveedores prov ON p.IDProveedor = prov.ID
        LEFT JOIN servicios s ON p.ID = s.Material
        WHERE p.Stock <= %s
        GROUP BY p.ID, p.Nombre, p.Stock, p.Precio, 
                prov.Nombre, prov.Teléfono
        ORDER BY p.Stock ASC
        """
        cursor.execute(query, (nivel_critico,))
        productos = cursor.fetchall()
        
        for producto in productos:
            if producto['UsoMensualPromedio'] > 0:
                dias_restantes = round(producto['Stock'] / 
                producto['UsoMensualPromedio'] * 30)
                producto['DiasHastaAgotamiento'] = dias_restantes
                producto['EstadoCrítico'] = dias_restantes < 30
            else:
                producto['DiasHastaAgotamiento'] = None
                producto['EstadoCrítico'] = False
        
        return {
            "NivelCrítico": nivel_critico,
            "TotalProductosCríticos": len(productos),
            "ProductosCríticos": productos,
            "FechaAnálisis": datetime.now().strftime('%Y-%m-%d')
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()
        
@router.get("/analytics/tendencias-temporada/", 
        tags=["Análisis"],
        summary="Análisis de ventas por temporada")
def get_tendencias_temporada(año: int = datetime.now().year):
    """
    Analiza las tendencias de ventas por temporadas del año.
    
    Parameters:
    - año: Año a analizar (por defecto el año actual)
    
    Returns:
    - Análisis por temporada:
        - Verano (Jun-Ago)
        - Otoño (Sep-Nov)
        - Invierno (Dic-Feb)
        - Primavera (Mar-May)
    Incluye:
        - Total ventas
        - Servicios más populares
        - Comparativa con año anterior
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        WITH Temporadas AS (
            SELECT 
                CASE 
                    WHEN MONTH(s.Fecha) IN (12, 1, 2) THEN 'Invierno'
                    WHEN MONTH(s.Fecha) IN (3, 4, 5) THEN 'Primavera'
                    WHEN MONTH(s.Fecha) IN (6, 7, 8) THEN 'Verano'
                    ELSE 'Otoño'
                END as Temporada,
                COUNT(*) as TotalServicios,
                ROUND(SUM(f.Total), 2) as VentasTotales,
                ROUND(AVG(f.Total), 2) as PromedioVenta
            FROM servicios s
            INNER JOIN facturas f ON s.ID = f.IDServicio
            WHERE YEAR(s.Fecha) = %s
            GROUP BY 
                CASE 
                    WHEN MONTH(s.Fecha) IN (12, 1, 2) THEN 'Invierno'
                    WHEN MONTH(s.Fecha) IN (3, 4, 5) THEN 'Primavera'
                    WHEN MONTH(s.Fecha) IN (6, 7, 8) THEN 'Verano'
                    ELSE 'Otoño'
                END
        )
        SELECT * FROM Temporadas
        """
        cursor.execute(query, (año,))
        tendencias = cursor.fetchall()
        
        query_servicios = """
        SELECT 
            CASE 
                WHEN MONTH(s.Fecha) IN (12, 1, 2) THEN 'Invierno'
                WHEN MONTH(s.Fecha) IN (3, 4, 5) THEN 'Primavera'
                WHEN MONTH(s.Fecha) IN (6, 7, 8) THEN 'Verano'
                ELSE 'Otoño'
            END as Temporada,
            s.Tipo as Servicio,
            COUNT(*) as Cantidad
        FROM servicios s
        WHERE YEAR(s.Fecha) = %s
        GROUP BY 
            CASE 
                WHEN MONTH(s.Fecha) IN (12, 1, 2) THEN 'Invierno'
                WHEN MONTH(s.Fecha) IN (3, 4, 5) THEN 'Primavera'
                WHEN MONTH(s.Fecha) IN (6, 7, 8) THEN 'Verano'
                ELSE 'Otoño'
            END,
            s.Tipo
        ORDER BY Temporada, Cantidad DESC
        """
        cursor.execute(query_servicios, (año,))
        servicios_populares = cursor.fetchall()
        
        for tendencia in tendencias:
            tendencia['ServiciosPopulares'] = [
                s for s in servicios_populares 
                if s['Temporada'] == tendencia['Temporada']
            ][:3]
            
        return {
            "Año": año,
            "Tendencias": tendencias,
            "FechaAnálisis": datetime.now().strftime('%Y-%m-%d')
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/satisfaccion-clientes/", 
        tags=["Análisis"],
        summary="Análisis de satisfacción y retención de clientes")
def get_satisfaccion_clientes(periodo_meses: int = 12):
    """
    Analiza patrones de retención y frecuencia de clientes.
    
    Parameters:
    - periodo_meses: Período de análisis en meses (default: 12)
    
    Returns:
    - Tasa de retención
    - Frecuencia de visitas
    - Patrones de uso de servicios
    - Clientes recurrentes vs. nuevos
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query_retencion = """
        WITH ClientesActivos AS (
            SELECT 
                c.ID,
                MIN(s.Fecha) as PrimeraVisita,
                MAX(s.Fecha) as UltimaVisita,
                COUNT(s.ID) as TotalVisitas,
                DATEDIFF(MAX(s.Fecha), MIN(s.Fecha)) as DiasEntrePrimeraUltima
            FROM clientes c
            INNER JOIN servicios s ON c.ID = s.IDCliente
            WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL %s MONTH)
            GROUP BY c.ID
        )
        SELECT 
            COUNT(*) as TotalClientes,
            SUM(CASE WHEN TotalVisitas > 1 THEN 1 ELSE 0 END) as ClientesRecurrentes,
            ROUND(AVG(TotalVisitas), 2) as PromedioVisitas,
            ROUND(AVG(DiasEntrePrimeraUltima / TotalVisitas), 0) as PromedioDiasEntreVisitas
        FROM ClientesActivos
        """
        cursor.execute(query_retencion, (periodo_meses,))
        retencion = cursor.fetchone()
        

        query_nuevos = """
        SELECT 
            DATE_FORMAT(MIN(s.Fecha), '%Y-%m') as Mes,
            COUNT(DISTINCT c.ID) as NuevosClientes
        FROM clientes c
        INNER JOIN servicios s ON c.ID = s.IDCliente
        WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL %s MONTH)
        GROUP BY DATE_FORMAT(s.Fecha, '%Y-%m')
        ORDER BY Mes
        """
        cursor.execute(query_nuevos, (periodo_meses,))
        nuevos_clientes = cursor.fetchall()
        
        tasa_retencion = round(
            (retencion['ClientesRecurrentes'] / retencion['TotalClientes']) * 100, 2
        ) if retencion['TotalClientes'] > 0 else 0
        
        return {
            "PeriodoAnálisis": f"Últimos {periodo_meses} meses",
            "TasaRetención": f"{tasa_retencion}%",
            "EstadísticasGenerales": {
                **retencion,
                "PromedioNuevosClientesPorMes": round(
                    sum(nc['NuevosClientes'] for nc in nuevos_clientes) / len(nuevos_clientes), 2
                ) if nuevos_clientes else 0
            },
            "TendenciaNuevosClientes": nuevos_clientes
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/comparativa-precios/", 
        tags=["Análisis"],
        summary="Análisis comparativo de precios por servicio")
def get_comparativa_precios():
    """
    Realiza un análisis comparativo de precios entre servicios similares.
    
    Returns:
    - Precio promedio por tipo de servicio
    - Variación de precios
    - Comparativa con el mercado
    - Tendencias de precios
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            s.Tipo,
            COUNT(*) as TotalServicios,
            ROUND(MIN(f.Total), 2) as PrecioMínimo,
            ROUND(MAX(f.Total), 2) as PrecioMáximo,
            ROUND(AVG(f.Total), 2) as PrecioPromedio,
            ROUND(STDDEV(f.Total), 2) as DesviacionEstándar
        FROM servicios s
        INNER JOIN facturas f ON s.ID = f.IDServicio
        GROUP BY s.Tipo
        ORDER BY PrecioPromedio DESC
        """
        cursor.execute(query)
        precios = cursor.fetchall()
        
        query_tendencia = """
        SELECT 
            s.Tipo,
            DATE_FORMAT(s.Fecha, '%Y-%m') as Mes,
            ROUND(AVG(f.Total), 2) as PrecioPromedio
        FROM servicios s
        INNER JOIN facturas f ON s.ID = f.IDServicio
        WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
        GROUP BY s.Tipo, DATE_FORMAT(s.Fecha, '%Y-%m')
        ORDER BY s.Tipo, Mes
        """
        cursor.execute(query_tendencia)
        tendencias = cursor.fetchall()
        
        for precio in precios:
            precio['TendenciaPrecio'] = [
                t for t in tendencias if t['Tipo'] == precio['Tipo']
            ]
            
            if len(precio['TendenciaPrecio']) >= 2:
                primer_precio = precio['TendenciaPrecio'][0]['PrecioPromedio']
                ultimo_precio = precio['TendenciaPrecio'][-1]['PrecioPromedio']
                variacion = ((ultimo_precio - primer_precio) / primer_precio) * 100
                precio['VariaciónPrecio'] = f"{round(variacion, 2)}%"
            else:
                precio['VariaciónPrecio'] = "Sin datos suficientes"
        
        return {
            "FechaAnálisis": datetime.now().strftime('%Y-%m-%d'),
            "ResumenPrecios": precios
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/eficiencia-empleados/", 
        tags=["Análisis"],
        summary="Análisis de eficiencia y productividad de empleados")
def get_eficiencia_empleados(periodo_dias: int = 30):
    """
    Analiza la eficiencia y productividad de los empleados.
    
    Parameters:
    - periodo_dias: Período de análisis en días (default: 30)
    
    Returns:
    - Servicios por empleado
    - Tiempo promedio por servicio
    - Ingresos generados
    - Satisfacción de clientes
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        WITH EmpleadosServicios AS (
            SELECT 
                e.ID,
                e.Nombre,
                COUNT(s.ID) as TotalServicios,
                ROUND(SUM(f.Total), 2) as IngresosGenerados,
                ROUND(AVG(f.Total), 2) as PromedioServicio,
                COUNT(s.ID) / %s as ServiciosPorDia
            FROM empleados e
            LEFT JOIN servicios s ON e.ID = s.IDEmpleado
            LEFT JOIN facturas f ON s.ID = f.IDServicio
            WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL %s DAY)
            GROUP BY e.ID, e.Nombre
        )
        SELECT 
            *,
            CASE 
                WHEN ServiciosPorDia > 2 THEN 'Alta'
                WHEN ServiciosPorDia > 1 THEN 'Media'
                ELSE 'Baja'
            END as Productividad
        FROM EmpleadosServicios
        ORDER BY IngresosGenerados DESC
        """
        cursor.execute(query, (periodo_dias, periodo_dias))
        eficiencia = cursor.fetchall()
        
        if eficiencia:
            total_ingresos = sum(e['IngresosGenerados'] for e in eficiencia)
            total_servicios = sum(e['TotalServicios'] for e in eficiencia)
            
            for empleado in eficiencia:
                empleado['PorcentajeIngresos'] = round(
                    (empleado['IngresosGenerados'] / total_ingresos) * 100, 2
                ) if total_ingresos > 0 else 0
                empleado['PorcentajeServicios'] = round(
                    (empleado['TotalServicios'] / total_servicios) * 100, 2
                ) if total_servicios > 0 else 0
        
        return {
            "PeriodoAnálisis": f"Últimos {periodo_dias} días",
            "TotalEmpleados": len(eficiencia),
            "EstadísticasEmpleados": eficiencia,
            "FechaAnálisis": datetime.now().strftime('%Y-%m-%d')
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()
        
@router.get("/analytics/servicios-empleado-tipo/", 
        tags=["Análisis"],
        summary="Análisis de servicios por empleado y tipo")
def get_servicios_empleado_tipo(periodo_dias: int = 30):
    """
    Analiza la distribución de servicios por empleado y tipo.
    
    Parameters:
    - periodo_dias: Período de análisis en días (default: 30)
    
    Returns:
    - Análisis por empleado y tipo de servicio
    - Especialización de empleados
    - Eficiencia por tipo de servicio
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            e.Nombre as Empleado,
            s.Tipo as TipoServicio,
            COUNT(*) as TotalServicios,
            ROUND(AVG(f.Total), 2) as PromedioIngreso,
            MIN(f.Total) as IngresoMínimo,
            MAX(f.Total) as IngresoMáximo
        FROM empleados e
        INNER JOIN servicios s ON e.ID = s.IDEmpleado
        INNER JOIN facturas f ON s.ID = f.IDServicio
        WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY e.Nombre, s.Tipo
        ORDER BY e.Nombre, TotalServicios DESC
        """
        cursor.execute(query, (periodo_dias,))
        resultados = cursor.fetchall()
        
        analisis_empleados = {}
        for resultado in resultados:
            empleado = resultado['Empleado']
            if empleado not in analisis_empleados:
                analisis_empleados[empleado] = {
                    'Servicios': [],
                    'TotalServicios': 0,
                    'IngresoTotal': 0
                }
            analisis_empleados[empleado]['Servicios'].append(resultado)
            analisis_empleados[empleado]['TotalServicios'] += resultado['TotalServicios']
            analisis_empleados[empleado]['IngresoTotal'] += (
                resultado['PromedioIngreso'] * resultado['TotalServicios']
            )
        
        return {
            "PeriodoAnálisis": f"Últimos {periodo_dias} días",
            "AnálisisEmpleados": analisis_empleados,
            "FechaAnálisis": datetime.now().strftime('%Y-%m-%d')
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/rendimiento-diario/", 
        tags=["Análisis"],
        summary="Análisis de rendimiento diario")
def get_rendimiento_diario(dias: int = 7):
    """
    Analiza el rendimiento diario del negocio.
    
    Parameters:
    - dias: Número de días a analizar (default: 7)
    
    Returns:
    - Análisis diario de:
        - Total servicios
        - Ingresos
        - Productos utilizados
        - Empleados activos
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            DATE(s.Fecha) as Fecha,
            COUNT(DISTINCT s.ID) as TotalServicios,
            COUNT(DISTINCT s.IDEmpleado) as EmpleadosActivos,
            COUNT(DISTINCT s.Material) as ProductosUtilizados,
            ROUND(SUM(f.Total), 2) as IngresoTotal,
            ROUND(AVG(f.Total), 2) as PromedioServicio
        FROM servicios s
        INNER JOIN facturas f ON s.ID = f.IDServicio
        WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY DATE(s.Fecha)
        ORDER BY Fecha DESC
        """
        cursor.execute(query, (dias,))
        rendimiento_diario = cursor.fetchall()
        
        if rendimiento_diario:
            promedio_servicios = sum(r['TotalServicios'] for r in rendimiento_diario) / len(rendimiento_diario)
            promedio_ingresos = sum(r['IngresoTotal'] for r in rendimiento_diario) / len(rendimiento_diario)
            
            for dia in rendimiento_diario:
                dia['ComparativoPromedio'] = {
                    'Servicios': round((dia['TotalServicios'] / promedio_servicios - 1) * 100, 2),
                    'Ingresos': round((dia['IngresoTotal'] / promedio_ingresos - 1) * 100, 2)
                }
        
        return {
            "PeriodoAnálisis": f"Últimos {dias} días",
            "RendimientoDiario": rendimiento_diario,
            "Promedios": {
                "Servicios": round(promedio_servicios, 2),
                "Ingresos": round(promedio_ingresos, 2)
            } if rendimiento_diario else None,
            "FechaAnálisis": datetime.now().strftime('%Y-%m-%d')
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/analytics/metodos-pago-analisis/", 
        tags=["Análisis"],
        summary="Análisis detallado de métodos de pago")
def get_metodos_pago_analisis(periodo_meses: int = 3):
    """
    Analiza el uso y eficiencia de diferentes métodos de pago.
    
    Parameters:
    - periodo_meses: Período de análisis en meses (default: 3)
    
    Returns:
    - Análisis por método de pago:
        - Frecuencia de uso
        - Montos promedio
        - Tendencias temporales
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            f.MétodoPago,
            COUNT(*) as TotalTransacciones,
            ROUND(SUM(f.Total), 2) as MontoTotal,
            ROUND(AVG(f.Total), 2) as MontoPromedio,
            MIN(f.Total) as MontoMínimo,
            MAX(f.Total) as MontoMáximo
        FROM facturas f
        INNER JOIN servicios s ON f.IDServicio = s.ID
        WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL %s MONTH)
        GROUP BY f.MétodoPago
        ORDER BY MontoTotal DESC
        """
        cursor.execute(query, (periodo_meses,))
        resumen_metodos = cursor.fetchall()
        
        query_temporal = """
        SELECT 
            DATE_FORMAT(s.Fecha, '%Y-%m') as Mes,
            f.MétodoPago,
            COUNT(*) as Transacciones,
            ROUND(SUM(f.Total), 2) as MontoTotal
        FROM facturas f
        INNER JOIN servicios s ON f.IDServicio = s.ID
        WHERE s.Fecha >= DATE_SUB(NOW(), INTERVAL %s MONTH)
        GROUP BY DATE_FORMAT(s.Fecha, '%Y-%m'), f.MétodoPago
        ORDER BY Mes, MontoTotal DESC
        """
        cursor.execute(query_temporal, (periodo_meses,))
        tendencias = cursor.fetchall()
        
        for metodo in resumen_metodos:
            metodo['TendenciaMensual'] = [
                t for t in tendencias if t['MétodoPago'] == metodo['MétodoPago']
            ]
            
            total_transacciones = sum(m['TotalTransacciones'] for m in resumen_metodos)
            metodo['PorcentajeUso'] = round(
                (metodo['TotalTransacciones'] / total_transacciones) * 100, 2
            )
        
        return {
            "PeriodoAnálisis": f"Últimos {periodo_meses} meses",
            "ResumenMétodosPago": resumen_metodos,
            "FechaAnálisis": datetime.now().strftime('%Y-%m-%d')
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()