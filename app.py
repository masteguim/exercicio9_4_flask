
from flask import Flask, jsonify, request

app = Flask(__name__)

itens = [
    {"id": 1, "nome": "Notebook", "preco": 3500.0},
    {"id": 2, "nome": "Mouse", "preco": 120.0},
]


@app.route("/")
def home():
    return jsonify({
        "mensagem": "API RESTful - Exercicio 9.4",
        "status": "online"
    })


@app.route("/items", methods=["GET"])
def listar_itens():
    return jsonify(itens), 200


@app.route("/items/<int:item_id>", methods=["GET"])
def buscar_item(item_id):
    item = next((i for i in itens if i["id"] == item_id), None)

    if item is None:
        return jsonify({"erro": "Item nao encontrado"}), 404

    return jsonify(item), 200


@app.route("/items", methods=["POST"])
def criar_item():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido"}), 400

    nome = dados.get("nome")
    preco = dados.get("preco")

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "Nome invalido"}), 400

    if isinstance(preco, bool) or not isinstance(preco, (int, float)) or not (0 <= preco < float("inf")):
        return jsonify({"erro": "Preco invalido"}), 400

    novo_id = max((item["id"] for item in itens), default=0) + 1

    novo_item = {
        "id": novo_id,
        "nome": nome.strip(),
        "preco": float(preco)
    }

    itens.append(novo_item)
    return jsonify(novo_item), 201


@app.route("/items/<int:item_id>", methods=["PUT"])
def atualizar_item(item_id):
    item = next((i for i in itens if i["id"] == item_id), None)

    if item is None:
        return jsonify({"erro": "Item nao encontrado"}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido"}), 400

    nome = dados.get("nome")
    preco = dados.get("preco")

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "Nome invalido"}), 400

    if isinstance(preco, bool) or not isinstance(preco, (int, float)) or not (0 <= preco < float("inf")):
        return jsonify({"erro": "Preco invalido"}), 400

    item["nome"] = nome.strip()
    item["preco"] = float(preco)

    return jsonify(item), 200


@app.route("/items/<int:item_id>", methods=["DELETE"])
def excluir_item(item_id):
    item = next((i for i in itens if i["id"] == item_id), None)

    if item is None:
        return jsonify({"erro": "Item nao encontrado"}), 404

    itens.remove(item)
    return jsonify({"mensagem": "Item excluido com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True)
