# -*- coding: utf-8 -*-

import simula_balance as sb
import metricas as met 

def activar_caja(banco, mercado, producto, plazo):
    def caja_a_producto():
        caja = banco.saldo()
        t0 = banco.tiempo_actual()
        glosa = str(t0) + '-act_caja_con_' + producto
        if caja <= 0:
            raise ValueError("No hay caja para activar en " + producto + ".")
        else:
            op = sb.Operacion(mercado[t0][producto], t0, plazo, caja,
                              {'id':glosa, 'ap':'activo', 'producto':producto})
            banco.cursa_operacion(op)
        return
    return caja_a_producto
    

def financia_caja(banco, mercado, producto, plazo):
    def caja_con_producto():
        caja = banco.saldo()
        t0 = banco.tiempo_actual()
        glosa = str(t0) + '-fin_caja_con_' + producto
        if caja >= 0:
            raise ValueError("La caja es positiva")
        else:
            op = sb.Operacion(mercado[t0][producto], t0, plazo, -caja,
                              {'id':glosa, 'ap':'pasivo', 'producto':producto})
            banco.cursa_operacion(op)
        return
    return caja_con_producto


def renovar(banco, mercado, producto, plazos):
    def renovar_producto():
        ops = banco.operaciones()
        t0 = banco.tiempo_actual()
        productos = [op for op in ops if op.vencimiento() == banco.tiempo_actual() and
                                 op.atributos()['producto'] == producto]
        for prod in productos:
            for plazo in plazos:
                porcentaje = plazos[plazo] / 100.0
                atrib = {'id':'r' + prod.atributos()['id'], 'ap':prod.atributos()['ap'], 'producto':producto}
                if plazo == 2:
                    new_prod = sb.Operacion(mercado[t0]['depo2'], t0, plazo, porcentaje * prod.flujo(), atrib)
                elif plazo == 3:
                    new_prod = sb.Operacion(mercado[t0]['depo3'], t0, plazo, porcentaje * prod.flujo(), atrib)
                else:
                    new_prod = sb.Operacion(mercado[t0]['depo4'], t0, plazo, porcentaje * prod.flujo(), atrib)                
                banco.cursa_operacion(new_prod)
    return renovar_producto


def cumple_c46(banco, plazos):
    c46 = met.c46(banco)
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
                new_depo = sb.Operacion(mercado['depo2'], t0, plazo, porcentaje * op.monto(), atrib)
            elif plazo == 3:
                new_depo = sb.Operacion(mercado['depo3'], t0, plazo, porcentaje * op.flujo(), atrib)
            else:
                new_depo = sb.Operacion(mercado['depo4'], t0, plazo, porcentaje * op.monto(), atrib)
            banco.cursa_operacion(new_depo)
    return
