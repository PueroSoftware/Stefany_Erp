-- ═══════════════════════════════════════════════════════════════════════════
-- BASE DE DATOS: TAJMELL STEFANY E-COMMERCE - VERSIÓN POSTGRESQL
-- VERSIÓN COMPLETA CON TODAS LAS MEJORAS
-- ═══════════════════════════════════════════════════════════════════════════
--
-- Cambios y mejoras incluidos:
--   1. ENUM color_producto: Eliminados opcionA, opcionB, opcionC, opcionD
--   2. ENUM peso_producto: normalizado a '50g' (sin duplicado '50gr')
--   3. ENUM aroma_producto: Eliminados opcionA, opcionB, opcionC, opcionD
--   4. Nueva tabla de ecommerce: historial_navegacion
--   5. orden_produccion: añadida columna prioridad (baja/normal/alta/urgente)
--   6. FKs de materia_prima en tablas de historial con RESTRICT (borrado lógico vía activo)
-- PENDIENTE (fase ecommerce): wishlist, reseñas, cupones, promociones, notificaciones,
--    procedimiento registrar_compra y triggers de automatización de stock/totales
-- ═══════════════════════════════════════════════════════════════════════════
-- ═══════════════════════════════════════════════════════════════════════════
-- CREAR BASE DE DATOS
-- ═══════════════════════════════════════════════════════════════════════════
-- DROP DATABASE IF EXISTS TiendaSoap;
-- CREATE DATABASE TiendaSoap
--     WITH ENCODING 'UTF8'
--     LC_COLLATE = 'es_ES.UTF-8'
--     LC_CTYPE = 'es_ES.UTF-8';
-- Conectar a la BD (ejecutar manualmente o desde psql con \c)
-- \c TiendaSoap;
-- ═══════════════════════════════════════════════════════════════════════════
-- ESQUEMA POR DEFECTO
-- ═══════════════════════════════════════════════════════════════════════════
CREATE SCHEMA IF NOT EXISTS public;
-- ═══════════════════════════════════════════════════════════════════════════
-- TIPOS ENUM (CORREGIDOS)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TYPE estado_proveedor AS ENUM ('activo', 'inactivo');
CREATE TYPE tipo_categoria_materia AS ENUM (
    'base',
    'aroma',
    'color',
    'aditivo',
    'molde',
    'empaque'
);
CREATE TYPE unidad_medida AS ENUM ('kg', 'gr', 'ml', 'lt', 'unidad');
CREATE TYPE tipo_factura AS ENUM ('factura', 'recibo', 'nota_venta', 'boleta');
CREATE TYPE estado_compra AS ENUM ('pendiente', 'recibida', 'cancelada', 'parcial');
CREATE TYPE estado_stock AS ENUM ('disponible', 'agotado', 'vencido', 'reservado');
CREATE TYPE tipo_movimiento AS ENUM ('entrada', 'salida', 'ajuste', 'transferencia');
CREATE TYPE motivo_movimiento AS ENUM (
    'compra',
    'produccion',
    'venta',
    'ajuste',
    'perdida',
    'devolucion',
    'inicial',
    'alerta'
);
CREATE TYPE aroma_producto AS ENUM (
    'lavanda',
    'limon',
    'canela',
    'coco',
    'vainilla',
    'pino_silvestre',
    'manzanilla',
    'romero',
    'rosa',
    'maracuya',
    'naranja',
    'floral',
    'manzana',
    'invictus',
    'dolce_gabanna',
    'kaiak_citrico',
    'kaiak_aero',
    'jockey_club',
    'arroz',
    'avena'
);
-- ═══════════════════════════════════════════════════════════════════════════
-- ENUM color_producto CORREGIDO (SIN opcionA, opcionB, opcionC, opcionD)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TYPE color_producto AS ENUM (
    'rosado_princesa',
    'oro_viejo',
    'rojo_navidad',
    'rojo_bandera',
    'rojo_num40',
    'verde_navidad',
    'verde_manzana',
    'verde_menta_vegetal',
    'green_num12',
    'azul_uva_vegetal',
    'violeta',
    'celeste',
    'negro',
    'amarillo5_vegetal',
    'anaranjado_vegetal'
);
-- ═══════════════════════════════════════════════════════════════════════════
-- ENUM peso_producto (normalizado, sin duplicado '50gr')
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TYPE peso_producto AS ENUM (
    '100g',
    '75g',
    '50g',
    'kit_animalito_75g',
    'kit_piecito_60gr',
    'kit_huellita_75g'
);
CREATE TYPE tipo_producto AS ENUM ('jabon', 'kit', 'promocion', 'muestra');
CREATE TYPE estado_orden_produccion AS ENUM (
    'planificada',
    'en_proceso',
    'completada',
    'cancelada',
    'pausada'
);
CREATE TYPE prioridad_orden AS ENUM ('baja', 'normal', 'alta', 'urgente');
CREATE TYPE tipo_usuario AS ENUM ('cliente', 'fabril');
CREATE TYPE estado_usuario AS ENUM ('activo', 'inactivo', 'bloqueado');
CREATE TYPE estado_pedido AS ENUM (
    'pendiente',
    'confirmado',
    'en_proceso',
    'listo',
    'enviado',
    'entregado',
    'cancelado'
);
CREATE TYPE metodo_pago AS ENUM (
    'efectivo',
    'transferencia',
    'paypal',
    'tarjeta',
    'datáfono'
);
CREATE TYPE estado_pago_pedido AS ENUM (
    'pendiente',
    'pagado',
    'parcial',
    'fallido',
    'reembolsado'
);
CREATE TYPE tipo_venta AS ENUM ('online', 'presencial', 'whatsapp', 'instagram');
CREATE TYPE estado_pago AS ENUM (
    'confirmado',
    'pendiente',
    'fallido',
    'reembolsado'
);
CREATE TYPE tipo_envio AS ENUM ('retiro', 'domicilio', 'correo', 'mensajeria');
CREATE TYPE estado_envio AS ENUM (
    'pendiente',
    'enviado',
    'entregado',
    'cancelado',
    'devuelto'
);
-- ═══════════════════════════════════════════════════════════════════════════
-- FUNCIÓN TRIGGER PARA ON UPDATE CURRENT_TIMESTAMP
-- ═══════════════════════════════════════════════════════════════════════════
CREATE OR REPLACE FUNCTION set_fecha_actualizacion() RETURNS TRIGGER AS $$ BEGIN NEW.fecha_actualizacion = NOW();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- ═══════════════════════════════════════════════════════════════════════════
-- TABLAS MAESTRAS
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE proveedor (
    id_proveedor INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ruc_ci VARCHAR(20),
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    estado estado_proveedor DEFAULT 'activo',
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_proveedor_ruc_ci UNIQUE (ruc_ci)
);
CREATE INDEX idx_proveedor_nombre ON proveedor(nombre);
CREATE INDEX idx_proveedor_estado ON proveedor(estado);
CREATE TABLE categoria_materia (
    id_categoria INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    tipo tipo_categoria_materia NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_categoria_nombre_tipo UNIQUE (nombre, tipo)
);
CREATE TABLE materia_prima (
    id_insumo INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_categoria INT,
    unidad_medida unidad_medida NOT NULL,
    stock_minimo DECIMAL(10, 2) DEFAULT 0,
    stock_maximo DECIMAL(10, 2),
    precio_promedio DECIMAL(10, 2) DEFAULT 0.00,
    observaciones TEXT,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_materia_prima_categoria FOREIGN KEY (id_categoria) REFERENCES categoria_materia(id_categoria) ON DELETE
    SET NULL
);
CREATE INDEX idx_materia_prima_nombre ON materia_prima(nombre);
CREATE INDEX idx_materia_prima_categoria ON materia_prima(id_categoria);
CREATE INDEX idx_materia_prima_activo ON materia_prima(activo);
-- ═══════════════════════════════════════════════════════════════════════════
-- MÓDULO DE COMPRAS
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE compra_materia_prima (
    id_compra INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_proveedor INT,
    numero_factura VARCHAR(50) NOT NULL,
    tipo_factura tipo_factura DEFAULT 'factura',
    fecha_compra DATE DEFAULT CURRENT_DATE,
    fecha_recepcion DATE,
    subtotal DECIMAL(10, 2) DEFAULT 0.00,
    iva DECIMAL(10, 2) DEFAULT 0.00,
    descuento DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) DEFAULT 0.00,
    estado estado_compra DEFAULT 'pendiente',
    observaciones TEXT,
    documento_url VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_compra_materia_prima_proveedor FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor) ON DELETE
    SET NULL,
        CONSTRAINT uq_compra_materia_prima_numero_factura UNIQUE (numero_factura)
);
CREATE INDEX idx_compra_materia_prima_fecha ON compra_materia_prima(fecha_compra);
CREATE INDEX idx_compra_materia_prima_proveedor ON compra_materia_prima(id_proveedor);
CREATE INDEX idx_compra_materia_prima_estado ON compra_materia_prima(estado);
CREATE TABLE detalle_compra (
    id_detalle_compra INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_compra INT,
    id_insumo INT,
    cantidad DECIMAL(10, 2) NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    lote VARCHAR(50),
    fecha_vencimiento DATE,
    observaciones TEXT,
    CONSTRAINT fk_detalle_compra_compra_materia_prima FOREIGN KEY (id_compra) REFERENCES compra_materia_prima(id_compra) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_compra_insumo FOREIGN KEY (id_insumo) REFERENCES materia_prima(id_insumo) ON DELETE RESTRICT
);
CREATE INDEX idx_detalle_compra_compra ON detalle_compra(id_compra);
CREATE INDEX idx_detalle_compra_insumo ON detalle_compra(id_insumo);
CREATE INDEX idx_detalle_compra_lote ON detalle_compra(lote);
-- ═══════════════════════════════════════════════════════════════════════════
-- MÓDULO DE INVENTARIO
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE stock_materia_prima (
    id_stock INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_insumo INT,
    lote VARCHAR(50),
    cantidad_disponible DECIMAL(10, 2) DEFAULT 0,
    cantidad_reservada DECIMAL(10, 2) DEFAULT 0,
    cantidad_total DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad_disponible + cantidad_reservada) STORED,
    fecha_entrada DATE DEFAULT CURRENT_DATE,
    fecha_vencimiento DATE,
    precio_compra DECIMAL(10, 2),
    ubicacion VARCHAR(50),
    estado estado_stock DEFAULT 'disponible',
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_stock_insumo FOREIGN KEY (id_insumo) REFERENCES materia_prima(id_insumo) ON DELETE RESTRICT,
    CONSTRAINT uq_stock_insumo_lote UNIQUE (id_insumo, lote)
);
CREATE INDEX idx_stock_insumo ON stock_materia_prima(id_insumo);
CREATE INDEX idx_stock_lote ON stock_materia_prima(lote);
CREATE INDEX idx_stock_vencimiento ON stock_materia_prima(fecha_vencimiento);
CREATE INDEX idx_stock_estado ON stock_materia_prima(estado);
CREATE TABLE movimiento_stock (
    id_movimiento INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_insumo INT,
    tipo_movimiento tipo_movimiento NOT NULL,
    cantidad DECIMAL(10, 2) NOT NULL,
    stock_anterior DECIMAL(10, 2),
    stock_nuevo DECIMAL(10, 2),
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo motivo_movimiento NOT NULL,
    referencia_id INT,
    referencia_tabla VARCHAR(50),
    observaciones TEXT,
    usuario_registro VARCHAR(100),
    CONSTRAINT fk_movimiento_insumo FOREIGN KEY (id_insumo) REFERENCES materia_prima(id_insumo) ON DELETE RESTRICT
);
CREATE INDEX idx_movimiento_insumo ON movimiento_stock(id_insumo);
CREATE INDEX idx_movimiento_fecha ON movimiento_stock(fecha_movimiento);
CREATE INDEX idx_movimiento_tipo_motivo ON movimiento_stock(tipo_movimiento, motivo);
CREATE INDEX idx_movimiento_referencia ON movimiento_stock(referencia_tabla, referencia_id);
-- ═══════════════════════════════════════════════════════════════════════════
-- MÓDULO DE PRODUCCIÓN
-- ═══════════════════════════════════════════════════════════════════════════
-- ═══════════════════════════════════════════════════════════════════════════
-- TABLA: producto_terminado (CON ENUMS CORREGIDOS)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE producto_terminado (
    id_producto INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_producto VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    aroma aroma_producto,
    color color_producto,
    peso peso_producto NOT NULL,
    tipo tipo_producto DEFAULT 'jabon',
    stock_disponible INT DEFAULT 0,
    stock_reservado INT DEFAULT 0,
    stock_total INT GENERATED ALWAYS AS (stock_disponible + stock_reservado) STORED,
    stock_minimo INT DEFAULT 10,
    stock_maximo INT DEFAULT 100,
    precio_costo DECIMAL(10, 2) DEFAULT 0.00,
    precio_venta DECIMAL(10, 2) DEFAULT 0.00,
    margen_ganancia DECIMAL(5, 2) GENERATED ALWAYS AS (
        CASE
            WHEN precio_costo > 0 THEN (
                (precio_venta - precio_costo) / precio_costo * 100
            )
            ELSE 0
        END
    ) STORED,
    -- Nuevas columnas para calificaciones
    calificacion_promedio DECIMAL(3, 2) DEFAULT 0,
    total_reseñas INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trg_producto_actualizacion BEFORE
UPDATE ON producto_terminado FOR EACH ROW EXECUTE FUNCTION set_fecha_actualizacion();
CREATE INDEX idx_producto_codigo ON producto_terminado(codigo_producto);
CREATE INDEX idx_producto_nombre ON producto_terminado(nombre);
CREATE INDEX idx_producto_aroma ON producto_terminado(aroma);
CREATE INDEX idx_producto_peso ON producto_terminado(peso);
CREATE INDEX idx_producto_tipo ON producto_terminado(tipo);
CREATE INDEX idx_producto_activo ON producto_terminado(activo);
CREATE INDEX idx_producto_stock ON producto_terminado(stock_disponible);
-- ═══════════════════════════════════════════════════════════════════════════
-- TABLA: formula_producto
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE formula_producto (
    id_formula INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_producto INT,
    id_insumo INT,
    cantidad DECIMAL(10, 4) NOT NULL,
    unidad VARCHAR(20),
    orden INT DEFAULT 1,
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_formula_producto FOREIGN KEY (id_producto) REFERENCES producto_terminado(id_producto) ON DELETE CASCADE,
    CONSTRAINT fk_formula_insumo FOREIGN KEY (id_insumo) REFERENCES materia_prima(id_insumo) ON DELETE RESTRICT,
    CONSTRAINT uq_formula_producto_insumo UNIQUE (id_producto, id_insumo)
);
CREATE INDEX idx_formula_producto ON formula_producto(id_producto);
CREATE INDEX idx_formula_insumo ON formula_producto(id_insumo);
-- ═══════════════════════════════════════════════════════════════════════════
-- TABLA: orden_produccion
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE orden_produccion (
    id_orden INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    numero_orden VARCHAR(20) UNIQUE,
    id_producto INT,
    cantidad_producir INT NOT NULL,
    cantidad_producida INT DEFAULT 0,
    fecha_programada DATE,
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    estado estado_orden_produccion DEFAULT 'planificada',
    prioridad prioridad_orden DEFAULT 'normal',
    responsable VARCHAR(100),
    observaciones TEXT,
    costo_total DECIMAL(10, 2) DEFAULT 0.00,
    costo_unitario DECIMAL(10, 2) DEFAULT 0.00,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_orden_producto FOREIGN KEY (id_producto) REFERENCES producto_terminado(id_producto) ON DELETE CASCADE
);
CREATE INDEX idx_orden_fecha ON orden_produccion(fecha_programada);
CREATE INDEX idx_orden_estado ON orden_produccion(estado);
CREATE INDEX idx_orden_producto ON orden_produccion(id_producto);
CREATE INDEX idx_orden_responsable ON orden_produccion(responsable);
-- ═══════════════════════════════════════════════════════════════════════════
-- TABLA: detalle_produccion
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE detalle_produccion (
    id_detalle_produccion INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_orden INT,
    id_insumo INT,
    cantidad_requerida DECIMAL(10, 4),
    cantidad_usada DECIMAL(10, 4),
    lote_usado VARCHAR(50),
    costo_insumo DECIMAL(10, 2),
    observaciones TEXT,
    CONSTRAINT fk_detalle_orden FOREIGN KEY (id_orden) REFERENCES orden_produccion(id_orden) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_insumo FOREIGN KEY (id_insumo) REFERENCES materia_prima(id_insumo) ON DELETE RESTRICT
);
CREATE INDEX idx_detalle_produccion_orden ON detalle_produccion(id_orden);
CREATE INDEX idx_detalle_produccion_insumo ON detalle_produccion(id_insumo);
-- ═══════════════════════════════════════════════════════════════════════════
-- NUEVAS TABLAS DE PRODUCCIÓN: FASES
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE fase_produccion (
    id_fase INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    orden_secuencia INT NOT NULL,
    tiempo_estimado_minutos INT DEFAULT 30,
    requiere_control_calidad BOOLEAN DEFAULT FALSE,
    requiere_insumos_especificos BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_fase_produccion_nombre UNIQUE (nombre),
    CONSTRAINT uq_fase_produccion_orden UNIQUE (orden_secuencia)
);
CREATE TABLE detalle_fase_produccion (
    id_detalle_fase INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_orden_produccion INT NOT NULL,
    id_fase INT NOT NULL,
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    responsable VARCHAR(100),
    estado VARCHAR(20) DEFAULT 'pendiente',
    observaciones TEXT,
    tiempo_real_minutos INT,
    incidencias TEXT,
    CONSTRAINT fk_detalle_fase_orden FOREIGN KEY (id_orden_produccion) REFERENCES orden_produccion(id_orden) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_fase_fase FOREIGN KEY (id_fase) REFERENCES fase_produccion(id_fase) ON DELETE RESTRICT,
    CONSTRAINT ck_detalle_fase_estado CHECK (
        estado IN (
            'pendiente',
            'en_proceso',
            'completada',
            'pausada',
            'cancelada'
        )
    )
);
CREATE INDEX idx_detalle_fase_orden ON detalle_fase_produccion(id_orden_produccion);
CREATE INDEX idx_detalle_fase_estado ON detalle_fase_produccion(estado);
CREATE INDEX idx_detalle_fase_fechas ON detalle_fase_produccion(fecha_inicio, fecha_fin);
-- ═══════════════════════════════════════════════════════════════════════════
-- NUEVAS TABLAS DE PRODUCCIÓN: MERMAS
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE merma_produccion (
    id_merma INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_orden_produccion INT,
    id_insumo INT,
    id_producto INT,
    tipo_merma VARCHAR(30) NOT NULL,
    cantidad_perdida DECIMAL(10, 2) NOT NULL,
    unidad VARCHAR(20),
    motivo VARCHAR(50) NOT NULL,
    valor_perdido DECIMAL(10, 2) DEFAULT 0,
    porcentaje_perdida DECIMAL(5, 2),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registrado_por VARCHAR(100),
    observaciones TEXT,
    CONSTRAINT fk_merma_orden FOREIGN KEY (id_orden_produccion) REFERENCES orden_produccion(id_orden) ON DELETE CASCADE,
    CONSTRAINT fk_merma_insumo FOREIGN KEY (id_insumo) REFERENCES materia_prima(id_insumo) ON DELETE
    SET NULL,
        CONSTRAINT fk_merma_producto FOREIGN KEY (id_producto) REFERENCES producto_terminado(id_producto) ON DELETE
    SET NULL,
        CONSTRAINT ck_merma_tipo CHECK (
            tipo_merma IN ('insumo', 'producto', 'material_empaque')
        ),
        CONSTRAINT ck_merma_motivo CHECK (
            motivo IN (
                'calidad',
                'exceso',
                'derrame',
                'caducidad',
                'defecto',
                'mal_manejo'
            )
        )
);
CREATE INDEX idx_merma_orden ON merma_produccion(id_orden_produccion);
CREATE INDEX idx_merma_fecha ON merma_produccion(fecha_registro);
CREATE INDEX idx_merma_tipo_motivo ON merma_produccion(tipo_merma, motivo);
CREATE TABLE merma_stock (
    id_merma_stock INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_insumo INT,
    cantidad DECIMAL(10, 2),
    fecha_vencimiento DATE,
    fecha_deteccion DATE DEFAULT CURRENT_DATE,
    motivo VARCHAR(50),
    responsable VARCHAR(100),
    observaciones TEXT,
    procesado BOOLEAN DEFAULT FALSE,
    fecha_procesamiento DATE,
    CONSTRAINT fk_merma_stock_insumo FOREIGN KEY (id_insumo) REFERENCES materia_prima(id_insumo) ON DELETE RESTRICT
);
CREATE INDEX idx_merma_stock_insumo ON merma_stock(id_insumo);
CREATE INDEX idx_merma_stock_fecha ON merma_stock(fecha_deteccion);
-- ═══════════════════════════════════════════════════════════════════════════
-- NUEVA TABLA: seguimiento_produccion
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE seguimiento_produccion (
    id_seguimiento INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_orden_produccion INT NOT NULL,
    id_producto INT NOT NULL,
    lote_produccion VARCHAR(50),
    numero_orden VARCHAR(20),
    fecha_inicio TIMESTAMP,
    fecha_fin_estimada TIMESTAMP,
    fecha_fin_real TIMESTAMP,
    estado_actual estado_orden_produccion,
    fase_actual VARCHAR(50),
    porcentaje_avance INT DEFAULT 0,
    responsable_actual VARCHAR(100),
    observaciones_continuas TEXT,
    tiempo_total_estimado_minutos INT,
    tiempo_total_real_minutos INT,
    eficiencia_porcentaje DECIMAL(5, 2),
    cumplimiento_plazo BOOLEAN,
    calidad_aprobada BOOLEAN,
    fecha_control_calidad TIMESTAMP,
    inspector_calidad VARCHAR(100),
    observaciones_calidad TEXT,
    CONSTRAINT fk_seguimiento_orden FOREIGN KEY (id_orden_produccion) REFERENCES orden_produccion(id_orden) ON DELETE CASCADE,
    CONSTRAINT fk_seguimiento_producto FOREIGN KEY (id_producto) REFERENCES producto_terminado(id_producto) ON DELETE CASCADE,
    CONSTRAINT uq_seguimiento_orden UNIQUE (id_orden_produccion)
);
CREATE INDEX idx_seguimiento_orden ON seguimiento_produccion(id_orden_produccion);
CREATE INDEX idx_seguimiento_lote ON seguimiento_produccion(lote_produccion);
CREATE INDEX idx_seguimiento_estado ON seguimiento_produccion(estado_actual);
-- ═══════════════════════════════════════════════════════════════════════════
-- MÓDULO DE ECOMMERCE
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE usuario (
    id_usuario INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    telefono VARCHAR(20),
    direccion TEXT,
    ciudad VARCHAR(50),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    tipo tipo_usuario DEFAULT 'cliente',
    estado estado_usuario DEFAULT 'activo',
    activo BOOLEAN DEFAULT TRUE
);
CREATE INDEX idx_usuario_correo ON usuario(correo);
CREATE INDEX idx_usuario_tipo ON usuario(tipo);
CREATE INDEX idx_usuario_estado ON usuario(estado);
CREATE INDEX idx_usuario_nombre_apellido ON usuario(nombre, apellido);
CREATE TABLE pedido (
    id_pedido INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    numero_pedido VARCHAR(20) UNIQUE,
    id_usuario INT,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado estado_pedido DEFAULT 'pendiente',
    metodo_pago metodo_pago,
    estado_pago estado_pago_pedido DEFAULT 'pendiente',
    subtotal DECIMAL(10, 2) DEFAULT 0.00,
    descuento DECIMAL(10, 2) DEFAULT 0.00,
    iva DECIMAL(10, 2) DEFAULT 0.00,
    envio DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) DEFAULT 0.00,
    observaciones TEXT,
    direccion_envio TEXT,
    contacto_envio VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_pedido_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE
    SET NULL
);
CREATE INDEX idx_pedido_usuario ON pedido(id_usuario);
CREATE INDEX idx_pedido_estado ON pedido(estado);
CREATE INDEX idx_pedido_fecha ON pedido(fecha_pedido);
CREATE INDEX idx_pedido_numero ON pedido(numero_pedido);
CREATE INDEX idx_pedido_estado_pago ON pedido(estado_pago);
CREATE TABLE carrito (
    id_carrito INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pedido INT,
    id_producto INT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2),
    descuento_unitario DECIMAL(10, 2) DEFAULT 0.00,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (
        (cantidad * precio_unitario) - (cantidad * descuento_unitario)
    ) STORED,
    CONSTRAINT fk_carrito_pedido FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    CONSTRAINT fk_carrito_producto FOREIGN KEY (id_producto) REFERENCES producto_terminado(id_producto) ON DELETE
    SET NULL,
        CONSTRAINT uq_carrito_pedido_producto UNIQUE (id_pedido, id_producto)
);
CREATE INDEX idx_carrito_pedido ON carrito(id_pedido);
CREATE INDEX idx_carrito_producto ON carrito(id_producto);
CREATE TABLE venta (
    id_venta INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pedido INT UNIQUE,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_venta DECIMAL(10, 2),
    tipo_venta tipo_venta DEFAULT 'online',
    vendedor VARCHAR(100),
    canal_venta VARCHAR(50),
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_venta_pedido FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE
);
CREATE INDEX idx_venta_fecha ON venta(fecha_venta);
CREATE INDEX idx_venta_tipo ON venta(tipo_venta);
CREATE INDEX idx_venta_vendedor ON venta(vendedor);
CREATE INDEX idx_venta_canal ON venta(canal_venta);
CREATE TABLE detalle_venta (
    id_detalle_venta INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_venta INT,
    id_producto INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    descuento_unitario DECIMAL(10, 2) DEFAULT 0.00,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (
        cantidad * (precio_unitario - descuento_unitario)
    ) STORED,
    costo_unitario DECIMAL(10, 2),
    ganancia_bruta DECIMAL(10, 2) GENERATED ALWAYS AS (
        (precio_unitario - descuento_unitario) - costo_unitario
    ) STORED,
    margen_porcentaje DECIMAL(5, 2) GENERATED ALWAYS AS (
        CASE
            WHEN costo_unitario > 0 THEN (
                (
                    (precio_unitario - descuento_unitario) - costo_unitario
                ) / costo_unitario * 100
            )
            ELSE 0
        END
    ) STORED,
    CONSTRAINT fk_detalle_venta_venta FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_venta_producto FOREIGN KEY (id_producto) REFERENCES producto_terminado(id_producto) ON DELETE
    SET NULL
);
CREATE INDEX idx_detalle_venta_venta ON detalle_venta(id_venta);
CREATE INDEX idx_detalle_venta_producto ON detalle_venta(id_producto);
CREATE TABLE pago (
    id_pago INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pedido INT,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metodo_pago metodo_pago,
    referencia VARCHAR(100),
    monto DECIMAL(10, 2),
    estado estado_pago DEFAULT 'pendiente',
    comprobante_url VARCHAR(255),
    observaciones TEXT,
    CONSTRAINT fk_pago_pedido FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE
);
CREATE INDEX idx_pago_pedido ON pago(id_pedido);
CREATE INDEX idx_pago_estado ON pago(estado);
CREATE INDEX idx_pago_fecha ON pago(fecha_pago);
CREATE TABLE envio (
    id_envio INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pedido INT,
    direccion TEXT,
    ciudad VARCHAR(50),
    telefono_contacto VARCHAR(20),
    tipo_envio tipo_envio DEFAULT 'domicilio',
    costo_envio DECIMAL(10, 2) DEFAULT 0.00,
    fecha_envio DATE,
    fecha_entrega_estimada DATE,
    fecha_entrega_real DATE,
    estado estado_envio DEFAULT 'pendiente',
    tracking_number VARCHAR(100),
    observaciones TEXT,
    CONSTRAINT fk_envio_pedido FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE
);
CREATE INDEX idx_envio_pedido ON envio(id_pedido);
CREATE INDEX idx_envio_estado ON envio(estado);
CREATE INDEX idx_envio_fecha ON envio(fecha_envio);
-- ═══════════════════════════════════════════════════════════════════════════
-- NUEVAS TABLAS DE ECOMMERCE
-- ═══════════════════════════════════════════════════════════════════════════
-- ═══════════════════════════════════════════════════════════════════════════
-- TABLA: historial_navegacion
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE historial_navegacion (
    id_historial INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario INT,
    id_producto INT,
    sesion_id VARCHAR(100),
    fecha_visita TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_historial_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_historial_producto FOREIGN KEY (id_producto) REFERENCES producto_terminado(id_producto) ON DELETE CASCADE
);
CREATE INDEX idx_historial_usuario ON historial_navegacion(id_usuario);
CREATE INDEX idx_historial_producto ON historial_navegacion(id_producto);
CREATE INDEX idx_historial_sesion ON historial_navegacion(sesion_id);