# Redisenio Institucional Frontend

## Objetivo

Modernizar la interfaz de BiblioApp como un sistema academico/institucional para pedidos de biblioteca, manteniendo el frontend actual en HTML, CSS y JavaScript y conservando compatibilidad con la API FastAPI existente.

## Alcance

- Login profesional centrado con marca institucional, campos claros y enlace de recuperacion.
- Dashboard visual con resumen de pedidos, accesos rapidos y menu lateral.
- Catalogo con buscador, filtros sobrios, tarjetas profesionales y accion para solicitar libro.
- Formulario visual de pedido listo para integrarse con el flujo actual de prestamos.
- Mis pedidos como tabla administrativa con estados diferenciados.
- Detalle de pedido como ficha administrativa estatica/lista para integracion posterior.
- Panel de bibliotecario/admin con gestion de libros y base visual para pedidos recibidos.

## Enfoque Visual

La interfaz usara una paleta sobria: azul institucional oscuro, grises claros, blanco, acentos celestes y verdes. El diseno priorizara claridad, accesibilidad, jerarquia tipografica, buen espaciado, bordes suaves y sombras ligeras.

## Arquitectura

Se conservara la arquitectura estatica actual. Los estilos se centralizaran en `frontend/css/styles.css`, `frontend/css/components.css` y `frontend/css/layout.css`. Las paginas HTML se actualizaran para compartir una estructura visual tipo sistema: barra lateral, encabezados de pagina, paneles, tablas y tarjetas.

## Datos y Limitaciones

El backend actual expone libros, autenticacion y prestamos. Las pantallas que requieren endpoints aun no existentes, como reportes o detalle completo con historial, se implementaran como estructura visual preparada, evitando datos falsos criticos. Donde exista informacion real, se consumira desde la API actual.

## Verificacion

- Validar sintaxis JS con `node --check`.
- Ejecutar pruebas backend focalizadas existentes.
- Verificar que frontend sirva HTML actualizado desde `http://127.0.0.1:3000`.
- Verificar que backend responda catalogo desde `http://127.0.0.1:8000/api/v1/libros`.
