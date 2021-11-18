from tree_sitter import Language, Parser
import os
import nx

os.makedirs('build', exist_ok=True)
if not os.path.exists('build/tree_sitter_langs.so'):
    Language.build_library(
        'build/tree_sitter_langs.so',
        [
            'tree_sitters/tree-sitter-cpp',
            'tree_sitters/tree-sitter-java',
            'tree_sitters/tree-sitter-javascript',
            'tree_sitters/tree-sitter-python',
        ]
    )


CPP_LANGUAGE = Language('build/tree_sitter_langs.so', 'cpp')
JAVA_LANGUAGE = Language('build/tree_sitter_langs.so', 'java')
JS_LANGUAGE = Language('build/tree_sitter_langs.so', 'javascript')
PYTHON_LANGUAGE = Language('build/tree_sitter_langs.so', 'python')


def get_parser(lang):
    ''' get parser for corresponding lang
    lang in [CPP_LANGUAGE, JAVA_LANGUAGE, JS_LANGUAGE, PYTHON_LANGUAGE]
    '''
    parser = Parser()
    parser.set_language(lang)
    return parser


def convert_to_nx(tree, content):
    '''Convert the tree to NX'''
    # DFS
    root = tree.root_node
    queue = [root]
    p_queue = [-1]
    nx_g = nx.MultiDiGraph()
    while (len(queue)) > 0:
        n = queue.pop(0)
        pid = p_queue.pop(0)
        nid = len(nx_g.nodes())
        n_content = content[n.start_byte:n.end_byte] if len(n.children) == 0\
                        else ""
        line_start = len(content[:(n.start_byte+1)].split("\n"))
        col_start = len(content[:(n.start_byte+1)].split("\n")[-1])

        line_end = len(content[:(n.end_byte)].split("\n"))
        col_end= len(content[:(n.end_byte)].split("\n")[-1])

        nx_g.add_node(nid, ntype=n.type, token=n_content,
                      start_line=line_start,
                      start_col=col_start,
                      end_line=line_end,
                      end_col=col_end)
        if pid != -1:
            nx_g.add_edge(pid, nid, label='parent_child')

        queue.extend(n.children)
        p_queue.extend([nid] * len(n.children))
    return nx_g


def convert_to_dict(tree, content):
    root = tree.root_node
    queue = [root]
    p_queue = [-1]
    out_dict = {"nodes": []}
    while (len(queue)) > 0:
        n = queue.pop(0)
        pid = p_queue.pop(0)
        nid = len(out_dict)
        n_content = content[n.start_byte:n.end_byte] if len(n.children) == 0\
                        else ""
        line_start = len(content[:(n.start_byte+1)].split("\n"))
        col_start = len(content[:(n.start_byte+1)].split("\n")[-1])

        line_end = len(content[:(n.end_byte)].split("\n"))
        col_end= len(content[:(n.end_byte)].split("\n")[-1])

        out_dict["nodes"].append(
            {
                "id": nid,
                "ntype": n.type,
                "token": n_content,
                "start_line": line_start,
                "start_col": col_start,
                "end_line": line_end,
                "end_col": col_end,
                "parent": pid
            }
        )
        queue.extend(n.children)
        p_queue.extend([nid] * len(n.children))
    return out_dict
