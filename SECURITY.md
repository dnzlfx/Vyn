# Política de Seguridad

## Reporte de vulnerabilidades

Si encuentras una vulnerabilidad, **no abras un issue público**. Escribe en
privado al mantenedor (Chris-devv) vía los canales del perfil de GitHub.
Intentaremos responder en un plazo razonable.

## Manejo de secretos

VYN **no contiene** credenciales en el repositorio:

- La API/keys y la config real viven en `config.json` y `.env`, **ignorados por git**.
- Usa `config_template.json` como base.
- Nunca subas `config.json`, `.env`, `*.db` ni claves SSH.

## Alcance

VYN ejecuta código en un sandbox y administra servidores por SSH. Ejecuta solo
en entornos donde confíes en la configuración y los modelos locales.

## Modelo de confianza de comandos

Toda ejecución de comandos de shell pasa por una **política fail-closed única**
(`modules/command_policy.py`):

- Solo un comando **simple y de solo lectura** (`ls`, `df -h`, `docker ps`, ...)
  se ejecuta sin confirmación.
- Comandos compuestos o con expansión de shell (`;`, `|`, `&&`, `$(...)`,
  backticks, redirecciones, saltos de línea) **siempre** piden confirmación,
  incluso si empiezan por un binario de la allowlist.
- Envoltorios (`sudo`, `doas`, `xargs`, `env`, ...) y subcomandos peligrosos de
  binarios "seguros" (`docker rm`, `systemctl restart`, `find -exec`) requieren
  confirmación.

> Corrección de seguridad: hasta la revisión previa, la clasificación usaba
> `str.startswith` contra una allowlist, por lo que `ls; rm -rf /` se consideraba
> "seguro" y se ejecutaba en el servidor remoto **sin confirmación**. Ver
> `tests/test_command_policy.py` (pruebas de regresión parametrizadas).
