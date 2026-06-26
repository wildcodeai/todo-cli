import json
import os
import pytest
from datetime import date, timedelta
from unittest.mock import patch

# Apuntamos el storage a un archivo temporal durante los tests
TEST_FILE = "/tmp/test_tasks.json"


@pytest.fixture(autouse=True)
def archivo_temporal(monkeypatch):
    """Redirige el archivo JSON a uno temporal y lo limpia después."""
    monkeypatch.setattr("storage.FILE", TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


# ── Agregar tareas ─────────────────────────────────────────────────────────────

def test_agregar_tarea_basica():
    from tasks import add
    from storage import load
    add("Tarea básica")
    tareas = load()
    assert len(tareas) == 1
    assert tareas[0]["title"] == "Tarea básica"
    assert tareas[0]["done"] is False
    assert tareas[0]["prioridad"] == "media"


def test_agregar_tarea_con_prioridad():
    from tasks import add
    from storage import load
    add("Urgente", prioridad="alta")
    tareas = load()
    assert tareas[0]["prioridad"] == "alta"


def test_agregar_tarea_prioridad_invalida(capsys):
    from tasks import add
    from storage import load
    add("Tarea", prioridad="urgente")
    assert len(load()) == 0
    assert "inválida" in capsys.readouterr().out


def test_agregar_tarea_con_fecha():
    from tasks import add
    from storage import load
    add("Con fecha", fecha="2026-12-31")
    assert load()[0]["fecha"] == "2026-12-31"


def test_agregar_tarea_fecha_invalida(capsys):
    from tasks import add
    from storage import load
    add("Tarea", fecha="31-12-2026")
    assert len(load()) == 0
    assert "inválida" in capsys.readouterr().out


# ── Listar tareas ──────────────────────────────────────────────────────────────

def test_listar_sin_tareas(capsys):
    from tasks import list_tasks
    list_tasks()
    assert "No hay tareas" in capsys.readouterr().out


def test_listar_muestra_tareas(capsys):
    from tasks import add, list_tasks
    add("Primera")
    add("Segunda")
    list_tasks()
    out = capsys.readouterr().out
    assert "Primera" in out
    assert "Segunda" in out


# ── Completar tareas ───────────────────────────────────────────────────────────

def test_marcar_completada():
    from tasks import add, complete
    from storage import load
    add("Tarea")
    complete(1)
    assert load()[0]["done"] is True


def test_completar_id_inexistente(capsys):
    from tasks import complete
    complete(99)
    assert "No se encontró" in capsys.readouterr().out


# ── Eliminar tareas ────────────────────────────────────────────────────────────

def test_eliminar_tarea():
    from tasks import add, delete
    from storage import load
    add("Borrame")
    delete(1)
    assert len(load()) == 0


def test_eliminar_id_inexistente(capsys):
    from tasks import delete
    delete(99)
    assert "No se encontró" in capsys.readouterr().out


# ── Filtros ────────────────────────────────────────────────────────────────────

def test_filter_pendiente(capsys):
    from tasks import add, complete, filter_tasks
    add("Pendiente")
    add("Completada")
    complete(2)
    capsys.readouterr()  # limpiar output previo
    filter_tasks("pendiente")
    out = capsys.readouterr().out
    assert "Pendiente" in out
    assert "Completada" not in out


def test_filter_completada(capsys):
    from tasks import add, complete, filter_tasks
    add("Pendiente")
    add("Completada")
    complete(2)
    capsys.readouterr()  # limpiar output previo
    filter_tasks("completada")
    out = capsys.readouterr().out
    assert "Completada" in out
    assert "Pendiente" not in out


def test_filter_vencida(capsys):
    from tasks import add, filter_tasks
    ayer = (date.today() - timedelta(days=1)).isoformat()
    manana = (date.today() + timedelta(days=1)).isoformat()
    add("Vencida", fecha=ayer)
    add("Futura", fecha=manana)
    capsys.readouterr()  # limpiar output previo
    filter_tasks("vencida")
    out = capsys.readouterr().out
    assert "Vencida" in out
    assert "Futura" not in out


def test_filter_invalido(capsys):
    from tasks import filter_tasks
    filter_tasks("otro")
    assert "inválido" in capsys.readouterr().out


# ── Editar tareas ──────────────────────────────────────────────────────────────

def test_editar_titulo():
    from tasks import add, edit
    from storage import load
    add("Original")
    edit(1, titulo="Modificado")
    t = load()[0]
    assert t["title"] == "Modificado"
    assert t["prioridad"] == "media"
    assert t["done"] is False


def test_editar_prioridad():
    from tasks import add, edit
    from storage import load
    add("Tarea")
    edit(1, prioridad="alta")
    assert load()[0]["prioridad"] == "alta"


def test_editar_fecha():
    from tasks import add, edit
    from storage import load
    add("Tarea")
    edit(1, fecha="2027-01-15")
    assert load()[0]["fecha"] == "2027-01-15"


def test_editar_sin_campos(capsys):
    from tasks import edit
    from storage import load
    edit(1)
    assert "al menos un campo" in capsys.readouterr().out
    assert len(load()) == 0


def test_editar_prioridad_invalida(capsys):
    from tasks import add, edit
    from storage import load
    add("Tarea")
    capsys.readouterr()
    edit(1, prioridad="urgente")
    assert "inválida" in capsys.readouterr().out
    assert load()[0]["prioridad"] == "media"


def test_editar_id_inexistente(capsys):
    from tasks import edit
    edit(99, titulo="X")
    assert "No se encontró" in capsys.readouterr().out
