# HornoRaíz · Frontend

Frontend de **HornoRaíz**, sistema de producción y venta de panadería (Bases de Datos II, Universidad de La Guajira). Consume la API REST del backend Django de este repositorio.

| | |
|---|---|
| Framework | Angular 22 (componentes *standalone*, *signals*, *zoneless*) |
| Interfaz | PrimeNG 22 (tema Aura), PrimeIcons y Tailwind CSS 4 |
| Pruebas | Vitest (`ng test`) |
| API | `http://127.0.0.1:8000/api` (`src/environments/`) |

## Qué incluye

- Plantilla con encabezado, menú lateral y pie.
- Inicio de sesión con JWT contra `/api/auth/` (guard, interceptor `Bearer`, perfil y cierre de sesión).
- CRUD de insumos contra `/api/catalog/supplies/`: listado, alta, edición, desactivación y borrado.
- Rutas de productos y ventas con carga perezosa.

## Cómo ejecutarlo

```bash
# Backend (en otra terminal)
cd ../Backend && source .venv/bin/activate && python manage.py runserver 0.0.0.0:8000

# Frontend
npm install
npm start                 # http://localhost:4200
npx ng test --no-watch    # pruebas
npx ng build              # build de producción en dist/hornoraiz-frontend
```

Se entra con un usuario del backend. Para la pantalla de insumos el usuario necesita un rol RBAC con los permisos de `/api/catalog/supplies/`.

## Bitácora

El paso a paso, con decisiones, problemas y capturas, está en [bitacora-frontend.md](../bitacora-frontend.md), en la raíz del repositorio junto a `backend-iss.md`.
