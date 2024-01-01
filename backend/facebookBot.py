from flask import Flask, request
#step1 - create a facebook shell using flask

a= [1,2,3]
b= ['a', 'b', 'c']

c = dict(zip(a,b))
print(c)

d = {1:2, 2:4}
d.update(c)
print(c)
print(d)