from tree_sitter import Language, Parser
import os
import networkx as nx
import json

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
        n_content = content[n.start_byte:n.end_byte].decode('utf-8') if len(n.children) == 0\
                        else ""
        line_start = len(content[:(n.start_byte+1)].decode('utf-8').split("\n"))
        col_start = len(content[:(n.start_byte+1)].decode('utf-8').split("\n")[-1])

        line_end = len(content[:(n.end_byte)].decode('utf-8').split("\n"))
        col_end= len(content[:(n.end_byte)].decode('utf-8').split("\n")[-1])

        nx_g.add_node(nid, ntype=n.type, token=n_content,
                      start_line=line_start,
                      start_col=col_start,
                      start_pos=n.start_byte,
                      end_line=line_end,
                      end_col=col_end,
                      end_pos=n.end_byte,
                      graph='ast'
                      )
        if pid != -1:
            nx_g.add_edge(pid, nid, label='parent_child')

        queue.extend(n.children)
        p_queue.extend([nid] * len(n.children))
    return nx_g


def convert_to_dict(tree, content):
    root = tree.root_node
    queue = [root]
    p_queue = [-1]
    out_dict = {"nodes": {}}
    while (len(queue)) > 0:
        n = queue.pop(0)
        pid = p_queue.pop(0)
        nid = len(out_dict["nodes"].keys())
        n_content = content[n.start_byte:n.end_byte].decode('utf-8') if len(n.children) == 0\
                        else ""
        line_start = len(content[:(n.start_byte+1)].decode('utf-8').split("\n"))
        col_start = len(content[:(n.start_byte+1)].decode('utf-8').split("\n")[-1])

        line_end = len(content[:(n.end_byte)].decode('utf-8').split("\n"))
        col_end= len(content[:(n.end_byte)].decode('utf-8').split("\n")[-1])

        out_dict["nodes"][nid] = {
                "ntype": n.type,
                "token": n_content,
                "start_line": line_start,
                "start_pos": n.start_byte,
                "start_col": col_start,
                "end_line": line_end,
                "end_col": col_end,
                "end_pos": n.end_byte,
                "parent": pid
        }
        queue.extend(n.children)
        p_queue.extend([nid] * len(n.children))
    out_dict["nodes"]['size'] = len(out_dict["nodes"].keys())
    return json.dumps(out_dict)


def ast_diff(fp1, fp2, parser):
    ''' Return a dictionary consists of a 'mapping' between src and dst node,
    list of 'deleted', and 'inserted' nodes
    '''
    cb1 = bytes(open(fp1).read(), encoding='utf-8')
    cb2 = bytes(open(fp2).read(), encoding='utf-8')
    tree1 = parser.parse(cb1)
    tree2 = parser.parse(cb2)
    dict1 = json.loads(convert_to_dict(tree1))
    dict2 = json.loads(convert_to_dict(tree2))
    concat_dict = {"file1": dict1, "file2": dict2}
    # Let's call gumtree utils here


cpp_parser = get_parser(CPP_LANGUAGE)
python_parser = get_parser(PYTHON_LANGUAGE)
java_parser = get_parser(JAVA_LANGUAGE)
js_parser = get_parser(JS_LANGUAGE)
