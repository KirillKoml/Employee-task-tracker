
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from employees.models import Employee, Task


class EmployeeSerializer(ModelSerializer):
    """Сериализатор для сотрудников."""
    class Meta:
        model = Employee
        fields = '__all__'


class TaskSerializer(ModelSerializer):
    """Сериализатор для задач, кроме создания."""
    def validate_status(self, value):
        """Проверка, если задачу отредактировали и поставили в статус True, удаляю задачу и вычёркиваю её из общего
        числа задач сотрудника."""
        if value:
            employee = Employee.objects.get(full_name=self.instance.employee)
            employee.task_count -= 1
            employee.save()
            self.instance.delete()
            raise serializers.ValidationError("Экземпляр модели был удалён, потому что задача выполнена.")
        return value

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(ModelSerializer):
    """Сериализатор для создания задач."""
    def validate_status(self, value):
        """Проверка на то, что статус у задачи - False."""
        if value:
            raise serializers.ValidationError("Поле 'status' не может быть True при создании задачи.")
        return value

    def validate_employee(self, value):
        """Проверка на то, назначили ли задаче при создании сотрудника или нет."""
        if value:
            employee = Employee.objects.get(full_name=value)
            employee.task_count += 1
            employee.save()
        return value

    class Meta:
        model = Task
        fields = '__all__'


class EmployeeWithTaskSerializer(ModelSerializer):
    """Сериализатор для сотрудников, который дополнительно выводит список их задач."""
    task = SerializerMethodField()

    def get_task(self, employee):
        """Метод для получения задач сотрудника."""
        return [task.pk for task in Task.objects.filter(employee=employee.pk)]

    class Meta:
        model = Employee
        fields = '__all__'


class ImportantTasksSerializer(ModelSerializer):
    """Сериализатор для важных задач."""
    employee = SerializerMethodField()

    def get_employee(self, task):
        """Метод для поиска сотрудника для задачи."""
        # Получил сотрудника с минимальным количеством задач
        employee_with_minimum_number_of_tasks = Employee.objects.order_by('task_count').first()

        # Проверяю есть ли у задачи ещё одна родительская задача
        if task.parent_task is not None:

            # получаю эту родительскую задачу и через неё нахожу сотрудника выполняющего её(если он есть)
            parent_task = Task.objects.get(pk=task.parent_task.pk)
            try:
                employee_performing_parent_task = Employee.objects.get(pk=parent_task.employee.pk)

                # Сравниваю у кого сколько задач и если у сотрудника выполняющего родительскую задачу задач максимум на
                # 2 больше чем у наименее загруженного сотрудника, то отдаю сотруднику выполняющего родительскую задачу
                if employee_performing_parent_task.task_count - employee_with_minimum_number_of_tasks.task_count <= 2:
                    return employee_performing_parent_task.full_name

                # если наоборот, то отдаю задачу наименее загруженному сотруднику
                else:
                    return employee_with_minimum_number_of_tasks.full_name

            except Exception as e:
                return employee_with_minimum_number_of_tasks.full_name

        else:
            return employee_with_minimum_number_of_tasks.full_name

    class Meta:
        model = Task
        fields = ('title', 'date', 'employee')
