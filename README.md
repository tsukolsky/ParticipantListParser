This project is used to put together a participant list for Ironman races.
Ironman.com does not publish the entrants to the race in an XML document or other nice format,
but in a PDF file. Using PDFMiner (see below) (ie pdf2txt.py with default settings) to scrape the words from the PDF document, this program goes through the output text file and puts together an entry list, age group breakdown, and 
Kona Q-Spot allocation. Usage is as follows:

./ParticipantParser.py <pdf2txt output file> [# kona spots offered]


For example, for IM Texas, the command is:

./ParticipantParser.py StartingLists/IMTexasStartlist.txt 75

Currently the program is scripted to not show anything but age group percentages and kona spots,
however it will progress and be more interactive and possibly include a GUI?


** PDF Miner Git Repo
https://github.com/euske/pdfminer.git
