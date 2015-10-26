#!/usr/bin/env python

import networkx as nx

G = nx.DiGraph()

G.add_node('Login')

G.add_edge('Login', 'Superadmin')
G.add_edge('Login', 'User')

G.add_edge('Superadmin', 'EditUser')
G.add_edge('Superadmin', 'Logout')

G.add_edge('User', 'Search')
G.add_edge('User', 'Upload')
G.add_edge('User', 'Logout')
G.add_edge('User', 'Information', color='blue')

G.add_edge('Search', 'SearchResult')

G.add_edge('SearchResult', 'Show', label='Another window')

G.add_edge('Upload', 'Preview')

G.add_edge('Preview', 'Confirm')

G.add_edge('Confirm', 'Search')


A = nx.to_agraph(G)

A.write('cloudshare_router.dot')

X = nx.from_agraph(A)
print("edges")
print(X.edges(data=True))
print("default graph attributes")
print(X.graph)
print("node node attributes")
print(X.node)
