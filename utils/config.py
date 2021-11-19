import os


class Config:
    jar_path = 'jars'
    os.makedirs(jar_path, exist_ok=True)

    gumtree_cmd = 'jars/ast_diff.jar'
