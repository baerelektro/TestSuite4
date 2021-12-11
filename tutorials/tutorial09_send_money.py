"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

'''

    This tutorial shows you how to send money and properly handle bounced messages.
    You will also learn how to send money along with the payload and decode it.
    В этом руководстве показано, как отправлять деньги и правильно обрабатывать отправленные сообщения.
    Вы также узнаете, как отправлять деньги вместе с полезной нагрузкой и расшифровывать ее.

'''


import tonos_ts4.ts4 as ts4

eq = ts4.eq


def test1():
    print('Transfer with bounce')
    # Deploy the sender's contract and register nickname to be used in the output
    # Разверните контракт отправителя и зарегистрируйте псевдоним, который будет использоваться в выводе
    sender = ts4.BaseContract('tutorial09', {}, nickname = 'Sender')
    addr_sender = sender.address
    balance_sender = 100 * ts4.GRAM

    # Сheck the sender's initial balance. There are 100 grams by default
    # Разверните контракт отправителя и зарегистрируйте псевдоним, который будет использоваться в выводе
    sender.ensure_balance(balance_sender)

    # The contract address of the recipient
    # Договорный адрес получателя
    addr_recipient = ts4.Address('0:c4a31362f0dd98a8cc9282c2f19358c888dfce460d93adb395fa138d61ae5069')

    # Register nickname to be used in the output
    # Зарегистрируйте псевдоним, который будет использоваться в выводе
    ts4.register_nickname(addr_recipient, 'Recipient1')

    # Сheck the recipient's balance. Until is not deployed it has no balance
    # Проверьте баланс получателя. Пока он не развернут, он не имеет баланса
    assert eq(None, ts4.get_balance(addr_recipient))

    # Send grams to the recipient with bounce flag
    # Отправить грамм получателю с флагом отскока
    amount = ts4.GRAM
    params = dict(addr = addr_recipient, amount = amount, bounce = True)
    sender.call_method('send_grams', params)

    # Pick up internal message that was created by `send_grams()` call
    # Забрать внутреннее сообщение, созданное вызовом " send_grams ()"
    msg_transfer = ts4.peek_msg()
    assert eq(addr_sender,    msg_transfer.src)
    assert eq(addr_recipient, msg_transfer.dst)
    assert eq(amount,         msg_transfer.value)

    # Dispatch created message
    # Отправка созданного сообщения
    ts4.dispatch_one_message()

    # Сheck the sender's current balance
    # Проверьте текущий баланс отправителя
    sender.ensure_balance(balance_sender - amount)

    # Pick up internal message that was bounced
    # Забрать внутреннее сообщение, которое было отправлено
    msg_bounced = ts4.peek_msg()
    assert eq(addr_recipient, msg_bounced.src)
    assert eq(addr_sender,    msg_bounced.dst)
    assert eq(amount,         msg_bounced.value)
    assert eq(True,           msg_bounced.bounced)

    # Dispatch bounced message
    # Отправка отскочившего сообщения
    ts4.dispatch_one_message()

    # Balance of the recipient should stay empty
    # Баланс получателя должен оставаться пустым
    assert eq(None, ts4.get_balance(addr_recipient))

    print('Transfer without bounce')
    # Send grams to the recipient without bounce flag
    # Отправляйте грамм получателю без флага отскока
    params = dict(addr = addr_recipient, amount = amount, bounce = False)
    sender.call_method('send_grams', params)

    # Dispatch created message
    # Отправка созданного сообщения
    ts4.dispatch_one_message()

    # Check balance of the recipient, it should be equal to transferred amount
    # Проверьте баланс получателя, он должен быть равен переведенной сумме
    assert eq(amount, ts4.get_balance(addr_recipient))

    # Сhecking the sender's balance, it should be decreased by the amount of the transfer
    # Проверка баланса отправителя, он должен быть уменьшен на сумму перевода
    sender.ensure_balance(balance_sender - amount)


def test2():
    print('Transfer with payload')
    # Deploy the sender's contract and register nickname to be used in the output
    # Разверните контракт отправителя и зарегистрируйте псевдоним, который будет использоваться в выводе
    sender = ts4.BaseContract('tutorial09', {}, nickname = 'Sender')
    balance_sender = sender.balance

    # Deploy the another one recipient's contract and register nickname to be used in the output
    # Разверните контракт другого получателя и зарегистрируйте псевдоним, который будет использоваться в выходных данных
    recipient = ts4.BaseContract('tutorial09', {}, nickname = 'Recipient')
    addr_recipient = recipient.address
    balance_recipient = recipient.balance

    # Send grams to the recipient without payload
    # Отправить граммы получателю без полезной нагрузки
    amount = 2 * ts4.GRAM
    comment = 'some comment'
    params = dict(addr = addr_recipient, amount = amount, comment = comment)
    sender.call_method('send_grams_with_payload', params)

    # Dispatch created message
    # Отправка созданного сообщения
    ts4.dispatch_one_message()

    # Сheck the current balance of the sender and recipient
    # Проверьте текущий баланс отправителя и получателя
    sender.ensure_balance(balance_sender - amount)
    recipient.ensure_balance(balance_recipient + amount)

    # Pick up event that was created by called method of the called contract
    # Забрать событие, созданное вызываемым методом вызываемого контракта
    event = ts4.pop_event()
    decoded = recipient.decode_event(event)
    # Check correctness of the received data
    # Проверьте правильность полученных данных
    assert eq(comment, decoded.comment)
    assert eq(amount,  decoded.amount)


def test3():
    print('Transfer with flags')

    # Deploy the sender's contract and register nickname to be used in the output
    # Разверните контракт отправителя и зарегистрируйте псевдоним, который будет использоваться в выводе
    sender = ts4.BaseContract('tutorial09', {}, nickname = 'Sender')
    balance_sender = sender.balance

    # Deploy the another one recipient's contract and register nickname to be used in the output
    # Разверните контракт другого получателя и зарегистрируйте псевдоним, который будет использоваться в выходных данных
    recipient = ts4.BaseContract('tutorial09', {}, nickname = 'Recipient')
    addr_recipient = recipient.address
    balance_recipient = recipient.balance

    # Send grams to the recipient (regular transfer)
    # Отправить граммы получателю (обычный перевод)
    amount = 3 * ts4.GRAM
    params = dict(addr = addr_recipient, amount = amount, flags = 0)
    sender.call_method('send_grams_with_flags', params)

    # Dispatch created message
    # Отправка созданного сообщения
    ts4.dispatch_one_message()

    # Сheck the current balance of the sender and recipient
    # Проверьте текущий баланс отправителя и получателя
    sender.ensure_balance(balance_sender - amount)
    recipient.ensure_balance(balance_recipient + amount)

    # Send remainig balance and self-destroy sender's contract
    # Отправить остаток средств и контракт отправителя на саморазрушение
    params = dict(addr = addr_recipient, amount = 0, flags = 160)
    sender.call_method('send_grams_with_flags', params)
    ts4.dispatch_one_message()

    # Сheck the current balance of the recipient, it's should be increased by sender's balance
    # Проверьте текущий баланс получателя, он должен быть увеличен на баланс отправителя 
    recipient.ensure_balance(balance_recipient + balance_sender)
    # Balance of the sender should be None, because of the contract destroyed
    # Баланс отправителя не должен быть равен нулю, так как контракт уничтожен

    assert eq(None, ts4.get_balance(sender.address))


# Initialize TS4 by specifying where the artifacts of the used contracts are located
# verbose: toggle to print additional execution info
# Инициализируйте TS4, указав, где находятся артефакты используемых контрактов
# подробное описание: переключитесь для печати дополнительной информации о выполнении
ts4.init('contracts/', verbose = True)

test1()

# Ensure we have no undispatched messages
# Убедитесь, что у нас нет неотправленных сообщений
ts4.reset_all()

test2()

ts4.reset_all()

test3()