 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..af933daf5121d52f5e7d71c2639bc466011f28fe
--- /dev/null
+++ b/README.md
@@ -0,0 +1,21 @@
+# Dimensionamento elétrico simplificado (Flask)
+
+## Como executar
+
+```bash
+python3 -m venv .venv
+source .venv/bin/activate
+pip install -r requirements.txt
+python app.py
+```
+
+Acesse: `http://localhost:2000`
+
+## O que faz
+
+- Permite cadastrar qualquer equipamento (sem lista fixa)
+- Agrupa em circuitos de iluminação, tomadas ou dedicado
+- Calcula corrente estimada por circuito
+- Sugere disjuntor e bitola de cabo (tabela simplificada)
+
+> Uso educacional. Para projeto real, seguir NBR 5410 e validação profissional.
 
EOF
)
