#!/usr/bin/env python3
# AUTOMATICALLY GENERATED FILE - Do not edit
#
# This file was generated from jupyter notebooks




import nbformat
import itertools
import os
import re


from enum import Enum
Directive = Enum("Directive", [
    "default_exp",
    "export",
    "noexport",
    "skip_notebook"
])

def split_metadata(code):
    """
    Remove the metadata from the top of a code cell
    """
    lines = code.splitlines()
    meta_lines = []
    rest_lines = []
    for num,line in enumerate(lines):
        if line.startswith("#|"):
            meta_lines.append(line[2:])
        else:
            rest_lines = lines[num:]
            break
    return meta_lines, '\n'.join(rest_lines)        

def metadata_dict(metadata_lines):
    metadata = {}
    for line in metadata_lines:
        key, val, *_ = line.split(":",1) + [None]            
        key = key.strip()
        if val:
            val = val.strip()
        metadata[key]=val
    return metadata

def parse_code_cell(cell):
    metadata, source = split_metadata(cell.source)
    return metadata_dict(metadata), source

# Break up the string __notebook__export__main__ so that it is not substituted
NOTEBOOK_MAIN_STR= '__' + 'notebook_export_main' + '__' 

def scan_notebooks(file_list, modules=None):
    if modules is None:
        modules = {}
    for nbfile in file_list:
        default_module = 'main.py'
        nb=nbformat.read(nbfile, nbformat.NO_CONVERT)
        for cell in nb.cells:
            export_module = None
            if cell.cell_type != 'code':
                continue
            metadata, source = parse_code_cell(cell)
            if Directive.skip_notebook.name in metadata:
                break
                
            if Directive.default_exp.name in metadata:
                default_module = metadata[Directive.default_exp.name] + ".py"
                export_module = default_module
            
            if Directive.noexport.name in metadata:
                continue
                
            if Directive.export.name in metadata:
                export_module = metadata[Directive.export.name] or default_module
                
            elif re.search("^[\\s]*(from .* )?import", source, re.MULTILINE):
                export_module = default_module
        
            if export_module:
                modules.setdefault(export_module,[]).append(source)
            
    return modules

DEFAULT_PREAMBLE="""#!/usr/bin/env python3
# AUTOMATICALLY GENERATED FILE - Do not edit
#
# This file was generated from jupyter notebooks
"""

def write_modules(module_dir, modules, preamble=DEFAULT_PREAMBLE):
    "Once notebooks have been scanned, export the resulting modules"
    if not os.path.isdir(module_dir):
        os.makedirs(module_dir)
    for module, sources in modules.items():
        
        sources = [ source.replace(NOTEBOOK_MAIN_STR, '__main__') for source in sources]
    
        with open(os.path.join(module_dir, module), "w") as f:
            print(f"Writing {module}")
            f.write(preamble)
            f.write("\n\n")
            f.write("\n\n".join(sources))
            

def export_notebook_dir(nb_dir, module_dir="lib"):
    "Enumerate the notebooks in nb_dir and export them all"
    notebooks=[ os.path.join(nb_dir,f) for f in os.listdir(nb_dir) if f.endswith(".ipynb") ]
    export_notebooks(notebooks, module_dir)

def export_notebooks(notebooks, module_dir):
    "Export the files listed in *notebooks*"
    modules = scan_notebooks(notebooks)
    write_modules(module_dir, modules)
    

def main():
    import sys
    USAGE=f"""
    nbexport: export one or more notebooks as python modules
    {os.path.basename(sys.argv[0])} [--help] [-d <export_dir>] notebook_file...
    """
    export_dir="."
    args = sys.argv[1:]
    
    if len(args)==0 or args[0] in ('-h', '--help', '-H'):
        print(USAGE)
        print("Directives:")
        print("\n".join(d.name for d in Directive))
        sys.exit(1)
        
    if args[0] == "-d":
        export_dir = args[1]
        args = args[2:]

    print(f'exporting {", ".join(args)}')
    print(f'export dir: {export_dir}')
    export_notebooks(args, export_dir)
    

if __name__ == "__main__":
    main()