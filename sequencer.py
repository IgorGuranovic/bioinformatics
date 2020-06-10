from helium import*
import bs4, re, time, os, shutil, glob, os.path
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd
from tkinter import *
from PIL import ImageTk, Image

# Inputs: Two-character string for the class of enzyme, family number of enzyme (Example: "GH", 29), path of desired directory, path of user download directory
# Creates Excel spreadsheet of Genbank numbers with information abour enzyme class 
# Creates a main CSV file of all Genbank numbers and CSV files of separate pages, in the CSV folder
# Creates a main TXT file of all sequences in the FullSequenceBank folder and TXT files of separate sequences in the TXT folder
# Creates a main FASTA file of all sequences in the FullSequenceBank folder and FASTA files of separate sequences in the FASTA folder
def Protein (type, n, directory, download_dir):

        n = int(n)

        # Returns how many pages of Genbank numbers there are for a specific class and family of enzyme.
        def PageNumber ():
                central = 'http://www.cazy.org/%s%d_all.html' % (type, n)
                uClient = uReq(central)
                read_page = uClient.read()
                uClient.close()
                main_list = soup(read_page, "html.parser")
                page_number_raw = main_list.find_all("span",{"class":"pages"})
                code0 = "href"
                string_pnr = str(page_number_raw)
                vals0 = [m.start() for m in re.finditer(code0, string_pnr)]
                if vals0 == []:
                        p = 1
                else:
                        last = string_pnr[vals0[-1]:-1]
                        code1 = "nofollow"
                        index = [m.start() for m in re.finditer(code1, last)]
                        p = int(last[(index[0]+10):-11])
                return p

        # Inputs: url of page, desired page number, main list of all Genbank numbers
        # Extracts all Genbank numbers from a given page and adds them onto the final list
        # Creates a CSV file for all Genbank numbers on a given page
        def ListAppender (input_url, g, final_list):
                url_main = input_url
                uClient = uReq(url_main)
                read_page = uClient.read()
                uClient.close()
                parsed_list = soup(read_page, "html.parser")
                code = "&amp;val="
                string_list = str(parsed_list)
                vals = [m.start() for m in re.finditer(code, string_list)]
                startvals = [x + 9 for x in vals]
                endvals = [x + 25 for x in vals]
                temp_list = []
                csv_list = []
                for x in range(len(vals)):
                        temp_list.append(string_list[startvals[x]:endvals[x]])
                for element in temp_list:
                        element = element.split('"')
                        element = element[0]
                        final_list.append(element)
                        csv_list.append(element)
                df = pd.DataFrame(csv_list)
                df.to_csv(os.path.join("%s/CSV" % (directory), 'genbank%d.csv' % (g+1)), sep=',', header=None, index=None)

        # Inputs: Number of pages, main list of all Genbank numbers
        # Calls the ListAppender function to extract all Genbank numbers for an enzyme family
        def FullList (p, final_list):
                for x in range(p):
                        url_specific = 'http://www.cazy.org/%s%d_all.html?debut_PRINC=%d000#pagination_PRINC' % (type,n,x)
                        ListAppender(url_specific, x, final_list)

        # Input: Path of user download directory
        # Halts the program from progressing until a file has been fully downloaded in the user download directory
        def wait(path_to_downloads):
                condition = True
                while condition:
                        time.sleep(1)
                        condition = False
                        for fname in os.listdir(path_to_downloads):
                                if fname.endswith('.crdownload'):
                                        condition = True

        # Input: Main list of all Genbank numbers
        # Downloads FASTA sequence files of all Genbank numbers in sets of 200 at a time; note that if one link is broken, the program will make the file a set of 199, and so on...
        def Sequencer (final_list):
                shortened_list = []
                for x in range(0, len(final_list), 200):
                        shortened_list = final_list[x:x+200]
                        link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=%s" % (shortened_list[0])
                        for x in range(len(shortened_list)-1):
                                link = link + "," + shortened_list[x+1]
                        new_link = link + "&rettype=fasta&retmode=text"
                        start_chrome(new_link)
                        wait("%s" % (download_dir))
                        kill_browser()

        # Input: Main list of all Genbank numbers
        # Moves all downloaded sequence files into the desired directory
        def MassMove (final_list):
                for x in range(int(len(final_list)/200+1)):
                        if x == 0:
                                shutil.move("%s/sequence.fasta" % (download_dir), "%s/Downloads" % (directory))
                        else:
                                shutil.move("%s/sequence (%d).fasta" % (download_dir, x), "%s/Downloads" % (directory))

        # Inputs: Name of input file, name of output file, location of input file in desired directory, location of output file in desired directory
        # Converts FASTA files into TXT files and places them in a specified directory
        def FASTA2TXT (input_file, output_file, fasta_location, txt_location):
                Input = open(os.path.join("%s%s" % (directory, fasta_location), input_file), "r")
                Output = open(os.path.join("%s%s" % (directory, txt_location), output_file), "w")
                for line in Input:
                        Output.write(line)
                Input.close()
                Output.close()

        # Inputs: Name of input file, name of output file, location of input file in desired directory, location of output file in desired directory
        # Converts TXT files into FASTA files and places them in a specified directory
        def TXT2FASTA (input_file, output_file, txt_location, fasta_location):
                Input = open(os.path.join("%s%s" % (directory, txt_location), input_file), "r")
                Output = open(os.path.join("%s%s" % (directory, fasta_location), output_file), "w")
                for line in Input:
                        Output.write(line)
                Input.close()
                Output.close()

        # Converts all downloaded FASTA files into TXT, places TXT files in the "TXT0" directory  
        def Download2TXT ():
                files = glob.glob("%s/Downloads/*" % (directory))
                for x in range(len(files)):
                        if x == 0:
                                FASTA2TXT("sequence.fasta", "sequence0.txt", "/Downloads", "/TXT0")
                        else:
                                FASTA2TXT("sequence (%d).fasta" % (x), "sequence%d.txt" % (x), "/Downloads", "/TXT0")

        # Input: TXT file
        # Returns a string of the TXT file
        def TXTReader (txt):
                with open (txt, "r") as text:
                        return text.read()

        # Input: String of multiple sequences
        # Returns a list of individual sequences in input string
        def Splitter (sequence_s):
                seq_list = []
                temp_seq = ""
                keyword0 = ">"
                indices = ([m.start() for m in re.finditer(keyword0, sequence_s)])
                for x in range(len(indices)-1):
                        temp_seq = sequence_s[indices[x]:indices[x+1]]
                        seq_list.append(temp_seq)
                temp_seq = sequence_s[indices[-2]:indices[-1]]
                seq_list.append(temp_seq)
                return seq_list

        # Input: Main list of all Genbank numbers
        # Returns amount of sequences for list of Genbank numbers, this is to account for broken links
        def Counter (final_list):
                count = 0
                files = glob.glob("%s/TXT0/*" % (directory))
                for x in range(len(files)):
                        count += Length(x)
                return count

        # Input: Assigned number of file in "TXT0" directory
        # Returns amount of sequences in a file with the given input number
        def Length (x):
                if x > -1:
                        return len(Splitter(TXTReader(os.path.join("%s/TXT0" % (directory), "sequence%d.txt" % (x)))))
                else:
                        return 0

        # Inputs: String of multiple sequences, assigned number of file in "TXT0" directory, main list of all Genbank numbers
        # Creates TXT files of individuals equences, stored in the "TXT" directory
        def SplitWriter (sequence_string, iteration, final_list):
                temp_seq = ""
                keyword0 = ">"
                indices = ([m.start() for m in re.finditer(keyword0, sequence_string)])
                for z in range(Length(iteration)-1):
                        number = 0
                        for y in range(iteration+1):
                                number += Length(y-1)
                        number += z+1
                        temp_seq = sequence_string[indices[z]:indices[z+1]]
                        notepad = open(os.path.join("%s/TXT" % (directory), "sequences%d.txt" % (int(number))), "w")
                        notepad.write(temp_seq)
                        notepad.close()
                temp_seq = sequence_string[indices[-1]:-1]
                if len(glob.glob("%s/Downloads/*" % (directory))) == (iteration + 1):
                        notepad = open(os.path.join("%s/TXT" % (directory), "sequences%d.txt" % (Counter(final_list))), "w")
                        notepad.write(temp_seq)
                        notepad.close()
                else:
                        number = 0
                        for y in range(iteration+1):
                                number += Length(y)
                        notepad = open(os.path.join("%s/TXT" % (directory), "sequences%d.txt" % (int(number))), "w")
                        notepad.write(temp_seq)
                        notepad.close()
        
        # Input: Main list of all Genbank numbers
        # Joins all sequences into one main TXT file, stored in the "FullSequenceBank" directory
        def Joiner (final_list):
                notepad = open(os.path.join("%s/FullSequenceBank" % (directory), "sequence.txt"), "w")
                newstr = MultiSplitter(final_list)
                notepad.write(newstr)
                notepad.close()

        # Inputs: Main list of all Genbank numbers
        # Writes a CSV file and an Excel spreadsheet for all Genbank numbers, including the class and family number in the spreadsheet
        def ExcelCSVWriter (final_list):
                word = ""
                if type == "GH":
                        word = "Glycoside Hydrolase Family"
                elif type == "GT":
                        word = "GlycosylTransferase Family"
                elif type == "PL":
                        word = "Polysaccharide Lyase Family"
                elif type == "CE":
                        word = "Carbohydrate Esterase Family"
                elif type == "AA":
                        word = "Auxiliary Activity Family"
                else:
                        word = "Unknown Family"
                frame = pd.DataFrame({"%s %d" % (word, n):final_list})
                final_data = pd.ExcelWriter(os.path.join("%s/Spreadsheet" % (directory), "spreadsheet.xlsx"), engine = 'xlsxwriter') #pylint: disable=abstract-class-instantiated
                frame.to_excel(final_data, sheet_name = 'Sheet1')
                final_data.save() 
                df =  pd.DataFrame(final_list)
                df.to_csv(os.path.join('%s/CSV' % (directory), 'genbank.csv'), sep=',', header=None, index=None)

        # Input: Sub-folder desired to be wiped
        # Removes all files from that folder
        def Remover (file_path):
                files = glob.glob("%s/%s/*" % (directory, file_path))
                for fi in files:
                        os.remove(fi)
        
        # Input: Main list of all Genbank numbers
        # Splits all sequences described by the Genbank numbers in the input list, returns a combined string of all sequences
        def MultiSplitter (final_list):
                sequence_list = ""
                temp1 = ''
                files = glob.glob("%s/TXT0/*" % (directory))
                for x in range(len(files)):
                        sequence_list += temp1.join(Splitter(TXTReader(os.path.join("%s/TXT0" % (directory), "sequence%d.txt" % (x)))))
                        SplitWriter(TXTReader(os.path.join("%s/TXT0" % (directory), "sequence%d.txt" % (x))), x, final_list)
                return sequence_list

        # Converts every individual sequence TXT file into a FASTA file, placed in the "FASTA" directory
        def Individual2FASTA ():
                files = glob.glob("%s/TXT/*" % (directory))
                for x in range(len(files)):
                        TXT2FASTA("sequences%d.txt" % (x+1), "sequences%d.fasta" % (x+1), "/TXT", "/FASTA")

        # Removes all files from the sub-folders from previous trials so they don't get mixed up with current trial
        Remover("CSV")
        Remover("FASTA")
        Remover("TXT")
        Remover("TXT0")
        Remover("Downloads")
        Remover("Spreadsheet")
        Remover("FullSequenceBank")

        # Initializes list that is going to contain all Genbank numbers
        final_list = []

        # Calls the necessary functions
        FullList(PageNumber(), final_list)
        ExcelCSVWriter(final_list)
        Sequencer(final_list)
        MassMove(final_list)
        Download2TXT()
        Joiner(final_list)
        Individual2FASTA()

        # Converts main sequence compilation into FASTA
        TXT2FASTA("sequence.txt", "sequence.fasta", "/FullSequenceBank", "/FullSequenceBank")

# This is the function called by pressing the "Enter" button in the GUI
# Calls the Protein function using the entered values in the GUI and then closes the program
def init ():
        if e1.get() != '' and e2.get() != '' and e3.get() != '' and e4.get() != '':
                Protein(e1.get(), e2.get(), e3.get(), e4.get())
                master.destroy()

#Setting up the GUI
master = Tk()

# GUI text labels
Label(master, text="ENZYME ", font="times 72").grid(row=0, sticky=E)
Label(master, text="SEQUENCER", font="times 72").grid(row=0, column=1, sticky=W)
Label(master, text="Enzyme Class:", font="times 48").grid(row=1, sticky=W)
Label(master, text="Family Number:", font="times 48").grid(row=2, sticky=W)
Label(master, text="This Folder's Directory:", font="times 48").grid(row=3, sticky=W)
Label(master, text="Downloads Directory:", font="times 48").grid(row=4, sticky=W)

# GUI image 1
im1 = Image.open('images/cazyimage.png')
im1 = im1.resize((484,134), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(im1)
Label(master, image=image1).grid(row=5)

# GUI image 2
im2 = Image.open('images/ncbi.jpg')
im2 = im2.resize((309,134), Image.ANTIALIAS)
image2 = ImageTk.PhotoImage(im2)
Label(master, image=image2).grid(row=5, column=1)

# GUI entry fields
e1 = Entry(master, font="times 48", width=3)
e2 = Entry(master, font="times 48", width=3)
e3 = Entry(master, font="times 48", width=23)
e4 = Entry(master, font="times 48", width=23)
e1.grid(row=1, column=1, sticky=W)
e2.grid(row=2, column=1, sticky=W)
e3.grid(row=3, column=1)
e4.grid(row=4, column=1)

# GUI buttons ("Enter" and "Cancel")
Button(master, text='Enter', font="times 48", command=init).grid(row=6, column=0, pady=4)
Button(master, text='Cancel', font="times 48", command=master.destroy).grid(row=6, column=1, pady=4)

# Opens GUI
master.mainloop()