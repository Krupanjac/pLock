# pLock - Тајмер Апликација

Једноставна апликација за управљање временом током презентација или квизова.

![pLock Screenshot](assets/screenshot.png)

## Садржај
- [Инсталација](#инсталација)
- [Употреба](#употреба)
- [Подешавања](#подешавања)
- [Пречице](#пречице)
- [Лиценца](#лиценца)

## Инсталација

1. **Обавезни предуслови**:
   - Python 3.x
   - Tkinter (обично већ инсталиран са Python-ом)
   - Pillow библиотека:  
     ```bash
     pip install Pillow
     ```

2. **Фонт**:
   - Преузмите фонт [DS-Digital](https://www.dafont.com/ds-digital.font)
   - Креирајте фолдер `fonts` у пројекту
   - Поставите `DS-DIGIT.ttf` у `fonts` фолдер

3. **Слике**:
   - Креирајте фолдер `assets` са следећим фајловима:
     - `replika.png` (60с)
     - `pitanje.png` (90с)
     - `novarec.png` (120с)
     - `tehnickareplika.png` (30с)

## Употреба

### Основне функције
- **Тајмер ТАЧКА ДНЕВНОГ РЕДА** (лево):
  - Подразумевано 20:00
  - Кликом на време ресетује се на почетну вредност
  - "Паузирај/Настави" дугме

- **Тајмер ДИЈАЛОГ** (десно):
  - Поставља се пречицама 1-4
  - "Паузирај Т2/Настави Т2" дугме

### Опције (дугмад 1-4):
1. **Реплика** - 60 секунди
2. **Питање** - 90 секунди 
3. **Нова Реч** - 120 секунди
4. **Техничка Реплика** - 30 секунди

Прелазом миша преко дугмета приказује се назив опције.

## Подешавања

Приступ преко дугмета „Подешавања“:
- Промена почетног времена за Тајмер А
- Измена трајања за сваку опцију
- Све промене се примењују одмах

## Пречице

- **1-4**: Покретање одговарајуће опције
- **Клик на Тајмер А**: Ресетовање
- **ALT + F4**: Затварање апликације

## Лиценца

Овај пројекат је лиценциран под MPL-2.0 лиценцом. Погледајте [LICENSE](LICENSE) фајл за детаље.
