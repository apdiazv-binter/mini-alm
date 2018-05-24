# -*- coding: utf-8 -*-

import simula_balance as sb
import metricas as met
import reglas_renovacion as rn 
import pprint

def test1():
    caja = sb.Caja()

    for i in range(1, 11):
        caja.imputa_movimiento('1', i, 100)

    for i in range(1, 11):
        print caja.saldo(i)

    print caja._movimientos
    return

def test2():
    caja = sb.Caja()

    credito = sb.Operacion(.12, 0, 24, 100, {'id':'1', 'ap':'activo'})
    print 'cred flujo venc: ', credito.flujo()
    
    deposito = sb.Operacion(.06, 0, 6, 100, {'id':'1', 'ap':'pasivo'})
    print 'dep flujo venc: ', deposito.flujo()

    banco = sb.Banco(caja, [credito, deposito])
    print 'saldo inicial: ', banco.saldo()
    print 'caja inicial: ', banco._caja._movimientos
    
    for i in range(0, 6):
        banco.avanza()
    print 'saldo final: ', banco.saldo()
    print 'caja final: ', banco._caja._movimientos
    
    return

def test3():
    operacion = sb.Operacion(.12, 0, 24, 100, {'id':'1', 'ap':'activo'})
    print "flujo credito normal: ", operacion.flujo()
    print "flujo credito con signo: ", operacion.flujo(True)

    operacion.atributos()['ap'] = 'pasivo'
    print "flujo pasivo normal: ", operacion.flujo()
    print "flujo paivo  con signo: ", operacion.flujo(True)

def test4():
    caja = sb.Caja()

    credito_1 = sb.Operacion(.12, 0, 1, 100, {'id':'1', 'ap':'activo'})
    credito_2 = sb.Operacion(.12, 0, 2, 100, {'id':'2', 'ap':'activo'})
    credito_3 = sb.Operacion(.12, 0, 3, 100, {'id':'3', 'ap':'activo'})
    
    deposito_1 = sb.Operacion(.06, 0, 1, 100, {'id':'4', 'ap':'pasivo'})
    deposito_2 = sb.Operacion(.06, 0, 2, 100, {'id':'5', 'ap':'pasivo'})
    deposito_3 = sb.Operacion(.06, 0, 3, 100, {'id':'6', 'ap':'pasivo'})

    ops = [credito_1, credito_2, credito_3, deposito_1, deposito_2, deposito_3]
    banco = sb.Banco(caja, ops)

    gap = met.construye_gap_liquidez(banco)
    print gap(0)
    print gap(1, False), gap(1)
    print gap(2, False), gap(2)
    print gap(3, False), gap(3)
    print gap(4, False), gap(4)

def test5():
    caja = sb.Caja()

    credito_1 = sb.Operacion(.12, 0, 6, 100, {'id':'1', 'ap':'activo'})
    credito_2 = sb.Operacion(.12, 0, 6, 100, {'id':'2', 'ap':'activo'})
    credito_3 = sb.Operacion(.12, 0, 6, 100, {'id':'3', 'ap':'activo'})
    
    deposito_1 = sb.Operacion(.0, 0, 1, 100, {'id':'4', 'ap':'pasivo'})
    deposito_2 = sb.Operacion(.0, 0, 2, 100, {'id':'5', 'ap':'pasivo'})
    deposito_3 = sb.Operacion(.0, 0, 3, 100, {'id':'6', 'ap':'pasivo'})

    ops = [credito_1, credito_2, credito_3, deposito_1, deposito_2, deposito_3]
    banco = sb.Banco(caja, ops, 150)

    print met.c46(banco)

def test6():
    """
    Verifica correcta renovación por operación overnight
    """
    capital = 10
    caja = sb.Caja()

    credito = sb.Operacion(.0, 0, 12, 100, {'id':'1', 'ap':'activo'})
    print 'cred flujo venc: ', credito.flujo()
    
    deposito = sb.Operacion(.00, 0, 1, 100, {'id':'1', 'ap':'pasivo'})
    print 'dep flujo venc: ', deposito.flujo()

    banco = sb.Banco(caja, [credito, deposito], capital)
    print 'saldo inicial: ', banco.saldo()
    print 'caja inicial: ', banco._caja._movimientos
    pp = pprint.PrettyPrinter(indent=4, depth=6)
    gap = met.construye_gap_liquidez(banco)
    pp.pprint(gap())
    print 'c46: ', met.c46(banco)
    print 'caja: ', banco.saldo()
    for i in range(0, 1):
        banco.avanza()
        gap = met.construye_gap_liquidez(banco)
        pp.pprint(gap())
        print 'c46: ', met.c46(banco)
        print 'caja: ', banco.saldo()
        rn.overnight(banco)
        gap = met.construye_gap_liquidez(banco)
        pp.pprint(gap())
        print 'c46: ', met.c46(banco)
        print 'caja: ', banco.saldo()
    return

def test7():
    """
    Verifica renovación con depo plazo.
    """
    plazos = {6:1.0}
    capital = 10
    caja = sb.Caja()

    credito = sb.Operacion(.0, 0, 12, 100, {'id':'1', 'ap':'activo'})
    print 'cred flujo venc: ', credito.flujo()
    
    deposito = sb.Operacion(.00, 0, 1, 100, {'id':'1', 'ap':'pasivo'})
    print 'dep flujo venc: ', deposito.flujo()

    banco = sb.Banco(caja, [credito, deposito], capital)
    print 'saldo inicial: ', banco.saldo()
    print 'caja inicial: ', banco._caja._movimientos
    pp = pprint.PrettyPrinter(indent=4, depth=6)
    gap = met.construye_gap_liquidez(banco)
    pp.pprint(gap())
    print 'c46: ', met.c46(banco)
    print 'caja: ', banco.saldo()
    for i in range(0, 12):
        banco.avanza()
        
        gap = met.construye_gap_liquidez(banco)
        print 'gap1'
        pp.pprint(gap())
        print 'c46: ', met.c46(banco)
        print 'caja: ', banco.saldo()
        
        rn.renueva_depos(banco, plazos)
        rn.overnight(banco)
        
        gap = met.construye_gap_liquidez(banco)
        print 'gap2'
        pp.pprint(gap())
        print 'c46: ', met.c46(banco)
        print 'caja: ', banco.saldo()

    return

def test8():
    """
    Verifica renovación con depo plazo y arreglo C46.
    """
    plazos = {6:1.0}
    capital = 10
    caja = sb.Caja()

    credito = sb.Operacion(.0, 0, 12, 100, {'id':'1', 'ap':'activo'})
    print 'cred flujo venc: ', credito.flujo()
    
    deposito = sb.Operacion(.00, 0, 1, 100, {'id':'1', 'ap':'pasivo'})
    print 'dep flujo venc: ', deposito.flujo()

    banco = sb.Banco(caja, [credito, deposito], capital)
    print 'saldo inicial: ', banco.saldo()
    print 'caja inicial: ', banco._caja._movimientos
    pp = pprint.PrettyPrinter(indent=4, depth=6)
    gap = met.construye_gap_liquidez(banco)
    pp.pprint(gap())
    print 'c46: ', met.c46(banco)
    print 'caja: ', banco.saldo()
    for i in range(0, 12):
        banco.avanza()
        
        gap = met.construye_gap_liquidez(banco)
        print 'gap1'
        pp.pprint(gap())
        print 'c46: ', met.c46(banco)
        print 'caja: ', banco.saldo()
        
        rn.renueva_depos(banco, plazos)
        rn.overnight(banco)
        rn.cumple_c46(banco, plazos)
        
        gap = met.construye_gap_liquidez(banco)
        print 'gap2'
        pp.pprint(gap())
        print 'c46: ', met.c46(banco)
        print 'caja: ', banco.saldo()

    return

if __name__ == "__main__":
    test2()