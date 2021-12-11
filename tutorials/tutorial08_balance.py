"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

'''

    This tutorial shows you how to check the balance
    of accounts with different states.
    Из этого туториала Вы узнаете, как проверить баланс.
    счетов с разными состояниями.

'''


import tonos_ts4.ts4 as ts4

eq = ts4.eq

# Initialize TS4 by specifying where the artifacts of the used contracts are located
# verbose: toggle to print additional execution info
# Инициализировать TS4, указав, где находятся артефакты используемых контрактов
# verbose: переключить на печать дополнительной информации о выполнении
ts4.init('contracts/', verbose = True)

# The address of a non-existing contract
# Адрес несуществующего контракта
empty_account = ts4.Address('0:c4a31362f0dd98a8cc9282c2f19358c888dfce460d93adb395fa138d61ae5069')

# Check balance of non-existing address
# Проверить баланс несуществующего адреса
assert eq(None, ts4.get_balance(empty_account))

default_balance = 100 * ts4.GRAM

# Deploy the contract
# Развернуть контракт
tut08 = ts4.BaseContract('tutorial08', {})

# Сheck balance of the deployed contract. There are 100 grams by default
# Проверить баланс развернутого контракта. По умолчанию 100 грамм
tut08.ensure_balance(default_balance)

# Another way to check the balance of contract
# Еще один способ проверить баланс контракта
assert eq(default_balance, tut08.balance)
