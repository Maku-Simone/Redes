from appJar import gui
import RRDFile as rrd
from PIL import Image, ImageTk
from PDFManager import createPDFFile as PDF
import Constants as C


def press(btn):
    print("Monitorizando " + btn + " IP: " + app.getEntry("IP") + " CN: " + app.getEntry(
        "Comunidad") + " Puerto: " + app.getEntry("Puerto"))
    createDataUI(app.getEntry("Comunidad"), app.getEntry("IP"), app.getEntry("Puerto"))
    return


def createUIMain():
    app.addLabel("Dirección de host: ")
    app.addEntry("IP")

    app.addLabel("Nombre de comunidad: ")
    app.addEntry("Comunidad")

    app.addLabel("Puerto: ")
    app.addEntry("Puerto")
    app.setEntryDefault("Puerto", "161")

    app.addButton("Monitorizar", press)

    app.go()
    return


def createDataUI(comunidad, host, puerto):
    createRRDFiles()
    updateRRDFiles(comunidad, host, puerto)
    graphRRDFiles(0)
    showImageUI()
    cycleData(comunidad, host, puerto, 1)
    return


def cycleData(comunidad, host, puerto, i):
    updateRRDFiles(comunidad, host, puerto)
    graphRRDFiles(i)
    updateImages()
    PDF(puerto, comunidad, host)
    cycleData(comunidad, host, puerto, i+1)
    return


def createRRDFiles():
    rrd.createRRDTOOL(C.RAM_RRD_FILENAME, 'N', '10')
    rrd.createRRDTOOL(C.CPU_RRD_FILENAME, 'N', '10')
    rrd.createRRDTOOL(C.HDD_RRD_FILENAME, 'N', '10')
    return


def updateRRDFiles(comunidad, host, puerto):
    rrd.updateRRD(C.RAM_NAME, comunidad, host, C.RAM_OID, puerto)
    rrd.updateRRD(C.CPU_NAME, comunidad, host, C.CPU_OID, puerto)
    rrd.updateRRD(C.HDD_NAME, comunidad, host, C.HDD_OID, puerto)
    return


def graphRRDFiles(i):
    rrd.graficarRRD(C.RAM_NAME, i)
    rrd.graficarRRD(C.CPU_NAME, i)
    rrd.graficarRRD(C.HDD_NAME, i)
    return


def showImageUI():
    app.removeAllWidgets()

    app.setSize("500x800")

    app.addImageData("CPU", cpuphoto, fmt="PhotoImage")

    app.addImageData("RAM", ramphoto, fmt="PhotoImage")

    app.addImageData("HDD", hddphoto, fmt="PhotoImage")

    return


def updateImages():
    app.reloadImage("RAM", "images/RAM.png")
    app.reloadImage("CPU", "images/CPU.png")
    app.reloadImage("HDD", "images/HDD.png")
    print("Updating")
    return


app = gui("Administración y Monitoreo de Redes", "378x264")

cpuphoto = ImageTk.PhotoImage(Image.open("images/CPU.png"))
ramphoto = ImageTk.PhotoImage(Image.open("images/RAM.png"))
hddphoto = ImageTk.PhotoImage(Image.open("images/HDD.png"))
createUIMain()
