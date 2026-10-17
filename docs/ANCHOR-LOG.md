# ANCHOR-LOG — Anclaje externo de head_hash

Mecanismo: el head_hash verificado de cada ledger serio se commitea en este
archivo; el historial público de GitHub time-stamps el anclaje. Un tercero
con el ledger privado recalcula verify_ledger y compara contra la entrada
más reciente aquí. Fall-Closed: una cadena rota NO se ancla.

| fecha_utc | ledger | head_hash | chain_ok | valid/total |
|---|---|---|---|---|
| 2026-10-17 01:14 | evidence/relay_META-AI.jsonl | 190918a87fe9838a38b5bac141db9acfe8c8032d82017893cec1f5df800f3131 | True | 11/11 |
| 2026-10-17 01:14 | evidence/relay_GROK.jsonl | 972906ddb7d39e1af8900441c5861cc977394f4aaf4cc13fbdfca59218193981 | True | 5/5 |
