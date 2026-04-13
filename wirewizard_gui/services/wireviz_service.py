from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from wirewizard_gui.domain.models import ProjectModel
from wirewizard_gui.domain.serializer import ProjectSerializer


class WireVizService:
    @staticmethod
    def render_svg(project: ProjectModel) -> tuple[bool, str, str | None]:
        wireviz_executable = shutil.which("wireviz")
        if not wireviz_executable:
            return False, "Команда 'wireviz' не найдена в PATH. Установи пакет wireviz и Graphviz.", None

        with tempfile.TemporaryDirectory(prefix="wirewizard_") as tmp_dir:
            tmp_path = Path(tmp_dir)
            yaml_path = tmp_path / "preview.yml"
            yaml_path.write_text(ProjectSerializer.to_wireviz_yaml(project), encoding="utf-8")

            try:
                result = subprocess.run(
                    [wireviz_executable, str(yaml_path)],
                    cwd=tmp_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except Exception as exc:
                return False, f"Ошибка запуска WireViz: {exc}", None

            if result.returncode != 0:
                stderr = result.stderr.strip() or result.stdout.strip() or "Unknown WireViz error"
                return False, stderr, None

            svg_path = tmp_path / "preview.svg"
            if not svg_path.exists():
                candidates = list(tmp_path.glob("*.svg"))
                if not candidates:
                    return False, "WireViz завершился без SVG output.", None
                svg_path = candidates[0]

            svg_text = svg_path.read_text(encoding="utf-8")
            return True, "OK", svg_text

    @staticmethod
    def run_full(project: ProjectModel, output_dir: str | Path, base_name: str = "harness") -> tuple[bool, str, list[str]]:
        wireviz_executable = shutil.which("wireviz")
        if not wireviz_executable:
            return False, "Команда 'wireviz' не найдена в PATH. Установи пакет wireviz и Graphviz.", []

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        yaml_path = output_path / f"{base_name}.yml"
        yaml_path.write_text(ProjectSerializer.to_wireviz_yaml(project), encoding="utf-8")

        try:
            result = subprocess.run(
                [wireviz_executable, str(yaml_path)],
                cwd=output_path,
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as exc:
            return False, f"Ошибка запуска WireViz: {exc}", []

        if result.returncode != 0:
            stderr = result.stderr.strip() or result.stdout.strip() or "Unknown WireViz error"
            return False, stderr, []

        generated = sorted(str(path.name) for path in output_path.glob(f"{base_name}.*") if path.name != yaml_path.name)
        message = "WireViz выполнен успешно. Созданы файлы: " + ", ".join(generated) if generated else "WireViz выполнен успешно."
        return True, message, generated
