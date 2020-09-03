# **runcodes System Simulator**
[![Py3.8](https://img.shields.io/badge/Python-3.8-blueviolet.svg)](https://docs.python.org/release/3.8.5/whatsnew/changelog.html#changelog)
[![license](https://img.shields.io/badge/license-MIT-blueviolet.svg)](https://github.com/biogui/simple-image-editor-with-openCV/blob/master/LICENSE)

Hi, I'm [Bio](https://github.com/biogui)!

And this is a script for [run.codes](https://we.run.codes/)' users testing yours programs before submit.

Thanks for testing, feedbacks are awesome! Feel free to contact me on telegram [here](https://t.me/gui_bio) :)

## **Setup**
Make sure to:
- Have a recent python version[(3.x.x)](https://realpython.com/installing-python/) installed.
- Have the command [`unzip`](https://www.hostinger.com/tutorials/how-to-unzip-files-linux/) installed in your terminal. 

After that, clone the repository and run setup.sh:

&nbsp;&nbsp;&nbsp;&nbsp;`$ git clone https://github.com/biogui/runcodes-system-simulator.git ~/.rcsimulator`

&nbsp;&nbsp;&nbsp;&nbsp;`$ cd ~/.rcsimulator`

&nbsp;&nbsp;&nbsp;&nbsp;`$ sh setup.sh`

## **Usage**
Now, in any directory, just using the `rcsim` command: `$ rcsim <flag> <prog-path> <tests-path>`

*ps.: `rcsim` can be exchange by `python3 rcsimulator.py`, but it is necessary to have c in the current directory.*

#### **The `<flag>`**
This program treats different line endings(CR, LF, CR + LF) by default, in order to
		ignore that, use the "-i" flag in your respective field.
- Use without flag:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ rcsim program.c Tests/`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Use example](/images/without_flag.jpg)
- Use with flag:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ rcsim -i program.c Tests/`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Use example](/images/with_flag.jpg)

#### **The `<prog-path>`**
This program suports *singular C program* or multiple files depending only on *Makefile* being included. In the `<prog-path>` field add the path to the .c file or Makefile.

#### **The `<tests-path>`**
This program suports both *ZIP archives* and *local directories* as for the test cases. In the `<files-path>` field add the path to the .zip file or directory with the test-cases.
