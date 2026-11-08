# BaTaKá TaKá

Minijuego web de **Bataká**, la bebida energética con NOx.

Las dos latas (Piña y Cereza) giran en 3D. Cada toque suena "ta-ka" y suma una lata al carrito; la lata crece y, con 18 takás, explota (TaKáBOOM) y vuelve a aparecer, sin límite. Descuento por escalones:

- 6 latas: 10 %
- 12 latas: 15 %
- explotar una lata: 20 %

Promo de lanzamiento (`CONFIG.promo`, del 7 al 15 de noviembre de 2026): con TaKáBOOM el pedido paga lo más barato entre −20 % y un solo 5x3 (lleva 5, paga 3) más el resto con la tabla. Pasada la fecha vuelve sola al −20 %. El mensaje de WhatsApp marca `🏷️5x3` cuando aplica.

Sitio estático (HTML + three.js). Archivos:

- `index.html`: página y lógica del juego (precios y escalones en el bloque `CONFIG`).
- `lata_pina.json`, `lata_cereza.json`: modelos 3D de las latas.
- `tex_pina.jpg`, `tex_cereza.jpg`: etiquetas.

El botón de pago abre WhatsApp con el pedido en lenguaje TaKá, por ejemplo: "TaKá! BaTaKá? TaKá 🍍×5 🍒×3 → 8 BaTaKáS TaKá $21.60". Precio: $3 por BaTaKá (`CONFIG.precio`); número de pedidos en `CONFIG.whatsapp`.