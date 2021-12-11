"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

'''

    This tutorial demonstrates how a contract can deploy another contract.
    Besides, it shows how these contract can be accessed via wrappers.
    В этом руководстве показано, как контракт может развернуть другой контракт.
    Кроме того, он показывает, как к этим контрактам можно получить доступ через обертки.

'''


from tonos_ts4 import ts4

eq = ts4.eq

# Initialize TS4 by specifying where the artifacts of the used contracts are located
# verbose: toggle to print additional execution info
# Инициализируйте TS4, указав, где находятся артефакты используемых контрактов
# подробная информация: переключите, чтобы напечатать дополнительную информацию о выполнении
ts4.init('contracts/', verbose = True)

# Load code and data of the second contract
# Загрузить код и данные второго контракта
code = ts4.load_code_cell('tutorial05_2.tvc')
data = ts4.load_data_cell('tutorial05_2.tvc')

# Register ABI of the second contract in the system beforehand
# Заранее зарегистрируйте ABI второго контракта в системе
ts4.register_abi('tutorial05_2')

# Deploy the first contract and register nickname to be used in the output
# Разверните первый контракт и зарегистрируйте псевдоним, который будет использоваться в выходных данных
contract1 = ts4.BaseContract('tutorial05_1', dict(code = code, data = data), nickname = 'Parent')

zero_address = ts4.Address('0:' + '0'*64)
assert eq(zero_address, contract1.call_getter('m_address'))

# Ask contract1 to deploy contract2 with a given key
# Попросите контракт 1 развернуть контракт 2 с заданным ключом
contract1.call_method('deploy', dict(key = 123))

# Fetch the address of the contract to be deployed
# Получить адрес контракта, который будет развернут
address2 = contract1.call_getter('m_address')
ts4.Address.ensure_address(address2)

# We register nickname for this contract so see it in the verbose output
# Мы регистрируем псевдоним для этого контракта, так что смотрите его в подробном выводе
ts4.register_nickname(address2, 'Child')

print('Deploying at {}'.format(address2))

# Dispatch unprocessed messages to actually construct a second contract
# Отправка необработанных сообщений для фактического создания второго контракта
ts4.dispatch_messages()

# At this point contract2 is deployed at a known address,
# so we create a wrapper to access it.
# На данный момент контракт 2 развернут по известному адресу,
# итак, мы создаем оболочку для доступа к ней.
contract2 = ts4.BaseContract('tutorial05_2', ctor_params = None, address = address2)

# Ensure the second contract has correct key and balance
# Убедитесь, что второй контракт имеет правильный ключ и баланс
assert eq(123, contract2.call_getter('m_key'))
assert eq(1_000_000_000, contract2.balance)
