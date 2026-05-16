---
language: es
persona_id: PERSONA-PARTNER-JOINT-EQUITY
channel_id: CHAN-EMAIL-INBOUND
artifact_class: intro_message
brand_voice: BRAND_SPANISH_PATTERNS
distance_variants_covered: [N2, N3]
last_review: 2026-04-30
---

## Variant — N2 (partner referido por puente conocido)

Hola [Nombre],

[Nombre del puente] me indicó que tienes una idea de SaaS y buscas un equipo capaz de construirla a cambio de equidad o revenue share. Es exactamente el tipo de colaboración que mantenemos en cartera.

Para acelerar la conversación, te paso el alcance compacto de cómo trabajamos en este modelo:

- Holistika entrega ingeniería + operación; el partner aporta el conocimiento del cliente final y la demanda.
- Arquitectura congelada antes de codificar; entrega gobernada con verificación automática.
- Modelo de remuneración: equidad / revenue share según el caso (a confirmar tras evaluar encaje).
- Criterios de entrada (necesitamos los tres): demanda recurrente real del cliente del partner, reutilización ≥ 60 % de nuestra pila técnica, y proyección de payback alineada con nuestro umbral interno LTV:CAC.

Propongo 30 min para entender tu hipótesis de producto y ver si encajamos. Si prefieres mandar primero un brief escrito, también es válido.

Un saludo,
[Nombre del fundador]
Holistika Research

> **Regla de voz (BRAND_SPANISH_PATTERNS):** N2 partner joint-equity — abrir nombrando al puente, declarar el modelo en bullet, listar los **3 criterios de entrada** (no se negocian). Tono peer_consulting, "tú".

---

## Variant — N3 (partner conocido a través de cadena de dos)

Hola [Nombre],

Me llega tu mensaje a través de [nombre del puente más cercano], que a su vez te conoce por [contexto del puente más lejano]. Agradezco la cadena de introducción y te respondo con el mismo formato compacto que usamos para evaluar oportunidades de equidad conjunta.

[Resto idéntico al variante N2, ajustando el primer párrafo]

> **Regla de voz:** N3 — explicitar la cadena completa para que la otra parte vea que la relación está mapeada; el resto del mensaje sigue el formato N2.

---

> **Nota operativa (no se envía).** Capturar al partner en `GOI_POI_REGISTER.csv` con `class=partner`, `distance_band=N2|N3`, `bridge_via=<puente más cercano>`. Cruzar la oportunidad con `CHANNEL_STRATEGY.md` Channel 6.
