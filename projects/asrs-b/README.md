# ASRS-B - local project workspace

Локальная рабочая папка проекта по автоматизированному хранению ящиков. Оригинальные требования и загруженные сторонние учебные файлы сохранены рядом, но исключены из Git: репозиторий публичен, а разрешение на публикацию данных заказчика и перераспространение вложений форума не проверялось.

## С чего начать

1. Прочитайте `customer-requirements.txt` и листы 2, 3, 6–14 файла `customer-layout-ASRS-B.pdf`.
2. Измерения PDF справочные. Перед точным масштабированием запросите исходный CAD/подтверждённые размеры.
3. Откройте `references/forum/PM-Process-10x5.vcmx` в отдельной копии VC как учебный пример, затем соответствующий XLSX. Не используйте пример сразу как производственную модель: в обсуждении автор сообщает, что `AssignProcess` и `Machine` являются пользовательскими statements.
4. Используйте `references/forum/PythonProcessHandlerExample.vcmx` для изучения обработчика процесса; совместимость с вашей сборкой VC нужно подтвердить.
5. Для API миссий смотрите `references/forum/PM-Missions-Reference.pdf`; `Quick-Start-Visual-Components.pdf` — общий учебник старой версии, поэтому его Python-примеры требуют проверки на совместимость.
6. Следуйте плану из `model-plan.md`. Создайте layout в `layout/` после подтверждения исходных данных.

## Статус

Здесь подготовлено окружение проекта и собраны учебные материалы. Модель ASRS-B ещё не создана; все исходные значения и допущения указаны в требованиях и плане. Точная версия установленной сборки VC не зафиксирована.

## Вложения форума

| Файл | Для чего пригодится | Источник |
|---|---|---|
| `PM-Process-10x5.vcmx`, `PM-Process-10x5.xlsx` | Маленький пример генерации связей/последовательностей из Excel | [Тема форума и предупреждение о custom statements](https://forum.visualcomponents.com/t/auto-transport-links-and-sequences-in-pm/6443) |
| `PM-Process-600x20.vcmx`, `PM-Process-600x20.xlsx` | Более крупный пример той же схемы | [Тема форума](https://forum.visualcomponents.com/t/auto-transport-links-and-sequences-in-pm/6443) |
| `PythonProcessHandlerExample.vcmx` | Образец собственного обработчика процесса | Вложение в [обсуждении примера](https://forum.visualcomponents.com/t/auto-transport-links-and-sequences-in-pm/6443) |
| `PM-Missions-Reference.pdf` | Collect/Deliver/Move/Wait, маршруты и миссии мобильного ресурса | [Справочник](https://forum.visualcomponents.com/uploads/short-url/jFUC2tu9xJsvTTvCgustZNMai1a.pdf) |
| `Quick-Start-Visual-Components.pdf` | Базовые понятия layouts, behaviors, joints и скриптов | [Руководство форума](https://forum.visualcomponents.com/uploads/short-url/5kI3XBDB7t99tnBeL3SmOgjoEcu.pdf), версия материала устарела |

## Важно про версии

Пример Process Modeling содержит пользовательские statements; они не гарантированно присутствуют в штатной библиотеке. Quick Start описывает старый Python 2.7. В VC 5.0 заявлен Python 3. При работе ориентируйтесь на версию приложения, в которой реально запускается ваша модель, и документацию именно этой версии.
