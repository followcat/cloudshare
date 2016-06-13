#!/usr/bin/env python

import networkx as nx

G = nx.DiGraph()

G.add_node('Login')

G.add_edge('Login', 'Superadmin')
G.add_edge('Login', 'User')

G.add_edge('Superadmin', 'EditUser')
G.add_edge('Superadmin', 'Logout')

G.add_edge('User', 'Search')
G.add_edge('User', 'JD-Search')
G.add_edge('User', 'Select-JD')
G.add_edge('User', 'UploadCV')
G.add_edge('User', 'Logout')
G.add_edge('User', 'Information', color='blue')

G.add_edge('Search', 'SearchResult')
G.add_edge('SearchResult', 'ShowCV', label='Another window')
G.add_edge('SearchResult', 'ShowPositions')
G.add_edge('SearchResult', 'ShowCompetency')
G.add_edge('SearchResult', 'ShowExperience')
G.add_edge('JD-Search', 'MatchResult')

G.add_edge('UploadCV', 'Preview')
G.add_edge('Preview', 'Confirm')
G.add_edge('Confirm', 'ShowCV')

G.add_edge('Select-JD', 'AddCompany')
G.add_edge('Select-JD', 'AddJD')
G.add_edge('Select-JD', 'FastMatching')
G.add_edge('Select-JD', 'ModifyJD')

G.add_edge('ShowCV', 'ModifyCV')
G.add_edge('ShowCV', 'Download')
G.add_edge('ShowCV', 'AddEnglish')
G.add_edge('ShowCV', 'AddTag')
G.add_edge('ShowCV', 'AddFollowup')
G.add_edge('ShowCV', 'AddComments')
G.add_edge('ShowCV', 'MatchJD')
G.add_edge('ShowCV', 'Similar')

G.add_edge('FastMatching', 'MatchResult')
G.add_edge('ShowCV', 'MatchJD')

G.add_edge('MatchJD', 'AddCompany')
G.add_edge('MatchJD', 'FastMatching')
G.add_edge('MatchJD', 'ModifyJD')
G.add_edge('MatchJD', 'DrawSingleChart')

G.add_edge('MatchResult', 'ChooseByRanking')
G.add_edge('MatchResult', 'ChooseByHistory')
G.add_edge('MatchResult', 'ShowCV')

G.add_edge('ChooseByRanking', 'DrawMultiRaderChart')
G.add_edge('ChooseByRanking', 'ShowCompetency')
G.add_edge('ChooseByRanking', 'ShowExperience')

G.add_edge('ChooseByHistory', 'DrawMultiRaderChart')
G.add_edge('ChooseByHistory', 'ShowCompetency')
G.add_edge('ChooseByHistory', 'ShowExperience')

A = nx.to_agraph(G)

A.write('cloudshare_router.dot')

X = nx.from_agraph(A)
print("edges")
print(X.edges(data=True))
print("default graph attributes")
print(X.graph)
print("node node attributes")
print(X.node)
