from math import ceil
from flask import Flask, render_template, request

app = Flask(__name__)

TENSAO_PADRAO = 220.0
FATOR_SEGURANCA = 1.25

DISJUNTORES_PADRAO = [10, 16, 20, 25, 32, 40, 50, 63]
CABOS = [
    (15, 1.5),
    (21, 2.5),
    (28, 4.0),
    (36, 6.0),
    (50, 10.0),
    (68, 16.0),
]


def escolher_disjuntor(corrente_a: float) -> int:
    for dj in DISJUNTORES_PADRAO:
        if dj >= corrente_a:
            return dj
    return DISJUNTORES_PADRAO[-1]


def escolher_cabo(corrente_a: float) -> float:
    for corrente_max, secao in CABOS:
        if corrente_a <= corrente_max:
            return secao
    return CABOS[-1][1]


def normalizar_nome(nome: str) -> str:
    return " ".join(nome.strip().split())


def classificar_circuito(nome: str, potencia_w: float, grupo: str) -> str:
    nome_l = nome.lower()

    if grupo == "dedicado" or potencia_w >= 2000 or "chuveiro" in nome_l:
        return f"Circuito exclusivo - {nome}"
    if grupo == "iluminacao":
        return "Circuito de iluminação (agrupado)"
    return "Circuito de tomadas gerais (TUG agrupado)"


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = []
    erro = None

    if request.method == "POST":
        try:
            tensao_v = float(request.form.get("tensao_v", TENSAO_PADRAO))
            nomes = request.form.getlist("nome[]")
            potencias = request.form.getlist("potencia[]")
            grupos = request.form.getlist("grupo[]")

            circuitos = {}
            for nome_raw, potencia_raw, grupo_raw in zip(nomes, potencias, grupos):
                nome = normalizar_nome(nome_raw)
                if not nome:
                    continue

                potencia = float(potencia_raw)
                if potencia <= 0:
                    continue

                grupo = grupo_raw if grupo_raw in {"iluminacao", "tomadas", "dedicado"} else "tomadas"
                circuito = classificar_circuito(nome, potencia, grupo)

                if circuito not in circuitos:
                    circuitos[circuito] = {"itens": [], "potencia_total_w": 0.0}

                circuitos[circuito]["itens"].append({"nome": nome, "potencia_w": potencia})
                circuitos[circuito]["potencia_total_w"] += potencia

            for circuito_nome, info in circuitos.items():
                potencia_total = info["potencia_total_w"]
                corrente = potencia_total / tensao_v
                corrente_projeto = corrente * FATOR_SEGURANCA
                disjuntor = escolher_disjuntor(corrente_projeto)
                cabo = escolher_cabo(disjuntor)

                resultado.append(
                    {
                        "circuito": circuito_nome,
                        "itens": info["itens"],
                        "potencia_total_w": round(potencia_total, 2),
                        "corrente_a": round(corrente, 2),
                        "corrente_projeto_a": round(corrente_projeto, 2),
                        "disjuntor_a": disjuntor,
                        "cabo_mm2": cabo,
                    }
                )

        except ValueError:
            erro = "Verifique os campos numéricos: tensão e potência devem ser números válidos."

    return render_template("index.html", resultado=resultado, erro=erro, tensao_padrao=TENSAO_PADRAO)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000, debug=True)
