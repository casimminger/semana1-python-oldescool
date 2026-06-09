# PROMPT 1 — Clasificador de Mails
# Técnica: Few-shot + Structured Output
# Uso: Clasificar mails entrantes automáticamente

CLASIFICADOR_MAILS = """Clasificá este mail en una de estas categorías:
- CONSULTA
- RECLAMO
- PRESUPUESTO
- URGENTE

Ejemplos:
Mail: "necesito el presupuesto para mañana" → PRESUPUESTO
Mail: "es un escándalo, nadie me responde" → RECLAMO
Mail: "el sistema cayó, necesito solución ya" → URGENTE

Ahora clasificá este:
Mail: "{mail}"

Respondé ÚNICAMENTE en JSON:
{{"categoria": "CATEGORIA", "razon": "explicación breve"}}
No agregues texto fuera del JSON."""
