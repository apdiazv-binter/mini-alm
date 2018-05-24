# -*- coding: utf-8 -*-

import simula_balance as sb
import metricas as met 

mercado = {'on_col': 0.0, 'on_cap':0.0, 'depo2':0.0312, 'depo3':0.033,'depo4':0.0348,
           'inversion':0.027, 'colocacion':0.045}

def inversion(banco):
    caja = banco.saldo()
    t0 = banco.tiempo_actual()
    glosa = 'inv-' + str(t0) + '-1'
    if caja <= 0:
        raise ValueError("No hay caja para tomar inversiones.")
    else:
        op = sb.Operacion(mercado['inversion'], t0, 1, caja, {'id':glosa, 'ap':'activo', 'producto':'inversion'})
        banco.cursa_operacion(op)
    return

def overnight(banco):
    caja = banco.saldo()
    t0 = banco.tiempo_actual()
    glosa = 'ov-' + str(t0) + '-1'
    if caja == 0:
        return
    elif caja > 0:
        op = sb.Operacion(mercado['on_col'], t0, 1, caja, {'id':glosa, 'ap':'activo', 'producto':'on-a'})
        banco.cursa_operacion(op)
    else:
        op = sb.Operacion(mercado['on_cap'], t0, 1, -caja, {'id':glosa, 'ap':'pasivo', 'producto':'on-p'})
        banco.cursa_operacion(op)
    return

def renueva_depos(banco, plazos):
    ops = banco.operaciones()
    t0 = banco.tiempo_actual()
    depos = [op for op in ops if op.vencimiento() == banco.tiempo_actual() and
                                 op.atributos()['ap'] == 'pasivo']
    for depo in depos:
        for plazo in plazos:
            porcentaje = plazos[plazo] / 100.0
            atrib = {'id':'r' + depo.atributos()['id'], 'ap':'pasivo', 'producto':'depo'}
            if plazo == 2:
                new_depo = sb.Operacion(mercado['depo2'], t0, plazo, porcentaje * depo.flujo(), atrib)
            elif plazo == 3:
                new_depo = sb.Operacion(mercado['depo3'], t0, plazo, porcentaje * depo.flujo(), atrib)
            else:
                new_depo = sb.Operacion(mercado['depo4'], t0, plazo, porcentaje * depo.flujo(), atrib)                
            banco.cursa_operacion(new_depo)
    return

def cumple_c46(banco, plazos, capital_cero = True):
    c46 = met.c46(banco, capital_cero)
    monto = c46 - banco.saldo()
    t0 = banco.tiempo_actual()
    if c46 > 0:
        plazo_inversion = 1
        op = sb.Operacion(mercado['inversion'], banco.tiempo_actual(), plazo_inversion, c46,
                          {'id':str(t0) + '-inv' , 'ap':'activo', 'producto':'inversion'})
        banco.cursa_operacion(op)
        for plazo in plazos:
            porcentaje = plazos[plazo] / 100.0
            atrib = {'id':str(t0) + '-fin_inv', 'ap':'pasivo', 'producto':'depo'}
            if plazo == 2:
                new_depo = sb.Operacion(mercado['depo2'], t0, plazo, porcentaje * monto, atrib)
            elif plazo == 3:
                new_depo = sb.Operacion(mercado['depo3'], t0, plazo, porcentaje * monto, atrib)
            else:
                new_depo = sb.Operacion(mercado['depo4'], t0, plazo, porcentaje * monto, atrib)
            banco.cursa_operacion(new_depo)
    return
