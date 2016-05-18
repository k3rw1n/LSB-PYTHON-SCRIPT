# coding=utf-8
#!usr/bin/env python
import time

class HideException(Exception):
    pass


class UsageException(HideException):

    def __str__(self):
        return self.message


def bin(s):
    return str(s) if s <= 1 else bin(s >> 1) + str(s & 1)


def byte2bin(bytes):
    for b in bytes:
        yield bin(ord(b)).zfill(8)
marker = 'iddqd'


def hide(bmp_filename, src_filename):
    src = open(src_filename, 'rb')
    secret = marker + src_filename + marker + src.read() + marker
    src.close()
    bmp = open(bmp_filename, 'rb+')
    bmp.seek(55)
    container = bmp.read()
    need = 8 * len(secret) - len(container)
    if need > 0:
        raise HideException(u'BMP 大小不足以隐藏该文件\n需要另外 %s byte.' % need)
    cbits = byte2bin(container)
    encrypted = []
    for sbits in byte2bin(secret):
        for bit in sbits:
            bits = cbits.next()
            bits = bits[:-1] + bit
            b = chr(int(bits, 2))
            encrypted.append(b)

    bmp.seek(55)
    bmp.write(''.join(encrypted))
    bmp.close()

def hidechar(bmp_filename, src_char):
    secret = marker + src_char + marker
    bmp = open(bmp_filename, 'rb+')
    bmp.seek(55)
    container = bmp.read()
    need = 8 * len(secret) - len(container)
    if need > 0:
        raise HideException(u'BMP 大小不足以隐藏该文件\n需要另外 %s byte.' % need)
    cbits = byte2bin(container)
    encrypted = []
    for sbits in byte2bin(secret):
        for bit in sbits:
            bits = cbits.next()
            bits = bits[:-1] + bit
            b = chr(int(bits, 2))
            encrypted.append(b)

    bmp.seek(55)
    bmp.write(''.join(encrypted))
    bmp.close()

def decrypt_char(container):
    sbits = ''
    for cbits in byte2bin(container):
        sbits += cbits[-1]
        if len(sbits) == 8:
            yield chr(int(sbits, 2))
            sbits = ''


def extract(bmp_filename):
    bmp = open(bmp_filename, 'rb')
    bmp.seek(55)
    container = bmp.read()
    bmp.close()

    decrypted = []
    for b in decrypt_char(container):
        decrypted.append(b)
        if (len(marker) == len(decrypted) and
                marker != ''.join(decrypted)):
            raise ExtractException(u"该BMP中不存在文件")
    if len(decrypted) > len(marker):
        decrypted = ''.join(decrypted).split(marker)
        src_filename = decrypted[1]
        src_data = decrypted[2]
        src = open(src_filename, 'wb')
        src.write(src_data)
        src.close()

def extract_char(bmp_filename):
    bmp = open(bmp_filename, 'rb')
    bmp.seek(55)
    container = bmp.read()
    bmp.close()

    decrypted = []
    for b in decrypt_char(container):
        decrypted.append(b)
        if (len(marker) == len(decrypted) and
                marker != ''.join(decrypted)):
            raise ExtractException(u"该BMP中不存在文件")
    if len(decrypted) > len(marker):
        decrypted = ''.join(decrypted).split(marker)
        # src_filename = decrypted[1]
        # src_data = decrypted[2]
        print decrypted



def main():
    print u"请选择需要进行数据隐藏的类型:"
    print u"1.LSB图像隐藏文字"
    print u"2.LSB图像隐藏文件"
    print u"3.LSB图像隐藏文字提取"
    print u"4.LSB图像隐藏文件提取"
    choice = raw_input("> ")

    if not choice.isdigit():
        exit(u"[-] 请正确输入您的选择")
    if choice == '1':
        print u"[+] 请输入原图像文件名："
        image = raw_input('1.> ')
        print u"[+] 请输入需要隐藏的文字"
        content = raw_input('1.> ')
        try:
            hidechar(image, content)
        except Exception, e:
            print '[-] ', e
        print u"[+] 信息隐藏成功"
    
    elif choice == '2':
        print u"[+] 请输入原文件名："
        image = raw_input('2.> ')
        if image[-3:].lower() != 'bmp':
            exit(u"[-] 请重新输入一个BMP文件")
        print u"[+] 请输入需要隐藏的文件名"
        content = raw_input('2.> ')
        try:
            hide(image, content)
        except Exception, e:
            print '[-] ', e
        print u"[+] 信息隐藏成功"
    elif choice == '3':
        print u"[+] 请输入添加数据后的图像名："
        files = raw_input('3.> ')
        print u"[+] 正在提取中.",
        for i in range(10):
            time.sleep(0.3)
            print ".",
        print
        try:
            extract_char(files)
        except Exception,e:
            print e            
        print u"[+] 信息提取成功"
    elif choice == '4':
        print u"[+] 请输入添加数据后的BMP文件名："
        files = raw_input('4.> ')
        if files[-3:].lower() != 'bmp':
            exit(u"[-] 请重新输入一个BMP文件")
        print u"[+] 正在提取中.",
        for i in range(10):
            time.sleep(0.3)
            print ".",
        try:
            extract_char(files)
        except Exception, e:
            print e
        print u"[+] 信息提取成功"


if __name__ == "__main__":
    main()
