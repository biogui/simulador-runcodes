# **runcodes System Simulator**
[![Py3.8](https://img.shields.io/badge/Python-3.8-blueviolet.svg)](https://docs.python.org/release/3.8.5/whatsnew/changelog.html#changelog)
[![license](https://img.shields.io/badge/license-MIT-blueviolet.svg)](https://github.com/biogui/simple-image-editor-with-openCV/blob/master/LICENSE)

Hi, I'm [Bio](https://github.com/biogui)!

And this is a script for run.codes' users testing yours programs before submit.

Thanks for testing, feedbacks are awesome! Feel free to contact me on telegram [here](https://t.me/gui_bio) :)

## **Setup**
Make sure to:
- Have a recent python version[(3.x.x)](https://realpython.com/installing-python/) installed.
- Have the command [`unzip`](https://www.hostinger.com/tutorials/how-to-unzip-files-linux/) installed in your terminal. 

After that, clone the repository with and run setup.sh:

&nbsp;&nbsp;&nbsp;&nbsp;`$ git clone https://github.com/biogui/runcodes-system-simulator.git ~/.rcsimulator`

&nbsp;&nbsp;&nbsp;&nbsp;`$ cd ~/.rcsimulator`

&nbsp;&nbsp;&nbsp;&nbsp;`$ sh setup.sh`

## **Usage**
Now, in any directory, just using the `rcsim` command:
&nbsp;&nbsp;&nbsp;`$ rcsim <flag> <prog-path> <tests-path>`

#### **The `<flag>`**
This program treats different line endings(CR, LF, CR + LF) by default, in order to
		ignore that, use the "-i" flag in your respective field.
- Use without flag:

&nbsp;&nbsp;&nbsp;&nbsp;`$ rcsim program.c Tests/`

![Use example](/images/without_i.png)
- Use with flag:

&nbsp;&nbsp;&nbsp;&nbsp;`$ rcsim -i program.c Tests/`

![Use example](/images/without_i.png)

#### **The `<prog-path>`**
This program have suports to *unic file* and *multiple files with a Makefile* projects. In the `<prog-path>` field add the path to the .c file or Makefile.

#### **The `<tests-path>`**
This program have suports to *zip files* and *pre-existing directory* with the test cases. In the `<files-path>` field add the path to the .zip file or directory with the test-cases.