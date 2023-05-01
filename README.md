<style>
.status {
  display: inline-block;
  padding: 2px 6px;
  color: white;
  border-radius:5%;
  font-weight: bold;
}
.hight {background-color: red;}
.medium {background-color: orange;}
.normal {background-color: green;}
</style>


# Что такое 1cloud ict?
Это терминальная утилита для управления облачными серверами 1cloud, доставки кода проекта на сервера и развертывания окружений на них. Ict придерживается двух базовых принципов:
 - Идемпотентность в работе - действия над серверами не повторяются при множественном обращение к инфраструктурному файлу;
 - Инфраструктурный файл - это единственно верный источник данных для ict. 

При работе через ict все изменения в состояния серверов 1cloud вносятся через инфраструктурный файл, при этом пользователь может вносить любые изменения в состояния серверов через веб-панель 1cloud, но при следующем обращении к инфраструктурному файлу -- состояние серверов будет приведено в соответствие с ним.  

# Как работает ict?
При каждом выполнении команды infra update - ict сравнивает количество, статусы и состояния серверов в Панели 1cloud с параметрами и серверов в инфраструктурном файле, при нахождении расхождений - ict приводит состояния серверов в Панели 1cloud к состоянию серверов в инфраструктурном файле. 

При выполнении команды ifra deploy - ict опять выполнить сравнение состояния серверов в Панели 1cloud с тем, что указано в инфраструктурном файле, если расхождений нет -- будет создан и выполненен инвентаризационный файл Ansible, если расхождения есть -- ict уведомит об этом и запросит подтверждения на изменения состояния серверов в Панели 1cloud. После этого будет выполнен процесс создания и выполнения инвентаризационного файла Ansible.

# Что может ict?
Ict может создавать и удалять виртуальные серверы 1cloud, а также изменять их конфигурацию. Ict может подключаться к серверам по SSH и работать с их окружением: доставлять код проекта на сервер, настраивать окружения и многое другое. Для этого он использует Ansible.

Ict в режиме реального времени собирает статистику по нагрузке на сервера. Делает он это через парсинг данных node_exporter, который устанавливается автоматически после создания сервера с помощью Ansible.

## Что нужно передалать/доделать/сделать:
 - Затащить Pydantic в процессы работы Ansible <span class="status high">High</span>
 - Написать docstrings ко всем функциям, классам, модулям, пакетам <span class="status-high">High</span>
 - Покрыть тестами код <span class="status-high">High</span>
 - Написать playbook для установки node_exporter <span class="status medium">Medium</span>
 - Написать демона, собирающего стату с серверов <span class="status medium">Medium</span>
 - Подумать, как реализовать групповое управление серверами: остановка, запуск, перезагрузка <span class="status medium">Medium</span>
 - Изучить code coveredge <span class="status medium">Medium</span>
 - Подумать, как реализовать работу с сетями <span class="status normal">Normal</span>
 - Продумать систему rollback <span class="status normal">Normal</span>
 - Продумать систему alerts <span class="status normal">Normal</span>
 - Продумать систему sheduling <span class="status normal">Normal</span> 

# Release notes:
## Beta_01
 - Затащил Pydantic модели во все процессы связанные с работой с инфраструктурными шаблонами и 1cloud API
 - Переделал логику работы с инфраструктурным файлом. Теперь есть только одна команда infra update _temp_name_
## Alpha_10:
 - Создал директорию tests;
 - Начал писать тесты для готовых функций;
 - Завел новый раздел для ведения перечня тестов;
 - Зарефачил Self.conf_worker();

## Alpha_09:
 - Удалил класс Deploy, растащив его в класс Sevice, Prepare и Ansible;
 - Создал новый класс Anible;
 - Создал новый класс Prepare;
 - Переделал логику hosts-файла. Теперь он в формате yaml, а ссылки на плейбуки лежат в нём же в виде переменных
## ALpha_08:
 - Переехал в Codespaces: настроил контейнер с Python3.11
 - Перевез проект на Python 3.11
 - Сделал ветку Dev 
## ALpha_07:
 - Убрал циклические зависимости. Теперь экземпляры классов передаются как аргументы. 

 # Tests stage:
 - Service.conf_worker() - complete