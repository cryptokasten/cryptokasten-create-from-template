import yaml
import os

from jinja2 import Environment, BaseLoader

TEMPLATE_DIR = "/data/template"
OUTPUT_DIR = "/data/output"
DOC_FN = "/data/doc.json"

def read_doc(doc_fn=DOC_FN):
    f = open(doc_fn, "rt")
    doc = yaml.load(f.read())
    f.close()
    return doc

def relwalk(root):
    directories = os.listdir(root)
    for d in directories:
        cur = os.path.join(root, d)
        if os.path.isdir(cur):
            yield ("d", d)
            for t, sub in relwalk(cur):
                yield(t, os.path.join(d, sub))
        else:
            yield("f", d)

def render_template(template, doc):
    rtemplate = Environment(loader=BaseLoader).from_string(template)
    return rtemplate.render(doc=doc)

def append_template(doc, template_dir=TEMPLATE_DIR, output_dir=OUTPUT_DIR):
    for t, name in relwalk(template_dir):
        if t == "d":
            print("Create directory", name)
            os.mkdir(os.path.join(output_dir, name))
        else:
            print("Create file", name)
            fi = open(os.path.join(template_dir, name), "rt")
            fo = open(os.path.join(output_dir, name), "wt")
            fo.write(render_template(fi.read(), doc))
            fi.close()
            fo.close()

doc = read_doc()

append_template(doc)
