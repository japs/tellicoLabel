# bookLabelTemplates.py
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

labelTemplate = unicode('''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE document SYSTEM "rml.dtd">
<document filename="labels.pdf">

<template>
    <pageTemplate id="main">
        <pageGraphics>
        </pageGraphics>
        <frame id="first" x1=".5cm" y1=".5cm" width="20cm" height="28.7cm"/>
    </pageTemplate>
</template>

<stylesheet>
    <blockTableStyle id="btstyle">
        <blockAlignment value="LEFT" />
        <blockValign value="TOP" />
    </blockTableStyle>
    
    <paraStyle>
        <leftIndent value="10cm" />
    </paraStyle>
</stylesheet>

<story>
    <blockTable style="btstyle"
                colWidths="3cm, 0.3cm, 6.7cm, 3cm, 0.3cm, 6.7cm"
                >
        
        %s

    </blockTable>
    
</story>

</document>
''')

tdTemplate = unicode('''            <td> <image file="%(image)s" width="2.87cm" height="2.87cm"/> </td>
            <td></td>
            <td>
                <para>%(title)s</para>
                <para spaceBefore="0.35cm">%(author)s</para>
            <para>%(ID)s - %(location)s</para></td> 
''')
