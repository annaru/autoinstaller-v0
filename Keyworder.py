#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       autoinstaller
#
#       Copyright 2012 Anna Rudkovskaya <anuta.rudik@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#
import random
from re import sub


def KeysGenerator(self):
    ResultFiles = {'keystxt': go(self, _format=0, _name='keys.txt'),
                   'random4': go(self, _format=3, _name='random4.txt'),
                   'random8': go(self, _format=7, _name='random8.txt'),
                   'random9': go(self, _format=8, _name='random9.txt')
                   }
    if self.options.ftps != None and self.options.ftps2 == None:
        if not self.options.format12 or self.options.format12 == "0":
            ResultFiles['spam'] = go(
                self, _format=1, _name='spam_' + self.domain)
        else:
            ResultFiles['spam'] = go(
                self, _format=12, _name='spam_' + self.domain)
        ResultFiles['spam1'] = None
        ResultFiles['spam2'] = None

    elif self.options.ftps != None and self.options.ftps2 != None:
        if not self.options.format12:
            temp = go(self, _format=1, _name='spam_' + self.domain)
        else:
            temp = go(self, _format=12, _name='spam_' + self.domain)
        fh = open(temp)
        fileArray = []
        for line in fh.readlines():
            # y = [value for value in line.split()]
            y = line
            fileArray.append(y)
        fh.close()
        fileArrayPart1 = fileArray[0:len(fileArray) / 2]
        fileArrayPart2 = fileArray[len(fileArray) - (
            len(fileArray) / 2) + 1:len(fileArray)]

        f1name = '/tmp/.tmp' + str(random.randint(1, 9999))
        f2name = '/tmp/.tmp' + str(random.randint(1, 9999))

        f1 = open(f1name, 'w')
        for line in fileArrayPart1:
            f1.write(line)
        f1.close()

        f2 = open(f2name, 'w')
        for line in fileArrayPart2:
            f2.write(line)
        f2.close()

        ResultFiles['spam'] = None
        ResultFiles['spam1'] = f1name
        ResultFiles['spam2'] = f2name

    else:
        ResultFiles['spam'] = None
        ResultFiles['spam1'] = None
        ResultFiles['spam2'] = None
    return ResultFiles


def go(self, _format, _name):
    # fileForResult = '/tmp/.keys'+str(random.randint(1, 9999))
    i = 0
    if _format != 0 and _format != 1:
        enterCount = self.options.rand[_format]
        if (not enterCount or enterCount == ""
                or enterCount == None or enterCount == "0"):
            return None
        ctArr = enterCount.split("-")
        ct1 = int(ctArr[0])
        ct2 = int(ctArr[1])
        if ct1 > ct2:
            print "Вы ввели неверно. Попробуйте ещё раз."
            exit()
        # isinstance(var, int)
        ct = random.randint(ct1, ct2)

    fileForResult = '/tmp/.keys' + str(random.randint(1, 9999))
    f = open(fileForResult, 'w+')
    keys = []
    for key in open(self.workdir + '/keywords/' + self.options.kwfile, 'r'):
        keys.append(key)
    random.shuffle(keys)
    for key in keys:
        i += 1
        key = key.strip()
        subkey = sub('\ ', '-', key)
        if self.options.dodot and (_format == 3 or _format == 1 or _format == 12):
            subkey = sub('\ ', '.', key)

        _str = {
            0: subkey + "\n",
            #$str = $key.' http://'.str_replace(" ","-",$key).'.'.$domain."\n";
            1: key + " http://" + subkey + '.' + self.domain + "\n",
            12: key + " http://" + subkey + '.' + self.domain,
            3: '<a href="http://' + subkey + '.' + self.domain + '">' + key + '</a>',
            7: key,
            8: '<a href="/' + subkey + '">' + key + '</a>',
        }
        strForWrite = _str[_format]

        if _format == 3 or _format == 8:
            if i < ct:
                f.write(strForWrite + ' | ')
            elif i == ct:
                i = 0
                ct = random.randint(ct1, ct2)
                f.write(strForWrite + "\n")
            else:
                print "error 1"
                exit(1)

        elif _format == 7:
            if i < ct:
                f.write(strForWrite + ', ')
            elif i == ct:
                i = 0
                ct = random.randint(ct1, ct2)
                f.write(strForWrite + "\n")
            else:
                print "error 1"
                exit(1)

        elif _format == 12:
            if i < ct:
                f.write(strForWrite + ' ')
            elif i == ct:
                i = 0
                ct = random.randint(ct1, ct2)
                f.write(strForWrite + "\n")
            else:
                print "error 1"
                exit(1)

        else:
            f.write(strForWrite)
    f.close()
    return fileForResult
