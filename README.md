This software aims at proving a simple way to register each time you do something and then display various statistics of your choice about it.
Its use ought to be relatively straightforward. Each time you want to register an instance is a "ping", a series of pings is a "ping stats series". 
See bellow for more information.

# Running this software
## Integration
On linux simply run the script install.sh to integrate the software. 

## Run executable
On linux and windows, you can simply run the executable file. It will create a "settings" file next to the executable. You need to choose a directory to save information the first time you launch this software.

## Python
Alternatively, you can run the python scirpt directly from the source without any compilation. 
On linux 
```
python3 main.py
```

On windows
```
python main.py
```

## Build executable from source
Simply run the python script "build.py"."

# Some information on configuration.
You can display different statistics about a given ping stats series by checking the proper boxes. Drag and drop the boxes to change the order of the corresponding displays.
You can also change the order of the ping stat series by drag and drop (from the main view, not the "setting" window).

## On transitivity
You can set one transitivity option per ping stat series. If A is set to have transitivity on B (through A's settings window), then whenever you ping A it will also register a ping on B.

# Bells and whistles
This is a small project I mostly did for myself. As such, it does not aim to include all possible features and might be unreliable.
If you use this software and there is a reasonable change you want, or if you want to use it but are facing issues, feel free to open an issue on github. I do not guarantee to maintain this proect in any way, but I am likely to be amenable to small requests.

# License
The code for this software is released under the MIT license. The executables are released under the GPL3 license. See LICENSE file for more.

# Acknowledgements
This software used the PyQt6 library.
The sources for this library can be found [here](https://pypi.org/project/PyQt6/#files).
PyQt6 is itself reliant on Qt6, the source of which can be found [here](https://wiki.qt.io/Building_Qt_6_from_Git#Getting_the_source_code)
I extend my sincere gratitude to these and the other free libraries I used.