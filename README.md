# CloudShare
share，edit your doc，pdf，md and so on...

## Dependencies

    PyYAML==3.11
    Flask==0.10.1
    dulwich==0.10.2
    pypandoc==1.0.1
    emaildata==0.3.2

    pandoc 1.13.2.1
    pdftohtml 0.18.4
    LibreOffice 4.3

## How to

1) Use method convert_folder in converterutils.py to convert your doc/docx/pdf.

``` python
>>> import core.converterutils
>>> import repointerface.gitinterface
>>> repo = repointerface.gitinterface.GitInterface("repo")
>>> core.converterutils.convert_folder(YOUR_DIR, repo)
```

    The generated docbook will save in folder docbook_output
    and markdown will save in folder md_output.

2) Run flask server and visit page http://localhost:4888/.

```
python run.py
```

