import sys
import tasks
from colorama import init, Fore, Style

init(autoreset=True)


def usage():
    C = Fore.CYAN
    Y = Fore.YELLOW
    G = Fore.GREEN
    W = Style.RESET_ALL
    print(f"""
{C}╔══════════════════════════════════════════════════════╗
║              TODO CLI — Gestión de tareas            ║
╚══════════════════════════════════════════════════════╝{W}

{Y}Uso:{W}  python3 main.py <comando> [argumentos]

{Y}Comandos:{W}
  {G}add{W} "título" [prioridad] [--fecha YYYY-MM-DD]
      Agrega una nueva tarea.
      Prioridades: {Fore.RED}alta{W}  {Fore.YELLOW}media{W}  {Fore.WHITE}baja{W}  (por defecto: media)

  {G}list{W}
      Lista todas las tareas.

  {G}filter{W} <pendiente|completada|vencida>
      Muestra solo las tareas con ese estado.

  {G}done{W} <id>
      Marca una tarea como completada.

  {G}delete{W} <id>
      Elimina una tarea.

  {G}edit{W} <id> [--titulo "nuevo"] [--prioridad alta|media|baja] [--fecha YYYY-MM-DD]
      Edita el título, prioridad o fecha de una tarea existente.

{Y}Ejemplos:{W}
  python3 main.py add "Escribir informe" alta --fecha 2026-07-10
  python3 main.py add "Revisar emails" baja
  python3 main.py list
  python3 main.py filter pendiente
  python3 main.py done 3
  python3 main.py delete 5
  python3 main.py edit 2 --titulo "Revisar informe" --prioridad alta
""")


def main():
    if len(sys.argv) < 2:
        usage()
        return

    cmd = sys.argv[1]

    if cmd == "help":
        usage()

    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Falta el título. Uso: python3 main.py add \"título\" [alta|media|baja] [--fecha YYYY-MM-DD]")
            return
        args = sys.argv[2:]

        # Extraer --fecha si existe
        fecha = None
        if "--fecha" in args:
            idx = args.index("--fecha")
            if idx + 1 >= len(args):
                print("Falta la fecha. Usa: --fecha YYYY-MM-DD")
                return
            fecha = args[idx + 1]
            args = args[:idx] + args[idx + 2:]

        # Extraer prioridad si el último arg es una prioridad
        if args and args[-1] in ("alta", "media", "baja"):
            prioridad = args[-1]
            titulo = " ".join(args[:-1])
        else:
            prioridad = "media"
            titulo = " ".join(args)

        tasks.add(titulo, prioridad, fecha)

    elif cmd == "list":
        tasks.list_tasks()

    elif cmd == "filter":
        if len(sys.argv) < 3:
            print("Falta el filtro. Uso: python3 main.py filter <pendiente|completada|vencida>")
            return
        tasks.filter_tasks(sys.argv[2])

    elif cmd == "done":
        if len(sys.argv) < 3:
            print("Falta el ID. Uso: python3 main.py done <id>")
            return
        tasks.complete(int(sys.argv[2]))

    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("Falta el ID. Uso: python3 main.py delete <id>")
            return
        tasks.delete(int(sys.argv[2]))

    elif cmd == "edit":
        if len(sys.argv) < 3:
            print('Falta el ID. Uso: python3 main.py edit <id> [--titulo "nuevo"] [--prioridad alta|media|baja] [--fecha YYYY-MM-DD]')
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("El ID debe ser un número entero.")
            return
        args = sys.argv[3:]

        titulo = prioridad = fecha = None

        for flag in ("--titulo", "--prioridad", "--fecha"):
            if flag in args:
                idx = args.index(flag)
                if idx + 1 >= len(args):
                    print(f"Falta el valor para {flag}")
                    return
                val = args[idx + 1]
                args = args[:idx] + args[idx + 2:]
                if flag == "--titulo":    titulo    = val
                if flag == "--prioridad": prioridad = val
                if flag == "--fecha":     fecha     = val

        tasks.edit(task_id, titulo=titulo, prioridad=prioridad, fecha=fecha)

    else:
        print(f"Comando desconocido: {cmd}")
        usage()


if __name__ == "__main__":
    main()
