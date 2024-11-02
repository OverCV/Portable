# data/data_manager.py
import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        # Rutas de los archivos
        self.productos_file = self.data_dir / "productos.json"
        self.ventas_file = self.data_dir / "ventas.json"
        self.deudores_file = self.data_dir / "deudores.json"

        # Inicializar archivos si no existen
        self._init_files()

    def _init_files(self):
        default_data = {"items": []}
        for file in [self.productos_file, self.ventas_file, self.deudores_file]:
            if not file.exists():
                with open(file, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=2)

    def _read_file(self, file_path: Path) -> Dict:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"items": []}

    def _write_file(self, file_path: Path, data: Dict):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Métodos para productos
    def get_productos(self) -> List[Dict]:
        data = self._read_file(self.productos_file)
        return data.get("items", [])

    def add_producto(self, producto: Dict):
        data = self._read_file(self.productos_file)
        producto["id"] = str(len(data["items"]) + 1)
        producto["created_at"] = datetime.now().isoformat()
        data["items"].append(producto)
        self._write_file(self.productos_file, data)
        return producto

    # Similar para ventas y deudores...
    # [Comentario: Aquí irían métodos similares para ventas y deudores]
