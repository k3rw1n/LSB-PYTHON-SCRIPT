# -*- coding: utf-8 -*-
from Tkinter import *
import tkFileDialog
import tkMessageBox
import base64


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
        print decrypted[0]


def main():
    root = Tk()
    root.title(u"LSB论文示例程序")

    Label(root, text=u"文件隐藏").grid(row=0, column=0, sticky=W+E, columnspan=2)
    Label(root, text=u"文字隐藏").grid(row=0, column=2, sticky=W+E, columnspan=2)
    Label(root, text=u"打开图像").grid(row=1, column=0, sticky=E)
    Label(root, text=u"打开文件").grid(row=2, column=0, sticky=E)
    Label(root, text=u"打开图像").grid(row=1, column=2, sticky=E)
    Label(root, text=u"文字内容").grid(row=2, column=2, sticky=E)

    imagename = ""
    filename = ""

    def findimage():
        global imagename
        imagename = tkFileDialog.askopenfilename()
        if imagename[-4:].lower() != '.bmp':
            imagename = ""
            tkMessageBox.showerror("message", "请输入BMP格式的图像")
            findimage()

    def findfile():
        global filename
        filename = tkFileDialog.askopenfilename()

    def hideButtonDown():
        global imagename, filename
        try:
            hide(imagename, filename)
        except Exception, e:
            print e
        tkMessageBox.showwarning("message", u"文件隐藏成功")

    def extraButtonDown():
        global imagename
        extract(imagename)
        tkMessageBox.showwarning("message", u"文件提取成功")

    def hidecharButtonDown(contentw):
        global imagename

        try:
            f = open(imagename, 'a+')
        except Exception, e:
            print '[-] ', e
        contentb = base64.standard_b64encode(contentw.get())
        f.write('\n')
        f.write(contentb)
        tkMessageBox.showwarning("message", u"信息隐藏成功")
        f.close()
        # tkMessageBox.showinfo("message",contentw.get())

    def extracharButtonDown():
        global imagename
        try:
            f = open(imagename, 'rb')
        except Exception, e:
            print e
        for line in f:
            pass
        f.close()
        contentb = line
        contentb = base64.decodestring(contentb)
        tkMessageBox.showinfo(u"隐藏的内容为", contentb)

    choseimage_B = Button(root, text=u"选择图像", command=findimage)
    choseimage_B.grid(row=1, column=1)
    chosefile_B = Button(root, text=u"选择文件", command=findfile)
    chosefile_B.grid(row=2, column=1)
    hidefile_B = Button(root, text=u"开始隐藏", command=hideButtonDown)
    hidefile_B.grid(row=3, column=0)
    extrfile_B = Button(root, text=u"开始提取", command=extraButtonDown)
    extrfile_B.grid(row=3, column=1)

    choseimage_B2 = Button(root, text=u"选择图像", command=findimage)
    choseimage_B2.grid(row=1, column=3)
    contentw = Entry(root)
    contentw.grid(row=2, column=3)

    hidefile_B2 = Button(
        root, text=u"开始隐藏", command=lambda: hidecharButtonDown(contentw))
    hidefile_B2.grid(row=3, column=2)
    extrfile_B2 = Button(root, text=u"开始提取", command=extracharButtonDown)
    extrfile_B2.grid(row=3, column=3)

    root.mainloop()


if __name__ == "__main__":
    main()
