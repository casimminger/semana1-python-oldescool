# PROMPT 5 — Chain-of-Thought para Análisis de Urgencia
# Técnica: Chain-of-thought
# Uso: Analizar situaciones complejas paso a paso antes de decidir
# Documentado como ejemplo de la técnica para el portfolio

CHAIN_OF_THOUGHT_URGENCIA = """Analizá esta situación paso a paso y tomá una decisión.

<situacion>
{situacion}
</situacion>

Seguí estos pasos obligatoriamente:
1. ¿Qué está pasando exactamente?
2. ¿Hay consecuencias si no se actúa rápido?
3. ¿Hay una fecha límite implícita o explícita?
4. ¿Qué información falta para decidir mejor?
5. Conclusión: ¿qué acción recomendás y por qué?

Pensá en voz alta en cada paso antes de dar la conclusión final.
No saltees pasos aunque la respuesta parezca obvia."""
