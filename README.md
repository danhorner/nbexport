# NBExport
A simple exporter to turn jupyter notebooks into a a python package. Write your code across multiple notebooks as needed, and export marked cells into python modules.

There is some support for literate programming by weaving together multiple notebook files into one or more output modules. When processing an entire directory, notebooks will be exported in lexicogrpahical order, so you can progressively write code that spans multiple notebooks.

This package is written in a notebook and which is then processed using `nbexport`

### Usage: ###

#### Command-line: ####

```shell
# Process a single file into the output directory
$ nbexport -d src/nbexport nbs/01_NbExport.ipynb 
```

#### Within a notebook ####

```python
from nbexport.nbexport import export_notebooks

# Process specific files
export_notebooks(["nbs/01_NbExport.ipynb"], "src/nbexport")

# Weave together all the files in a directory
export_notebook_dir("nbs", "src")
```

### Notebook directives
The following directives can be placed in the first line

| directive               | meaning                                 |
|-------------------------|-----------------------------------------|
| `default_exp: <module>` | Put code from this file into `<module>`
| `export`                | export the code in this cell to the default module
| `export <module>`       | export the code in this cell into a different `<module>`
| `noexport`              | do not export the code in this cell, even if it contains an import statement
| `skip_notebook`         | do not process any further cells in this notebook

