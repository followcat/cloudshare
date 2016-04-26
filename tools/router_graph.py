#!/usr/bin/env python

import networkx as nx

G = nx.DiGraph()

G.add_node('Login')

G.add_edge('Login', 'Superadmin')
G.add_edge('Login', 'User')

G.add_edge('Superadmin', 'EditUser')
G.add_edge('Superadmin', 'Logout')

G.add_edge('User', 'Search')
G.add_edge('User', 'UploadCV')
G.add_edge('User', 'AddCompany')
G.add_edge('User', 'Logout')
G.add_edge('User', 'Information', color='blue')

G.add_edge('Search', 'SearchResult')

G.add_edge('SearchResult', 'ShowCV', label='Another window')
G.add_edge('ShowCV', 'MatchCV', label='Another window')
G.add_edge('ShowCV', 'MatchJD', label='Another window')

G.add_edge('UploadCV', 'Preview')

G.add_edge('Preview', 'Confirm')

G.add_edge('Confirm', 'Search')

G.add_edge('AddCompany', 'AddJD')
G.add_edge('AddJD', 'MatchCV')
G.add_edge('AddJD', 'ModifyJD')

G.add_edge('MatchJD', 'GraphInfo', label='Popup window')
G.add_edge('MatchCV', 'GraphInfo')

A = nx.to_agraph(G)

A.write('cloudshare_router.dot')

X = nx.from_agraph(A)
print("edges")
print(X.edges(data=True))
print("default graph attributes")
print(X.graph)
print("node node attributes")
print(X.node)
