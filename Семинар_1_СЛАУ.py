# -*- coding: utf-8 -*-
"""СЛАУ.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/sw-shar/552e296fddba4bae583b27a41f01bc34/.ipynb

# Прямы и итерационные методы решения СЛАУ

Как правило, при решении большинства практических задач задача решения систем
линейных алгебраических уравнений (СЛАУ) встречается в виде некоторой вспомогательной подзадачи. Стоит заметить, что современные суперкомпьютеры тратят примерно 80% своего рабочего времени именно на численное решение СЛАУ, что ещё раз подчёркивает важность данной темы.

[МФТИ](https://mipt.ru/upload/medialibrary/e9b/norms.pdf) + [МФТИ](https://mipt.lectoriy.ru/file/synopsis/pdf/Maths-NumAnalysis-M02-Lobanov-140910.03.pdf) + [ИНТУИТ](https://intuit.ru/studies/courses/1012/168/lecture/4592) + [maxis42](https://notebook.community/maxis42/ML-DA-Coursera-Yandex-MIPT/1%20Mathematics%20and%20Python/Lectures%20notebooks/9%20vector%20operations/vector_operations)

Методы решения систем алгебраических уравнений можно разделить
на два класса:
* **Прямые методы**. Данные методы позволяют получить точное
решение задачи (без учета ошибок округления) за конечное число
арифметических действий.
* **Итерационные методы** или методы последовательных
приближений. Позволяют вычислять последовательность
векторов x (n) , которая при n → ∞ сходится к решению задачи. На
практике используют некоторое конечное приближение в
зависимости от допустимого уровня погрешности.

**Рассмотрим Итерационные методы**

Приближенные алгоритмы затем и нужны чтобы при решении матриц - уменьшить асимтотическую сложность. Потому что перемножение матриц - это $$N^3$$ операций.А при использовании метода например Якоби иожно уменишьть сложность операции до $$n^2$$

## Введем норму вектора
"""

import pandas as pd
import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import cdist

# Алгоритмы линейной алгебры
import scipy.linalg as sla

# Библиотека для работы с разреженными матрицами
import scipy.sparse as sps

# Алгоритмы линейной алгебры для разреженных матриц
import scipy.sparse.linalg as spla

#Широкий набор специальных математических функций
from scipy import special

"""В пространстве V каждому вектору x∈V ставим в соответствие некоторое неотрицательное число  так, чтобы для произвольных векторов x,y ∈V и произвольного скаляра λ выполнялись следующие условия:

тогда и только тогда, когда x=0.
.
(неравенство треугольника).
называется нормой (длиной, модулем) вектора x∈V .

Примеры норм в линейных пространствах

* **m-норма** - максимальное по модулу значение вектора (кубическая)
"""

abs(V).max()

"""* p-норма
p-норма (норма Гёльдера) для вектора $x = (x_{1}, \dots, x_{n}) \in \mathbb{R}^{n}$ вычисляется по формуле:

$$ \left\Vert x \right\Vert_{p} = \left( \sum_{i=1}^n \left| x_{i} \right|^{p} \right)^{1 / p},~p \geq 1. $$
В частных случаях при:

$p = 1$ получаем $\ell_{1}$ норму
$p = 2$ получаем $\ell_{2}$ норму

$\ell_{1}$ норма (также известная как **манхэттенское расстояние или октаэдрическая**) для вектора $x = (x_{1}, \dots, x_{n}) \in \mathbb{R}^{n}$ вычисляется по формуле:

$$ \left\Vert x \right\Vert_{1} = \sum_{i=1}^n \left| x_{i} \right|. $$
Ей в функции numpy.linalg.norm(x, ord=None, ...) соответствует параметр ord=1
"""

a = np.array([-1, 2, -1])
norm(a, ord=1)

"""$\ell_{2}$ норма
$\ell_{2}$ норма (также известная как **евклидова норма**) для вектора $x = (x_{1}, \dots, x_{n}) \in \mathbb{R}^{n}$ вычисляется по формуле:

$$ \left\Vert x \right\Vert_{2} = \sqrt{\sum_{i=1}^n \left( x_{i} \right)^2}. $$
Ей в функции numpy.linalg.norm(x, ord=None, ...) соответствует параметр ord=2.

1.   Новый пункт
2.   Новый пункт


"""

print('L2 норма вектора a:\n', norm(a, ord=2))

"""## Расстояние межу векторами

Для двух векторов $x = (x_{1}, \dots, x_{n}) \in \mathbb{R}^{n}$ и $y = (y_{1}, \dots, y_{n}) \in \mathbb{R}^{n}$ $\ell_{1}$ и $\ell_{2}$ раccтояния вычисляются по следующим формулам соответственно:

$$ \rho_{1}\left( x, y \right) = \left\Vert x - y \right\Vert_{1} = \sum_{i=1}^n \left| x_{i} - y_{i} \right| $$$$ \rho_{2}\left( x, y \right) = \left\Vert x - y \right\Vert_{2} = \sqrt{\sum_{i=1}^n \left( x_{i} - y_{i} \right)^2}. $$
"""

a = np.array([1, 2, -3])
b = np.array([-4, 3, 8])

print('L1 расстояние между векторами a и b:\n', norm(a - b, ord=1))

print('L2 расстояние между векторами a и b:\n', norm(a - b, ord=2))

"""Скалярное произведение в пространстве $\mathbb{R}^{n}$ для двух векторов $x = (x_{1}, \dots, x_{n})$ и $y = (y_{1}, \dots, y_{n})$ определяется как:

$$ \langle x, y \rangle = \sum_{i=1}^n x_{i} y_{i}. $$
Скалярное произведение двух векторов можно вычислять с помощью функции numpy.dot(a, b, ...) или метода vec1.dot(vec2), где vec1 и vec2 — исходные векторы.
"""

print('Скалярное произведение a и b (через функцию):', np.dot(a, b))

"""Длиной вектора $x = (x_{1}, \dots, x_{n}) \in \mathbb{R}^{n}$ называется квадратный корень из скалярного произведения, то есть длина равна евклидовой норме вектора:

$$ \left| x \right| = \sqrt{\langle x, x \rangle} = \sqrt{\sum_{i=1}^n x_{i}^2} = \left\Vert x \right\Vert_{2}. $$
Теперь, когда мы знаем расстояние между двумя ненулевыми векторами и их длины, мы можем вычислить угол между ними через скалярное произведение:

$$ \langle x, y \rangle = \left| x \right| | y | \cos(\alpha) \implies \cos(\alpha) = \frac{\langle x, y \rangle}{\left| x \right| | y |}, $$
где $\alpha \in [0, \pi]$ — угол между векторами $x$ и $y$.
"""

cos_angle = np.dot(a, b) / norm(a) / norm(b)
print( 'Косинус угла между a и b:', cos_angle)
print( 'Сам угол:', np.arccos(cos_angle))

"""## Норма матриц

Различают несколько норм матрицы, например:
1. ∞–норма матрицы – это максимальная сумма модулей элементов каждой из строк матрицы: 

2. 1-норма – это максимальная сумма модулей элементов каждого из столбцов матрицы: 

3. 2-норма (евклидова норма) – длина вектора в n-мерном пространстве (корень суммы квадратов всех элементов матрицы):
"""

A_1=np.arange(12).reshape(3,4)

print(A_1)
print('1-норма матрицы',np.linalg.norm(A_1, ord=1))

print('евклидова норма матрицы',np.linalg.norm(A_1, ord=2))

"""## Обусловленность задачи

посмотрим как меняет небольшое изменение в данных на решение линейного уравнения
"""

L = np.array([[1, 0], [10**20, 1]])
U = np.array([[10**(-20), 1], [0, 1-10**20]])

L_bad = np.array([[1., 0], [10**20, 1.]])
U_bad = np.array([[10**(-20), 1.], [0, 1.-10**20]])

print(L.dot(U))
print(L_bad.dot(U_bad))

"""Очевидно, значение последнего элемента неправильно во втором случае, когда все вычисления делаются в плавающих точках.

В первом случае часть вычислений делается в целых числах (возможно, в bigint), то есть абсолютно точно. Погрешность же вычислений с плавающей точкой \approx 10^{-17}≈10 
−17
 , и там неверен даже последний элемент матрицы UU, в нём теряется слагаемое 11.

Отметим, что в реальных вычислениях матричные элементы почти наверняка с самого начала будут числами с плавающей точкой (а не целыми).

Система уравнений считается хорошо обусловленной, если малые изменения в коэффициентах
матрицы или в правой части вызывают малые изменения в решении.

Система уравнений считается плохо обусловленной, если малые изменения в коэффициентах
матрицы или в правой части вызывают большие изменения в решении.
"""

# Пусть решается система
from scipy.linalg import svd
import numpy as np

A = np.array([[10,9],[9,8]])
V = np.array([19.,17]) # вектор ответов

"""
причем матрица известна точно, а правая часть получена округлением
до целого (погрешность не более 3%). Посмотрим, на какую точность
можно рассчитывать при решении системы.
Отметим, что определитель матрицы det A = 10 · 8 − 9
2 = −1 6= 0. С
точки зрения линейной алгебры, проблем при решении данной
системы не должно быть.

Фактически, при решении системы мы пытаемся разложить вектор
* f = (19, 17)
T по базису из векторов
* e1 = (10, 9)
* e2 = (9, 8)
"""

np.linalg.solve(A, V)

np.linalg.norm((A), ord=2)

A = np.array([[10,9],[9,8]])
V = np.array([18.9,17.1]) # вектор ответов

np.linalg.solve(A, V)

"""**Задача оказалась плохо обусловленной**

Сравнительно небольшие возмущения системы уравнений привели к существенным отклонениям в решении.
Обусловленность задачи не связана с конкретным численным
методом, это неустранимая ошибка. Существуют способы снижения
погрешности, вызванной плохой обусловленностью:
*  Каким-то образом перейти к хорошо обусловленной
эквивалентной системе.
*  Повысить точность определения коэффициентов СЛАУ и правой
части.
Плохо обусловленные системы являются обобщением понятия
вырожденных систем. Системы «близкие» к вырожденным скорее
всего будут плохо обусловлены.

"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

soa = np.array([[0, 0, 10, 9], [0, 0, 9, 8]])
X, Y, U, V = zip(*soa)
plt.figure()
ax = plt.gca()
ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1)
ax.set_xlim([-1, 10])
ax.set_ylim([-1, 10])
plt.draw()
plt.show()

"""**Числом обусловленности матрицы - μ** важное соотношение, показывающее, на сколько возрастают относительные ошибки решения СЛАУ в случае наличия относительных ошибок при задании правых частей и элементов матриц.

Число обусловленности cond (A) является количественной оценкой обусловленности. Отметим, что всегда cond (A) ≥ 1. Если 3 cond (A) ≥ 1000 , то говорят, что матрица А плохо обусловлена. Если 1 ≤ cond(A) ≤ 100, то матрица считается хорошо обусловленной. 

Как правило, если число обусловленности $$(f)=10^{k}$$, то вы можете потерять до **k** цифр точности сверх того, что будет потеряно для числового значения из-за потери точности из арифметических методов.

Однако число обусловленности не дает точного значения максимальной погрешности, которая может возникнуть в алгоритме. Обычно это просто ограничивает его оценкой (чье вычисленное значение зависит от выбора нормы для измерения погрешности).Учитывая, что $$ μ (A) >=1$$, то наилучшим числом обусловленности является 1.
"""

np.linalg.cond(A)
