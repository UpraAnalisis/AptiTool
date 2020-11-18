# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# neighbors.py
# Created on: 2018-12-06 09:05:01.00000
#   (generated by ArcGIS/ModelBuilder)
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import datetime
import sys

arcpy.env.overwriteOutput = True

# Local variables:
def Reporte_neigbors(Capa_Entrada, area_no_permitida, tipo_validacion, ruta):

        ##definir listas, longitudes
    id_menores25,id_conVecinos8,id_NoAptoPermitido,id_exclusiones,id_aptitudes,campos_busqueda1,id_NoApto, id_AptoPermitdo,id_AconVecinos8= [],[],[],[],[],[],[],[],[]
    id_menores25_U,id_NoAptoPermitido_U,id_exclusiones_u,id_aptitudes_u,id_NoApto_U,id_AptoPermitdo_u,id_AconVecinos8= [],[],[],[],[],[],[]
    N_menores25,N_aptitudes,N_exclusiones,N_NoAptoPermitidos,N_NoApto,N_AptoPermitdo = [],[],[],[],[],[]

    ###Valores_gridcode
    valor_permitido = 8
    Valor_noapto = 0
    Valores_aptitud = list(set([fila[0] for fila in arcpy.da.SearchCursor(Capa_Entrada,["gridcode"])]))
    Valores_aptitud.remove(Valor_noapto)
    Valores_aptitud.remove(valor_permitido)


    ####Definir campos para procesar Polygon neighbors
    campo_oid = str([campo.name for campo in arcpy.Describe(Capa_Entrada).fields if campo.type == 'OID'][0])
    Campos_neighbors = "%s;gridcode;Shape_Area"%(campo_oid)


    # Process: Polygon Neighbors
    nombre_gdb = "pol_vecinos_%s"%(datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S"))
    nombre_gdb = nombre_gdb.replace(".","")
    gdb=arcpy.CreateFileGDB_management(ruta,nombre_gdb)
    Capa_neighbors = str(gdb)+ "\\"+ os.path.basename (Capa_Entrada) + "_Neighbor"
    Tabla_neighbors= arcpy.PolygonNeighbors_analysis(Capa_Entrada, Capa_neighbors, Campos_neighbors, "NO_AREA_OVERLAP", "BOTH_SIDES", "", "METERS", "SQUARE_METERS")


    ##Analisis de poligonos permitidos
    campos_busqueda1 = Campos_neighbors.split(";")

    campos= ["src_"+campos_busqueda1[0],"nbr_"+campos_busqueda1[0],"src_"+campos_busqueda1[1],"nbr_"+campos_busqueda1[1],"src_"+campos_busqueda1[2],"nbr_"+campos_busqueda1[2]]
    with arcpy.da.SearchCursor(Tabla_neighbors,campos) as cursor:
        for fila in cursor:
            if fila[4] < int(area_no_permitida):
                id_menores25.append(fila[0])
                if fila[2] == Valor_noapto:
                    if fila[3] == valor_permitido:
                        id_conVecinos8.append(fila[0])
                    elif fila[3] <> valor_permitido:
                        id_NoApto.append(fila[0])
                if fila[2] in Valores_aptitud:
                    if fila[3] == valor_permitido:
                        id_AconVecinos8.append(fila[0])
                    elif fila[3] <> valor_permitido:
                        id_aptitudes.append(fila[0])
                elif fila[2] == valor_permitido:
                    id_exclusiones.append(fila[0])
            else:
                pass

    [id_NoAptoPermitido.append(OID_SRC) for OID_SRC in id_conVecinos8 if id_conVecinos8.count(OID_SRC) == id_menores25.count(OID_SRC)]
    [id_AptoPermitdo.append(OID_SRC) for OID_SRC in id_AconVecinos8 if id_AconVecinos8.count(OID_SRC) == id_menores25.count(OID_SRC)]

####Eliminar duplicados en las listas
    id_NoAptoPermitido_U=list(set(id_NoAptoPermitido))
    id_menores25_U = list(set(id_menores25))
    id_exclusiones_u = list(set(id_exclusiones))
    id_aptitudes_u = list(set(id_aptitudes))
    id_NoApto_U = list(set(id_NoApto))
    id_AptoPermitdo_u = list(set(id_AptoPermitdo))

####poligonos con menos de 25 ha
    N_menores25 = len(id_menores25_U)
    N_aptitudes = len(id_aptitudes_u)
    N_AptoPermitdo  = len(id_AptoPermitdo_u)
    N_exclusiones = len(id_exclusiones_u)
    N_NoAptoPermitidos = len(id_NoAptoPermitido_U)
    N_NoApto = len(id_NoApto_U)

    campoOID = campos_busqueda1[0]


#####ESCRIBIR LAS CONSULTAS DEPENDIENDO DEL TIPO DE VALIDACIÓN
    pol_Vecinos = "Hay %s polígonos con menos de 25 Ha \n \n" %(N_menores25)

    if tipo_validacion == "TODOS":
        if N_NoAptoPermitidos == 0 and N_exclusiones == 0 and N_AptoPermitdo == 0 :
            pass
        else:
            pol_Vecinos =pol_Vecinos + "------ Polígonos con menos de 25 Ha PERMITIDOS: \n \n -----"
            if N_NoAptoPermitidos > 0:
                pol_Vecinos = pol_Vecinos + "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas NO APTAS rodeadas de EXCLUSIONES. \n  %s in %s \n \n" %(N_NoAptoPermitidos,campoOID,str(tuple(id_NoAptoPermitido_U)))
            if N_AptoPermitdo > 0:
                pol_Vecinos = pol_Vecinos + "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas APTAS,rodeadas de EXCLUSIONES.\n %s in %s \n \n" %(N_AptoPermitdo,campoOID,str(tuple(id_AptoPermitdo_u)))
            if N_exclusiones > 0:
                pol_Vecinos = pol_Vecinos + "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas de EXCLUSIONES.\n %s in %s \n \n" %(N_exclusiones,campoOID,str(tuple(id_exclusiones_u)))

        if N_aptitudes == 0 and N_NoApto ==0  :
            pass
        else:
            pol_Vecinos = pol_Vecinos + "#### Polígonos con menos de 25 Ha NO PERMITIDOS \n \n ####"
            if N_aptitudes > 0:
                pol_Vecinos = pol_Vecinos + "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas APTAS, rodeadas de polígonos diferentes a exclusiones.\n %s in %s \n \n" %(N_aptitudes,campoOID,str(tuple(id_aptitudes_u)))
            if N_NoApto > 0:
                pol_Vecinos = pol_Vecinos +  "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas NO APTAS, rodeadas de polígonos diferentes a exclusiones.\n %s in %s \n \n" %(N_NoApto,campoOID,str(tuple(id_NoApto_U)))
    elif   tipo_validacion == "PERMITIDOS":
        if N_NoAptoPermitidos == 0 and N_exclusiones == 0 and N_AptoPermitdo == 0 :
            pass
        else:
            pol_Vecinos =pol_Vecinos + "#### Polígonos con menos de 25 Ha PERMITIDOS: \n \n ####"
            if N_NoAptoPermitidos > 0:
                pol_Vecinos = pol_Vecinos + "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas NO APTAS rodeadas de EXCLUSIONES. \n  %s in %s \n \n" %(N_NoAptoPermitidos,campoOID,str(tuple(id_NoAptoPermitido_U)))
            if N_AptoPermitdo > 0:
                pol_Vecinos = pol_Vecinos + "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas APTAS,rodeadas de EXCLUSIONES.\n %s in %s \n \n" %(N_AptoPermitdo,campoOID,str(tuple(id_AptoPermitdo_u)))
            if N_exclusiones > 0:
                pol_Vecinos = pol_Vecinos + "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas de EXCLUSIONES.\n %s in %s \n \n" %(N_exclusiones,campoOID,str(tuple(id_exclusiones_u)))
    elif tipo_validacion == "NO PERMITIDOS":
        if N_aptitudes == 0 and N_NoApto ==0  :
            pass
        else:
            pol_Vecinos = pol_Vecinos + "#### Polígonos con menos de 25 Ha NO PERMITIDOS \n \n ####"
            if N_aptitudes > 0:
                pol_Vecinos = pol_Vecinos + "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas APTAS, rodeadas de polígonos diferentes a exclusiones.\n %s in %s \n \n" %(N_aptitudes,campoOID,str(tuple(id_aptitudes_u)))
            if N_NoApto > 0:
                pol_Vecinos = pol_Vecinos +  "Hay %s polígonos con menos de 25 Ha, que corresponden a áreas NO APTAS, rodeadas de polígonos diferentes a exclusiones.\n %s in %s \n \n" %(N_NoApto,campoOID,str(tuple(id_NoApto_U)))

    return pol_Vecinos



