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

### for test

    nose==1.3.7

    node.js 4.1.2
    npm 2.14.4
    gulp CLI 3.9.0

You can do the automatic test by using Jenkins with karma, nose and so on.
Here is a demo bash script to run Jenkins test:

```
    #!/bin/bash
    pkill java

    export JENKINS_ROOT=/home/followcat/Projects/jenkins
    export CLOUDSHARE_HOME=/home/followcat/Projects/cloudshare
    export CLOUDSHARE_CI_HOME=/home/followcat/Projects/cloudshare_ci

    export JENKINS_HOME=$CLOUDSHARE_CI_HOME/tools/jenkins-ci

    rm -rf $CLOUDSHARE_CI_HOME
    git clone $CLOUDSHARE_HOME $CLOUDSHARE_CI_HOME
    (cd $CLOUDSHARE_CI_HOME/webapp/static/js; npm install;)
    (cd $CLOUDSHARE_CI_HOME; git branch $CLOUDSHARE_CI_BRANCH);

    source ~/Virtualenv/charelation/bin/activate
    java -jar $JENKINS_ROOT/jenkins.war --httpPort=8001
```

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

