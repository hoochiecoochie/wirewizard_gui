# wireviz_gui
This is GUI wrapper for WireViz project. You can create cable assemblies drawings using simple GUI with standard controls. You can preview result, save/load project? import/export YAML files in WireViz Syntax, and finally call WireViz to get resulting html drawing and bom.

To run on Win10:
in CMD:

1) cd <ProjectPath>\wirewizard_gui
2) python -m venv .venv
3) .venv\Scripts\activate.bat
4) python -m pip install -r requirements.txt

if needed, install:

5) pip install wireviz

6) cd..
7) python -m wirewizard_gui.app
