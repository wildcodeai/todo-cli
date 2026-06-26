# todo-cli

CLI de gestión de tareas en Python con prioridades, fechas de vencimiento y filtros por estado.

## Instalación

```bash
pip install colorama
```

## Uso

```
python3 main.py <comando> [argumentos]
```

### Comandos

| Comando | Descripción |
|---------|-------------|
| `add "título" [prioridad] [--fecha YYYY-MM-DD]` | Agrega una nueva tarea |
| `list` | Lista todas las tareas |
| `filter <pendiente\|completada\|vencida>` | Filtra tareas por estado |
| `done <id>` | Marca una tarea como completada |
| `edit <id> [--titulo "nuevo"] [--prioridad ...] [--fecha ...]` | Edita una tarea existente |
| `delete <id>` | Elimina una tarea |
| `help` | Muestra la ayuda |

### Prioridades

- `alta` — urgente
- `media` — normal (por defecto)
- `baja` — sin prisa

### Ejemplos

```bash
# Agregar tareas
python3 main.py add "Escribir informe" alta --fecha 2026-07-10
python3 main.py add "Revisar emails" baja

# Ver y filtrar
python3 main.py list
python3 main.py filter pendiente
python3 main.py filter vencida

# Editar una tarea
python3 main.py edit 2 --titulo "Revisar informe final" --prioridad alta

# Completar y eliminar
python3 main.py done 3
python3 main.py delete 5
```

## Tests

```bash
python3 -m pytest test_tasks.py -v
```
