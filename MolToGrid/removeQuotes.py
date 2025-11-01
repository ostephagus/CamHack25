# The json of albuquerque coords has quotes in it which makes python interpret the numbers as strings
# This program removes said quotes
with open("albuquerque.json","r+") as f:
    content = f.read()
    
content = content.replace('"','')
print(content[:10])

with open("albuquerqueFixed.json","w+") as f:
    f.write(content)
