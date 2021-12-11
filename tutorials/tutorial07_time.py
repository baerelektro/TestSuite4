"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

'''

    This tutorial demonstrates how you can change the current time that the TVM uses
    В этом руководстве показано, как изменить текущее время, используемое TVM.

'''


import time
import tonos_ts4.ts4 as ts4

eq = ts4.eq

now = int(time.time())
# Initialize TS4: ts4.init(path, verbose = False, time = 0)
# path: set a directory where the artifacts of the used contracts are located
# verbose: toggle to print additional execution info
# time: in seconds. TS4 uses either real-clock or virtual time. Once you set time you switch
#    to virtual time mode, where you can move time to future on your own
# Инициализировать TS4: ts4.init (path, verbose = False, time = 0)
# путь: установить каталог, в котором находятся артефакты используемых контрактов
# verbose: переключить на печать дополнительной информации о выполнении
# время: в секундах. TS4 использует либо реальное, либо виртуальное время. Как только вы установите время, вы переключаете
# в режим виртуального времени, где вы можете самостоятельно перемещать время в будущее
ts4.init('contracts/', verbose = True, time = now)

# Deploy a contract
# Развернуть контракт
tut07 = ts4.BaseContract('tutorial07', {})

# Call the getter and ensure that the required time has not yet arrived
# Вызвать геттер и убедиться, что необходимое время еще не пришло
assert eq(False, tut07.call_getter('isUnlocked'))

DAY = 86400
# Fast forward 7 days
# Перемотаем вперед на 7 дней
one_week_later = now + 7 * DAY
ts4.core.set_now(one_week_later)

# Ensure that the time was rewound correctly
# Убедитесь, что время было перемотано правильно
assert eq(ts4.core.get_now(), one_week_later)

# ... and ensure that the required time has come
# ... и убедитесь, что нужное время пришло
assert eq(True, tut07.call_getter('isUnlocked'))

# P.S. Traveling into the future is easy. Isn't it?
# PS Путешествовать в будущее легко. Не так ли?
