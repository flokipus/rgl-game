# rgl-game

Тестовый проект для изучения архитектурных аспектов написания ПО.
Игра планировалась как пошаговая rogue-like rpg.

Пара мыслей про код (посвящается будущему себе).

## Мысль 1: об MVC
В какой-то момент дошел до идеи использования паттерна MVC. Интересно, что в книге Nystrom "Game Programming Patterns" про эту модель сказано очень вскользь.
Для своих нужд (прежде всего научно-исследовательско-эстетических) реализовал паттерн несколько неклассически: вместо того, чтобы у Model был слушатель View, которого Model оповещает, когда что-то произошло, я решил сделать более явно. 

А именно, Model содержит в себе всю логику игрового мира (tile-карту мира, всех сейчас обитающих на нем монстров, различных препятствий на карте, etc). 
Кроме того, Model содержит вспомогательный объект для обработки цикла ходов. В Model'и обрабатывает один полный цикл ходов: обрабатывается ход персонажа пользователя, затем, если этот ход непустой (т.е. был соответствующий input от пользователя), обрабатываются все ходы неигровых персонажей (npc) (соответственно, если input'а не было, то ничего не происходит -- ждем; все как в классических rogue-like). 

После того, как все ходы обработаны, Model выдает список Event'ов, т.е. произошедших событий. Эти события (хранящиеся списком) теперь должен "применить" View. Таким образом, View как бы догоняет Model. 

Если по простому и картинкой:

Model ----> List[Event] ----> View


Использование именно списка событий вроде бы дает некоторые преимущества, например, если все персонажи в области видимости сделали ход-движение в соседний тайл, то View может отрисовывать их анимации одновременно, что экономит время игрока (представьте себе, что бы было, если бы условные 20 npc ходили по очереди по 0.2 секунды (например, столько будет занимать время анимации их движения) после того, как игрок всего лишь шагнул к магазину в безопасном городе 100x100 тайлов).

С другой стороны, если обновления картинок "тяжелые" (например, все ходы npc -- это атаки, а каждая атака=просчитывание AI оптимального хода, что может занимать чувствительное количество процессорных тактов), то список может затормозить геймплей: после input'а пользователя может появиться чувствительный лаг. Если бы все было последовательно (один ход -- один notify), то лаг можно было бы замаскировать анимацией (View же у нас будет работать в другом потоке, так?). 
В rogue-like, по идее, таких тяжелых ходов быть не должно :)

С третьей стороны, второй подход выглядит лучше: View может обрабатывать события в режиме "как можно быстрее", так что если группа неписей всего лишь подвинулись с одного тайла на другой, это заняло не так много процессорного времени и уместилось в один игровой фрейм. 


На момент 19 апреля: во-первых, интуитивно использование такой мутировавшей версии паттерна "распутывает код". Можно не думать про то, как все будет отрисовываться. Плюс, это позволит (возможно) в дальнейшем использование Machine learning для обкатки баланса. View можно просто выкинуть и использовать Model для расчета итогов боя (кто кого убил).


## Мысль 2: паттерн command

Казалось бы, удобным с точки зрения разработки был бы паттерн command. Как сделано сейчас: View обрабатывает пользовательский InputDevice (в моем случае -- это клавиатура), передает пользовательскую команду Controller'у (для простоты, пусть пользователь нажал клавишу 'D', которая проинтерпретировалась View как команда "MoveRight"). 

Затем Controller получает от View команду "MoveRight" и просит Model "подвинуть главного персонажа вправо" (на данный момент, Controller просто append'ит команду в буффер команд для пользовательского персонажа).

Затем уже Model начинает интерпретировать команду "подвинуть главного персонажа вправо" в реальное для нее действие: например, если справа от персонажа находится монстр, то персонаж должен не перепеститься в соответствующий тайл, а ударить монстра!

В свете указанного получается следующая проблема. Команд может быть много: MoveRight, MoveLeft, JumpRight, JumpLeft, SwingBySwordLeft, etc. Интерпретации команд  сложные с кучами if-ветвений: а что если в тайле монстр, а что если персонаж оглушен, а что если персонаж лежит на земле/лаве/в воде/где-нибудь еще, ...
Получается, что метод Model.command2event (тот самый метод, который должен будет получить команду и преобразовать, или "проинтерпретировать" ее в событие, то есть в то, что реально должно произойти, например "атака монстра в соседнем тайле") станет этаким суперметодом с кучей if-ов, с кучей проверок и пр.

Чтобы этого не было можно сделать так: у Controller будет ассоциативный массив, ключи которого -- команды View ("MoveRight", "MoveLeft", ...), а значениями будут являться callback-и. Эти коллбеки будут реализацией соответствующего command2event. На вход такой callback должен будет получить Model и gameobject, которому этот callback адресован (в рассмотренном нами примере, это пользовательский персонаж; но точно также можно применить этот подход и для npc, просто команды будет поставлять не View, а соответствующий AI (и не через контроллер, само собой)).

Итого, псевдокодом:
```
user_command = View.get_user_command()
backend_command = Controller.backend_commands[user_command]
Model.handle_command(backend_command),
```
где
```
class BackendCommand:
  def command2event(self, model: Model, gobj: GameObject) -> List[Event]: ...
 ```
