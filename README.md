# Statistical Machine Translation 
## IBM model 1:
The code runs the IBM 1 model.<br />
In order to run the model, write the following line:<br />
python3 ./IBM1.py english_file french_file<br />
for example: python3 ./IBM1.py ./data/hansards.e ./data/hansards.f<br />
**Output:**<br />
A file called aligment_IBM1.txt that contains the alignment,<br />
And another file called t_IBM1.txt containing the probability table t.<br />
<br />
**Pseudo Code:**<br />
![image](https://user-images.githubusercontent.com/72921611/182416353-53412aab-c88f-4fc9-b62a-9faf4b32f4ac.png)


## IBM model 2:
The code runs the IBM 2 model.<br />
In order to run the model, write the following line:<br />
python3 ./IBM2.py english_file french_file<br />
for example: python3 ./IBM2.py ./data/hansards.e ./data/hansards.f<br />
**Output**<br />
A file called aligment_IBM2.txt that contains the alignment<br />
