11.05.2020

Use the DEPID via the main.py file. It can be applied either to a single file or a number of files in a directory.
run python main.py -h to find out the appropriate flags

The output is written into standard output. The output includes:
- the number of tokens
- the depid value
- the depid value with repetitions excluded

More detailed output is written in the output file. If the output folder is not specified then a default folder is created in the project folder
In the output file, each word is on a separate line and among the more obvious information in the first columns the following information is presented:
T - the word is counted as token
the proposition if the word together with its head make up a proposition
R - if this is the first instance of this proposition

Runnning this script requires:
- python 3.6
- spacy together with English models
