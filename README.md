# Plantilla de OpenGL para SGI (UPV)

Esta plantilla está pensada para poder compilar código en C con OpenGL, GLUT, GLEW (y compañía) desde Linux para Windows, por requisitos de la asignatura.

Sólo está testeada en Archlinux, aunque debería funcionar igual en cualquier distribución, siempre y cuando tenga todas las dependencias necesarias instaladas. El código de los scripts de Python está pensado para ser multiplataforma, por lo que se podría usar para compilar a Linux desde Windows con mínimas modificaciones.

Esta plantilla está preparada para descargar y enlazar **estáticamente** las siguientes dependencias:
- GLUT (freeglut) → `#include <GL/freeglut.h>`
- GLEW → `#include <GL/glew.h>`

## Dependencias

- `cmake >= 3.16`
- `clang` + `llvm`
- `mingw-w64` + `llvm-windres`  para compilar a Windows desde Linux.
  - Según la distribución de Linux, se puede serparar en varios paquetes: 
  - `mingw-w64-crt` `mingw-w64-headers` `mingw-w64-gcc`
  - `mingw-w64-binutils` (para `llvm-windres`)
- `libx11`, `libxmu`, `libxi`, `libgl`, `libxrandr` (Normalmente con `-dev` en Ubuntu, el nombre puede variar).
- `ninja` (opcional) para compilaciones más rápidas.
- OpenGL
- Python para la descarga de dependencias y generación de scripts.

**Archlinux**

```bash
sudo pacman -S clang cmake ninja llvm mingw-w64 libx11 libxmu libxi libgl 
```

## Uso

1. Clonar y moverse al repositorio

2. `python install-deps.py` para descargar las dependencias a `deps/`.

3. `python build-scripts.py` para generar los scripts de compilación de cmake. Puedes añadir `--ninja` para usar `ninja` en lugar de `make`.

4. `cmake --build build/<target>` para compilar a la arquitectura + OS seleccionado (ej.: x86_64-linux).

5. `./bin/<target>/main` para ejecutar el binario.

## Cambios y extensiones

**Nombre del projecto/ejecutable**

Basta con cambiar `main` en `CMakeLists.txt`, en `set(PROJECT_NAME, main)`, por otra cosa.

**Crear un nuevo target de compilación**

Debería bastar con crear un nuevo archivo en `toolchains/` (usando `x86_64-linux.cmake` como base), siempre y cuando todas las dependencias soporten dicha arquitectura (no debería ser un problema) y estén todas las dependencias de desarrollo instaladas.
