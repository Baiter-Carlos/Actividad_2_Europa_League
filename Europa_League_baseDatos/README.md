Aqui se le deja los comandos que se uso para hacer la replica de la base de datos.

## acceso a la base de datos primary:
mongosh --host localhost --port 27018.

## Inicializar los servicios:
rs.initiate.

## Servicios inicializados:
rs.status()

## Enviar los datos del servidor a la direccion de las carpetas:
mongod --replSet RS --dbpath="C:\data\db\replica1" --port 27018
