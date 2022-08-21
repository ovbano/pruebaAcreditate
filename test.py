import unittest
from datetime import datetime
from src.Acreditate import PersonaAcreditada


class TestAcreditate(unittest.TestCase):

    def test_invalid_cedula(self):
        """
        Pruebe que la cédula no válida genera ValueError
        """
        cedula = '230016101'
        now = datetime.now()
        date, tm = now.strftime("%Y-%m-%d %H:%M").split()
        with self.assertRaises(ValueError):
            result = PersonaAcreditada(cedula, date, tm).evaluar()
        print("Probando cédula erronea (9 dígitos)")

    
    def test_invalid_date(self):
        """
        Pruebe que la fecha no válida genera ValueError
        """
        cedula = '2300166101'  # cédula única
        now = datetime.now()
        date, tm = now.strftime("%d/%m/%Y %H:%M").split()
        with self.assertRaises(ValueError):
            result = PersonaAcreditada(cedula, date, tm).evaluar()
        print("Fecha errónea")

    
    def test_invalid_time(self):
        """
        Pruebe que el tiempo no válido genera ValueErro
        """
        cedula = '2300166101'  # cédula única
        now = datetime.now()
        date, tm = now.strftime("%Y/%m/%d %H:%M:%S").split()
        with self.assertRaises(ValueError):
            result = PersonaAcreditada(cedula, date, tm).evaluar()
        print("Hora errónea")



    def test_holiday(self):
        """
        Prueba que se restringen las vacaciones
        """
        date = '2020/12/25'  # navidad, viernes
        cedula = "2300166101"  # cédula única prohivida para lunes
        tm = '14:00'  # dentro de las horas laborables
        result = PersonaAcreditada(cedula, date, tm).evaluar()
        self.assertTrue(result)
        print("Vacaciones")


    def test_weekend(self):
        """
        Prueba que los fines de semana no están restringidos
        """
        date = '2021/04/25'  # Domingo
        cedula = '2300166101'  # vehículo privado
        tm = '14:00'  # dentro de las horas laborables
        result = PersonaAcreditada(cedula, date, tm).evaluar()
        self.assertTrue(result)
        print("Fines de semana")


    def test_outside_peak_hours(self):
        """
        Pruebe que el tiempo fuera de las horas laborables no está restringido
        """
        date = '2021/04/27'  # martes
        cedula = '2300166101'  # vehiculo privado prohibido los martes
        tm = '20:00'  # fuera de las horas laborables
        result = PersonaAcreditada(cedula, date, tm).evaluar()
        self.assertTrue(result)
        print("Hora no laborable")

if __name__ == '__main__':
    unittest.main()