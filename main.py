import ezdxf

import acronymDic
import devices_templates


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
    lines_in_layer.append("".join(my_str_array).lstrip("_"))


fileName = "BS16Y3"
doc = ezdxf.readfile(fileName + ".dxf")
msp = doc.modelspace()
layer_list = []
lines = []
lines_in_layer = []
string_to_nx = ""
for layer in doc.layers:
    layer_list.append(layer.dxf.name)

for layer_number in layer_list:
    lines_in_layer = []
    all_MText = doc.query(f'''MTEXT[layer=="{layer_number}"]''')
    entityArray = all_MText.query('*[style=="ROMANS"]')
    entity_list = list(entityArray)
    entity_list.sort(key=lambda ix: ix.dxf.insert.x)
    for e in entity_list:
        edit_entity(e)
    all_att_def = doc.query(f'''ATTDEF[layer=="{layer_number}"]''')
    # TROVA TUTTI I NOMI SOPRA OGNI LAYER
    for component in all_att_def:
        if 270 > component.dxf.insert.y > 250:
            device_in_layer = str(component.dxf.tag).replace(".", "_").replace("-", "_").replace("/", "_")
            # todo controllo caso se esiste già device_in_layer in string_to_nx
            # Filtro Dispositivo
            if "PCD1" in device_in_layer:
                # Filtro Pin
                if any("DI" in mtext.text for mtext in list(all_MText)):
                    prepared_string = ""
                    prepared_string += f'''---\ndev = {device_in_layer}\n--- \n'''
                    prepared_string += devices_templates.PCD1_E1000_A10_DI
                    # todo se length di entity list uguale a template
                    i = 0
                    for acronym in lines_in_layer:
                        pin_number = "{:02d}".format(i)
                        prepared_string = prepared_string.replace("DI" + pin_number + " = ",
                                                                  "DI" + pin_number + " = " + acronym)
                        i = i + 1
                    print(prepared_string)
            elif "ISMA" in device_in_layer:
                # todo
                print("ISMA")
with open(fileName + '.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
