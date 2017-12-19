#!/usr/bin/env python

from anytree import Node, RenderTree


webtest           = Node("WebappTest")
registration      = Node("Registration", parent=webtest)
smsconfirm        = Node("SMSconfirm", parent=registration)
login             = Node("Login", parent=smsconfirm)
useruploadCV      = Node("UserUploadCV", parent=login)
usermatchJD       = Node("UserMatchJD", parent=useruploadCV)
bemember          = Node("BeMember", parent=login)
addprj            = Node("AddProject", parent=bemember)
memuploadCV       = Node("MemberUploadCV", parent=addprj)
memupfollowupCV   = Node("MemberFollowupCV", parent=memuploadCV)
previewCV         = Node("PreviewCV", parent=memuploadCV)
addbid            = Node("AddBidding", parent=addprj)
modbid            = Node("ModifyBidding", parent=addbid)
addcus            = Node("AddCustomer", parent=addbid)
addJD             = Node("AddJD", parent=addcus)
JDmatchCV         = Node("JDmatchCV", parent=addJD)
JDmatchCVMultiDB  = Node("JDmatchCVMultiDB", parent=JDmatchCV)
previewMatchCV    = Node("previewMatchCV", parent=JDmatchCVMultiDB)
CVraderChart      = Node("CVraderChart", parent=JDmatchCVMultiDB)


from anytree.exporter import DotExporter
DotExporter(webtest).to_picture("webtest.png")
