# -*- coding: utf-8 -*-
import os
import arcpy
import xlsxwriter
import pythonaddins

arcpy.env.overwriteOutput = True



class AptiTool(object):
    """Implementation for Upra_add_ins_addin.tool (Tool)"""
    def __init__(self): ###función para obtener coordenadas con un click del mouse
        self.enabled = True
        self.varpath = r''
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.x = 0
        self.y = 0

    def get_geodatabase_path(self, input_table):  ### Una función para obtener una ruta de geodatabase desde la clase de entidad o tabla
        '''Return the Geodatabase path from the input table or feature class.
        :param input_table: path to the input table or feature class
        '''
#       workspace = os.path.dirname(input_table)
        workspace = input_table
        if not [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
            return workspace
        else:
           return os.path.dirname(workspace)

        print "no hay capa"

    def onMouseDown(self, x, y, button, shift):
        pass

    def onMouseDownMap(self, x, y, button, shift):
        if pythonaddins.GetSelectedTOCLayerOrDataFrame() is not None:
            Listvars.items = []
            a = pythonaddins.GetSelectedTOCLayerOrDataFrame() ###Muestra la capa o el marco de datos seleccionado en la tabla de contenidos.
            gdbpath = self.get_geodatabase_path(a.workspacePath) ###obtiene el path de los datos seleccionados del TOC
    #       message = "Your mouse clicked \n longitud: " + str(x) + ", \n Latitud: " + str(y) + "\n And your selected \\
    #       layer is: " + a.name + "\n Located in gdb: " + a.workspacePath + "\n And GDB PATH is: " + gdbpath
    #       pythonaddins.MessageBox(message, "My Coordinates")
            varpath = gdbpath + r'\1_VARIABLES.gdb' ####path de las variables que se compone de del path de la capa seleccionada y la gdb "1_VARIABLES.gdb"
            listFC = [] ###instanciando la lista de los featureclass
            dts = [] ### instanciar lista de las rutas de los feature class contenidos en un dataset
            ft = [] #instanciamos la lista de los featureclass que estan contenidos dentro de un dataset
            ruta, nombre_gdb=os.path.split(a.workspacePath) ###Se hace un split para obtener la ruta y el nombre de la gdb de la capa seleccionada en el TOC
            if os.path.exists(varpath):####Si el path existe retorna True
                # pythonaddins.MessageBox(varpath, "GDB for Variables")
                arcpy.env.workspace = r''+varpath
                print arcpy.env.workspace ####Imprime el workspace (cuando se ejecuta el AddIn, es útil porque con este mensaje sabemos si esta tomando la ruta correcta)
                listFC = arcpy.ListFeatureClasses(wild_card="V_*") ####permite obtener la lista de los feature class que se encuentran en la gdb y cuyo nombre empiece por V_
                ras =  arcpy.ListRasters(wild_card="V_*") ####permite obtener la lista de los raster que se encuentran en la gdb y cuyo nombre empiece por V_
                dt = arcpy.ListDatasets() ###permite obtener la lista de los datasets

                for d in dt: # para todos los elementos del dataset,
                    ft = arcpy.ListFeatureClasses(wild_card="V*", feature_type = 'All', feature_dataset = d) ###lista de los featureclass que estan contenidos dentro de un dataset y empiezan por V
                    dta= [d + '\\' + f for f in ft] ## Obtiene la ruta para todos los featureclass que estan en el dataset
                    dts.extend(dta) ### el método extend agrega el contenido de dta (las rutas de fc ) a la lista dts
                    listFC.extend(ft) ### el método extend agrega el cotenido de ft ( variables fc que estan en un dataset) en a la lsita listFC

                listFC.extend(ras) ### el método extend agrega el cotenido de ras (variables tipo raster) en a la lsita listFC
                dts.extend(ras) ### el método extend agrega el cotenido de ras (variables tipo raster) en a la lsita dts
                # pythonaddins.MessageBox(listFC, "Variables")
                # pythonaddins.MessageBox(dts, "Variables")
                ## se elimino de la linea 63 a la linea 98 de la versio 09032018
            else:
                r =  r''+ gdbpath[0:-12] + r'\1_VARIABLES\{}'.format(nombre_gdb)
                pythonaddins.MessageBox("GDB for Variables don't exist"+r, "Error GDB is not present in route")
            Listvars.refresh()
            for layer in dts:
                Listvars.items.append(layer)
            self.x = x
            self.y = y
            tool.deactivate()
            pass
        else:
          pythonaddins.MessageBox('No tiene un criterio seleccionado!!!', "Mensaje de advertencia")

    def onMouseUp(self, x, y, button, shift):
        pass

    def onMouseUpMap(self, x, y, button, shift):
        pass

    def onMouseMove(self, x, y, button, shift):
        pass

    def onMouseMoveMap(self, x, y, button, shift):
        pass

    def onDblClick(self):
        pass

    def onKeyDown(self, keycode, shift):
        pass

    def onKeyUp(self, keycode, shift):
        pass

    def deactivate(self):
        pass

    def onCircle(self, circle_geometry):
        pass

    def onLine(self, line_geometry):
        pass

    def onRectangle(self, rectangle_geometry):
        pass


class Listvars(object):
    """Implementation for Upra_add_ins_addin.Listvars (ComboBox)"""
    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWWWWWWWWWWW'

    def getValoresVector(self,targetFeatures,joinFeatures,out_feature_class,campo):
        join_operation="JOIN_ONE_TO_ONE"
        join_type="KEEP_COMMON"
        match_option="INTERSECT"
        search_radius=""
        distance_field_name=""
        field_mapping=""
        arcpy.SpatialJoin_analysis (target_features=targetFeatures, join_features=joinFeatures, out_feature_class=out_feature_class,
        join_operation=join_operation, join_type=join_type, field_mapping=field_mapping, match_option=match_option, search_radius=search_radius, distance_field_name=distance_field_name)
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        ly=arcpy.mapping.ListLayers(mxd,arcpy.Describe(out_feature_class).name)[0]
        arcpy.mapping.RemoveLayer(df,ly)
        valor=[x[0] for x in arcpy.da.SearchCursor(out_feature_class,campo)][0]

        return valor

    def getCampoPrefijo(self, capa, prefijos):
        campos_capa_join=[campo.name for campo in arcpy.Describe(capa).fields]
        campos_join=[campo for p in prefijos  for campo in campos_capa_join if p in campo]
        return campos_join[0]

    def report(self,table):
        rows = arcpy.da.TableToNumPyArray(table,'*')
        path=pythonaddins.SaveDialog("Guardar Reporte de AptiTool","Aptitool_report.xlsx","C:")
        array = [['X','Y','Variable', 'Aptitud', 'Valor']]
        for i in range(2,len(rows[0])):
            aa=[rows[0][1][0],rows[0][1][1]]
            [aa.append(x) for x in rows[0][i].split('_')]
            array.append(aa)
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()
        col = 0
        for row, data in enumerate(array):
            worksheet.write_row(row, col, data)
        workbook.close()

    def onSelChange(self, selection):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        addLayer = arcpy.mapping.Layer(tool.varpath + selection)
        pythonaddins.MessageBox("Cargando: %s"%(tool.varpath + selection), "Carga Layer")
        arcpy.mapping.AddLayer(df, addLayer, "TOP")
        layer = arcpy.CreateFeatureclass_management(r'{0}\Users\{1}\Documents\ArcGIS\Default.gdb'.format(os.environ['systemdrive'],os.environ['username']), "data", "POINT").getOutput(0)
        fcaux = r'{0}\Users\{1}\Documents\ArcGIS\Default.gdb\data'.format(os.environ['systemdrive'],os.environ['username'])
        ras = arcpy.mapping.ListLayers(mxd, "V_*")
        ras = [ i for i in ras if i.isRasterLayer]
        names = [i.name for i in ras]
        [arcpy.AddField_management (fcaux, field_name=i.name, field_type="TEXT") for i in ras]
        vec = [ i for i in ras if not i.isRasterLayer and i.name != 'data']
        rdat = [arcpy.GetCellValue_management(i.name,"{} {}".format(tool.x,tool.y),"1").getOutput(0) for i in ras]
        fields = ["SHAPE@XY"]
        fields.extend(names)
        cursor = arcpy.da.InsertCursor(fcaux, fields)
        xy = (tool.x, tool.y)
        fields = [xy]
        fields.extend(rdat)
        cursor.insertRow(fields)
        vect = arcpy.mapping.ListLayers(mxd, "V_*")
        prefijos=["Des_"]
        vec = [ i for i in vect if i.isFeatureLayer and i.name != 'data']
        vector_name =[i.name for i in vec]
        [arcpy.AddField_management (fcaux, field_name=i.name, field_type="TEXT") for i in vec]
        vector_fields=[self.getCampoPrefijo(i,prefijos) for i in vec]
        valores_vector = [str(self.getValoresVector(fcaux,i,"in_memory//"+arcpy.Describe(i).name,self.getCampoPrefijo(i,prefijos)).encode('utf-8').strip()) for i in vec]
        with arcpy.da.UpdateCursor(fcaux, vector_name) as cursor:
            for fila in cursor:
                for num in xrange(len(valores_vector)):
                    expre = """fila[%s] = valores_vector[%s]"""%(str(num),str(num))
                    exec(expre)
                cursor.updateRow(fila)
        extent = arcpy.Extent(tool.x-5000, tool.y-5000, tool.x+5000, tool.y+5000)
        # tool.deactivate()
        mxd = arcpy.mapping.MapDocument("CURRENT")
        lyr=arcpy.mapping.ListLayers(mxd)
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        lyr = arcpy.mapping.ListLayers(mxd, "data", df)[0]
        arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", ' "OBJECTID" = 1 ')
        # df.zoomToSelectedFeatures()
        df.extent = extent#lyr.getSelectedExtent()
        sel = pythonaddins.MessageBox('Generar Reporte?','Reporte',4)
        if sel == 'Yes':
            self.report(fcaux)
        elif sel == 'No':
            pass
        else:
            pass

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        self.items = []
        pass


class UpdateLayers(object):
    """Implementation for Upra_add_ins_addin.UpdateLayers (Extension)"""
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self.enabled = True

    def itemAdded(self, new_item):
        pass

    def itemDeleted(self, deleted_item):
        pass
