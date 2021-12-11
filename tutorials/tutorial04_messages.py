"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

'''

    This tutorial shows how to dispatch internal messages between contracts,
    as well as how to catch events fired by a contract.
    В этом руководстве показано, как отправлять внутренние сообщения между контрактами,
    а также о том, как отловить события, вызванные контрактом.

'''


import tonos_ts4.ts4 as ts4

eq = ts4.eq


def test1():
    # In this scenario we are processing messages step by step
    # В этом сценарии мы обрабатываем сообщения шаг за шагом

    print('Starting call chain (step by step)...')
    t_value = 4276994270
    contract1.call_method('ping_neighbor', dict(neighbor=neighbor2, value=t_value))

    # Get internal message that was created by previous call
    # Получить внутреннее сообщение, созданное предыдущим вызовом
    msg_ping = ts4.peek_msg()
    assert eq(neighbor1, msg_ping.src)
    assert eq(neighbor2, msg_ping.dst)
    assert msg_ping.is_call('ping')
    assert eq(t_value, int(msg_ping.params['request']))

    # Dispatch created message
    # Отправка созданного сообщения
    ts4.dispatch_one_message()

    # Pick up event that was created by called method of the callee contract
    # Событие приема, созданное вызываемым методом контракта вызываемого абонента
    msg_event1 = ts4.pop_event()

    # Check correctness of event addresses
    # Проверьте правильность адресов событий
    assert msg_event1.is_event('ReceivedRequest', src = neighbor2, dst = ts4.Address(None))
    assert eq(t_value, int(msg_event1.params['request']))

    # Get internal message that was created by last call
    # Получить внутреннее сообщение, созданное последним вызовом
    msg_pong = ts4.peek_msg()
    assert eq(neighbor2, msg_pong.src)
    assert eq(neighbor1, msg_pong.dst)
    assert msg_pong.is_call('pong')
    assert eq(t_value, int(msg_pong.params['reply']))

    # Dispatch next message
    # Отправить следующее сообщение
    ts4.dispatch_one_message()

    # Pick up last event and check its parameters
    # Выберите последнее событие и проверьте его параметры
    msg_event2 = ts4.pop_event()
    assert msg_event2.is_event('ReceivedReply', src = neighbor1, dst = ts4.Address(None))
    assert eq(t_value, int(msg_event2.params['reply']))

    # Working with raw JSON data is not always convenient. That's why we
    # provide a way to decode data:
    # Работа с необработанными данными JSON не всегда удобна. Вот почему мы
    # предоставьте способ декодирования данных:
    event2 = contract1.decode_event(msg_event2)
    assert eq(t_value, event2.reply)


def test2():
    # In most cases it is not necessary to control each message (while possible),
    # so here is the shorter version of the same scenario
    # В большинстве случаев нет необходимости контролировать каждое сообщение (пока это возможно),
    # итак, вот более короткая версия того же сценария

    print('Starting call chain (in one step)...')
    t_value = 255
    contract1.call_method('ping_neighbor', dict(neighbor=neighbor2, value=t_value))

    # Dispatch all internal messages in one step
    # Отправка всех внутренних сообщений за один шаг
    ts4.dispatch_messages()

    # Skip first event
    # Пропустить первое мероприятие
    ts4.pop_event()

    # Processing last event
    # Обработка последнего события
    msg_event = ts4.pop_event()

    # Ensure that dst address is empty (one more variant)
    # Убедитесь, что адрес dst пуст (еще один вариант)
    assert msg_event.is_event('ReceivedReply', src = neighbor1, dst = ts4.Address(None))
    assert eq(t_value, int(msg_event.params['reply']))


# Initialize TS4 by specifying where the artifacts of the used contracts are located
# verbose: toggle to print additional execution info
# Инициализируйте TS4, указав, где находятся артефакты используемых контрактов
# подробная информация: переключите, чтобы напечатать дополнительную информацию о выполнении
ts4.init('contracts/', verbose = True)

# Deploy contracts
# Развертывание контрактов
contract1 = ts4.BaseContract('tutorial04_1', {})
neighbor1 = contract1.addr
contract2 = ts4.BaseContract('tutorial04_2', {})
neighbor2 = contract2.addr

# Register nicknames to be used in the output
# Зарегистрируйте псевдонимы, которые будут использоваться в выводе
ts4.register_nickname(neighbor1, 'Alice')
ts4.register_nickname(neighbor2, 'Bob')

print('Contract 1 deployed at {}'.format(neighbor1))
print('Contract 2 deployed at {}'.format(neighbor2))

test1()

# Ensure we have no undispatched messages
# Убедитесь, что у нас нет бесспорных сообщений.
ts4.ensure_queue_empty()

test2()
