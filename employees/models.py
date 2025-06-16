from django.db import models

class Employee(models.Model):
    """Модель сотрудника."""
    full_name = models.CharField(max_length=50, verbose_name='ФИО')
    post = models.CharField(max_length=35, verbose_name='Должность')
    task_count = models.PositiveIntegerField(verbose_name='Количество задач сотрудника', default=0)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.full_name}'


class Task(models.Model):
    """Модель задачи."""
    title = models.CharField(max_length=50, verbose_name='Название')
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, verbose_name='Исполнитель',
                                 related_name='employee_task', null=True, blank=True)
    date = models.DateField(verbose_name='До какого числа нужно выполнить')
    status = models.BooleanField(default=False, verbose_name='Статус False - задача выполняется, статус True - задача'
                                                             'выполнена')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.title}'
