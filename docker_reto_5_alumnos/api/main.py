from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host="db",
        user="clase",
        password="clase123",
        database="creditos",
        cursorclass=pymysql.cursors.DictCursor
    )


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando"
    }



@app.get("/clientes")
def obtener_clientes():
    proposito = request.args.get("proposito")
    limit = request.args.get("limit", default=100000, type=int)
    offset = request.args.get("offset", default=0, type=int)

    # Comprobamos que limit y offset sean correctos
    if limit is None or limit <= 0:
        return {
            "error": {
                "code": 400,
                "message": "El limite debe ser mayor que 0"
            }
        }, 400

    if offset is None or offset < 0:
        return {
            "error": {
                "code": 400,
                "message": "El offset no puede ser negativo"
            }
        }, 400

    conexion = get_connection()

    with conexion.cursor() as cursor:
        if proposito:
            cursor.execute(
                "SELECT * FROM clientes_credito WHERE proposito = %s ORDER BY row_id LIMIT %s OFFSET %s",
                (proposito, limit, offset)
            )
        else:
            cursor.execute(
                "SELECT * FROM clientes_credito ORDER BY row_id LIMIT %s OFFSET %s",
                (limit, offset)
            )

        clientes = cursor.fetchall()

    conexion.close()

    return jsonify(clientes), 200


@app.get("/clientes/<id>")
def obtener_cliente(id):
    conexion = get_connection()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM clientes_credito WHERE id = %s", (id,))
        cliente = cursor.fetchone()

    conexion.close()

    if cliente is None:
        return {"error": {"code": 404, "message": "Cliente no encontrado"}}, 404

    return jsonify(cliente), 200



@app.post("/clientes")
def crear_cliente():
    datos = request.get_json()

    # Comprobar que recibimos datos
    if datos is None:
        return {
            "error": {
                "code": 400,
                "message": "No se han recibido datos"
            }
        }, 400

    # Comprobar campos obligatorios
    campos = ["id", "edad", "ingresos",
              "monto_inicial", "proposito"]

    for c in campos:
        if c not in datos:
            return {
                "error": {
                    "code": 400,
                    "message": f"Falta: {c}"
                }
            }, 400

    # Validar los valores
    if type(datos["edad"]) != int or datos["edad"] <= 0:
        return {
            "error": {
                "code": 400,
                "message": "La edad debe ser un entero positivo"
            }
        }, 400

    if type(datos["ingresos"]) not in [int, float] or datos["ingresos"] < 0:
        return {
            "error": {
                "code": 400,
                "message": "Los ingresos deben ser un numero no negativo"
            }
        }, 400

    if type(datos["monto_inicial"]) not in [int, float] or datos["monto_inicial"] <= 0:
        return {
            "error": {
                "code": 400,
                "message": "El monto inicial debe ser positivo"
            }
        }, 400

    conexion = get_connection()

    with conexion.cursor() as cursor:

        # Comprobar si el ID ya existe
        cursor.execute(
            "SELECT * FROM clientes_credito WHERE id = %s",
            (datos["id"],)
        )

        cliente = cursor.fetchone()

        if cliente is not None:
            conexion.close()
            return {
                "error": {
                    "code": 409,
                    "message": "Ya existe un cliente con ese ID"
                }
            }, 409

        # Insertar el nuevo registro
        cursor.execute(
            "INSERT INTO clientes_credito "
            "(id, edad, ingresos, monto_inicial, proposito) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                datos["id"],
                datos["edad"],
                datos["ingresos"],
                datos["monto_inicial"],
                datos["proposito"]
            )
        )

    conexion.commit()
    conexion.close()

    return jsonify(datos), 201


@app.delete("/clientes/<id>")
def eliminar_cliente(id):
    conexion = get_connection()

    with conexion.cursor() as cursor:
        # Comprobar si existe el cliente
        cursor.execute(
            "SELECT * FROM clientes_credito WHERE id = %s",
            (id,)
        )

        cliente = cursor.fetchone()

        if cliente is None:
            conexion.close()
            return {
                "error": {
                    "code": 404,
                    "message": "Cliente no encontrado"
                }
            }, 404

        # Eliminar el cliente
        cursor.execute(
            "DELETE FROM clientes_credito WHERE id = %s",
            (id,)
        )

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Cliente eliminado correctamente"
    }, 200


@app.put("/clientes/<id>")
def actualizar_cliente(id):
    datos = request.get_json()

    # Comprobar que recibimos datos
    if datos is None:
        return {
            "error": {
                "code": 400,
                "message": "No se han recibido datos"
            }
        }, 400

    # Comprobar campos obligatorios
    campos = ["edad", "ingresos", "monto_inicial", "proposito"]

    for c in campos:
        if c not in datos:
            return {
                "error": {
                    "code": 400,
                    "message": f"Falta: {c}"
                }
            }, 400

    # Validar valores
    if type(datos["edad"]) != int or datos["edad"] <= 0:
        return {
            "error": {
                "code": 400,
                "message": "La edad debe ser un entero positivo"
            }
        }, 400

    if type(datos["ingresos"]) not in [int, float] or datos["ingresos"] < 0:
        return {
            "error": {
                "code": 400,
                "message": "Los ingresos deben ser un numero no negativo"
            }
        }, 400

    if type(datos["monto_inicial"]) not in [int, float] or datos["monto_inicial"] <= 0:
        return {
            "error": {
                "code": 400,
                "message": "El monto inicial debe ser positivo"
            }
        }, 400

    conexion = get_connection()

    with conexion.cursor() as cursor:

        # Comprobar si existe el cliente
        cursor.execute(
            "SELECT * FROM clientes_credito WHERE id = %s",
            (id,)
        )

        cliente = cursor.fetchone()

        if cliente is None:
            conexion.close()
            return {
                "error": {
                    "code": 404,
                    "message": "Cliente no encontrado"
                }
            }, 404

        # Actualizar los datos
        cursor.execute(
            "UPDATE clientes_credito "
            "SET edad = %s, ingresos = %s, "
            "monto_inicial = %s, proposito = %s "
            "WHERE id = %s",
            (
                datos["edad"],
                datos["ingresos"],
                datos["monto_inicial"],
                datos["proposito"],
                id
            )
        )

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Cliente actualizado correctamente"
    }, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)