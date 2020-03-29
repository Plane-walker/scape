import os
import shutil
import scape


def get_project_path(template_path, project_path):
    project_name = os.path.split(project_path)[1]
    middle_path = []
    while len(middle_path) == 0 or middle_path[-1] != 'template':
        template_path, tail = os.path.split(template_path)
        middle_path.append(tail)
    middle_path.pop(-1)
    while len(middle_path) != 0:
        tail = middle_path.pop(-1)
        if tail == 'project_name':
            tail = project_name
        project_path = os.path.join(project_path, tail)
    return project_path


def init(args):
    project_base = os.path.join(os.getcwd(), args[0])
    template_path = os.path.join(scape.__path__[0], 'template')
    if os.path.exists(template_path):
        for root, dirs, files in os.walk(template_path):
            project_path = get_project_path(root, project_base)
            if not os.path.exists(project_path):
                os.makedirs(project_path)
            for file in files:
                shutil.copy(os.path.join(root, file), os.path.join(project_path, file))
