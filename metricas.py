# -*- coding: utf-8 -*-

import simula_balance as sb

def construye_gap_liquidez(banco):
    """
    Calcula el gap de liquidez dt a dt y acumulado
    """
    cuantos = 24 / sb.periodo
    
    if cuantos == 24: # periodo mensual
        gap = {0:banco.saldo(),
               1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0,
               13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0,
               25:0, 26:0, 27:0, 28:0, 29:0, 30:0, 31:0, 32:0, 33:0, 34:0, 35:0, 36:0,
               37:0, 38:0, 39:0, 40:0, 41:0, 42:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0}
    elif cuantos == 8: # periodo trimestral
        gap = {0:banco.saldo(),
               1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0,
               9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
    else: # periodo semestral
        gap = {0:banco.saldo(),
               1:0, 2:0, 3:0, 4:0,
               5:0, 6:0, 7:0, 8:0}

    for op in banco.operaciones():
        vcto = op.vencimiento() - banco.tiempo_actual()
        if vcto > 0:
            gap[vcto] += op.flujo(True)
    def gap_liquidez(plazo = 0, acumulado = True):
        if plazo == 0:
            return gap
        else:
            if acumulado:
                acum = 0
                for i in range(0, plazo + 1):
                    acum += gap[i]
                return acum
            else:
                return gap[plazo]
    return gap_liquidez

def c46(banco, capital_cero = False):
    """
    Calcula el c46 del banco.
    c46 = suma(pasivos, vencimiento <= 3) - suma(activos, vencimiento <=3)
    """
    if capital_cero:
        capital = 0.0
    else:
        capital = banco.capital()
    gap = construye_gap_liquidez(banco)
    if sb.periodo == 1:
        dif = -gap(3) - 2 * capital
        return dif
    elif sb.periodo == 3:
        dif = -gap(1) - 2 * capital
        return dif
    else:
        raise TypeError("El periodo establecido no permite el cálculo del C46.")


