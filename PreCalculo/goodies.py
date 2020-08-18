#/usr/bin/python3
# -*- coding: utf-8 -*-

# This script changes how things look like
# from the the previous TeX4ht generated version.
#
# Author: Pedro H A Konzen - UFRGS - Jan/2018

import sys
import os
from os import walk
import numpy as np
import string
import urllib.parse
import datetime

#stackoverflow:begin
import re
import unicodedata

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return text
#stackoverflow:end

def text_to_initials(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    ini = ""
    s = 0
    while (s != -1):
        ini += text[s]
        text = text[s+1:]
        s=-1
        if (len(text)>0):
            s = text.find("_")
        if (s != -1):
            s += 1
    return ini

sdirname = "./.tmp/"
dest_dirname = "../on_server/PreCalculo/livro/"

#preliminar - list of hotsites
ifhs = open("../lisths.aux",'r')
lisths = ""
for line in ifhs:
    hsname = line.split(";")
    lisths += '<li><a href="../../'+hsname[0]+'/index.html">'\
           +hsname[1].strip("\n")+'</a></li>'
ifhs.close()

lfiles = []
for (dirpath, dirnames, filenames) in walk (sdirname):
    lfiles.extend (filenames)
    break

for index, f in enumerate (lfiles):
    lfiles[index] = os.path.splitext(f)[0]
print("Source files: ", lfiles)

listOfContents = []

#create names for hrefs in main.html
ifile = open(sdirname + "main.html", 'r')
text = ifile.read()

s = text.index('<div class="tableofcontents">')
rtext = text[s:]

s = rtext.find('href="main')
saux = s
while (saux != -1):
    auxText = rtext[s+10:]
    e = s + 10 + auxText.index('"')
    rep = 'name ="main'
    aux_e = s + 10 + auxText.find(".html")+5
    rep += rtext[s+10:aux_e] + '"'
    rep += rtext[s:aux_e]
    sub = rtext[s:e]
    rtext = rtext.replace(sub, rep)

    #add to listOfContents
    e = sub.index(".html")
    listOfContents.append((sub[6:e],sub[6:e+5]))

    s += auxText.index("</a>")
    saux = rtext[s:].find('href="main')
    s += saux
    
s = text.index('<div class="tableofcontents">')
text = text.replace(text[s:],rtext)
ifile.close()

#change titleHead and title
#title
title = "<title>Pré-calculo - Um Livro Colaborativo"
s = text.index('<title>')
e = text.index('</title>')
text = text.replace(text[s:e], title)

#titleHead
text = text.replace('<h2 class="titleHead">Pré-calculo<br />',
                    '<h2 class="titleHead">Pré-calculo<br /><small>')
s = text.index('<h2 class="titleHead">')
auxText = text[s:]
e = s + auxText.index('</h2>')
text = text.replace(text[s:e],text[s:e]+"</small>")

ofile = open(sdirname + "main.html", 'w')
ofile.write(text)
ofile.close()

#print(text)
#raise Error("Oie")

print("listOfContents = ")
print(listOfContents)

lFilesAndTitles = []

for index, f in enumerate (lfiles):
    print ("Changing %s file." % (f))
    ifile = open(sdirname + f + ".html", "r")
    ofile = open(dest_dirname + f +".html", "w")

    text = ifile.read()

    ##############################################
    # head
    ##############################################

    #replace meta charset
    text = text.replace("iso-8859-1","utf-8")

    #include in head
    hfaux = open("../livro_head.aux", "r")
    head_include = hfaux.read()
    hfaux.close()
    
    # #include head
    # headname = "top.aux"
    
    # head_aux_file = open(headname, "r")
    # head_include = head_aux_file.read()
    
    #get chapterHead or sectionHead to include in <meta> keywords
    s=-1
    e=-1
    title = []
    #partHead
    s = text.find('<h1 class="partHead">')
    if (s != -1):
        auxText = text[s:]
        s = auxText.find('</a>')+4
        e = auxText.index('</h1>')
        kw = auxText[s:e]
        title = kw
    else:
        #chapterHead
        s = text.find('<h2 class="chapterHead">')
        if (s != -1):
            auxText = text[s:]
            s = auxText.find('</a>')+4
            e = auxText.index('</h2>')        
            kw = auxText[s:e]
            title = kw
        else:
            #likechapterHead
            s = text.find('<h2 class="likechapterHead">')
            if (s != -1):
                auxText = text[s:]
                s = auxText.find('</a>')+4
                e = auxText.index('</h2>')
                kw = auxText[s:e]
                title = kw
            else:
                #appendixHead
                s = text.find('<h2 class="appendixHead">')
                if (s != -1):
                    auxText = text[s:]
                    s = auxText.find('</a>')+4
                    e = auxText.index('</h2>')
                    kw = auxText[s:e]
                    title = kw
                else:
                    #sectionHead
                    s = text.find('<h3 class="sectionHead">')
                    if (s != -1):
                        auxText = text[s:]
                        s = auxText.find('</a>')+4
                        e = auxText.index('</h3>')
                        kw = auxText[s:e]
                        title = kw
                        #subsectionHead
                        s=-1
                        e=-1
                        s = auxText.find('<h4 class="subsectionHead">')
                        while (s != -1):
                            auxText = auxText[s:]
                            s = auxText.find('</a>')+4
                            e = auxText.index('</h4>')
                            kw += ", " + auxText[s:e]
                            s = auxText.find('<h4 class="subsectionHead">',e)
                    else:
                        kw = []

    head1 = "<meta name='keywords' content='"
    head1 += "Livro, Pré-calculo"
    if (len(kw) != 0):
        head1 += ", " + kw
    head1 += "'>\n"
    
    head_include = head1 + head_include + "\n";

    text = text.replace("</head>", head_include)

    ##############################################
    # body
    ##############################################

    tbfaux = open("topBody.aux", "r")
    body_include = tbfaux.read()
    tbfaux.close()

    text = text.replace("<body \n>", body_include)

    #book title
    text = text.replace("+++tituloDoLivro+++","Pré-calculo - Um Livro Colaborativo")

    #hrule abaixo de h3, h4
    if ((f[0:6] == "mainse") or (f[0:6] == "mainli") or (f[0:6] == "mainch")):
        text = text.replace("</h2>",'</h2><hr class="section">')
        text = text.replace("</h3>",'</h3><hr class="section">')
        text = text.replace("</h4>",'</h4><hr class="section">')
        text = text.replace("</h5>",'</h5><hr class="section">')

    #include on bottom
    bottom_aux_file = open("../livro_bottom.aux", "r")
    bottom_include = bottom_aux_file.read()
    bottom_aux_file.close()
    
    text = text.replace("</body></html>", bottom_include)

    #remove original crosslinks
    #top crosslinks
    s = text.find('<div class="crosslinks">')
    if (s != -1):
        auxText = text[s:]
        e = s + auxText.index('</div>') + 6
        text = text.replace(text[s:e], "")
    #bottom crosslinks
    s = text.find('<div class="crosslinks">')
    if (s != -1):
        auxText = text[s:]
        e = s + auxText.index('</div>') + 6
        text = text.replace(text[s:e], "")

    #configure navigation links
    if ((f[0:6] == "mainch") or (f[0:6] == "mainse") or
        (f[0:6] == "mainli") or (f[0:6] == "mainap") or
        (f[0:6] == "mainpa")):

        #find file at listOfContents
        pos = -1
        for i, content in enumerate(listOfContents):
            if (content[0] == f):
                pos = i
                break
        if (pos == -1):
            print("file %s not found in listOfContents" % f)
            raise
        if (pos == 0):
            text = text.replace('#Previous#',('%s' % "main.html"))
        else:
            text = text.replace('#Previous#',('%s' % listOfContents[pos-1][1]))

        text = text.replace('#TableOfContents#',('main.html#%s.html' %f))
        if (pos == len(listOfContents)-1):
            text = text.replace('<span class="glyphicon glyphicon-menu-right">', "")
        else:
            text = text.replace('#Next#',('%s' % listOfContents[pos+1][1]))
    else:
        text = text.replace('<span class="glyphicon glyphicon-menu-left">', "")
        text = text.replace('<span class="glyphicon glyphicon-menu-hamburger">', "")
        text = text.replace('<span class="glyphicon glyphicon-menu-right">', "")


    #global alert
    ifalert = open("../globalAlert.aux","r")
    globalAlert = ifalert.read()
    ifalert.close()
    text = text.replace("+++alertaGeral+++",globalAlert)

    #nabar - REAMAT - list of hotsites
    text = text.replace("+++listaDeHotsites+++",lisths)

    #sectionTOCS title
    if (f[0:6] == "mainch"):
        rep = '<div class="sectionTOCS">'
        rep += '<h3 class="sectionHead">Sumário</h3><hr class="section">'
        text = text.replace('<div class="sectionTOCS">', rep)

    #invitations
    sfinvite = open("../emConstrucao.aux", "r")
    inviteText = sfinvite.read()
    sfinvite.close()
    text = text.replace("+++emConstrucao+++",inviteText)

    sfinvite = open("../foraDoEstilo.aux", "r")
    inviteText = sfinvite.read()
    sfinvite.close()
    text = text.replace("+++foraDoEstilo+++",inviteText)

    sfinvite = open("../construirSec.aux", "r")
    inviteText = sfinvite.read()
    sfinvite.close()
    text = text.replace("+++construirSec+++",inviteText)

    sfinvite = open("../construirExeresol.aux", "r")
    inviteText = sfinvite.read()
    sfinvite.close()
    text = text.replace("+++construirExeresol+++",inviteText)

    sfinvite = open("../construirResol.aux", "r")
    inviteText = sfinvite.read()
    sfinvite.close()
    text = text.replace("+++construirResol+++",inviteText)

    sfinvite = open("../construirExer.aux", "r")
    inviteText = sfinvite.read()
    sfinvite.close()
    text = text.replace("+++construirExer+++",inviteText)

    sfinvite = open("../construirResp.aux", "r")
    inviteText = sfinvite.read()
    sfinvite.close()
    text = text.replace("+++construirResp+++",inviteText)


    #edit on GitHub
    s = text.find("#srcPath:")
    if (s!=-1):
        auxText = text[s+9:]
        e = auxText.find("#")
        auxText = text[s+9:s+9+e]
        text = text.replace("+++paginaNoGitHub+++",
                            "https://github.com/reamat/PreCalculo/blob/master/"+auxText)
        s = text.find("#srcPath:")
        auxText = text[s+9:]
        e = auxText.find("#")
        auxText = text[s:s+9+e+1]
        text = text.replace(auxText,"")
    else:
        text = text.replace("+++paginaNoGitHub+++",
                            "https://github.com/reamat/PreCalculo")


    #collapse demo's
    lbc = [] #list of collapses buttoms
    s = text.find("<!--prova begin-->")
    count = 0
    while (s != -1):
        count += 1
        sub =  '<div class="container-fluid">\n'
        sub += '<button type="button" class="btn btn-info" data-toggle="collapse" data-target="#demo'
        sub += str(count) + '">Demonstração</button>\n'
        sub += '<div id="demo' + str(count) + '" class="collapse out">\n'

        lbc.append("demo"+str(count))
        
        text = text.replace("<!--prova begin-->",sub,1)
        text = text.replace("<!--prova end-->",'</div></div>',1)
        s = text.find("<!--prova begin-->")

    #collapse resp's
    s = text.find("<!--resp begin-->")
    count = 0
    while (s != -1):
        count += 1
        sub =  '<div class="container-fluid">\n'
        sub += '<button type="button" class="btn btn-info" data-toggle="collapse" data-target="#resp'
        sub += str(count) + '">Resposta</button>\n'
        sub += '<div id="resp' + str(count) + '" class="collapse out">\n'

        lbc.append("resp"+str(count))

        text = text.replace("<!--resp begin-->",sub,1)
        text = text.replace("<!--resp end-->",'</div></div>',1)
        s = text.find("<!--resp begin-->")

    #collapse resol's
    s = text.find("<!--resol begin-->")
    count = 0
    while (s != -1):
        count += 1
        sub =  '<div class="container-fluid">\n'
        sub += '<button type="button" class="btn btn-info" data-toggle="collapse" data-target="#resol'
        sub += str(count) + '">Solução</button>\n'
        sub += '<div id="resol' + str(count) + '" class="collapse out">\n'

        lbc.append("resol"+str(count))

        text = text.replace("<!--resol begin-->",sub,1)
        text = text.replace("<!--resol end-->",'</div></div>',1)
        s = text.find("<!--resol begin-->")

    #change title
    if (len(title) != 0):
        s = -1
        e = -1
        s = text.index('<title>')+7
        e = text.index('</title>')
        text = text.replace(text[s:e], title)

        auxName = text_to_id(title)
        auxName = urllib.parse.quote(auxName)
        lFilesAndTitles.append((f,auxName))

    #fixing the MathJax
    #remove mathsize="big"
    text = text.replace('mathsize="big"','mathsize="normal"')

    #rescale Math's to fit window.innerWidth
    for i, bid in enumerate(lbc):
        sub = '<script> $(function(){$("#' + bid + '").on("shown.bs.collapse", function () {var math = document.getElementsByClassName("MathJax_SVG"); var arrayLength = math.length; for (var i = 0; i < arrayLength; i++) { math[i].style.display = "inline"; var w = math[i].offsetWidth; math[i].style.display = ""; if (w > window.innerWidth) { math[i].style.fontSize = Math.floor((window.innerWidth-75)/w * 100) + "%";} MathJax.Hub.Queue(["Rerender",MathJax.Hub,math[i]]); } });}); </script>'
        sub += "</body>" + "\n"

        text = text.replace("</body>", sub)

    #set version change
    text = text.replace("+++urlsumario+++","../livro/main.html")
    text = text.replace("+++urlpdf+++","../livro/livro.pdf")

    #add update date and time
    data = datetime.datetime.now()
    text = text.replace("+++atualizadoem+++",
            'Página gerada em ' +
            str(data.day) + '/' + str(data.month) + '/' + str(data.year) +
            ' às ' + str(data.hour) + ':' + str(data.minute) +
            ':' + str(data.second) +
            '.')


    ofile.write(text)
    ifile.close ()
    ofile.close ()

#change main.css
ifile = open(dest_dirname + "main.css",'r')
bookfile = open("../livro_aux.css",'r')
ofile = open(dest_dirname + "livro.css",'w')

for line in ifile:
    ofile.write (line)

for line in bookfile:
    ofile.write (line)

ifile.close ()
bookfile.close ()
ofile.close ()

os.system('mv '+dest_dirname+'livro.css '+dest_dirname+'main.css ')


print(lFilesAndTitles)


#replace url by titles
chapName = []
currentChap = -1
for i, content in enumerate(listOfContents):
    if ((content[0][0:6] == "mainli") or
        (content[0][0:6] == "mainch") or
        (content[0][0:6] == "mainap")):
        currentChap += 1
        s = [x[0] for x in lFilesAndTitles].index(content[0])
        chap_aux = text_to_initials(lFilesAndTitles[s][1])
        count = 0
        for c in chapName:
            if (c[0:len(chap_aux)] == chap_aux):
                count += 1
        if (count > 0):
            chapName.append(chap_aux+str(count))
        else:
            chapName.append(chap_aux)

        s = [x[0] for x in lFilesAndTitles].index(content[0])
        lFilesAndTitles[s] = (lFilesAndTitles[s][0],chapName[currentChap])
    else:
        s = [x[0] for x in lFilesAndTitles].index(content[0])
        lFilesAndTitles[s] = (lFilesAndTitles[s][0], chapName[currentChap] + "-" + lFilesAndTitles[s][1])
        
print("New lFilesAndTitles =")
print(lFilesAndTitles)

sdirname = dest_dirname
lfiles = []
for (dirpath, dirnames, filenames) in walk (sdirname):
    lfiles.extend (filenames)
    break

for index, f in enumerate (lfiles):
    if (os.path.splitext(f)[1] == ".html"):
        file = open(dest_dirname + f, 'r')
        text = file.read()
        file.close()

        for i, ft in enumerate(lFilesAndTitles):
            text = text.replace(ft[0]+".html", ft[1]+".html")
        file = open(dest_dirname + f, 'w')
        file.write(text)
        file.close()

        fn = os.path.splitext(f)[0]
        ii = -1
        try:
            ii = [y[0] for y in lFilesAndTitles].index(fn)
        except:
            pass
        if (ii != -1):
            print('mv %s/%s %s/%s%s' % (dest_dirname, f, dest_dirname, lFilesAndTitles[ii][1], ".html"))
            os.system('mv %s/%s %s/%s%s' % (dest_dirname, f, dest_dirname, lFilesAndTitles[ii][1], ".html"))
