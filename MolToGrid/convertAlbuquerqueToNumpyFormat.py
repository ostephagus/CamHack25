import ast

with open("albuquerqueString.json","r") as f:
    content = ast.literal_eval(f.read())

with open("albNP.txt","a+") as f:
    for i in content:
        f.write(i[0]+" "+i[1]+"\n")
