# Что эта штука уже умеет делать: 
- Создавать серверы по инфраструктурнуму шаблону
- Удалять серверы по инфраструктурнуму шаблону
- Изменяет конфигурацию сервер только на увелечение (нельзя уменьшат размер HDD)
- Умеет создавать inventory.ini и запускать Ansible по указанным плейбукам в инфраструктурном шаблоне

# Release notes:
## ALpha_08:
 - Переехал в Codespaces: настроил контейнер с Python3.11
 - Перевез проект на Python 3.11
 - Сделал ветку Dev 
## ALpha_07:
 - Убрал циклические зависимости. Теперь экземпляры классов передаются как аргументы. 