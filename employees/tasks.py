
from celery import shared_task

from employees.models import Employee, Task

from django.db.models import OuterRef, Exists


@shared_task
def assignment_tasks_to_employees():
    """Автоматическое распределение задач между сотрудниками"""
    subqueries = Task.objects.filter(parent_task=OuterRef('pk'))
    tasks = Task.objects.annotate(has_children=Exists(subqueries)).filter(has_children=True, employee=None)
    for task in tasks:
        # Получил сотрудника с минимальным количеством задач
        employee_with_minimum_number_of_tasks = Employee.objects.order_by('task_count').first()

        # Проверяю есть ли у задачи ещё одна родительская задача
        if task.parent_task is not None:

            # получаю эту родительскую задачу и через неё нахожу сотрудника выполняющего её(если он есть)
            parent_task = Task.objects.get(pk=task.parent_task.pk)
            try:
                employee_performing_parent_task = Employee.objects.get(pk=parent_task.employee.pk)

                # Сравниваю у кого сколько задач и если у сотрудника выполняющего родительскую задачу задач максимум на 2
                # больше чем у наименее загруженного сотрудника, то отдаю сотруднику выполняющего родительскую задачу
                if employee_performing_parent_task.task_count - employee_with_minimum_number_of_tasks.task_count <= 2:

                    # Обновляю данные по количеству задач у пользователя
                    new_number_of_tasks = employee_performing_parent_task.task_count +1
                    employee_performing_parent_task.task_count = new_number_of_tasks
                    employee_performing_parent_task.save()

                    # Назначаю задаче нового пользователя
                    task.employee = employee_performing_parent_task
                    task.save()

                # если наоборот, то отдаю задачу наименее загруженному сотруднику
                else:

                    # Обновляю данные по количеству задач у пользователя
                    new_number_of_tasks = employee_with_minimum_number_of_tasks.task_count + 1
                    employee_with_minimum_number_of_tasks.task_count = new_number_of_tasks
                    employee_with_minimum_number_of_tasks.save()

                    # Назначаю задаче нового пользователя
                    task.employee = employee_with_minimum_number_of_tasks
                    task.save()

            except Exception as e:

                # Обновляю данные по количеству задач у пользователя
                new_number_of_tasks = employee_with_minimum_number_of_tasks.task_count + 1
                employee_with_minimum_number_of_tasks.task_count = new_number_of_tasks
                employee_with_minimum_number_of_tasks.save()

                # Назначаю задаче нового пользователя
                task.employee = employee_with_minimum_number_of_tasks
                task.save()

        else:
            # Обновляю данные по количеству задач у пользователя
            new_number_of_tasks = employee_with_minimum_number_of_tasks.task_count + 1
            employee_with_minimum_number_of_tasks.task_count = new_number_of_tasks
            employee_with_minimum_number_of_tasks.save()
            # Назначаю задаче нового пользователя
            task.employee = employee_with_minimum_number_of_tasks
            task.save()
            print(employee_with_minimum_number_of_tasks.full_name)
    print('Важных задач больше нет')
