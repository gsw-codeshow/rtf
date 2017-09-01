#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import time
import string
import codecs
import re

class RTF():
    codepage = "gbk"
    text = ""
    isReadControlWord = True
    groupId = 0
    # fileName must refer to an RTF file.
    # Input is not validated.
    @staticmethod
    def toPlainText(self, fileName):
        file = open(fileName)
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
        print (self.text)
        file.close()
        return self.text

    def isKey(self, item):
        return bool(re.search(r"^\\[a-zA-Z]+\d*\s?$",item))

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
                if self.isKey(groupItem):
                    continue
                if 2 < len(groupItem) and "\\'" == groupItem[:2]:
                    groupItem = groupItem.replace("\\'", "")
                    hexGroupItem = codecs.decode(groupItem, "hex_codec")
                    groupItemStr = hexGroupItem.decode("gbk")
                    self.text += groupItemStr
                    continue
                self.text += groupItem

        self.groupId -= 1
        return

    def rawListAppend(self, word):
        top = self.rawList[-1]
        if "\\'" == top[:2] and "\\'" == word[:2]:
            self.rawList[-1] = top + word
        else:
            self.rawList.append(word)

    def __init__(self, fileName):
        self.rawList = [""]
        self.fileName = fileName

    def plainText(self):
        return self.toPlainText(self, self.fileName)

    def toTXT(self, fileName):
        try:
            file = open(fileName, "w+")
            file.write(self.plainText())
            file.close()
            return True
        except:
            return False

def main():
    RTF(".\\sample\\text1.rtf").plainText()

main()
