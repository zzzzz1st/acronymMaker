<img src="https://user-images.githubusercontent.com/52376408/163709688-c3c96f71-a5cb-4c26-8bae-cc79104d2046.png" width="20%" height="20%"><img src="https://user-images.githubusercontent.com/52376408/163709667-57463b29-77f4-44fa-9d34-0915c411be95.png" width="20%" height="20%">


## Overview
This project is one the beauties in the world that saved me a lot of time. The story is that when you want to program a controller or in other words an industrial cpu (PLC) you should map each variable on it. For mapping the variables you should use a framework (in my case) that's called Niagara NX [@tridium](https://github.com/tridium) and you should write the register address and its name. For example you might want to map the DO1 (which stands for the pin digital output 1) as a Heat pump comand. Sometimes those names are too long and it's not standard to write all of the name. Because on a long term period it may create anomalies for saving the historical data on the local and cloud databases. As an example we might have a variable whose name is "<em>Scattato Termico Pompa Scambiatore Preparatore ACS 2  (QECI+ACS) </em>". In this case it's inappropriate to save a pin as this long name.<br><br>
So what will you do ? <br>
<b>YOU WILL MAKE AN ACRONYM FOR EACH NAME</b><br><br>
So you should look at the original electrical scheme, think about acronyms for each name and write it manually on the framework. As an example, for that long name above, you should think about an acronym like : <em>QECIACS_ACS2_PmpScambPrep_ScatTerm</em> and write it on the specific register as its name. It's notable that these acronyms have an standard and each company has its own standard. But the problem is that you should pick each name from the electrical scheme manually, think about its acronym and write that manually on the program. This takes so much time and time means money for a company 😄. <br><br>

As you can see that's an algorithmic problem and it might be resolvable by a computer. So what i've done recently is that I made a program which takes an electrical scheme as a dxf (a CAD format) file and gives a list of acronyms for each pin name.

## Implementation

It reads a dxf file with [ezdxf](https://github.com/mozman/ezdxf) library, searches for a specific style format (in this case ROMANS style) and format each word. Then it looks on a predefined python dictionary and gets acronyms for each word. In the end it concatenates each word for making the acronym of the original word. Every word which is not in the dictionary file, gets shortened by a prefixed length. One thing that you should do before running the program is to change the wanted words style to the ROMANS style on the dxf file (You can do it with Autocad).

<img src="https://user-images.githubusercontent.com/52376408/163709718-c3b48103-0434-4fe6-a2bc-83decb473921.png" width="50%" height="50%">

On the picture above you can see the highlighted words that need to have ROMANS style in order to be selected.

## Contribution

You might want to see the issues if you'd like to contribute to this project but I'll be happy if you have any ideas and you'd like to contribute.<br>
Feel free to ask any questions that you might have on this project.
