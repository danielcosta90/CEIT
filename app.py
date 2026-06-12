from flask import Flask, jsonify, request
from db import conectar
from flask import render_template

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

@app.route("/categorias/<int:id>", methods=["PUT"])
def atualizar_categoria(id):
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

        cursor.execute("SELECT id FROM categoria WHERE id = %s;", (id,))
        categoria = cursor.fetchone()

        if not categoria:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Categoria não encontrada."
            }), 404

        cursor.execute(
            """
            UPDATE categoria
            SET nome = %s, descricao = %s
            WHERE id = %s;
            """,
            (nome, descricao, id)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Categoria atualizada com sucesso."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500

@app.route("/categorias/<int:id>", methods=["DELETE"])
def deletar_categoria(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM categoria WHERE id = %s;", (id,))
        categoria = cursor.fetchone()

        if not categoria:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Categoria não encontrada."
            }), 404

        cursor.execute("DELETE FROM categoria WHERE id = %s;", (id,))
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Categoria removida com sucesso."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500

@app.route("/fornecedores", methods=["GET"])
def listar_fornecedores():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, cnpj, telefone, email, endereco
            FROM fornecedor
            ORDER BY id;
        """)
        resultados = cursor.fetchall()

        fornecedores = []
        for item in resultados:
            fornecedores.append({
                "id": item[0],
                "nome": item[1],
                "cnpj": item[2],
                "telefone": item[3],
                "email": item[4],
                "endereco": item[5]
            })

        cursor.close()
        conexao.close()

        return jsonify(fornecedores)

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500
        
@app.route("/fornecedores", methods=["POST"])
def cadastrar_fornecedor():
    try:
        dados = request.get_json()

        nome = dados.get("nome")
        cnpj = dados.get("cnpj")
        telefone = dados.get("telefone")
        email = dados.get("email")
        endereco = dados.get("endereco")

        if not nome:
            return jsonify({
                "status": "erro",
                "mensagem": "O campo nome é obrigatório."
            }), 400

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO fornecedor (nome, cnpj, telefone, email, endereco)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (nome, cnpj, telefone, email, endereco)
        )

        id_novo = cursor.fetchone()[0]
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Fornecedor cadastrado com sucesso.",
            "id": id_novo
        }), 201

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500
        
@app.route("/fornecedores/<int:id>", methods=["PUT"])
def atualizar_fornecedor(id):
    try:
        dados = request.get_json()

        nome = dados.get("nome")
        cnpj = dados.get("cnpj")
        telefone = dados.get("telefone")
        email = dados.get("email")
        endereco = dados.get("endereco")

        if not nome:
            return jsonify({
                "status": "erro",
                "mensagem": "O campo nome é obrigatório."
            }), 400

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM fornecedor WHERE id = %s;", (id,))
        fornecedor = cursor.fetchone()

        if not fornecedor:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Fornecedor não encontrado."
            }), 404

        cursor.execute(
            """
            UPDATE fornecedor
            SET nome = %s, cnpj = %s, telefone = %s, email = %s, endereco = %s
            WHERE id = %s;
            """,
            (nome, cnpj, telefone, email, endereco, id)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Fornecedor atualizado com sucesso."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500  
        
@app.route("/fornecedores/<int:id>", methods=["DELETE"])
def deletar_fornecedor(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM fornecedor WHERE id = %s;", (id,))
        fornecedor = cursor.fetchone()

        if not fornecedor:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Fornecedor não encontrado."
            }), 404

        cursor.execute("DELETE FROM fornecedor WHERE id = %s;", (id,))
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Fornecedor removido com sucesso."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500    
        
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT 
                p.id,
                p.nome,
                p.descricao,
                p.codigo_barras,
                p.preco_custo,
                p.preco_venda,
                p.quantidade_estoque,
                p.estoque_minimo,
                p.id_categoria,
                c.nome AS categoria,
                p.id_fornecedor,
                f.nome AS fornecedor
            FROM produto p
            INNER JOIN categoria c ON p.id_categoria = c.id
            INNER JOIN fornecedor f ON p.id_fornecedor = f.id
            ORDER BY p.id;
        """)
        resultados = cursor.fetchall()

        produtos = []
        for item in resultados:
            produtos.append({
                "id": item[0],
                "nome": item[1],
                "descricao": item[2],
                "codigo_barras": item[3],
                "preco_custo": float(item[4]),
                "preco_venda": float(item[5]),
                "quantidade_estoque": item[6],
                "estoque_minimo": item[7],
                "id_categoria": item[8],
                "categoria": item[9],
                "id_fornecedor": item[10],
                "fornecedor": item[11]
            })

        cursor.close()
        conexao.close()

        return jsonify(produtos)

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500
        
@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    try:
        dados = request.get_json()

        nome = dados.get("nome")
        descricao = dados.get("descricao")
        codigo_barras = dados.get("codigo_barras")
        preco_custo = dados.get("preco_custo")
        preco_venda = dados.get("preco_venda")
        quantidade_estoque = dados.get("quantidade_estoque")
        estoque_minimo = dados.get("estoque_minimo")
        id_categoria = dados.get("id_categoria")
        id_fornecedor = dados.get("id_fornecedor")

        if not nome or id_categoria is None or id_fornecedor is None:
            return jsonify({
                "status": "erro",
                "mensagem": "Nome, categoria e fornecedor são obrigatórios."
            }), 400

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM categoria WHERE id = %s;", (id_categoria,))
        categoria = cursor.fetchone()

        if not categoria:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Categoria não encontrada."
            }), 404

        cursor.execute("SELECT id FROM fornecedor WHERE id = %s;", (id_fornecedor,))
        fornecedor = cursor.fetchone()

        if not fornecedor:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Fornecedor não encontrado."
            }), 404

        cursor.execute(
            """
            INSERT INTO produto (
                nome, descricao, codigo_barras, preco_custo, preco_venda,
                quantidade_estoque, estoque_minimo, id_categoria, id_fornecedor
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                nome,
                descricao,
                codigo_barras,
                preco_custo,
                preco_venda,
                quantidade_estoque,
                estoque_minimo,
                id_categoria,
                id_fornecedor
            )
        )

        id_novo = cursor.fetchone()[0]
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Produto cadastrado com sucesso.",
            "id": id_novo
        }), 201

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500
        
@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    try:
        dados = request.get_json()

        nome = dados.get("nome")
        descricao = dados.get("descricao")
        codigo_barras = dados.get("codigo_barras")
        preco_custo = dados.get("preco_custo")
        preco_venda = dados.get("preco_venda")
        quantidade_estoque = dados.get("quantidade_estoque")
        estoque_minimo = dados.get("estoque_minimo")
        id_categoria = dados.get("id_categoria")
        id_fornecedor = dados.get("id_fornecedor")

        if not nome or id_categoria is None or id_fornecedor is None:
            return jsonify({
                "status": "erro",
                "mensagem": "Nome, categoria e fornecedor são obrigatórios."
            }), 400

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM produto WHERE id = %s;", (id,))
        produto = cursor.fetchone()

        if not produto:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Produto não encontrado."
            }), 404

        cursor.execute("SELECT id FROM categoria WHERE id = %s;", (id_categoria,))
        categoria = cursor.fetchone()

        if not categoria:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Categoria não encontrada."
            }), 404

        cursor.execute("SELECT id FROM fornecedor WHERE id = %s;", (id_fornecedor,))
        fornecedor = cursor.fetchone()

        if not fornecedor:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Fornecedor não encontrado."
            }), 404

        cursor.execute(
            """
            UPDATE produto
            SET nome = %s,
                descricao = %s,
                codigo_barras = %s,
                preco_custo = %s,
                preco_venda = %s,
                quantidade_estoque = %s,
                estoque_minimo = %s,
                id_categoria = %s,
                id_fornecedor = %s
            WHERE id = %s;
            """,
            (
                nome,
                descricao,
                codigo_barras,
                preco_custo,
                preco_venda,
                quantidade_estoque,
                estoque_minimo,
                id_categoria,
                id_fornecedor,
                id
            )
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Produto atualizado com sucesso."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500
        
@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM produto WHERE id = %s;", (id,))
        produto = cursor.fetchone()

        if not produto:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Produto não encontrado."
            }), 404

        cursor.execute("DELETE FROM produto WHERE id = %s;", (id,))
        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Produto removido com sucesso."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500   
        
@app.route("/movimentacoes", methods=["GET"])
def listar_movimentacoes():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT 
                m.id,
                m.id_produto,
                p.nome,
                m.tipo_movimentacao,
                m.quantidade,
                m.data_movimentacao,
                m.observacao
            FROM movimentacao_estoque m
            INNER JOIN produto p ON m.id_produto = p.id
            ORDER BY m.id;
        """)
        resultados = cursor.fetchall()

        movimentacoes = []
        for item in resultados:
            movimentacoes.append({
                "id": item[0],
                "id_produto": item[1],
                "produto": item[2],
                "tipo_movimentacao": item[3],
                "quantidade": item[4],
                "data_movimentacao": str(item[5]),
                "observacao": item[6]
            })

        cursor.close()
        conexao.close()

        return jsonify(movimentacoes)

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500
        
@app.route("/movimentacoes", methods=["POST"])
def cadastrar_movimentacao():
    try:
        dados = request.get_json()

        id_produto = dados.get("id_produto")
        tipo_movimentacao = dados.get("tipo_movimentacao")
        quantidade = dados.get("quantidade")
        observacao = dados.get("observacao")

        if id_produto is None or not tipo_movimentacao or quantidade is None:
            return jsonify({
                "status": "erro",
                "mensagem": "Produto, tipo de movimentação e quantidade são obrigatórios."
            }), 400

        if tipo_movimentacao not in ["ENTRADA", "SAIDA"]:
            return jsonify({
                "status": "erro",
                "mensagem": "Tipo de movimentação deve ser ENTRADA ou SAIDA."
            }), 400

        if quantidade <= 0:
            return jsonify({
                "status": "erro",
                "mensagem": "A quantidade deve ser maior que zero."
            }), 400

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, quantidade_estoque
            FROM produto
            WHERE id = %s;
        """, (id_produto,))
        produto = cursor.fetchone()

        if not produto:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Produto não encontrado."
            }), 404

        estoque_atual = produto[1]

        if tipo_movimentacao == "SAIDA" and quantidade > estoque_atual:
            cursor.close()
            conexao.close()
            return jsonify({
                "status": "erro",
                "mensagem": "Estoque insuficiente para realizar a saída."
            }), 400

        cursor.execute("""
            INSERT INTO movimentacao_estoque (
                id_produto, tipo_movimentacao, quantidade, observacao
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (id_produto, tipo_movimentacao, quantidade, observacao))

        id_movimentacao = cursor.fetchone()[0]

        if tipo_movimentacao == "ENTRADA":
            novo_estoque = estoque_atual + quantidade
        else:
            novo_estoque = estoque_atual - quantidade

        cursor.execute("""
            UPDATE produto
            SET quantidade_estoque = %s
            WHERE id = %s;
        """, (novo_estoque, id_produto))

        conexao.commit()

        cursor.close()
        conexao.close()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Movimentação cadastrada com sucesso.",
            "id_movimentacao": id_movimentacao,
            "estoque_atualizado": novo_estoque
        }), 201

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500

@app.route("/produtos/estoque-baixo", methods=["GET"])
def listar_produtos_estoque_baixo():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT 
                p.id,
                p.nome,
                p.quantidade_estoque,
                p.estoque_minimo,
                c.nome AS categoria,
                f.nome AS fornecedor
            FROM produto p
            INNER JOIN categoria c ON p.id_categoria = c.id
            INNER JOIN fornecedor f ON p.id_fornecedor = f.id
            WHERE p.quantidade_estoque <= p.estoque_minimo
            ORDER BY p.id;
        """)

        resultados = cursor.fetchall()

        produtos = []
        for item in resultados:
            produtos.append({
                "id": item[0],
                "nome": item[1],
                "quantidade_estoque": item[2],
                "estoque_minimo": item[3],
                "categoria": item[4],
                "fornecedor": item[5]
            })

        cursor.close()
        conexao.close()

        return jsonify(produtos)

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500
        
@app.route("/produtos/busca", methods=["GET"])
def buscar_produto_por_nome():
    try:
        nome = request.args.get("nome")

        if not nome:
            return jsonify({
                "status": "erro",
                "mensagem": "Informe o nome para busca."
            }), 400

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT 
                p.id,
                p.nome,
                p.descricao,
                p.codigo_barras,
                p.preco_custo,
                p.preco_venda,
                p.quantidade_estoque,
                p.estoque_minimo,
                c.nome AS categoria,
                f.nome AS fornecedor
            FROM produto p
            INNER JOIN categoria c ON p.id_categoria = c.id
            INNER JOIN fornecedor f ON p.id_fornecedor = f.id
            WHERE p.nome ILIKE %s
            ORDER BY p.id;
        """, (f"%{nome}%",))

        resultados = cursor.fetchall()

        produtos = []
        for item in resultados:
            produtos.append({
                "id": item[0],
                "nome": item[1],
                "descricao": item[2],
                "codigo_barras": item[3],
                "preco_custo": float(item[4]),
                "preco_venda": float(item[5]),
                "quantidade_estoque": item[6],
                "estoque_minimo": item[7],
                "categoria": item[8],
                "fornecedor": item[9]
            })

        cursor.close()
        conexao.close()

        return jsonify(produtos)

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500 
        
@app.route("/app")
def pagina_inicial():
    return render_template("index.html")
                   
if __name__ == "__main__":
    app.run(debug=True)     