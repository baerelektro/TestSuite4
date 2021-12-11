"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

'''

    This tutorial demonstrates how to encode a payload for use in a transfer function call
    В этом руководстве показано, как кодировать полезную нагрузку для использования при вызове передающей функции

'''


from tonos_ts4 import ts4

eq = ts4.eq

def test1():
    # Deploy a contract (encoder/sender)
     # Развертывание контракта (кодировщик/отправитель)
    sender = ts4.BaseContract('tutorial10_1', {})

    # Register nickname to be used in the output
    # Зарегистрируйте псевдоним, который будет использоваться в выводе
    ts4.register_nickname(sender.address, 'Sender')

    # Deploy a contract (receiver) with an alternate method of setting nickname
    # Развертывание контракта (получателя) с альтернативным способом установки псевдонима
    receiver = ts4.BaseContract('tutorial10_2', {}, nickname='Receiver')
    
    # Ensure that current value in the receiver contract is default
    # Убедитесь, что текущее значение в контракте получателя установлено по умолчанию
    assert eq(0, receiver.call_getter('m_value'))

    value = 0xbeaf
    # Encode calling of the receiver contract
     # Кодирование вызова контракта получателя
    payload = sender.call_getter('encode', {'value': value})

    # Call receiver contract's method via sender contract
    # Метод контракта получателя вызова через контракт отправителя
    sender.call_method('call_it', {'dest': receiver.address, 'payload': payload})

    # Dispatch created internal message from sender to receiver
    # Отправка созданного внутреннего сообщения от отправителя получателю
    ts4.dispatch_one_message()

    # Ensure that current value was set
    # Убедитесь, что текущее значение было установлено
    assert eq(value, receiver.call_getter('m_value'))


def test2():
    # Deploy a contract (encoder/sender)
    # Развертывание контракта (кодировщик/отправитель)
    sender = ts4.BaseContract('tutorial10_1', {}, nickname='Sender')

    # Deploy a contract (receiver)
    # Развертывание контракта (получателя)  
    receiver = ts4.BaseContract('tutorial10_2', {}, nickname='Receiver')

    # Ensure that current value in the receiver contract is default
    # Убедитесь, что текущее значение в контракте получателя установлено по умолчанию
    assert eq(0, receiver.call_getter('m_value'))

    value = 0xabba
    # Encode calling of the receiver contract
    # Кодирование вызова контракта получателя
    payload = ts4.encode_message_body('tutorial10_2', 'call_me', {'value': value})

    # Call receiver contract's method via sender contract
    # Метод контракта получателя вызова через контракт отправителя
    sender.call_method('call_it', {'dest': receiver.address, 'payload': payload})

    # Dispatch created internal message from sender to receiver
    # Отправка созданного внутреннего сообщения от отправителя получателю
    ts4.dispatch_one_message()

    # Ensure that current value was set
    # Убедитесь, что текущее значение было установлено
    assert eq(value, receiver.call_getter('m_value'))


# Initialize TS4 by specifying where the artifacts of the used contracts are located
# verbose: toggle to print additional execution info
# Инициализируйте TS4, указав, где находятся артефакты используемых контрактов
# подробное описание: переключитесь для печати дополнительной информации о выполнении
ts4.init('contracts/', verbose = True)

test1()
test2()
