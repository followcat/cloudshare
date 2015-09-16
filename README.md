# CloudShare
share，edit your doc，pdf，md and so on...

## Dependencies

    yaml
    flask
    dulwich
    pypandoc
    emaildata
    python-magic

    pandoc
    pdftohtml
    libreoffice

## How to

1) Use method convert_folder in converterutils.py to convert your doc/docx/pdf.

    ```python
    >>> import converterutils
    >>> converterutils.convert_folder(YOUR_DIR)
    ```

    The generated docbook will save in folder docbook_output
    and markdown will save in folder md_output.

2) Run flask server and visit page http://localhost:4888/listdata.

    ```
    python server.py
    ```

