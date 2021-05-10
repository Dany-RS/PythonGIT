import csv
from pathlib import Path

class Fichero:

    def __init__(self, fichero):
        self.fichero = fichero

    def lee_fichero(self):
        with open(self.fichero, mode='r', encoding='utf-8') as file:
            self.lector_csv = csv.reader(file, delimiter=',')
            self.datos = []
            for fila in self.lector_csv:
                self.datos.append(fila)

    def escribe_fichero(self):
        try:
            with open(self.fichero, mode='w', encoding='utf-8', newline='') as file:
                escribe_csv = csv.writer(file, delimiter=',')
                escribe_csv.writerows(self.datos)

        except Exception as err:
            print('Error al escribir fichero')
            print(err)

class ProducData(Fichero):
    #ProductData
    '''
    #Ej product_data:
    #['11700', '', 'PRODUCT', '', '', '', 'Dto cuota 50% 6m sin CP', 'Critical', 'Dto cuota 50% 6m sin CP', '', 'false', 'true', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Active', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'F2', '', '', '', '']
    '''
    reg_prodData = ['', '', 'PRODUCT', '', '', '', '', 'Critical', '', '', 'false', 'true', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', '', 'Active', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'F2', '', '', '', '']

    def __init__(self, fichero, productID, descr, ref):
        super().__init__(fichero=fichero)
        self.productID = productID
        self.descr = descr
        self.referencia = ref

    #Genera registro Product Data: inserta campos 1,7,9 ->[0,6,8]
    def generaRegistroPData(self):
        ProducData.reg_prodData[0] = self.productID
        ProducData.reg_prodData[6] = self.descr
        ProducData.reg_prodData[8] = self.descr
        self.__buscaRefPData()

    #Busca el de referencia para insertarlo a continuación
    def __buscaRefPData(self):
        for i in range(len(self.datos)):
            if self.datos[i][0] == self.referencia:
                self.__insertaDato(i)

    #función para insertar el registro en el siguiente valor del índice
    def __insertaDato(self, indice):
        self.datos.insert(indice+1, ProducData.reg_prodData)
        #print('Registro {0} insertado en posicion {1}'.format(self.productID, (indice+2)))
        self.escribe_fichero()
        print('Product Data escrito')

class Characteristics(Fichero):
    #Characteristics
    '''
    #Ej registro Characteristics completo:                    
    PRODUCT,11697,,,CHARACTERISTIC,AccionOriginal,,,,,,,F2
    PRODUCT,11697,,,CHARACTERISTIC,ListaAtributosBajaFac,,,,CODIGO BSCS,,,F2
    PRODUCT,11697,,,CHARACTERISTIC,ModuloFacturacion,,,,S,,,F2
    PRODUCT,11697,,,CHARACTERISTIC,NivelAplicacion,,,,Cuenta,,,F2  <--Esta línea solo aplica si 'Nivel Asignación' != Linea. En la excel de los datos, pestaña Definición PRomo, esta el campo.
    PRODUCT,11697,,,CHARACTERISTIC,OrdenSubTipo,,,,,,,F2
    PRODUCT,11697,,,CHARACTERISTIC,OrdenTipo,,,,,,,F2
    PRODUCT,11697,,,CHARACTERISTIC,ProductoTipo,,,,Modulo,,,F2
    PRODUCT,11697,,,CHARACTERISTIC,PromocionId,,,,4536,,,F2 <-- Aquí 4536 es la promocion de Siebel, pesaña Producto Siebel: modifica posiciones 2, 10 [1, 9]
    '''
    dicCharact = {
        'reg1': ['PRODUCT', '', '', '', 'CHARACTERISTIC', 'AccionOriginal', '', '', '', '', '', '', 'F2'],
        'reg2': ['PRODUCT', '', '', '', 'CHARACTERISTIC', 'ListaAtributosBajaFac', '', '', '', 'CODIGO BSCS', '', '', 'F2'],
        'reg3': ['PRODUCT', '', '', '', 'CHARACTERISTIC', 'ModuloFacturacion', '', '', '', 'S', '', '', 'F2'],
        'reg4': ['PRODUCT', '', '', '', 'CHARACTERISTIC', 'NivelAplicacion', '', '', '', 'Cuenta', '', '', 'F2'],
        'reg5': ['PRODUCT', '', '', '', 'CHARACTERISTIC', 'OrdenSubTipo', '', '', '', '', '', '', 'F2'],
        'reg6': ['PRODUCT', '', '', '', 'CHARACTERISTIC', 'OrdenTipo', '', '', '', '', '', '', 'F2'],
        'reg7': ['PRODUCT', '', '', '', 'CHARACTERISTIC', 'ProductoTipo', '', '', '', 'Modulo', '', '', 'F2'],
        'reg8': ['PRODUCT', '', '', '', 'CHARACTERISTIC', 'PromocionId', '', '', '', '', '', '', 'F2']
    }
    def __init__(self, fichero, productID, ref, linea, promoSiebel):
        super().__init__(fichero)
        self.productID = productID
        self.referencia = ref
        self.linea = linea
        self.promoSiebel = promoSiebel

    #Genera Registro Characteristic: informa posicion 1 (productID) y el último posicion 9 (promo Siebel)
    def generaRegistroCharact(self):
        for i in Characteristics.dicCharact:
            Characteristics.dicCharact[i][1] = self.productID
        #Especial para la fila 8 el producto siebel
        lista_8 = Characteristics.dicCharact["reg8"]
        lista_8[9] = self.promoSiebel

        self.__buscaRefPChar()

    #Función búsqueda del último registro de referencia para insertar por debajo
    def __buscaRefPChar(self):
        for i in range(len(self.datos)):
            if self.datos[i][1] == self.referencia:
                ultIndice = i  # va leyendo los que tienen la referencia y al salir del bucle, tenemos el último índice
        self.__insertaDatoCharac(ultIndice)
        self.escribe_fichero()
        print('Characteristics escrito')

    #función para insertar los registros del Characteristics
    def __insertaDatoCharac(self, indice):
        #Genero una lista Key,Value con los items del diccionario, para luego hacer bucle
        elementos = Characteristics.dicCharact.items()
        #Se insertan todos y la 4ª en función de linea =='Y'
        for key, val in elementos:
            if (key != 'reg4' or (key == 'reg4' and self.linea == 'Y')):
                indice += 1
                self.datos.insert(indice, val)

class ProductComprised(Fichero):
    #ProductComprised
    '''
    PRODUCT,11700,,,PRODUCT,Módulo Administrativo CBP,,,,,,,,100,100,,true,,F2,, <-- pos 1
    PRODUCT,10000,,,PRODUCT,11700,,,,,,,,1101077,898934,1101077,false,,F2,, <-- pos 5 y la secuencia +1,-1,+1: pos13,14,15
    '''
    dic_PrCompr = {
        'reg1': ['PRODUCT', '10000', '', '', 'PRODUCT', '', '', '', '', '', '', '', '', '', '', '', 'false', '', 'F2', '', ''],
        'reg2': ['PRODUCT', '', '', '', 'PRODUCT', 'Módulo Administrativo CBP', '', '', '', '', '', '', '', '100', '100', '', 'true', '', 'F2', '', '']
    }

    def __init__(self, fichero, productID, ref):
        super().__init__(fichero)
        self.productID = productID
        self.referencia = ref

    def generaRegistroProdCompr(self):
        #hay que buscar primero los 2 registros de este fichero, el primero nos da la secuencia de los campos 13,14,15 y necesitamos ambos índices para escribir después de cada uno
        self.__buscaRefProdCompr()
        #print(self.ind1, self.ind2)
        self.elementos = ProductComprised.dic_PrCompr.items()

        for k,v in self.elementos:
            if k == 'reg1':
                v[5] = self.productID
                v[13] = str(self.ref1)
                v[14] = str(self.ref2)
                v[15] = str(self.ref3)
            if k == 'reg2':
                v[1] = self.productID

        self.__insertaDatoProCompr()

    def __buscaRefProdCompr(self):
        self.ind1=self.ind2 = 0
        
        for i in range(len(self.datos)):
            
            if self.datos[i][5] == self.referencia:
                self.ind1 = i
                #print(i)
                #print('datos; ' , self.datos[i][13], self.datos[i][14], self.datos[i][15])
                self.ref1 = int(self.datos[i][13]) + 1
                self.ref2 = int(self.datos[i][14]) - 1
                self.ref3 = int(self.datos[i][15]) + 1
                #print('datos nuevos: ', self.ref1, self.ref2, self.ref3)
            if self.datos[i][1] == self.referencia:
                self.ind2 = i

    def __insertaDatoProCompr(self):
        for key, val in self.elementos:
            if key == 'reg1':
                self.datos.insert(self.ind1+1, val)
                self.escribe_fichero()
                print('Product Comprised reg1 escrito')
            else:
                #una vez escrito el primer registro, el segundo hay que sumar dos porque ya está el primero insertado y se mueve 1 más
                self.datos.insert(self.ind2+2, val)
                self.escribe_fichero()
                print('Product Comprised reg2 escrito')
        
class PlanFragment(Fichero):
    #ejemplo: PRODUCT,11700,,,PLANFRAGMENT,NON_EXECUTING,,,,,,,,,,,,F2 <--posicion 1
    #Este registro es común para los 4 ficheros Plan Fragment
    reg_PlanFragment = ['PRODUCT','','','','PLANFRAGMENT','NON_EXECUTING','','','','','','','','','','','','F2']

    def __init__(self, fichero, productID, ref, nombre):
        super().__init__(fichero)
        self.productID = productID
        self.referencia = ref
        self.nombre = nombre

    def generaRegPlanFragment(self):
        PlanFragment.reg_PlanFragment[1] = self.productID
        indice = self.__buscaPlanFragment()
        self.datos.insert(indice+1, PlanFragment.reg_PlanFragment)
        self.escribe_fichero()
        print('{} escrito'.format(self.nombre))

    def __buscaPlanFragment(self):
        for i in range(len(self.datos)):
            if self.datos[i][1] == self.referencia:
                return i

class Busqueda(Fichero):
    def __init__(self, fichero, productID):
        super().__init__(fichero)
        self.productID = productID

    def buscaProducID(self):
        existe = 0
        for i in range(len(self.datos)):
            existe += self.datos[i].count(self.productID)

        if (existe != 0):
            print('El producto aparece {0} veces en el fichero {1}. '.format(existe, self.fichero))
            return True
        else:
            return False

#Funciones para tratar cada fichero
def trata_Product_DATA(productID, descr, ref):
    fichero = Path('./PD.csv')
    F1 = Fichero(fichero)
    PD = ProducData(F1.fichero, productID, descr, ref)
    PD.lee_fichero()
    PD.generaRegistroPData()

def trata_Characteristic(productID, ref, linea, promoSiebel):
    fichero = Path('./Char.csv')
    F2 = Fichero(fichero)
    CH = Characteristics(F2.fichero, productID, ref, linea, promoSiebel)
    CH.lee_fichero()
    CH.generaRegistroCharact()

def trata_Pr_Comprised(productID, ref):
    fichero = Path('./PCO.csv')
    F3 = Fichero(fichero)
    PC = ProductComprised(F3.fichero, productID, ref)
    PC.lee_fichero()
    PC.generaRegistroProdCompr()

def trata_PlanFragment(productID, ref):
    dicPlanFragment = {
        'CancelPlanFragment' : Path('./PF1.csv'),
        'CeasePlanFragment'  : Path('./PF2.csv'),
        'ProvidePlanFragment': Path('./PF3.csv'),
        'UpdatePlanFragment' : Path('./PF4.csv')
    }
    #Listado de elementos del diccionario
    elemPlanFragment = dicPlanFragment.items()
    
    for nombre, fichero in elemPlanFragment:
        F = Fichero(fichero)
        PF = PlanFragment(F.fichero, productID, ref, nombre)
        PF.lee_fichero()
        PF.generaRegPlanFragment()

def buscaProducto():
    print('Indicar producto para buscar: ')
    productID = input()
    #Ubicamos los archivos, misma carpeta que script
    archivos = Path('./').glob('*.csv')
    existe = False
    for fichero in archivos:
        F = Fichero(fichero)
        Search = Busqueda(F.fichero, productID)
        Search.lee_fichero()
        #Con que exista en algún fichero ya cambia el indicador
        if (Search.buscaProducID()): existe = True
    
    if (existe == False): print('No hay registros en ningún fichero. \n')
def insertaProducto():
    '''
    Pedimos los datos para insertar registros y validamos sus entradas
    '''

    while True:
        try:
            print('Indica el ProductID nuevo: ')
            v_productID = int(input())
            if v_productID <= 0:
                print('ProductID no puede ser cero o negativo.')
                continue
        except Exception as err:
            print('Error al indicar ProductID no numérico.')
            print(err)
        #si ha ido bien sale del bucle de preguntar dejandolo como string
        else:
            v_productID = str(v_productID)
            break

    while True:
        try:
            print('Indica Descripción: ')
            v_desc = input()
            if v_desc == '' or v_desc == None:
                print('La descripción debe ir informada.')
                continue
        except Exception as err:
            print('Error grave en Descripción.')
            print(err)
        else:
            break

    while True:
        try:
            print(
                'Indica ProductID anterior ya existente (el nuevo se inserta a continuación):')
            v_referencia = int(input())
            if v_referencia <= 0:
                print('Valor de referencia no puede ser cero o negativo.')
                continue
        except Exception as err:
            print('Error al indicar Referencia, no numérico.')
            print(err)
        else:
            v_referencia = str(v_referencia)
            break

    while True:
        try:
            print('Indica si es Línea o no: (Y/N)')
            v_linea = input().upper()
            if (v_linea != 'Y' and v_linea != 'N'):
                print('Valor incorrecto, informar Y/N')
                continue
        except Exception as err:
            print('Error grave al indicar Linea.')
            print(err)
        else:
            break

    while True:
        try:
            print('Indica promocion Siebel:')
            v_promoSiebel = int(input())
            if v_promoSiebel <= 0:
                print('El valor de la promo Siebel no puede ser cero o negativo.')
                continue
        except Exception as err:
            print('Error grave al indicar promocion Siebel, no numérico.')
            print(err)
        else:
            v_promoSiebel = str(v_promoSiebel)
            break

    #print(type(v_productID), type(v_referencia),  type(v_promoSiebel))
    
    trata_Product_DATA(v_productID, v_desc, v_referencia)
    trata_Characteristic(v_productID, v_referencia, v_linea, v_promoSiebel)
    trata_Pr_Comprised(v_productID, v_referencia)
    trata_PlanFragment(v_productID, v_referencia)


'''
1. Los ficheros a tratar tienen que estar en la misma carpeta que el script
2. De momento solo está para OCAs
'''
if __name__ == '__main__':

    while True:
        print('Selecciona opcion: \n\
            1. Buscar Producto \n\
            2. Insertar Registros \n\
            3. Salir \n')
        opcion = input()

        if opcion == '1': buscaProducto()
        elif opcion == '2': insertaProducto()
        elif (opcion != '1' and opcion != '2'):break
        else:
            print(
                'Opción incorrecta, selecciona una de las opciones indicadas en el menú.')
            continue
        
    
    


