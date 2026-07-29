# Rezzy Nuke Bot

Bot de Discord para spam/raid sin permisos de administrador.

## Comandos

- `/hi` - El bot dice "Hi, I'm ready to nuke."
- `/nuke` - Envía 3 mensajes de spam con @everyone
- `/custom` - Spam con mensaje personalizado (solo Premium)
- `/help` - Muestra los comandos disponibles

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `DISCORD_TOKEN` | Token del bot de Discord |
| `REQUIRED_GUILD_ID` | ID del servidor donde están los roles |
| `BOOSTER_ROLE_ID` | ID del rol Premium |

## Requisitos

- Python 3.10+
- discord.py
- python-dotenv

## Instalación

1. Clona el repositorio
2. Instala dependencias: `pip install -r requirements.txt`
3. Crea archivo `.env` con las variables
4. Ejecuta: `python main.py`
