from __future__ import annotations

import json
from pathlib import Path

from wirewizard_gui.domain.models import ProjectModel
from wirewizard_gui.domain.serializer import ProjectSerializer


class ProjectService:
    @staticmethod
    def save_project(path: str | Path, project: ProjectModel) -> None:
        Path(path).write_text(json.dumps(project.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def save_project_yaml(path: str | Path, project: ProjectModel) -> None:
        Path(path).write_text(ProjectSerializer.to_wireviz_yaml(project), encoding="utf-8")

    @staticmethod
    def load_project(path: str | Path) -> ProjectModel:
        path = Path(path)
        suffix = path.suffix.lower()
        text = path.read_text(encoding="utf-8")
        if suffix in {".yml", ".yaml"}:
            return ProjectSerializer.from_wireviz_yaml(text)
        data = json.loads(text)
        return ProjectModel.from_dict(data)

    @staticmethod
    def import_yaml(path: str | Path) -> ProjectModel:
        return ProjectSerializer.from_wireviz_yaml(Path(path).read_text(encoding="utf-8"))

    @staticmethod
    def export_yaml(path: str | Path, project: ProjectModel) -> None:
        Path(path).write_text(ProjectSerializer.to_wireviz_yaml(project), encoding="utf-8")
