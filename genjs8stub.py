import sys
import pickle


if len(sys.argv) == 1: exit()

picklefile = sys.argv[1]

loaded = None
with open(picklefile, "rb") as f:
    loaded = pickle.load(f)

def generate_class(info, level): #name, type, doc
    name, t, doc, objpath, filepath, extra = info
    #we got all the subclasses of this one
    #and foreach subclass we generate its template based on indenetation level as well
    generated_fields=generate_fields_for(objpath, level+1).rstrip() or "{spaces}\tpass".format(spaces=(level+1) * "    ")
    tmpl=""
    tmpl += """
{spaces}class {name}:
{generated_fields}
    """.format(spaces=level * "    ", name=name, generated_fields=generated_fields)

    return tmpl

def generate_fields_for(objpath, level=0):
    keys=sorted([k for k in loaded.keys() if objpath in k and k.count(".") - objpath.count(".")==1])
    vals = [loaded[key] for key in keys]
    ret = ""
    for val in vals:

        if len(val) == 6:
            name, t, doc, objp, filepath, extra = val
            if t in ("const"):
                ret += generate_field(val, level)
            if t in  ("method", "property"):
                ret += generate_method(val, level)
            if t in ('class'):
                ret += generate_innerclass(val, level)
    # import pudb; pu.db
    return ret

def generate_innerclass(info, level):
    name, t, doc, objpath, filepath, extra = info
    generated_fields=generate_fields_for(objpath, level+1).rstrip() or (level+1)*"    "+"\tpass"

    tmpl = """
{spaces}class {name}:
{generated_fields}
""".format(spaces=(level)*"    ", name=name, generated_fields=generated_fields)
    return tmpl

def generate_field(info, level):
    name, t, doc, objpath, filepath, extra = info
    return "{spaces}{name} = None\n".format(spaces="    "*level, name=name)

def generate_method(info, level):
    name, t, doc, objpath, filepath, extra = info
    if doc is not None:
        doc=doc.replace("'", '"')
    return """\n
{spaces}@staticmethod
{spaces}def {methodname}({methodargs}):
{spaces}\t'''
{spaces}{doc}
{spaces}\t'''
{spaces}\tpass\n""".format(spaces=(level)*"    ", methodname=name, methodargs=extra or '', doc=doc)

#classes = [(k,v) for (k,v) in loaded.items() if len(v)==6 and v[1]=='class']

with open("res.py", "w") as f:
    tmpl = ""
    i=iter(loaded.items())
    c, v = next(i) #first one.
    tmpl += generate_class(v, 0)
    tmpl = tmpl.replace("\t", "    ")
    f.write(tmpl)
# with open("res.py", "w") as f:
#
#     for c, v in classes:
#         tmpl = ""
#         name, t, doc, objpath, filepath, extra = v
#         #is it a main or a sub?
#         parent=".".join(objpath.split(".")[:-1])
#         if parent in loaded and loaded[parent][1] == 'class':
#             continue
#         else:
#             print("Main: ", name)
#             tmpl += generate_class(v, 0)
#             tmpl = tmpl.replace("\t", "    ")
#
#         f.write(tmpl)






#print(classes)
