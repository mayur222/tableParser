# Table parser

## Prerequisite
1. opencv-python
2. pytesseract

## How to use it 

### Input Image

![Input Image](https://github.com/mayur222/tableParser/blob/master/Input_Horizontal_Table.JPG?raw=true)

Run below commmand
```
python withBord.py Input_Horizontal_Table.JPG
```
this will generate file Input_Horizontal_Table.xml in same file from where image file is taken
```
cat Input_Horizontal_Table.xml 
```
```
<table>
<tr><td>Name:</td><td>Ram Kumar</td><td>Shyam Kumar</td></tr>
<tr><td>Telephone:</td><td>9987654321</td><td>7894561230</td></tr>
<tr><td>Address:</td><td>Mumbai, India</td><td>Delhi, India</td></tr>
</table>
```
