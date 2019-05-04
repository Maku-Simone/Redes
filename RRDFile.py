import time
from SNMP import *
import rrdtool


def createRRDTOOL(nombre,start,step):
    ret = rrdtool.create("files/"+nombre,"--start",start,"--step",step,"DS:"+"cosa"+":COUNTER:600:U:U","RRA:AVERAGE:0.5:1:700")
    if ret:
        print(rrdtool.error())
    return


def updateRRD(archivo, comunidad, host, oid, puerto):
    con = 0
    while con < 10:
        input_data_snmp = int(consultaSNMP(comunidad,puerto,host,oid))
        valor = "N:" + str(input_data_snmp)
        rrdtool.update("files/"+archivo+".rrd", valor)
        # rrdtool.dump("files/"+archivo+".rrd")
        con += 1
    return 900


def graficarRRD(nombre, i):
    tiempo_final = int(rrdtool.last("files/" + nombre + ".rrd"))
    tiempo_inicial = int(rrdtool.first("files/" + nombre + ".rrd"))
    ret = rrdtool.graphv("images/" + nombre + ".png",
                         "--start", str(tiempo_inicial + 6800),
                         "--end", str(tiempo_final),
                        "--vertical-label=Bytes/s",
                        "DEF:"+nombre+"=files/" + nombre + ".rrd:"+"cosa"+":AVERAGE",
                        "AREA:"+nombre+"#00FF00:" + nombre)
    return
