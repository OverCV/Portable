# data/csv_manager.py
import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from backend.data.manager import Manager

from backend.app.enums.application import Portalapp
from backend.app.enums.reports import Reports
from backend.app.enums.manager import CSVModels


class CSVManager(Manager):
    def __init__(self):
        # Directorio base para los archivos
        self.data_dir = Path(Portalapp.DATABASE_PATH)
        self.data_dir.mkdir(exist_ok=True)

        # Rutas de los archivos
        self.productos_file = self.data_dir / CSVModels.PRODUCTOS
        self.ventas_file = self.data_dir / CSVModels.VENTAS
        self.deudores_file = self.data_dir / CSVModels.DEUDORES

        # Inicializar archivos CSV con columnas si no existen
        self._init_files()

    def _init_files(self):
        default_columns = {
            self.productos_file: ['id', 'nombre', 'descripcion', 'creacion'],
            self.ventas_file: ['id', 'id_producto', 'cantidad', 'fecha_venta', 'ganancia'],
            self.deudores_file: ['id', 'nombre_cliente', 'valor_deuda', 'creacion'],
        }
        for file, columns in default_columns.items():
            if not file.exists():
                with open(file, 'w', newline='', encoding=Reports.ENCODING) as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)

    def _read_file(self, file_path: Path) -> List[Dict[str, Any]]:
        with open(file_path, 'r', encoding=Reports.ENCODING) as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def _write_file(self, file_path: Path, data: List[Dict[str, Any]]):
        with open(file_path, 'w', newline='', encoding=Reports.ENCODING) as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

    def get_data(self, source: str) -> List[Dict]:
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            return self._read_file(file_path)
        raise ValueError(f"Source '{source}' not recognized.")

    def add_data(self, source: str, item: Dict):
        file_path = getattr(self, f'{source}_file', None)
        if file_path:
            data = self._read_file(file_path)
            item['id'] = str(len(data) + 1)
            item['creacion'] = datetime.now().isoformat()
            data.append(item)
            self._write_file(file_path, data)
            return item
        raise ValueError(f"Source '{source}' not recognized.")
