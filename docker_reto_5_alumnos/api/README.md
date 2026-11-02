# RETO_5_AMARILLO

## API REST de préstamos - Reto 5

En este reto hemos creado una **API REST con Python y Flask** para consultar y modificar información de préstamos guardada en una base de datos **MySQL**. También hemos utilizado una API externa de **Eurostat** para consultar datos de desempleo de España. Los datos se trabajan con formato JSON.

Hemos probado las peticiones con **Postman** y hemos utilizado los datos obtenidos de nuestra API para trabajar en **Power BI**.

## Herramientas que hemos utilizado

- **Python y Flask:** para programar la API.
- **MySQL y PyMySQL:** para almacenar y consultar los préstamos.
- **Requests:** para hacer la petición a Eurostat.
- **Docker:** para ejecutar los servicios del proyecto.
- **Postman:** para probar que funcionan las rutas.
- **Power BI:** para analizar los préstamos de Automóvil.

## Cómo iniciar la API

El código de nuestra API está en el **archivo main.py.**

Para ponerla en marcha, seguimos estos pasos:

1. Abrimos una **terminal** en la carpeta del proyecto.
2. Entramos en la **carpeta** donde están los archivos de **Docker**:
   cd docker_reto_5_alumnos
3. **Abrimos Docker Desktop** y comprobamos que está funcionando.
4. En la misma terminal ejecutamos: **docker compose up**
5. Dejamos la terminal abierta mientras usamos la API. Cuando los servicios estén iniciados, podemos comprobar que funciona entrando en: `http://127.0.0.1:8000`
   Si todo está correcto, aparece el mensaje **API funcionando**.

## Rutas de la API

| Método | Ruta               | Función                                     | Respuesta habitual |
| ------- | ------------------ | -------------------------------------------- | ------------------ |
| GET     | `/`              | Comprobar que la API está funcionando.      | 200                |
| GET     | `/clientes`      | Obtener la lista de préstamos.              | 200                |
| GET     | `/clientes/<id>` | Consultar un préstamo por su identificador. | 200 / 404          |
| POST    | `/clientes`      | Añadir un nuevo préstamo.                  | 201 / 400 / 409    |
| PUT     | `/clientes/<id>` | Modificar los datos de un préstamo.         | 200 / 400 / 404    |
| DELETE  | `/clientes/<id>` | Eliminar un préstamo.                       | 200 / 404          |
| GET     | `/desempleo`     | Consultar los datos de Eurostat.             | 200 / 502          |

## Cómo hacer las pruebas

Con la API y la base de datos en funcionamiento, utilizamos **Postman** con la dirección `http://127.0.0.1:8000`.

### Consultar préstamos

```text
GET http://127.0.0.1:8000/clientes
```

También podemos utilizar los parámetros `proposito`, `limit` y `offset` para filtrar y paginar los resultados:

```text
GET http://127.0.0.1:8000/clientes?proposito=Automóvil&limit=10&offset=0
```

- `proposito`: propósito de los préstamos que queremos consultar.
- `limit`: número máximo de registros que devuelve la petición (por defecto, 100000).
- `offset`: posición desde la que empieza a devolver registros (por defecto, 0).

Para consultar un préstamo concreto:

```text
GET http://127.0.0.1:8000/clientes/ID_DEL_PRESTAMO
```

Sustituimos `ID_DEL_PRESTAMO` por un identificador existente.

### Añadir un préstamo

En Postman elegimos **POST**, la ruta `/clientes` y **Body → raw → JSON**. Por ejemplo:

```json
{
  "id": "PRUEBA001",
  "edad": 30,
  "ingresos": 25000,
  "monto_inicial": 15000,
  "proposito": "Automóvil"
}
```

### Modificar o eliminar un préstamo

Para modificar un registro utilizamos `PUT /clientes/<id>` y enviamos un JSON con `edad`, `ingresos`, `monto_inicial` y `proposito`.

Para eliminar un registro utilizamos `DELETE /clientes/<id>`.

Como POST, PUT y DELETE pueden cambiar los datos de MySQL, así que las pruebas las realizamos con registros de prueba.

## Códigos de respuesta

| Código | Significado en nuestra API                  |
| ------- | ------------------------------------------- |
| 200     | La petición se ha realizado correctamente. |
| 201     | Se ha creado un préstamo.                  |
| 400     | Faltan datos o hay valores incorrectos.     |
| 404     | No se ha encontrado el préstamo.           |
| 409     | Ya existe un préstamo con ese ID.          |
| 502     | Ha fallado la consulta a Eurostat.          |

## Consulta a Eurostat

La ruta `GET /desempleo` consulta la API de Eurostat con la librería `requests`.

```text
GET http://127.0.0.1:8000/desempleo
```

En nuestro código utilizamos estos parámetros:

- `geo=ES`: España.
- `sex=T`: total de sexos.
- `age=TOTAL`: total de edades.
- `unit=PC_ACT`: porcentaje de la población activa.
- `s_adj=SA`: datos ajustados estacionalmente.

## Comprobaciones realizadas

Hemos realizado pruebas con Postman para comprobar que las rutas funcionan y devuelven respuestas JSON. También hemos probado errores de validación, por ejemplo enviar el campo `proposito` vacío en una petición POST o PUT, que devuelve un **400**.

Finalmente, hemos utilizado la información de `/clientes` en Power BI para analizar la cartera de préstamos de Automóvil de Lagun Aro.
