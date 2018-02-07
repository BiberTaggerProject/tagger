import glob, random, shutil, re, csv

# sets filepath for where to extract files from (parsed corpus)
path = 'C:/Users/brett/Desktop/Language Data/Parsed Longman Corpus Sample/*'

# file for where the output from this program will go
outfile = 'C:/Users/brett/Desktop/dr egbert Work/the grammar project/Precision.csv'
fileout = open(outfile, 'w+')
wr = csv.writer(fileout, dialect = 'excel', lineterminator='\n')

kwiclist = []
filelist = []
# loops through each file in the corpus one by one
for files in glob.glob(path):

    filelist.append(files)

    with open(files, encoding='utf-8', errors='ignore') as file_open:
        text = file_open.read()
        split_text = text.split("\n")

        # creates the KWICS

        for i, words in enumerate(split_text):
            wordslist = []
            bibertagslist = []
            clawstagslist = []
            if i > 7 and i + 7 < len(split_text) and 'NEC' in words:
            # creates lists with each list being a word in the KWIC
                kwic = split_text[i-7] + " " + split_text[i-6] + " " + split_text[i-5] + " " + split_text[i-4] + " " + split_text[i-3] + " " + split_text[i-2] + " " + split_text[i-1] + " " + \
                        split_text[i] + " " + split_text[i+1] + " " + split_text[i+2] + " " + split_text[i+3] + " " + split_text[i+4] + \
                        " " + split_text[i+5] + " " + split_text[i+6] + " " + split_text[i+7]

                kwic = kwic.split(' ')
                # divides kwics into lists of words, bibertags, and clawstags; their indexes should correspond
                for i, items in enumerate(kwic):
                    if i == 0 or i % 3 == 0:
                        wordslist.append(items)
                    elif i % 3 == 1:
                        bibertagslist.append(items)
                    else:
                        clawstagslist.append(items)
                print(wordslist)
                # writes a row of words then a row of biber then claws and then an empty row to separate them
                wr.writerow(wordslist)
                wr.writerow(bibertagslist)
                wr.writerow(clawstagslist)
                fileout.write('\n')