# -*- coding: utf-8 -*-
from __future__ import division

# Período expresado en meses, esto se ingresa a mano.
periodo = 3

# Esto es un cálculo
dt = 1.0 / periodo

class Operacion:
    def __init__(self, tasa, inicio, plazo, monto, atributos):
        self._tasa = round(tasa, 4)
        self._inicio = round(inicio, 4)
        self._plazo = round(plazo, 4)
        self._monto = round(monto, 4)
        self._interes = round(monto * tasa * plazo * periodo / 12, 4)
        self._atributos = atributos
        return

    def monto(self, con_signo=False):
        if con_signo:
            if self._atributos['ap'] == 'activo':
                return self._monto
            else:
                return -self._monto
        else:       
            return self._monto
        
    def inicio(self):
        return self._inicio
    
    def tasa(self):
        return self._tasa
    
    def interes(self):
        return self._interes

    def flujo(self, con_signo=False):
        if con_signo:
            if self._atributos['ap'] == 'activo':
                return self._monto + self._interes
            else:
                return -self._monto - self._interes
        else:       
            return self._monto + self._interes

    def atributos(self):
        return self._atributos

    def vencimiento(self):
        return self._inicio + self._plazo

    def interes_devengado(self, tiempo):
        if tiempo < self._inicio:
            return 0.0
        elif tiempo >= self._inicio + self._plazo:
            return 0.0
        else:
            return round(self._monto * self._tasa * (tiempo - self._inicio) * periodo / 12, 4)

    def saldo(self, tiempo):
        if tiempo < self._inicio:
            return 0.0
        elif tiempo >= self._inicio + self._plazo:
            return 0.0
        else:
            return round(self._monto * (1 + self._tasa * (tiempo - self._inicio) * periodo / 12), 4)
        
    def interes_pagado(self, tiempo):
        if tiempo >= self._inicio + self._plazo:
            return self._interes
        else:
            return 0.0

class Caja:
    def __init__(self):
        self._movimientos = []
        return

    def imputa_movimiento(self, glosa, tiempo, monto):
        self._movimientos.append((glosa, tiempo, round(monto, 4)))
        return
        
    def saldo(self, tiempo):
        return round(sum([caja[2] for caja in self._movimientos if caja[1] <= tiempo]), 4)

class Banco:

    def __init__(self, caja_inicial, operaciones, capital = 0):
        self._inicio = 0
        self._tiempo_actual = 0
        self._caja = caja_inicial
        self._operaciones = []
        self._capital = capital
        self._caja.imputa_movimiento('capital', self._tiempo_actual, capital)
        for op in operaciones:
            self.cursa_operacion(op)
        return

    def tiempo_actual(self):
        return self._tiempo_actual

    def capital(self):
        return self._capital

    def operaciones(self):
        return self._operaciones
        
    def cursa_operacion(self, operacion):
        glosa = operacion.atributos()['id'] + operacion.atributos()['producto']
        self._caja.imputa_movimiento(glosa, self._tiempo_actual, -operacion.monto(True))
        self._operaciones.append(operacion)
        return
 
    def avanza(self):
        self._tiempo_actual += 1
        for op in self._operaciones:
            if op.vencimiento() == self._tiempo_actual:
                glosa = op.atributos()['id'] + op.atributos()['producto']
                if op.atributos()['ap'] == 'activo':
                    self._caja.imputa_movimiento(glosa, self._tiempo_actual, op.flujo())
                else:
                    self._caja.imputa_movimiento(glosa, self._tiempo_actual, -op.flujo())

    def movimiento_caja(self, glosa, tiempo, monto):
        self._caja.imputa_movimiento(glosa, tiempo, monto)
        return

    def saldo(self, tiempo = None):
        if tiempo is not None:
            return self._caja.saldo(tiempo)
        else:
            return self._caja.saldo(self._tiempo_actual)

    def activos(self):
        return [op for op in self._operaciones if op.atributos()['ap'] == 'activo']

    def pasivos(self):
        return [op for op in self._operaciones if op.atributos()['ap'] == 'pasivo']

    def estado_resultados(self):
        result = {'activo':{'intereses_recibidos':0.0, 'intereses_devengados':0.0},
                  'pasivo':{'intereses_pagados':0.0, 'intereses_devengados':0.0}}
        intereses_recibidos = 0.0
        intereses_pagados = 0.0
        intereses_devengados = 0.0
        for act in self.activos():
            intereses_recibidos += act.interes_pagado(self._tiempo_actual)
            intereses_devengados += act.interes_devengado(self._tiempo_actual)
        result['activo']['intereses_recibidos'] = intereses_recibidos
        result['activo']['intereses_devengados'] = intereses_devengados

        intereses_pagados = 0.0
        intereses_devengados = 0.0
        for pas in self.pasivos():
            intereses_pagados += pas.interes_pagado(self._tiempo_actual)
            intereses_devengados += pas.interes_devengado(self._tiempo_actual)
        result['pasivo']['intereses_pagados'] = intereses_pagados
        result['pasivo']['intereses_devengados'] = intereses_devengados
        return result

    def cartera(self):
        ops = []
        for act in self.activos():
            int_dev = act.interes_devengado(self._tiempo_actual)
            int_rec = act.interes_pagado(self._tiempo_actual)
            atb = act.atributos()
            op = (atb['ap'], atb['producto'], atb['id'], act.inicio(), act.vencimiento(), act.monto(), act.tasa(), int_dev, int_rec)
            ops.append(op)
        for pas in self.pasivos():
            int_dev = pas.interes_devengado(self._tiempo_actual)
            int_pag = pas.interes_pagado(self._tiempo_actual)
            atb = pas.atributos()
            op = (atb['ap'], atb['producto'], atb['id'], pas.inicio(), pas.vencimiento(), pas.monto(True), pas.tasa(), -int_dev, -int_pag)
            ops.append(op)
        return ops
    
    def balance(self):
        saldo_caja = self._caja.saldo(self._tiempo_actual)
        result = {'activo':{'caja':saldo_caja if saldo_caja >=0 else 0.0},
                  'pasivo':{'sobregiro':saldo_caja if saldo_caja < 0 else 0.0},
                  'patrimonio':{'capital_pagado':-self._capital}}
        for act in self.activos():
            if act.atributos()['producto'] not in result['activo']:
                result['activo'][act.atributos()['producto']] = act.saldo(self._tiempo_actual)
            else:
                result['activo'][act.atributos()['producto']] += act.saldo(self._tiempo_actual)
        for pas in self.pasivos():
            if pas.atributos()['producto'] not in result['pasivo']:
                result['pasivo'][pas.atributos()['producto']] = -pas.saldo(self._tiempo_actual)
            else:
                result['pasivo'][pas.atributos()['producto']] -= pas.saldo(self._tiempo_actual)
        return result

    def inv_sobre_col(self):
        inversiones = [op.saldo(self._tiempo_actual) for op in self._operaciones if op._atributos['producto'] == 'inversion']
        colocaciones = [op.saldo(self._tiempo_actual) for op in self._operaciones if op._atributos['producto'] == 'credito']
        return sum(inversiones) / sum(colocaciones)
        
        






