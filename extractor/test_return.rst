    >>> import extractor.utils_parsing
    >>> import extractor.extract_experience as exp
    >>> from baseapp.datadbs import SVC_CV_REPO
    >>> yamls = ['8zclxllv.yaml', 't37poj9k.yaml', 'ix79uk39.yaml', 'kb25hq1l.yaml']
    >>> for y in yamls:
    ...     try:
    ...         assert extractor.utils_parsing.returns_with_time(exp.fix, y, SVC_CV_REPO.getmd(y))
    ...     except IOError:
    ...         continue
