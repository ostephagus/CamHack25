import ast

with open("cambridge.json","r") as f:
    content = ast.literal_eval(f.read())

with open("MolToGrid/cambNP.txt","a+") as f:
    for i in content:
        f.write(str(i[0])+" "+str(i[1])+"\n")
