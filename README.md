# NBExport
A simple exporter to turn jupyter notebooks into a a python package. Write your code across multiple notebooks as needed, and export marked cells into python modules.

There is some support for literate programming by weaving together multiple notebook files into one or more output modules. When processing an entire directory, notebooks will be exported in lexicogrpahical order, so you can progressively write code that spans multiple notebooks.

This package is written in a notebook and which is then processed using `nbexport`

**See Also**: The excellent [nbdev project](https://nbdev.fast.ai) by fast.ai which is a full book-authoring package along these lines. I didn't want to opt in to the the quarto documentation and the CI tooling. Rather, I like to work on smaller projects by writing a notebook and then diffing only the generated sources during code review.

### Install: ###
```console
$ pip install git+https://github.com/danhorner/nbexport
```

Or just clone the git repo and run directly:
```console
$ git clone https://github.com/danhorner/nbexport
$ python nbexport/src/nbexport/nbexport.py <args>
```

### Usage: ###

#### Command-line: ####

```shell
# Process one or more files into the output directory
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

