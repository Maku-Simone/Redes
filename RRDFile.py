import Constants as C
from SNMP import *
import rrdtool


def createRRDTOOL(nombre,start,step):
    ret = rrdtool.create("files/"+nombre,"--start",start,"--step",step,"DS:"+"cosa"+":GAUGE:600:U:U","RRA:LAST:0.5:1:700")
    if ret:
        print(rrdtool.error())
    return


def updateRRD(archivo, comunidad, host, oid, puerto):
    con = 0
    while con < 5:
        input_data_snmp = int(consultaSNMP(comunidad,puerto,host,oid))
        if oid == C.RAM_OID:
            input_data_snmp = int(consultaSNMP(comunidad, puerto, host, C.TOTAL_RAM_OID)) - input_data_snmp
        valor = "N:" + str(input_data_snmp)
        rrdtool.update("files/"+archivo+".rrd", valor)
        rrdtool.dump("files/"+archivo+".rrd","files/"+archivo+".xml")
        con += 1
    return 900


def graficarRRD(nombre, i):
    tiempo_final = int(rrdtool.last("files/" + nombre + ".rrd"))
    lateral = "";
    if nombre == C.CPU_NAME:
        lateral = "--vertical-label=%"
    else:
        lateral = "--vertical-label=Bytes"
    tiempo_inicial = int(rrdtool.first("files/" + nombre + ".rrd"))
    ret = rrdtool.graphv("images/" + nombre + ".png",
                         "--start", str(tiempo_inicial + 6800),
                         "--end", str(tiempo_final),
                        lateral,
                        "DEF:"+nombre+"=files/" + nombre + ".rrd:"+"cosa"+":AVERAGE",
                        "AREA:"+nombre+"#00FF00:" + nombre)
    return
