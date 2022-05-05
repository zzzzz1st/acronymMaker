import ezdxf

import acronymDic


# helper function
def edit_entity(e):
    myStr = e.text.replace("\P", " ")
    myStr = myStr.replace("\p", " ")
    myStr = myStr.replace("xqc;", "")
    myStr = myStr.replace("\A1;", "")
    if "RISERVA" not in myStr:
        lines.append(myStr.replace("  ", "\n"))
    myStr = myStr.replace(")", "")
    myStr = myStr.replace("(", "")
    myStr = myStr.replace("/", "")
    myStr = myStr.replace(".", "")
    myStr = myStr.replace("-", "")
    myStr = myStr.replace("DI ", "")
    myStr = myStr.replace("ATTUATORE ", "")
    myStr = myStr.replace("SENSORE ", "")
    myStr = myStr.replace("SONDA ", "")
    # Caso nome sonda vf20 e funzionamento
    array = myStr.split("  ")
    if len(array) > 1:
        array.pop(0)
    myStr = array[0].strip()
    myStrArray = myStr.split(" ")
    myStrArray = list(dict.fromkeys(myStrArray))
    if myStrArray[0] != "RISERVA":
        # Caso Sonda e Temperatura
        # Toglie elemento mandata e lo mette in fine
        nquadro = ""
        vquadro = False
        if myStrArray[-1][0:1] == "Q":
            nquadro = myStrArray.pop(-1)
            vquadro = True
        if myStrArray[0] == "TEMPERATURA" or myStrArray[0] == "SCATTATO" or myStrArray[0] == "LIVELLO":
            myStrArray.append(myStrArray.pop(0))
            myStrArray.append(myStrArray.pop(0))
        else:
            # Caso normale che comando va in fine
            myStrArray.append(myStrArray.pop(0))
        if vquadro is True:
            myStrArray.insert(0, nquadro)
        # TODO HANDLE ELSE -  QUANDO TUTTI IF SONO FALSI DEVE ANDARE IN ELSE
        lines.append(str(myStrArray))
        for i in range(len(myStrArray)):
            if myStrArray[i][0:1] != "Q":
                acron = acronymDic.Dict.get(myStrArray[i])
                if acron is None:
                    acron = myStrArray[i].capitalize()
                    # Caso Sez passa if
                    if len(acron) > 3:
                        acron = acron[0:3]
                    # Caso Caldo C passa if
                if len(acron) > 1:
                    acron = "_" + acron
                myStrArray[i] = acron
        lines.append("".join(myStrArray).lstrip("_"))
        lines.append("---------------------------------------")


fileName = "BN02Y0"
doc = ezdxf.readfile(fileName + ".dxf")
msp = doc.modelspace()
entities = msp.query('MTEXT')
entityArray = entities.query('*[style=="ROMANS"]')
lines = []
entity_list = list(entityArray)
entity_list.sort(key=lambda ix: ix.dxf.insert.x)
for e in entity_list:
    edit_entity(e)
    print(str(e.dxf.insert.x) + "--------------" + e.text)
with open(fileName + '.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
