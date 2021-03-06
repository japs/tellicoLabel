# tellicoLabel.py
# Copyright 2011(C) Jacopo Nespolo <j.nespolo@gmail.com>
#
# This file is part of tellicoLabel.
#
# tellicoLabel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tellicoLabel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tellicoLabel.  If not, see <http://www.gnu.org/licenses/>.

from xml.etree.ElementTree import ElementTree
from qrencode import encode_scaled
from Image import Image
from bookLabelTemplates import labelTemplate, tdTemplate
from os.path import exists, realpath
from os import mkdir
from subprocess import call
from codecs import open as copen
from xml.sax.saxutils import escape

class Book:
    def __init__(self, title, author, isbn, ID, location, shelf):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.ID = ID
        self.location = location
        self.shelf = shelf
    #enddef
    
    def bookFilter(self, string):
        ''' filters the book for string.
        '''
        for value in self.__dict__.values():
            if (string.lower() in value.lower())==True:
                return self
        return None
    #enddef
    
    def __repr__(self):
        return unicode(str(self.__dict__))
    #enddef
#endclass

def filterBookList(booklist, pattern):
    l = []
    for b in booklist:
        a = b.bookFilter(pattern)
        if a != None:
            l.append(a)
    return l
#endef

def create_book(entry):
    '''Transforms Tellico's entries into python dictionaries'''
    try: 
        authors = unicode("; ").join([i.text for i in list(entry.find(ns+"authors").iterfind(ns+"author")) ])
    except AttributeError: authors = ""
    att = []
    for at in attributes:
        try:
            att.append(unicode(entry.find(ns+at).text))
        except AttributeError: att.append("")
    return Book(att[0],
                authors,
                att[1],
                att[2],
                att[3],
                att[4]
                )
#enddef

def bookQr(book):
    '''save qr representation of book class to 
       ./tmp/$ID.png
       returns relative path to image file    
    '''
    if not exists('./tmp'):
        mkdir('./tmp')
    filename = "./tmp/%s.jpg" %unicode(book.ID)
    fileout = open(filename, 'w')
    im = encode_scaled(unicode(book.__repr__()), 2)[2]
    im.save(fileout)
    return filename
#enddef

def bookLabel(book):
    ''' calls bookQr and creates rml code for the book's label,
        saving it in ./tmp/$ID.rml
        it returns the rml file path.
    '''
    im = bookQr(book)
    fileout = "./tmp/%s.rml" %unicode(book.ID)
    f = copen(fileout, mode="w", encoding="utf-8")
    #f = open(fileout, "w")
    td = tdTemplate % {'image':im,
                       'title':unicode(escape(book.title)),
                       'author':unicode(escape(book.author)),
                       'ID':book.ID,
                       'location':" ".join([book.location, book.shelf])}
    f.write(td)
    f.close()
    return realpath(fileout)
#enddef

def makeLabelList(bookList):
    labelList = []
    for b in bookList:
        labelList.append(bookLabel(b))
    return labelList
#enddef

def typesetLabels(labelList):
    ''' takes an array containing the rml files generated
        by bookLabel and inserts them in the template file.
        fileout is ./tmp/labels.rml
        the file is compiled and if everything goes well the 
        ./tmp and all its content is deleted.
        the pdf file is saved in ./labels.pdf
        The ./tmp directory is removed after pdf generation.
    '''
    labels = []
    for l in labelList:
        f = open(l, 'r')
        labels.append(f.read())
        f.close()
    del labelList
    del f
    
    row = "</tr><tr>"
    i = len(labels)
    if i%2 == 0:
        labels.insert(i, "</tr>")
        i-=2
    else: 
        labels.insert(i,
            "<td></td><td></td><td></td>\n</tr>")
        i-=1
    while i > 0:
        labels.insert(i, row)
        i-=2
    labels.insert(0, "<tr>")
    text = "\n".join(labels)
    del labels
    
    f = copen("./tmp/labels.rml", "w", encoding="utf-8")
    a = unicode(labelTemplate % unicode(text))
    f.write(a)
    f.close()
    a = call("trml2pdf %s > ./labels.pdf" %realpath("./tmp/labels.rml"),
               shell=True)
#enddef

def cleanTmp():
    return call("rm -r ./tmp", shell=True)
#enddef

def createLabels(bookList):
    ''' This is simply a shortcut to automate the process.
        It takes a list of book objects in input, creates the
        labels and clean temporary files.
    '''
    typesetLabels(makeLabelList(bookList))
    cleanTmp()
#enddef

####################################################################

# parsing happens here
attributes = ["title", "isbn", "id", "location", "shelf"]
tree = ElementTree()
tree.parse("./libri.xml")

ns = "{http://periapsis.org/tellico/}"

coll = tree.find(ns+"collection")
entries = coll.findall(ns+"entry")

## save all xml information into Book objects
allbooks = []

for entry in entries:
    allbooks.append(create_book(entry))
# end parsing


def createAllLabels():
    typesetLabels(makeLabelList(allbooks))
#enddef