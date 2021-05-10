# PythonGIT
Repositorio con archivos de ejemplo .CSV y script de consola para su tratamiento.

El script consta de un menú con 2 opciones:
1.Búsqueda
2.Inserción o edición

El apartado de búsqueda realiza una búsqueda en todos los archivos en los que se encuentre el script para encontrar un 'productID' solicitado. Si no existe se emite un mensaje de que no existe

El aparatado de Inserción o edición se realiza solo sobre una serie de archivos, si se quiere se puede ampliar a más. 
Cada archivo tiene su propia clase y métodos para leer, buscar y escribir uno o varios registros en el .csv

La clase padre es Fichero, que contiene 2 métodos, leer y escribir.
Las clases hijas, tienen sus propios métodos de búsqueda e inserción ya que cada .csv puede tener una estructura diferente.

Se indican ejemplos de como se estructura cada línea del registro y donde se modifican los datos.

El objetivo final es obtener los ficheros modificados insertando sus registros nuevos por debajo de los ya existentes en el orden en que existen en el fichero.
