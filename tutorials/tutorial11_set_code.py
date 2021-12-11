"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

'''

    This tutorial demonstrates you how to use the contract code update functionality.
    В этом руководстве показано, как использовать функцию обновления кода контракта.


'''


from tonos_ts4 import ts4
eq = ts4.eq

# Initialize TS4 by specifying where the artifacts of the used contracts are located
# verbose: toggle to print additional execution info
# Инициализируйте TS4, указав, где находятся артефакты используемых контрактов
# подробная информация: переключите, чтобы напечатать дополнительную информацию о выполнении
ts4.init('contracts/', verbose = True)

# Preparing the new contract code
# Подготовка нового кода контракта
code = ts4.load_code_cell('tutorial11_2')

# Deploy the contract and register nickname to be used in the output
# Разверните контракт и зарегистрируйте псевдоним, который будет использоваться в выходных данных
tut11 = ts4.BaseContract('tutorial11_1', {}, nickname = 'Tutorial11')

# Call the getter and ensure that we received correct value
# Позвоните получателю и убедитесь, что мы получили правильное значение
assert eq(21, tut11.call_getter('test'))

# We send the new code to the contract
# Мы отправляем новый код в контракт
tut11.call_method('upgrade', {'code': code})

# Update ABI
# Обновление ABI
ts4.set_contract_abi(tut11, 'tutorial11_2')

# Call the getters from the updated code and ensure that we received correct value:
# modified function of the old contract
# Позвоните получателям из обновленного кода и убедитесь, что мы получили правильное значение:
# изменена функция старого контракта
assert eq(162, tut11.call_getter('test'))
# new function of the new contract
# новая функция нового контракта
assert eq(165, tut11.call_getter('new_func'))
