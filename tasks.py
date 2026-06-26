from colorama import init, Fore, Style
from datetime import date
from storage import load, save

init(autoreset=True)


PRIORIDADES = {
    "alta":  (Fore.RED,    "!!"),
    "media": (Fore.YELLOW, "! "),
    "baja":  (Fore.WHITE,  "  "),
}


def _formato_fecha(fecha_str):
    """Devuelve la fecha coloreada según si está vencida, hoy, o futura."""
    if not fecha_str:
        return ""
    hoy = date.today()
    fecha = date.fromisoformat(fecha_str)
    diff = (fecha - hoy).days
    if diff < 0:
        return f"{Fore.RED}[vence: {fecha_str} ✗]{Style.RESET_ALL}"
    elif diff == 0:
        return f"{Fore.YELLOW}[vence: hoy]{Style.RESET_ALL}"
    else:
        return f"{Fore.WHITE}[vence: {fecha_str}]{Style.RESET_ALL}"


def _print_tarea(t):
    prioridad = t.get("prioridad", "media")
    p_color, p_icon = PRIORIDADES[prioridad]
    fecha_txt = _formato_fecha(t.get("fecha"))
    if t["done"]:
        print(f"{Fore.GREEN}[{t['id']}] ✓  {t['title']} {p_color}[{prioridad}]{Style.RESET_ALL} {fecha_txt}")
    else:
        print(f"{Fore.CYAN}[{t['id']}] ○ {p_color}{p_icon}{Style.RESET_ALL} {t['title']} {p_color}[{prioridad}]{Style.RESET_ALL} {fecha_txt}")


def add(title, prioridad="media", fecha=None):
    if prioridad not in PRIORIDADES:
        print(f"{Fore.RED}Prioridad inválida. Usa: alta, media, baja")
        return
    if fecha:
        try:
            date.fromisoformat(fecha)
        except ValueError:
            print(f"{Fore.RED}Fecha inválida. Usa el formato YYYY-MM-DD (ej: 2026-07-01)")
            return
    tasks = load()
    next_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "done": False, "prioridad": prioridad, "fecha": fecha}
    tasks.append(task)
    save(tasks)
    color, _ = PRIORIDADES[prioridad]
    fecha_txt = f" vence: {fecha}" if fecha else ""
    print(f"{Fore.GREEN}✓ Tarea agregada:{Style.RESET_ALL} {title} {color}[{prioridad}]{Style.RESET_ALL}{fecha_txt}")


def edit(task_id, titulo=None, prioridad=None, fecha=None):
    if titulo is None and prioridad is None and fecha is None:
        print(f"{Fore.RED}Debes indicar al menos un campo para editar.")
        return
    if prioridad is not None and prioridad not in PRIORIDADES:
        print(f"{Fore.RED}Prioridad inválida. Usa: alta, media, baja")
        return
    if fecha is not None:
        try:
            date.fromisoformat(fecha)
        except ValueError:
            print(f"{Fore.RED}Fecha inválida. Usa el formato YYYY-MM-DD (ej: 2026-07-01)")
            return
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            cambios = []
            if titulo is not None:
                cambios.append(f"título: '{t['title']}' → '{titulo}'")
                t["title"] = titulo
            if prioridad is not None:
                cambios.append(f"prioridad: {t['prioridad']} → {prioridad}")
                t["prioridad"] = prioridad
            if fecha is not None:
                cambios.append(f"fecha: {t.get('fecha')} → {fecha}")
                t["fecha"] = fecha
            save(tasks)
            print(f"{Fore.GREEN}✓ Tarea {task_id} editada:{Style.RESET_ALL} {', '.join(cambios)}")
            return
    print(f"{Fore.RED}No se encontró la tarea {task_id}")


def list_tasks():
    tasks = load()
    if not tasks:
        print(f"{Fore.YELLOW}No hay tareas.")
        return
    for t in tasks:
        _print_tarea(t)


def filter_tasks(estado):
    """Filtra por: pendiente | completada | vencida"""
    tasks = load()
    hoy = date.today()

    if estado == "pendiente":
        result = [t for t in tasks if not t["done"]]
    elif estado == "completada":
        result = [t for t in tasks if t["done"]]
    elif estado == "vencida":
        result = [
            t for t in tasks
            if not t["done"] and t.get("fecha") and date.fromisoformat(t["fecha"]) < hoy
        ]
    else:
        print(f"{Fore.RED}Filtro inválido. Usa: pendiente, completada, vencida")
        return

    if not result:
        print(f"{Fore.YELLOW}No hay tareas con ese filtro.")
        return
    for t in result:
        _print_tarea(t)


def complete(task_id):
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save(tasks)
            print(f"{Fore.GREEN}✓ Completada: {t['title']}")
            return
    print(f"{Fore.RED}No se encontró la tarea {task_id}")


def delete(task_id):
    tasks = load()
    new = [t for t in tasks if t["id"] != task_id]
    if len(new) == len(tasks):
        print(f"{Fore.RED}No se encontró la tarea {task_id}")
        return
    save(new)
    print(f"{Fore.GREEN}✓ Tarea {task_id} eliminada")
