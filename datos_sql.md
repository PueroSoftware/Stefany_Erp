 
Los datos de conexión para acceder a tu PostgreSQL nativo son:

Host (Servidor): localhost o 127.0.0.1

Puerto: 5432

Nombre de la Base de Datos: TiendaSoap

Usuario principal: postgres (propietario por defecto de las 23 tablas)

Usuario alternativo: admin (clave admin123, configurado previamente)


Formas de Ingresar
1. Desde la Terminal (como usuario postgres):

Bash
sudo -u postgres psql -d TiendaSoap
2. Desde la Terminal (como usuario admin):

Bash
psql -h localhost -U admin -d TiendaSoap
