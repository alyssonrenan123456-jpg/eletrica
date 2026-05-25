# Dimensionamento elétrico simplificado (Flask)

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse: `http://localhost:2000`

## O que faz

- Permite cadastrar qualquer equipamento (sem lista fixa)
- Agrupa em circuitos de iluminação, tomadas ou dedicado
- Calcula corrente estimada por circuito
- Sugere disjuntor e bitola de cabo (tabela simplificada)

> Uso educacional. Para projeto real, seguir NBR 5410 e validação profissional.
