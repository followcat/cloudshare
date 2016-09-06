# CloudShare
share，edit your doc，pdf，md and so on...

## Dependencies

    PyYAML==3.11
    Flask==0.10.1
    Flask-Login==0.3.2
    Flask-Session==0.2.2
    Flask-RESTful==0.3.5
    Flask-Cors==2.1.2
    dulwich==0.10.2
    pypandoc==1.0.1
    emaildata==0.3.2
    jieba==0.38
    gensim==0.12.3
    APScheduler==3.0.6
    Theano==0.7.0(choosable)
    Pattern==2.6(choosable)

    pandoc 1.13.2.1
    pdftohtml 0.18.4
    LibreOffice 4.3

### for test

    nose==1.3.7
    Flask-Testing==0.4.2

### draw && view router graph

    xdot 0.4
    networkx==1.10
    pygraphviz==1.4.dev


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


## Front-end Building

### Dependencies

    node@6.1.0
    npm@3.8.6
    gulp@3.9.1

### Install

Enter ```/static``` folder, run ```npm install``` to install the packages.


## How to

0) Install libreoffice/Openoffice, add libreoffice uno env, and start service.

```
export PYTHONPATH=/usr/share/pyshared:$PYTHONPATH
export LD_LIBRARY_PATH=/usr/lib/libreoffice/program:$LD_LIBRARY_PATH
libreoffice --invisible "--accept=socket,host=localhost,port=8100;urp;"
```

1) Front-end building: enter ```/webapp``` root folder, and run
```
sh ./build.sh
```
there were generate two folders ```/static/dist/``` and ```/templates_dist/```

2) Run flask server and visit page http://localhost:4888/.

```
python run.py
```

