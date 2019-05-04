from fpdf import FPDF
import SNMP as S
import Constants as C


def createPDFFile(port, comunityName, host):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Trabajando con el servidor ' + host + ":" + port + " - " + comunityName)
    pdf.ln()
    pdf.cell(40, 10, 'Equipo: x')
    pdf.ln()
    pdf.cell(40, 10, 'Integrantes:')
    pdf.ln()
    pdf.cell(40, 10, 'Frías Mercado Carlos Elliot')
    pdf.ln()
    pdf.cell(40, 10, '8/05/2019')
    pdf.ln()
    pdf.cell(40, 10, 'Información del equipo: ')
    pdf.ln()
    pdf.cell(40, 10, S.consultaStrSNMP(comunityName, host, C.SO_OID, port))
    pdf.ln()
    pdf.cell(40, 10, 'Número de interfaces: ' + S.consultaSNMP(comunityName, port, host, C.INTERFACE_OID))
    pdf.ln()
    timeticks = int(S.consultaSNMP(comunityName, port, host, C.LIFETIME_OID)) / 6000
    pdf.cell(40, 10, 'Tiempo de actividad: ' + str(timeticks) + " minutos")
    pdf.ln()
    addPDFImages(pdf)
    addServiceInfo(pdf)
    pdf.output("Evidencia" + ".pdf", 'F')
    return


def addPDFImages(pdf):
    pdf.cell(40, 10, "Imagen del monitoreo de " + C.RAM_NAME)
    pdf.ln()
    pdf.image("images/" + C.RAM_NAME + ".png")
    pdf.ln()

    pdf.cell(40, 10, "Imagen del monitoreo de " + C.HDD_NAME)
    pdf.ln()
    pdf.image("images/" + C.HDD_NAME + ".png")
    pdf.ln()

    pdf.cell(40, 10, "Imagen del monitoreo de " + C.CPU_NAME)
    pdf.ln()
    pdf.image("images/" + C.CPU_NAME + ".png")
    pdf.ln()
    return

def addServiceInfo(pdf):
    pdf.cell(40, 10, "Administración de Servicios")
    pdf.ln()
    pdf.cell(40, 10, "Monitoreo de FTP")
    pdf.ln()
    pdf.cell(40, 10, "Monitoreo de HTTP")
    pdf.ln()
    pdf.cell(40, 10, "Monitoreo de DNS")
    pdf.ln()
    pdf.cell(40, 10, "Monitoreo de SMTP")
    pdf.ln()
    pdf.cell(40, 10, "Monitoreo de ACEESO")
    pdf.ln()
    return