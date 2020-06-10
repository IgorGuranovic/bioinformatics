REQUIREMENTS:
Google Chrome
Install pip, installation found in "get-pip" folder
	Necessary imports:
	pip install helium
	pip install bs4
Python 3.7.6 64-bit ('base': conda) works best in this version
Installing Anaconda would be preferred, since without it, you have to install more packages than the two listed.

HOW TO USE:
Step 1: Download this whole "bioinformatics" repository, extract it, and paste it into a directory of your choosing.
Step 2: Create the necessary folders
	CREATE THESE FOLDERS, name them exactly like what is written in quotations:
	"CSV" folder: Where all CSV files are found, main file as well as the ones that are split into ~1000 Genbank numbers each
	"Downloads" folder: Not to be confused with your main downloads folder, this is the one where your downloaded files get 	transfered from your main Downloads folder
	"FASTA" folder: This is where all the individual FASTA sequence files will be stored
	"FullSequenceBank" folder: This is where a FASTA file and a TXT file of the full compilation of all sequences will be stored
	"get-pip" folder: U for pip installation
	"images" folder: Storage area for images for the GUI
	"Spreadsheet" folder: This is where the spreadsheet (with enzyme class and family number information) will be stored
	"TXT" folder: This is where all the individual TXT sequence files will be stored
	"TXT0" folder: This is where the unrefined files are stored after the downloaded FASTA files are converted into TXT
Step 3: Open the sequencer.py file to start the program, a GUI will pop up.
Step 4: Find the two-letter enzyme class of your desired enzyme and enter it into the first field.
	KEY:
	GH is for Glycoside Hydrolases
	GT is for GlycosylTransferases
	PL is for Polysaccharide Lyases
	CE is for Carbohydrate Esterases
	AA is for Auxiliary Activities
Step 5: Find the family number of your desired enzyme and enter it into the second field.
Step 6: Type the file path of your directory where you put the "bioinformatics" folder. (Example: D:/bioinformatics)
Step 7: Type the file path of your downloads directory. (Example: C:/Users/Igor/Downloads)
	In other words, this is the directory where you get files when you download them off the internet.
Step 8: Hit Enter and wait for all the Chrome windows to open and close. You know the program finished its job when the GUI disappears.
Step 9: Enjoy the results!

THIS PROGRAM GIVES YOU:
A CSV file of all the Genbank numbers as well as separate CSV files with ~1000 numbers each
An Excel spreadsheet with enzyme class and family number information
TXT files and FASTA files of individual sequences
TXT file and FASTA file of all sequences combined into one
