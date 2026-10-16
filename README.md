# BaTaKá TaKá

Minijuego web de **Bataká**, la bebida energética con NOx.

Las dos latas (Piña y Cereza) giran en 3D. Cada toque suena "ta-ka" y suma una lata al carrito; la lata crece y, con 18 takas, explota y abre el carrito con descuento por escalones:

- 6 latas: 10 %
- 12 latas: 15 %
- explotar una lata: 20 %

Sitio estático (HTML + three.js). Archivos:

- `index.html`: página y lógica del juego (precios y escalones en el bloque `CONFIG`).
- `lata_pina.json`, `lata_cereza.json`: modelos 3D de las latas.
- `tex_pina.jpg`, `tex_cereza.jpg`: etiquetas.

El botón de pago abre WhatsApp con el pedido: "TaKá! BaTaKá? TaKá X BaTaKáS TaKá $X". Toda la página usa el lenguaje TaKá de las promos. El precio por lata es de ejemplo (`CONFIG.precio`) y el número está en `CONFIG.whatsapp`.
