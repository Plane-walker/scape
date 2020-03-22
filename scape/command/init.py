import os
import shutil
import scape


def go_through(template_path, project_path):
    for root, dirs, files in os.walk(template_path):
        for file in files:
            shutil.copy(os.path.join(root, file), project_path)
        for dirt in dirs:
            if not os.path.exists(os.path.join(project_path, dirt)):
                os.makedirs(os.path.join(project_path, dirt))
            go_through(os.path.join(template_path, dirt), os.path.join(project_path, dirt))


def init(args):
    project_path = os.path.join(os.getcwd(), args[0])
    template_path = os.path.join(scape.__path__[0], 'template')
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    if os.path.exists(template_path):
        go_through(template_path, project_path)

