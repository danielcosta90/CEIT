from flask import Flask, jsonify, request
from db import conectar

app = Flask(__name__)

@app.route("/")
def home():
    return "API do projeto C.E.I.T. está funcionando!"

@app.route("/teste-banco")
def teste_banco():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT version();")
        versao = cursor.fetchone()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Conexão com banco realizada com sucesso",
            "versao_postgresql": versao[0]
        })
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        })

@app.route("/categorias", methods=["GET"])
def listar_categorias():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome, descricao FROM categoria ORDER BY id;")
        resultados = cursor.fetchall()

        categorias = []
        for item in resultados:
            categorias.append({
                "id": item[0],
                "nome": item[1],
                "descricao": item[2]
            })

        cursor.close()
        conexao.close()

        return jsonify(categorias)

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        })

@app.route("/categorias", methods=["POST"])
def cadastrar_categoria():
    try:
        dados = request.get_json()

        nome = dados.get("nome")
        descricao = dados.get("descricao")

        if not nome:
            return jsonify({
                "status": "erro",
                "mensagem": "O campo nome é obrigatório."
            }), 400

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO categoria (nome, descricao) VALUES (%s, %s) RETURNING id;",
            (nome, descricao)
        )

        id_novo = cursor.fetchone()[0]
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Categoria cadastrada com sucesso.",
            "id": id_novo
        }), 201

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)