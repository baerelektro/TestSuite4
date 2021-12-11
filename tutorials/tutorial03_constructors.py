"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

'''

    This tutorial demonstrates the different variants for working with the constructor.
    В этом уроке демонстрируются различные варианты работы с конструктором.

'''


import tonos_ts4.ts4 as ts4

eq = ts4.eq


def test1():
    # Deploy a contract. Constructor is called automatically.
    # Разверните контракт. Конструктор вызывается автоматически.
    tut = ts4.BaseContract('tutorial03_1', {})

    # Call a getter and ensure that we received correct integer value
    # Вызовите геттер и убедитесь, что мы получили правильное целочисленное значение
    expected_value = 3735928559
    assert eq(expected_value, tut.call_getter('m_number'))


def test2():
    t_number = 12648430

    # Deploy a contract without construction
    # Развертывание контракта без строительства
    tut = ts4.BaseContract('tutorial03_2', ctor_params = None)

    # And construct it manually with an external message
    # И создайте его вручную с помощью внешнего сообщения
    tut.call_method('constructor', {'t_number': t_number})

    # Call a getter and ensure that we received correct integer value
    # Вызовите геттер и убедитесь, что мы получили правильное целочисленное значение
    assert eq(t_number, tut.call_getter('m_number'))


def test3():
    t_number = 3054

    # Deploy a contract with calling constructor (offchain)
    # Разверните контракт с вызывающим конструктором (цепочка)
    tut = ts4.BaseContract('tutorial03_2', ctor_params = {'t_number': t_number})

    # Call a getter and ensure that we received correct integer value
    # Вызовите геттер и убедитесь, что мы получили правильное целочисленное значение
    assert eq(t_number, tut.call_getter('m_number'))


def test4():
    # Generating a pair of keys
    # Создание пары ключей
    keypair = ts4.make_keypair()

    t_number = 14613198

    # Deploy a contract with given (by public key) owner.
    # Private key is needed here only when constructor checks 
    # that message is signed.
    # Разверните контракт с данным (открытым ключом) владельцем.
    # Закрытый ключ необходим здесь только при проверке конструктора 
    # это сообщение подписано.
    tut = ts4.BaseContract('tutorial03_3',
        ctor_params = dict(t_number = t_number),
        keypair = keypair
    )

    # Check the validity of the key pair
    # Проверьте правильность пары ключей
    assert eq(keypair, tut.keypair)

    # Call a getter and ensure that we received correct integer value
    # Вызовите геттер и убедитесь, что мы получили правильное целочисленное значение
    assert eq(t_number, tut.call_getter('m_number'))


# Initialize TS4 by specifying where the artifacts of the used contracts are located
# verbose: toggle to print additional execution info
# Инициализируйте TS4, указав, где находятся артефакты используемых контрактов
# подробная информация: переключите, чтобы напечатать дополнительную информацию о выполнении
ts4.init('contracts/', verbose = True)

test1()
test2()
test3()
test4()
