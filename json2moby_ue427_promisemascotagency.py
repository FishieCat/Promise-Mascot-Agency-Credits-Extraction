import json, sys

text = ''

creds = {}
root = []

with open(sys.argv[1], encoding='utf-8') as f:
    data = json.load(f)
        
    for i in data:
        i_name = i['Name']
        if i['Name'].startswith('Cred') or i['Type'].startswith('Credit'):

            if 'Properties' in i and 'Text' in i['Properties']:
                name = i['Properties']['Text']['CultureInvariantString']
                cred_id = i['Properties']['Slot']['ObjectPath']
                creds[cred_id] = name
                if 'eader' in i['Type']:
                    creds[cred_id] = '\n'+name
                name = name.replace('\\r\\n','\n')
                text += name + '\n\n'
        elif i['Name'].startswith('Uniform') or i['Name'].startswith('Vertical'):
            
            if not 'Slots' in i['Properties']:
                continue
            
            #print(i_name)
            x = []
            for obj in i['Properties']['Slots']:
                x.append(obj)
            if 'Slot' in i['Properties']:
                creds[i['Properties']['Slot']['ObjectPath']] = x
            else:
                #print('adding root')
                root = x
        

def recobj(text, creds, cid):
    if cid in creds:
        thing = creds[cid]
    else:
        return text
    if isinstance(thing, str):
        text += '\n'+thing
        return text
    else:
        for something in thing:
            text = recobj(text, creds, something['ObjectPath'])
        return text

text2 = ''

for thing in root:
    objp = thing['ObjectPath']
    text2 = recobj(text2, creds, objp)

text = text.strip()
text2 = text2.strip()

with open(sys.argv[1] + '_moby.txt', 'w', newline='', encoding='utf-8') as f:
    f.write(text)

with open(sys.argv[1] + '_moby_2.txt', 'w', newline='', encoding='utf-8') as f:
    f.write(text2)