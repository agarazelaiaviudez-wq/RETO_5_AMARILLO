from flask import Flask, jsonify
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
    conexion = get_connection()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM clientes_credito LIMIT 100")
        clientes = cursor.fetchall()

    conexion.close()

    return jsonify(clientes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)