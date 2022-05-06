import ezdxf

import acronymDic


# helper function
def edit_entity(e):
    my_str = e.text.replace("\P", " ")
    my_str = my_str.replace("\p", " ")
    my_str = my_str.replace("xqc;", "")
    my_str = my_str.replace("\A1;", "")
    my_str = my_str.replace(")", "")
    my_str = my_str.replace("(", "")
    my_str = my_str.replace("/", "")
    my_str = my_str.replace(".", "")
    my_str = my_str.replace("-", "")
    my_str = my_str.replace("DI ", "")
    my_str = my_str.replace("ATTUATORE ", "")
    my_str = my_str.replace("SENSORE ", "")
    my_str = my_str.replace("SONDA ", "")
    # Caso nome sonda vf20 e funzionamento
    array = my_str.split("  ")
    if len(array) > 1:
        array.pop(0)
    my_str = array[0].strip()
    my_str_array = my_str.split(" ")
    my_str_array = list(dict.fromkeys(my_str_array))
    if my_str_array[0] != "RISERVA":
        # Caso Sonda e Temperatura
        # Toglie elemento mandata e lo mette in fine
        nquadro = ""
        vquadro = False
        if my_str_array[-1][0:1] == "Q":
            nquadro = my_str_array.pop(-1)
            vquadro = True
        if my_str_array[0] == "TEMPERATURA" or my_str_array[0] == "SCATTATO" or my_str_array[0] == "LIVELLO":
            my_str_array.append(my_str_array.pop(0))
            my_str_array.append(my_str_array.pop(0))
        else:
            # Caso normale che comando va in fine
            my_str_array.append(my_str_array.pop(0))
        if vquadro is True:
            my_str_array.insert(0, nquadro)
        for i in range(len(my_str_array)):
            if my_str_array[i][0:1] != "Q":
                acron = acronymDic.Dict.get(my_str_array[i])
                if acron is None:
                    acron = my_str_array[i].capitalize()
                    # Caso Sez passa if
                    if len(acron) > 3:
                        acron = acron[0:3]
                    # Caso Caldo C passa if
                if len(acron) > 1:
                    acron = "_" + acron
                my_str_array[i] = acron
        lines.append("".join(my_str_array).lstrip("_"))


fileName = "BS16Y3"
doc = ezdxf.readfile(fileName + ".dxf")
msp = doc.modelspace()
layer_list = []
lines = []
for layer in doc.layers:
    layer_list.append(layer.dxf.name)
for layer_number in layer_list:
    entityArray = doc.query(f'''MTEXT[layer=="{layer_number}"]''').query('*[style=="ROMANS"]')
    entity_list = list(entityArray)
    entity_list.sort(key=lambda ix: ix.dxf.insert.x)
    for e in entity_list:
        edit_entity(e)
with open(fileName + '.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
