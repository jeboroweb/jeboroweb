from calendar import HTMLCalendar
from datetime import date, timedelta 

# Create your models here.


class CalendarioPersonalizadoHTML(HTMLCalendar):

    DIAS_SEMANA = ['L', 'M', 'X', 'J', 'V', 'S', 'D']

    def __init__(self, iniciar_con_primer_progenitor="colormadre"):
        super().__init__()
        self.progenitor_actual = "colordiadecambio"
        self.vacaciones_activas = False
        self.contador_dias_madre = 0
        self.contador_dias_padre = 0
        self.aplicar_color_alterno = False
        self.fiestas_del_año = {
            "Dia del Trabajadro" : (5,1),
            "Dia del Padre" : (3,19),
            "Dia de todos los Santos" : (11,1),
            "Dia de la Comunidad" : (10,9),
        }
        
    def formatear_mes(self, anyo, mes, con_anyo=True):
        contenido = []
        agregar = contenido.append
        agregar('<table class="table table-bordered table-hover">')
        agregar(self.encabezado_dias_semana())
        semanas = self.monthdays2calendar(anyo, mes)
        es_anyo_par = anyo % 2 == 0
        clase_color = 'default'
        for semana in semanas:
            dias_semana = []
            for (dia, dia_semana) in semana:
                if dia == 0:
                    dias_semana.append('<td class="empty"></td>')
                    continue

                fecha_actual = date(anyo, mes, dia)
                """se controla el inicio de año segun sea par o impar hasta el 2do viernes"""
                if mes == 1:
                    es_anyo_par = anyo % 2 == 0
                    segundo_viernes_enero = self.obtener_segundo_viernes(anyo, 1)
                    if fecha_actual < segundo_viernes_enero and es_anyo_par:
                        """al ser año par se asigna el dia a colormadre"""
                        clase_color = 'colormadre'
                        self.progenitor_actual = clase_color                       
                        dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                        self.contador_dias(clase_color)                     
                        continue
                    #seguimos estando en fechas anteriores al segund viernes de enero
                    if fecha_actual < segundo_viernes_enero and not es_anyo_par:
                        """al ser año impar se asigna el dia a color padre"""
                        clase_color = 'colorpadre' 
                        self.progenitor_actual = clase_color                 
                        dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                        self.contador_dias(clase_color)                      
                        continue
                    #encontramos el segundo viernes de enero que será primer dia de cambio del año
                    if fecha_actual == segundo_viernes_enero:
                        dias_semana.append(self.formatear_dia(dia, dia_semana, 'colordiadecambio'))
                        self.aplicar_color_alterno = True
                        continue

                if mes == 2 or mes == 3 or mes == 4 :
                        fiestas_la_magdalena = self.calcular_fiestas_magdalena(anyo)
                        fiestas_semana_santa = self.calcular_semana_santa(anyo)
                        """para las fechas de cambio en Magdalena y Pascua aplicamos colordiadecambio"""
                        if fecha_actual == fiestas_semana_santa["Miercoles_inicio"] or fecha_actual == fiestas_semana_santa["Lunes_de_Mona"] \
                            or fecha_actual == fiestas_semana_santa["Cambio_Pascua"] or fecha_actual == fiestas_la_magdalena["Fin"] \
                                or fecha_actual == fiestas_la_magdalena["Mitad"]: 
                            dias_semana.append(self.formatear_dia(dia, dia_semana, 'colordiadecambio'))
                            # self.aplicar_color_alterno = True
                            self.contador_dias(clase_color)
                            continue

                        if fecha_actual >= fiestas_semana_santa["Jueves Santo"] and fecha_actual < fiestas_semana_santa["Cambio_Pascua"] \
                            or fecha_actual >= fiestas_la_magdalena["Inicio"] and fecha_actual < fiestas_la_magdalena["Mitad"]:
                            """entrados en las fiestas de Magdalena o Pascua, desde el inicio hasta la mitad aplicamos la norma par o impar para
                            aplicar el color que corresponda"""
                            es_anyo_par = anyo % 2 == 0
                            clase_color = 'colormadre' if es_anyo_par else 'colorpadre'
                            # self.progenitor_actual = self.cambiar_clase_color(clase_color)                       
                            dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                            self.contador_dias(clase_color)
                            continue
                        
                        if fecha_actual >= fiestas_semana_santa["Cambio_Pascua"] and fecha_actual < fiestas_semana_santa["Lunes_de_Mona"] \
                            or fecha_actual >= fiestas_la_magdalena["Mitad"] and fecha_actual < fiestas_la_magdalena["Fin"]:
                            """entrados en las fiestas de Magdalena o Pascua, desde la mitad hasta el final aplicamos la norma par o impar para
                            aplicar el color que corresponda"""
                            es_anyo_par = anyo % 2 != 0
                            clase_color = 'colormadre' if es_anyo_par else 'colorpadre'
                            # self.progenitor_actual = self.cambiar_clase_color(clase_color)                       
                            dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                            self.contador_dias(clase_color)
                            continue
                         
                if mes == 6:
                    """en junio controlamos el inicio de las vacacones de verano, que empiezan el ultimo viernes del mes"""
                    ultimo_viernes_junio = self.obtener_ultimo_viernes(anyo, 6)
                    if fecha_actual == ultimo_viernes_junio:
                        dias_semana.append(self.formatear_dia(dia, dia_semana, 'colordiadecambio'))
                        es_anyo_par = anyo % 2 == 0
                        clase_color = "colormadre" if es_anyo_par else "colorpadre"
                        self.progenitor_actual = clase_color
                        self.aplicar_color_alterno = True
                        self.contador_dias(clase_color)
                        continue
                    elif fecha_actual > ultimo_viernes_junio:
                        es_anyo_par = anyo % 2 == 0
                        clase_color = 'colormadre' if es_anyo_par else 'colorpadre'
                        dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                        self.contador_dias(clase_color)
                        continue

                if mes == 7 and (fecha_actual == date(anyo, 7, 31) or fecha_actual == date(anyo, 7, 15)) or \
                    mes == 8 and fecha_actual == date(anyo, 8, 15) or mes == 9 and \
                    fecha_actual == date(self.obtener_primer_viernes(anyo,9).year,\
                    self.obtener_primer_viernes(anyo,9).month,self.obtener_primer_viernes(anyo,9).day):  
                        dias_semana.append(self.formatear_dia(dia, dia_semana, 'colordiadecambio'))    
                        continue

                if mes == 12 and fecha_actual == self.calcular_cambio_navidad(anyo) or mes == 12 and fecha_actual == self.ultimo_viernes_lectivo_diciembre :
                    dias_semana.append(self.formatear_dia(dia, dia_semana, 'colordiadecambio'))
                    self.contador_dias(clase_color)
                    continue

                if self.es_vacaciones(anyo, mes, dia):
                    self.vacaciones_activas = True
                    if self.es_dia_cambio_especifico(mes, dia):
                        self.progenitor_actual = clase_color
                        clase_color = 'colordecambio'
                        dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                        self.contador_dias(clase_color)
                        continue
                    else:
                        """para las vacaciones de verano y navidad llamamos a la funcion para optener el progenitor (colormadre o colorpadre)"""    
                        clase_color = self.obtener_color_vacaciones(anyo, fecha_actual)
                        dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                        self.progenitor_actual = clase_color
                        self.contador_dias(clase_color)
                        continue
                else:
                    self.vacaciones_activas = False
                    """si no son vacaciones los viernes son los dias de cambio de color y lo marcamos como tal"""                                 
                    if dia_semana == 4:
                        # if self.es_dia_cambio_especifico(mes,dia):
                        #     dias_semana[3]=self.formatear_dia(dia-1,dia_semana-1,'colordecambio')                            

                        # else:                        
                        dias_semana.append(self.formatear_dia(dia, dia_semana, 'colordiadecambio'))                        
                        'despues de aplicar colordiadecambio del viernes dejamos activo aplicar_color_alterno'
                        self.aplicar_color_alterno = True
                        continue
                        """el resto de dias fuera de vacaciones o festivos hemos de controlar los cambios de color por semana"""
                    else:
                        if self.aplicar_color_alterno == False:
                            clase_color = self.progenitor_actual
                            dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                            self.aplicar_color_alterno = False
                            self.contador_dias(clase_color)
                        else:
                            clase_color = self.cambiar_clase_color(self.progenitor_actual)
                            self.progenitor_actual = clase_color
                            dias_semana.append(self.formatear_dia(dia, dia_semana, clase_color))
                            self.aplicar_color_alterno = False
                            self.contador_dias(clase_color)

            agregar(f"<tr>{''.join(dias_semana)}</tr>")
        agregar('</table>')
        return ''.join(contenido) + f'<p>P->{self.contador_dias_padre} / M->{self.contador_dias_madre}</p>'


    def cambiar_clase_color(self,clase_color):
        if clase_color == "colorpadre":
            return "colormadre"
        else:
            return "colorpadre"
       
    def encabezado_dias_semana(self):
        """Devuelve una fila con las iniciales de los días de la semana."""
        return '<tr>' + ''.join(f'<th class="text-center">{dia}</th>' for dia in self.DIAS_SEMANA) + '</tr>'
    
    def formatear_dia(self, dia, dia_semana, clase_color):
        if dia == 0:
            return '<td class="empty"></td>'  # Día vacío
        else:
            # Crear el HTML del botón con la clase de color correspondiente
            return f'<td class="text-center" ><button type="button" class="{clase_color}" onclick="">{dia}</button></td>'

    def obtener_color_vacaciones(self, anyo, fecha_actual):
        """Determina el color basado en los períodos de vacaciones (verano y Navidad) y el anyo par/impar."""
        es_anyo_par = anyo % 2 == 0
        if self.es_vacaciones_navidad(fecha_actual, anyo):
            return self.obtener_color_vacaciones_navidad(anyo, fecha_actual, es_anyo_par)
        if self.es_vacaciones_verano(fecha_actual, anyo):
            return self.obtener_color_vacaciones_verano(anyo, fecha_actual, es_anyo_par)
        return None
    
    def obtener_segundo_viernes(self, anyo, mes):
        """Devuelve el segundo viernes de un mes específico."""
        primer_viernes = self.obtener_primer_viernes(anyo, mes)
        return primer_viernes + timedelta(days=7)
    
    def obtener_primer_viernes(self, anyo, mes):
        """Devuelve el primer viernes de un mes específico."""
        primer_dia = date(anyo, mes, 1)
        while primer_dia.weekday() != 4:  # 4 representa el viernes
            primer_dia += timedelta(days=1)
        return primer_dia

    def es_vacaciones(self, anyo, mes, dia):
        """Verifica si una fecha específica está dentro de un rango de vacaciones."""
        fecha_actual = date(anyo, mes, dia)
        return self.es_vacaciones_navidad(fecha_actual, anyo) or self.es_vacaciones_verano(fecha_actual, anyo)

    def es_vacaciones_navidad(self, fecha_actual, anyo):
        """Determina si la fecha está en el período de vacaciones de Navidad."""
        self.ultimo_viernes_lectivo_diciembre (anyo)
        segundo_viernes_enero = self.obtener_segundo_viernes(anyo + 1, 1)
        return self.ultimo_viernes_lectivo_diciembre(anyo) <= fecha_actual <= segundo_viernes_enero

    def es_vacaciones_verano(self, fecha_actual, anyo):
        """Determina si la fecha está en el período de vacaciones de verano."""
        ultimo_viernes_junio = self.obtener_ultimo_viernes(anyo, 6)
        primer_viernes_septiembre = self.obtener_primer_viernes(anyo, 9)
        return ultimo_viernes_junio <= fecha_actual <= primer_viernes_septiembre

    def ultimo_viernes_lectivo_diciembre(self, anyo):
        """Devuelve el último viernes antes o igual al 21 de diciembre."""
        ultimo_dia = date(anyo, 12, 21)
        while ultimo_dia.weekday() != 4:  # 4 representa el viernes
            ultimo_dia -= timedelta(days=1)
        return ultimo_dia

    def obtener_ultimo_viernes(self, anyo, mes):
        """Devuelve el último viernes de un mes específico."""
        # Calcula el último día del mes
        ultimo_dia = (date(anyo, mes, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        while ultimo_dia.weekday() != 4:  # 4 representa el viernes
            ultimo_dia -= timedelta(days=1)
        return ultimo_dia
    
    def es_dia_cambio_especifico(self, mes, dia):
        """Verifica si el día y el mes corresponden a un día de cambio específico en verano."""
        if (mes == 7 and dia in [15, 31]) or (mes == 8 and dia == 15):
            # print(f"Día de cambio específico encontrado: {mes}/{dia}")  # Depuración
            return True
         # Verificación en el diccionario de fechas festivas
        for _, (mes_fiesta, dia_fiesta) in self.fiestas_del_año.items():
            if mes_fiesta == mes and dia_fiesta == dia:
                # Usar el año actual para verificar si es viernes
                fecha = date(date.today().year, mes, dia)
                if fecha.weekday() == 4:  # 4 es viernes
                    return True

        return False
    
    def obtener_color_vacaciones_verano(self, anyo, fecha_actual, es_anyo_par):
        """Determina el color para el período de vacaciones de verano."""
        ultimo_viernes_junio = self.obtener_ultimo_viernes(anyo, 6)
        quince_julio = date(anyo, 7, 15)
        treintauno_julio = date(anyo, 7, 31)
        quince_agosto = date(anyo, 8, 15)
        primer_viernes_septiembre = self.obtener_primer_viernes(anyo, 9)

        if ultimo_viernes_junio <= fecha_actual < quince_julio:
            return 'colormadre' if es_anyo_par else 'colorpadre'
        if quince_julio <= fecha_actual < treintauno_julio:
            return 'colorpadre' if es_anyo_par else 'colormadre'
        if treintauno_julio <= fecha_actual < quince_agosto:
            return 'colormadre' if es_anyo_par else 'colorpadre'
        if quince_agosto <= fecha_actual <= primer_viernes_septiembre:
            return 'colorpadre' if es_anyo_par else 'colormadre'
        return None
    
    def obtener_color_vacaciones_navidad(self, anyo, fecha_actual, es_anyo_par):
        """Determina el color para el período de vacaciones de Navidad."""
        self.ultimo_viernes_lectivo_diciembre (anyo)
        fin_de_anyo = date(anyo, 12, 31)
        
        # Período de vacaciones de Navidad desde el último viernes lectivo hasta el fin de anyo
        if self.ultimo_viernes_lectivo_diciembre(anyo) <= fecha_actual <= self.calcular_cambio_navidad(anyo):
            return 'colormadre' if es_anyo_par else 'colorpadre'
        elif fecha_actual > self.calcular_cambio_navidad(anyo) and fecha_actual <= fin_de_anyo:
            return  'colorpadre' if es_anyo_par else 'colormadre'

        
        segundo_viernes_enero = self.obtener_segundo_viernes(anyo + 1, 1)
        
        # Continuación de las vacaciones de Navidad hasta el segundo viernes de enero del anyo siguiente
        if date(anyo + 1, 1, 1) <= fecha_actual <= segundo_viernes_enero:
            return 'colorpadre' if es_anyo_par else 'colormadre'
        return None
    
    def calcular_pascua(self,anyo):
        # Algoritmo de Gauss para calcular el Domingo de Pascua
        a = anyo % 19
        b = anyo // 100
        c = anyo % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        mes = (h + l - 7 * m + 114) // 31
        dia = ((h + l - 7 * m + 114) % 31) + 1
       
        # Fecha del Domingo de Pascua
        domingo_pascua = date(anyo, mes, dia)
        return domingo_pascua
    
    def calcular_cambio_navidad(self, anyo):
        """Calcula la fecha en el medio entre el último viernes lectivo de diciembre y el primer viernes de enero del siguiente año."""
        ultimo_viernes_diciembre = self.ultimo_viernes_lectivo_diciembre(anyo)
        segundo_viernes_enero = self.obtener_segundo_viernes(anyo + 1, 1)
        
        # Contar la cantidad de días entre ambas fechas
        diferencia_dias = (segundo_viernes_enero - ultimo_viernes_diciembre).days
        
        # Dividir la diferencia por 2 para encontrar la fecha en el medio
        dias_medio = diferencia_dias // 2
        
        # Calcular la fecha a partir del último viernes lectivo de diciembre
        fecha_medio = ultimo_viernes_diciembre + timedelta(days=dias_medio)
        return fecha_medio

    def calcular_semana_santa(self,anyo):
        domingo_pascua = self.calcular_pascua(anyo)
        domingo_ramos = domingo_pascua - timedelta(days=7)
        viernes_santo = domingo_pascua - timedelta(days=2)
        sabado_gloria = domingo_pascua - timedelta(days=1)
        jueves_santo = domingo_pascua - timedelta(days=3)
        lunes_de_mona = jueves_santo + timedelta(days=11)
        miercoles_inicio = jueves_santo - timedelta(days=1)
        cambio_pascua = jueves_santo + timedelta(days=5)
        
        
        return {
            "Domingo de Ramos": domingo_ramos,
            "Viernes Santo": viernes_santo,
            "Sábado de Gloria": sabado_gloria,
            "Domingo de Pascua": domingo_pascua,
            "Jueves Santo": jueves_santo,
            "Lunes_de_Mona": lunes_de_mona,
            "Miercoles_inicio": miercoles_inicio,
            "Cambio_Pascua" : cambio_pascua,
        }

    def calcular_fiestas_magdalena(self, anyo):
        # Calcular el Domingo de Pascua
        domingo_pascua = self.calcular_pascua(anyo)
        # Miércoles de Ceniza (40 días antes del Domingo de Pascua)
        miercoles_ceniza = domingo_pascua - timedelta(days=53)
        # Tercer sábado de Cuaresma (tres semanas después del Miércoles de Ceniza)
        tercer_sabado_cuaresma = miercoles_ceniza + timedelta(weeks=3, days=3)
        # Fin de las fiestas (nueve días después del inicio)
        fin_fiestas_magdalena = tercer_sabado_cuaresma + timedelta(days=8)
        # Mitad de las fiestas es dia de cambio de la Magdalena
        mitad_fiestas_magdalena = fin_fiestas_magdalena - timedelta(days=4)

        return {
            "Inicio": tercer_sabado_cuaresma,
            "Fin": fin_fiestas_magdalena,
            "Mitad": mitad_fiestas_magdalena,
        }

    def contador_dias(self, clase_color):
        if clase_color == "colorpadre":
            self.contador_dias_padre += 1
            return 1
        elif clase_color == 'colormadre':
            self.contador_dias_madre += 1
            return 1
        else:
            return 0

