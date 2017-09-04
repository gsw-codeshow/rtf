#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import time
import string
import codecs
import re

class RTF():
    
    # we must recieve a file_name as parameter to determine which file will be parsed
    def __init__(self, file_name):
        self.rawList = [""]
        self.file_name = file_name
        self.codepage = "gbk"
        self.text = ""
        # the first char of a rtf file is always '{'
        self.isReadControlWord = True 
        self.groupId = 0

    def PlainText(self):
        file = open(self.file_name)
        readFlag = True

        while readFlag:
            char = file.read(1)
            otherStr = char
            if not char:
                readFlag = False
                break         
            if self.isReadControlWord:
                if "{" == char:
                    self.rawList.append("{")
                    self.groupId += 1
                    continue
                if "}" == char:
                    self.parseGroup()
                    continue
                if "\\" == char:
                    self.isReadControlWord = False
            while readFlag:
                otherWord = file.read(1)
                if not otherWord:
                    readFlag = False
                    break
                if  "\'" == otherWord or otherWord.isalnum() or otherWord.isalpha() or otherWord.isdigit():
                    otherStr += otherWord
                    continue
                if " " == otherWord:
                    otherStr += otherWord
                    break
                file.seek(file.tell() - 1)
                break
            self.isReadControlWord = True
            self.rawListAppend(otherStr)
        file.close()
        return self.text

    def parseGroup(self):
        listPos = len(self.rawList) - 1
        while listPos != 0:
            if "{" == self.rawList[listPos]:
                break
            listPos -= 1
        groupList = self.rawList[listPos+1:]
        self.rawList = self.rawList[:listPos]
        if 1 == self.groupId:
            for groupItem in groupList:
                if bool(re.search(r"^\\[a-zA-Z]+\d*\s?$",groupItem)):
                    # we will check control words later
                    # for example: codepage control words can't be ignored
                    pass
                elif 2 < len(groupItem) and "\\'" == groupItem[:2]:
                    # this is a chain of encoded  hex string
                    # we will convert them to a unicode string according to self.codepage
                    groupItem = groupItem.replace("\\'", "")
                    hexGroupItem = codecs.decode(groupItem, "hex_codec")
                    groupItemStr = hexGroupItem.decode(self.codepage)
                    self.text += groupItemStr
                else:
                    self.text += groupItem
        self.groupId -= 1
        return

    def rawListAppend(self, word):
        top = self.rawList[-1]
        if "\\'" == top[:2] and "\\'" == word[:2]:
            self.rawList[-1] = top + word
        else:
            self.rawList.append(word)

if __name__ == "__main__":
    rtf_object = RTF(os.path.abspath("sample/text1.rtf"))
    print(rtf_object.PlainText())
