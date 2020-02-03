from django.shortcuts import render
from django.views.generic.edit import FormView
from conteo_palabras.forms import ContadorPalabras


def capturar_noticias(**kwargs):    
    # Ruta de los archivos
    path='../Dataset/'
    grupo_noticias = []
    palabras_noticia = dict()
    frecuencia_palabra_noticia = dict()
    
    argumentos = kwargs.get('archivos', None)
    top = kwargs.get('top', 1)
    #for i in sys.argv[2:len(sys.argv)]:     
    for i in argumentos[2:len(argumentos)]:     
        total_palabras = 0
        with open(path + i, 'rb') as f:
            s = BeautifulSoup(f, 'html.parser')
            palabras = []
            for j in s.find_all('body'):
                total_palabras += len(contar_palabras(j.text))
                palabras.append(j.text)
                grupo_noticias.append(j.text)
            palabras_noticia.update({i:len(contar_palabras(palabras))})
            frecuencia_palabra_noticia.update({i:Counter(contar_palabras(palabras))})
        f.close()

class ContadorView(FormView):
    template_name='contador_palabras.html'
    form_class = ContadorPalabras
    

    def form_valid(self, form):        
        noticias = capturar_noticias(archivos='reut2-000.sgm')
        return super().form_valid(form)
