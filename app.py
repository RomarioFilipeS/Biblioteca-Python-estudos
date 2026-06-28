from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

ARQUIVO_DADOS = "livros.json"


def carregar_livros():
    """Lê os livros do arquivo livros.json. Se o arquivo não existir, cria
    o acervo com alguns livros de exemplo."""
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return [
        {"titulo": "Lógica em Python", "autor": "Ana Ferreira", "disponivel": True},
        {"titulo": "Estruturas de Dados", "autor": "Carlos Mendes", "disponivel": False},
        {"titulo": "Algoritmos na Prática", "autor": "Beatriz Lima", "disponivel": True},
    ]


def salvar_livros():
    """Grava a lista atual de livros no arquivo livros.json."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(livros, f, ensure_ascii=False, indent=2)


livros = carregar_livros()


# ---------- rota que entrega o próprio site ----------
@app.route("/")
def home():
    return send_from_directory(".", "biblioteca.html")


# ---------- API ----------

@app.route("/api/livros", methods=["GET"])
def listar_livros():
    return jsonify(livros)


@app.route("/api/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.get_json()
    titulo = (dados.get("titulo") or "").strip()
    autor = (dados.get("autor") or "").strip()

    if not titulo or not autor:
        return jsonify({"erro": "Título e autor são obrigatórios"}), 400

    livros.append({"titulo": titulo, "autor": autor, "disponivel": True})
    salvar_livros()
    return jsonify(livros), 201


@app.route("/api/livros/<int:indice>/emprestar", methods=["POST"])
def emprestar_livro(indice):
    if indice < 0 or indice >= len(livros):
        return jsonify({"erro": "Livro não encontrado"}), 404

    livros[indice]["disponivel"] = False
    salvar_livros()
    return jsonify(livros)


@app.route("/api/livros/<int:indice>/devolver", methods=["POST"])
def devolver_livro(indice):
    if indice < 0 or indice >= len(livros):
        return jsonify({"erro": "Livro não encontrado"}), 404

    livros[indice]["disponivel"] = True
    salvar_livros()
    return jsonify(livros)


@app.route("/api/livros/<int:indice>", methods=["DELETE"])
def remover_livro(indice):
    if indice < 0 or indice >= len(livros):
        return jsonify({"erro": "Livro não encontrado"}), 404

    livros.pop(indice)
    salvar_livros()
    return jsonify(livros)


if __name__ == "__main__":
    app.run(debug=True)