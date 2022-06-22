import ezdxf

import acronymDic
import devices_templates
import devices_pins


# helper function
def edit_entity(e):
    array = replace_string(e)
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


# Va messo il nome di ogni dispositivo
def get_generic_name(specific_name):
    if "PCD1_E1000_A10" in specific_name:
        return "PCD1_E1000_A10"
    elif "PCD1_A1000_A20" in specific_name:
        return "PCD1_A1000_A20"
    elif "PCD1_G2000_A20" in specific_name:
        return "PCD1_G2000_A20"
    elif "PCD1_G5010_A20" in specific_name:
        return "PCD1_G5010_A20"
    elif "PCD1_G2200_A20" in specific_name:
        return "PCD1_G2200_A20"
    else:
        return "NUll"


def replace_string(entity):
    my_str = entity.text.replace("\P", " ")
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
    return array


def select_pin(output_string, pin):
    prepared_string = ""
    header_string = f'''---\ndev = {device_in_layer}\n--- \n'''
    prepared_string += header_string
    try:
        prepared_string += devices_templates.Devices.get(get_generic_name(device_in_layer) + "_" + pin)
    except TypeError:
        print("An unknown device on this page")
    if len(lines_in_layer) == devices_pins.Devices.get(str(get_generic_name(device_in_layer)) + "_" + pin):
        i = 0
        for acronym in lines_in_layer:
            pin_number = "{:02d}".format(i)
            prepared_string = prepared_string.replace(pin + pin_number + " = ",
                                                      pin + pin_number + " = " + acronym)
            i = i + 1
        # controllo caso se esiste già device_in_layer in string_to_nx
    if header_string in output_string:
        output_string = output_string.replace(header_string, prepared_string)
    else:
        output_string += prepared_string
    return output_string


fileName = "QFS785"
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
    all_layer_pins = []
    for mtext in all_MText:
        # Isola la parte pins
        if 270 > mtext.dxf.insert.y > 230:
            all_layer_pins.append(mtext)
    entity_list.sort(key=lambda ix: ix.dxf.insert.x)
    for e in entity_list:
        edit_entity(e)
    all_att_def = doc.query(f'''ATTDEF[layer=="{layer_number}"]''')
    # TROVA TUTTI I NOMI SOPRA OGNI LAYER
    for component in all_att_def:
        if 270 > component.dxf.insert.y > 250:
            device_in_layer = str(component.dxf.tag).replace(".", "_").replace("-", "_").replace("/", "_")
            # Filtro Dispositivo
            if "PCD1" in device_in_layer:
                # Filtro Pin
                if any("DO1" in mtext.text for mtext in all_layer_pins) or any(
                        "NO1" in mtext.text for mtext in all_layer_pins):
                    string_to_nx = select_pin(string_to_nx, "DO")
                elif any("DI1" in mtext.text for mtext in all_layer_pins):
                    string_to_nx = select_pin(string_to_nx, "DI")
                elif any("UI1" in mtext.text for mtext in all_layer_pins):
                    string_to_nx = select_pin(string_to_nx, "UI")
                elif any("AI1" in mtext.text for mtext in all_layer_pins):
                    string_to_nx = select_pin(string_to_nx, "AI")
                elif any("AO1" in mtext.text for mtext in all_layer_pins):
                    string_to_nx = select_pin(string_to_nx, "AO")
            elif "ISMA" in device_in_layer:
                # todo
                print("ISMA")

with open(fileName + '.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
with open(fileName + 'output.txt', 'w') as f:
    f.write(string_to_nx)
    f.write('\n')
