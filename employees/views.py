
from django.db.models import OuterRef, Exists
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from employees.models import Employee, Task
from employees.serializers import EmployeeSerializer, TaskSerializer, EmployeeWithTaskSerializer, TaskCreateSerializer, \
    ImportantTasksSerializer


class EmployeeListAPIView(ListAPIView):
    """Класс для вывода всех сотрудников."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveAPIView(RetrieveAPIView):
    """Класс для просмотра детальной информации о сотруднике."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeCreateAPIView(CreateAPIView):
    """Класс для создания сотрудника."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer



class EmployeeUpdateAPIView(UpdateAPIView):
    """Класс для редактирования сотрудников."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDestroyAPIView(DestroyAPIView):
    """Класс для удаления сотрудников."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TaskListAPIView(ListAPIView):
    """Класс для вывода всех задач."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveAPIView(RetrieveAPIView):
    """Класс для просмотра детальной информации о задаче."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCreateAPIView(CreateAPIView):
    """Класс для создания задачи."""
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer



class TaskUpdateAPIView(UpdateAPIView):
    """Класс для редактирования задачи."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyAPIView(DestroyAPIView):
    """Класс для удаления задачи."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_destroy(self, instance):
        """При удалении объекта через DestroyAPIView, тоже убираем задачу из общего числа задач у сотрудника если он
        есть."""
        # Получаю пользователя если он есть
        employee = instance.employee
        if employee:
            employee.task_count -= 1
            employee.save()
        # Выполняем удаление
        super().perform_destroy(instance)


class EmployeeWithTaskListAPIView(ListAPIView):
    """Класс выводит список сотрудников с их задачами и общим количеством задач с возможностью сортировки."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeWithTaskSerializer
    # Сортировка по задачам
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ('task_count',)


class ImportantTasksListAPIView(ListAPIView):
    """Класс, который получает список задач не взятых в работу, но от которых зависят другие задачи и выводит
    {важная задача, срок, фио сотрудника}."""
    # Этот подзапрос создает набор всех дочерних задач, где поле parent_task связано с текущим объектом задачи
    # (используется OuterRef для ссылки на внешний запрос).
    subqueries = Task.objects.filter(parent_task=OuterRef('pk'))

    #  Этот шаг добавляет аннотацию has_children, которая показывает, существуют ли дочерние задачи для текущей задачи.
    #  Если существует хотя бы одна дочерняя задача, то has_children будет True. А также фильтр выбирает только те
    #  задачи, которые являются корневыми и у которых есть хотя бы одна дочерняя задача и нет назначенного сотрудника.
    queryset = Task.objects.annotate(has_children=Exists(subqueries)).filter(has_children=True, employee=None)
    serializer_class = ImportantTasksSerializer
from django.shortcuts import render

# Create your views here.
