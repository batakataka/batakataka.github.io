# BaTaKá TaKá

Minijuego web de **Bataká**, la bebida energética con NOx.

Las dos latas (Piña y Cereza) giran en 3D. Cada toque suena "ta-ka" y suma una lata al carrito; la lata crece y, con 18 takás, explota (TaKáBOOM) y vuelve a aparecer, sin límite. Descuento por escalones:

- 6 latas: 10 %
- 12 latas: 15 %
- explotar una lata: 20 %

Promo 5x3 (`CONFIG.promo`, desde el 7 de noviembre de 2026, sin fecha de fin): con TaKáBOOM el pedido paga lo más barato entre −20 % y un solo 5x3 (lleva 5, paga 3) más el resto con la tabla. Para ponerle fin, agrega `hasta` en `CONFIG.promo`; pasada esa hora vuelve sola al −20 %. El mensaje de WhatsApp marca `🏷️5x3` cuando aplica y el carrito tiene el botón "Quedarme con 5 por $9".

Sitio estático (HTML + three.js). Archivos:

- `index.html`: página y lógica del juego (precios y escalones en el bloque `CONFIG`).
- `lata_pina.json`, `lata_cereza.json`: modelos 3D de las latas.
- `tex_pina.jpg`, `tex_cereza.jpg`: etiquetas.

El botón de pago abre WhatsApp con el pedido en lenguaje TaKá, por ejemplo: "TaKá! BaTaKá? TaKá 🍍×5 🍒×3 → 8 BaTaKáS TaKá $21.60". Precio: $3 por BaTaKá (`CONFIG.precio`); número de pedidos en `CONFIG.whatsapp`.

Promos y topes (`CONFIG`):
- `tope`: ningún pedido recibe más del 20 % de descuento, salvo el ahorro de $6 del pack 5x3 (5 latas por $9).
- `caja`: Caja Grupo 24 a $58 (envío incluido, porque los pedidos de más de $50 ya lo incluyen).
- `regalos`: en el carrito, "5 vacías = 1 llena" o "Me invitó un pana" (+1 lata, máximo 1 por pedido; se confirma por WhatsApp). El link `?pana=1` deja marcado "Me invitó un pana".
- El mensaje de WhatsApp marca `🏷️5x3`, `🏷️Caja24`, `🏷️+1 vacías` o `🏷️+1 pana:Nombre`.
- La cinta de promos (`#ticker`) abre el carrito en la sección de promos.

