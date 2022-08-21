import datetime
import requests
import os
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC, JUL
from holidays.holiday_base import HolidayBase


class HolidayEcuador(HolidayBase):
    """
    Una clase para representar un feriado en Ecuador por provincia (HolidayEcuador)
    Su objetivo es determinar si un
    fecha específica es u nas vacaciones lo más rápido y flexible posible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Hereda la clase HolidayBase)
    ----------
    prov: str
        código de provincia según ISO3166-2
    Métodos
    -------
    __init__(self, plate, fecha, tiempo, online=False):
        Construye todos los atributos necesarios para el objeto HolidayEcuador.
    _poblar(uno mismo, año):
        Devoluciones si una fecha es feriado o no
    """     
    # Códigos ISO 3166-2 para las principales subdivisiones,
    # provincias llamadas
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCES = ["EC-P"]  # TODO añadir más provincias

    def __init__(self, **kwargs):
        """
        Construye todos los atributos necesarios para el objeto HolidayEcuador
        """         
        self.country = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        """
        Comprueba si una fecha es feriado o no
        
         Parámetros
         ----------
             año: str
                 año de una fecha
         Devoluciones
         -------
             Devuelve verdadero si una fecha es un día festivo, de lo contrario, se muestra como verdadero.
        """
        # Festividades santo domingo
        self[datetime.date(year, JUL, 3)] = "Cantonalización de Santo Domingo" 
        self[datetime.date(year, NOV, 6)] = "Provincialización de Santo Domingo"

        # Festividades parroquiales 'Luz de américa'
        self[datetime.date(year, AUG, 2)] = "Fiestas patronales"

        # Día de Año Nuevo 
        self[datetime.date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        
        # Navidad
        self[datetime.date(year, DEC, 25)] = "Navidad [Christmas]"
        
        # semana Santa
        self[easter(year) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(year)] = "Día de Pascuas [Easter Day]"
        
        # Carnaval
        total_lent_days = 46
        self[easter(year) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(year) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Día laboral
        trabajo = "Día Nacional del Trabajo [Labour Day]"
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al viernes o lunes inmediato anterior
        # respectivamente
        if year > 2015 and datetime.date(year, MAY, 1).weekday() in (5,1):
            self[datetime.date(year, MAY, 1) - datetime.timedelta(days=1)] = trabajo
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio sera para el lunes siguiente
        elif year > 2015 and datetime.date(year, MAY, 1).weekday() == 6:
            self[datetime.date(year, MAY, 1) + datetime.timedelta(days=1)] = trabajo
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
        # se moverá al viernes de esa semana
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, MAY, 1) + rd(weekday=FR)] = trabajo
        else:
            self[datetime.date(year, MAY, 1)] = trabajo      
        
        # Primer Grito de Independencia, las reglas son las mismas que el día del trabajo
        grito = "Primer Grito de la Independencia [First Cry of Independence]"
        if year > 2015 and datetime.date(year, AUG, 10).weekday() in (5,1):
            self[datetime.date(year, AUG, 10)- datetime.timedelta(days=1)] = grito
        elif year > 2015 and datetime.date(year, AUG, 10).weekday() == 6:
            self[datetime.date(year, AUG, 10) + datetime.timedelta(days=1)] = grito
        elif year > 2015 and  datetime.date(year, AUG, 10).weekday() in (2,3):
            self[datetime.date(year, AUG, 10) + rd(weekday=FR)] = grito
        else:
            self[datetime.date(year, AUG, 10)] = grito       
        
        # Independencia de Guayaquil, las reglas son las mismas que el día del trabajo
        independencia = "Independencia de Guayaquil [Guayaquil's Independence]"
        if year > 2015 and datetime.date(year, OCT, 9).weekday() in (5,1):
            self[datetime.date(year, OCT, 9) - datetime.timedelta(days=1)] = independencia
        elif year > 2015 and datetime.date(year, OCT, 9).weekday() == 6:
            self[datetime.date(year, OCT, 9) + datetime.timedelta(days=1)] = independencia
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, OCT, 9) + rd(weekday=FR)] = independencia
        else:
            self[datetime.date(year, OCT, 9)] = independencia        
        
        # Día de Muertos
        fieles = "Día de los difuntos [Day of the Dead]" 
        if (datetime.date(year, NOV, 2).weekday() == 5 and  datetime.date(year, NOV, 3).weekday() == 6):
            self[datetime.date(year, NOV, 2) - datetime.timedelta(days=1)] = fieles    
        elif (datetime.date(year, NOV, 3).weekday() == 2):
            self[datetime.date(year, NOV, 2)] = fieles
        elif (datetime.date(year, NOV, 3).weekday() == 3):
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = fieles
        elif (datetime.date(year, NOV, 3).weekday() == 5):
            self[datetime.date(year, NOV, 2)] =  fieles
        elif (datetime.date(year, NOV, 3).weekday() == 0):
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = fieles
        else:
            self[datetime.date(year, NOV, 2)] = fieles
            
        # Fundación de Quito, aplica solo para la provincia de Pichincha,
        # las reglas son las mismas que el día del trabajo
        Fundacion = "Fundación de Quito [Foundation of Quito]"        
        if self.prov in ("EC-P"):
            if year > 2015 and datetime.date(year, DEC, 6).weekday() in (5,1):
                self[datetime.date(year, DEC, 6) - datetime.timedelta(days=1)] = Fundacion
            elif year > 2015 and datetime.date(year, DEC, 6).weekday() == 6:
                self[(datetime.date(year, DEC, 6).weekday()) + datetime.timedelta(days=1)] =Fundacion
            elif year > 2015 and  datetime.date(year, DEC, 6).weekday() in (2,3):
                self[datetime.date(year, DEC, 6) + rd(weekday=FR)] = Fundacion
            else:
                self[datetime.date(year, DEC, 6)] = Fundacion

class PersonaAcreditada:
    """
    La clase persona bono servirá para identificar si una persona es beneficiaria
    al bono de desarrollo humano que entrega el gobiendo nacional juntos con el 
    Ministerio de Inclusión Económica y Socia:
    http://www.ecuadorlegalonline.com/consultas/consultar-si-cobro-el-bono-de-emergencia-del-mies/
    ...

     ATRIBUTOS
     -----------
             cedula:str
                 Valor numérico que representa el la identidad ciudadana de un persona
             fecha:str
                Fecha en la que el usuario desee retirar su crédito.
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             hora: str
                 Tiempo en se permiten el servicio de la adquisición del bono
                 esta siguiendo el formato
                 HH:MM: por ejemplo, 08:35, 19:30
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos

    Methods
    -------
     __init__(self, cedula, fecha, hora, online=False):
         Este método sive para construir todo los atributos correspondientes al 
         objeto personaBono
     cedula(self):
         Obtiene el valor del atributo de cédula
     cedula(self, value):
         Establece el valor del atributo de la cédula
     fecha(self):
         Obtiene el valor del atributo de fecha
     fehca(self, value):
         Establece el valor del atributo de la fecha
     hora(self):
         Obtiene el valor del atributo de hora
     hora(self, value):
         Establece el valor del atributo de la hora
     encontrar_día(self, fecha):
         Devuelve el día a partir de la fecha: por ejemplo, Jueves
     es_tiempo_descanso(self, check_time):
         Returns True if provided time is inside the forbidden peak hours, otherwise False
     esFeriado:
         Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo
         en Ecuador, de lo contrario, False
     evaluar(self):
         Devuelve True si una persona cumple con todos los prámetros para la adquisición
         del crédito al bono de desarrollo humano.
    """ 
    # Dias de la semana
    days = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]

    # Restricciones para los día segun el ultimo dígito de la cédula.
    restrictions = {
     "LUNES": [1, 2],
     "MARTES": [3, 4],
     "MIERCOLES": [5, 6],
     "JUEVES": [7, 8],
     "VIERNES": [9, 0],
     "SABADO": [],
     "DOMINGO": []}


    def __init__(self, cedula, fecha, hora, online=False):
        """
        Construye todos los atributos necesarios para la clase..
        
         PARAMETROS
         ----------
             cedula:str
                 Valor numérico que representa el la identidad ciudadana de un persona
             fecha:str
                 Fecha en la que el usuario desee retirar su crédito.
                 Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             hora: str
                 Tiempo en se permiten el servicio de la adquisición del bono
                 esta siguiendo el formato
                 HH:MM: por ejemplo, 08:35, 19:30
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos              
        """                
        self.cedula = cedula
        self.fecha = fecha
        self.hora = hora
        self.online = online


    @property
    def cedula(self):
        """Obtiene el valor del atributo de cedula"""
        return self._cedula

    @cedula.setter
    def cedula(self, value):
        """
        Establece el valor del atributo cedula

         Parámetros
         ----------
             valor: cadena de carácteres
                 El valor del atributo cédula debe darse en forma de cadena de carácteres

        
         RETORNA
         ------
             ValorError 
                 Si la cadena de valor cédula no tiene el siguiete 
                 formato: XXXXXXXXXX.
                 Donde X son los diez numeros correspondientes a la cédula de cuidadanía
        """
        if not re.match('^[0-9]{10}$', value):
            raise ValueError(
                'La cédula debe tener el siguiente formato: XXXXXXXXXX, donde X son los diez números correspondientes a la cédula de cuidadanía')
        self._cedula = value


    @property
    def fecha(self):
        """Obtiene el valor del atributo de fecha"""
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        """
        Establece el valor del atributo de fecha

         Parámetros
         ----------
             valor: cadena de carácteres
                 El valor del atributo cédula debe darse en forma de cadena de carácteres
        
         RETORNA
         ------
             ValorError
                 Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021/04/02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y/%m/%d")
        except ValueError:
            raise ValueError('La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021/04/02)') from None
        self._fecha = value
        

    @property
    def hora(self):
        """Obtiene el valor del atributo hora"""
        return self._hora


    @hora.setter
    def hora(self, value):
        """
        Establece el valor del atributo de hora

         Parameters
         ----------
             value : str
                 Valor que permite determinar si el horario es el correcto o no
        
         Raises
         ------
             ValueError
                 Si la cadena de valor no tiene el formato HH:MM (por ejemplo, 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', value):
            raise ValueError(
                'La hora debe tener el siguiente formato: HH:MM (por ejemplo, 08:31, 14:22, 00:01)')
        self._hora = value


    def __encontrar_dia(self, fecha):
        """
        Encuentra el día a partir de la fecha: por ejemplo, jueves
        
         Parámetros
         ----------
             fecha: str
                 Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        
         Devoluciones
         -------
             Devuelve el día a partir de la fecha como una cadena
        """        
        dia = datetime.datetime.strptime(fecha, '%Y/%m/%d').weekday()
        return self.days[dia]


    def __es_tiempo_descanso(self, check_hora):
        """
        Método que comprueba si el tiempo proporcionado está dentro de las horas laborables,
        donde las horas laborales son: 07:30 - 12:00 y 13:00 - 16:30
        
         PARAMETRO
         ----------
             check_hora : str
                 Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15
        
         RETORNA
         -------
             Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario, False
        """          
        tiempo = datetime.datetime.strptime(check_hora, '%H:%M').time()
        return ((tiempo >= datetime.time(7, 30) and tiempo <= datetime.time(11, 59)) or
                (tiempo >= datetime.time(13, 00) and tiempo <= datetime.time(16, 30)))


    def __es_feriado(self, fecha, online):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador.
        si online == Verdadero, utilizará una API REST, de lo contrario, generará los días 
        festivos del año examinado
        
         Parámetros
         ----------
             fecha: str
                 Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos
        
         RETORNA
         -------
             Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
        """          
        y, m, d = fecha.split('/')

        if online:
            # abstractapi Holidays API, free version: 1000 requests per month
            # 1 request per second
            # retrieve API key from enviroment variable
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # This means there is a missing API key
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # if there is no holiday we get an empty array
                return False
            # Fix Maundy Thursday incorrectly denoted as holiday
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = HolidayEcuador(prov='EC-P')
            return fecha in ecu_holidays


    def evaluar(self):
        """
        Comprueba si una persona es beneficiaria al crédito del bono de desarrollo
        humano según los parametros ingresados.
        http://www.ecuadorlegalonline.com/consultas/credito-de-desarrollo-humano/

         Devoluciones
         -------
             Devoluciones Verdadero si el persona es puede recibir el crédito en la
             hora, fecha y según el ultimo dígito de su cédula, en tal día.
        """
        # Comprobar si la fecha es un día festivo
        if self.__encontrar_dia(self.fecha):
            return True

        # Consultar 
        # o si se utilizan sólo dos letras
        if self.cedula[1] in 'AUZEXM' or len(self.cedula.split('-')[0]) == 2:
            return True

        # Compruebe si el tiempo esta dentro de las horas laborables propuestas.
        if not self.__es_tiempo_descanso(self.hora):
            return True

        day = self.__es_feriado(self.fecha)  # Buscar el día de la semana a partir de la fecha

        # Verifique si el último dígito de la cédula no está restringido en este día en particular
        if int(self.cedula[-1]) not in self.restrictions[day]:
            return True
        return False


if __name__ == '__main__':
    
    cedula = input("Digite la cedula: ")
    fecha = input("Digite la fecha: ")
    hora = input("Digite la hora: ")
    online = False

    x = PersonaAcreditada(cedula,fecha,hora,online)
    x.evaluar()
