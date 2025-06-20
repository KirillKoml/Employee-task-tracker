
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee, Task


class EmployeeTestCase(APITestCase):
    """Тесты для CRUD сотрудников."""
    def setUp(self):
        """Создаю пользователя для тестов."""
        self.employee = Employee.objects.create(full_name='test_1', post='test_1')

    def test_employee_create(self):
        """Тест на создание пользователя."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:employee-create')

        # Act(совершаю действие которое тестирую)
        data = {'full_name': 'test_2', 'post': 'test_2'}
        response = self.client.post(url, data)

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Employee.objects.all().count(), 2
        )

    def test_employee_update(self):
        """Тест на обновление пользователя."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:employee-update', args=(self.employee.pk,))

        # Act(совершаю действие которое тестирую)
        data = {'full_name': 'test_new'}
        response = self.client.patch(url, data)
        data = response.json()

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('full_name'), 'test_new'
        )

    def test_employee_delete(self):
        """Тест на удаление пользователя."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:employee-destroy', args=(self.employee.pk,))

        # Act(совершаю действие которое тестирую)
        response = self.client.delete(url)

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Employee.objects.all().count(), 0
        )

    def test_employee_retrieve(self):
        """Тест на детальный просмотр пользователя."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:employee-retrieve', args=(self.employee.pk,))

        # Act(совершаю действие которое тестирую)
        response = self.client.get(url)
        data = response.json()

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('full_name'), self.employee.full_name
        )

    def test_employee_list(self):
        """Тест на просмотр всех пользователей."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:employee-list')

        # Act(совершаю действие которое тестирую)
        response = self.client.get(url)

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = [
            {
                "id": self.employee.pk,
                "full_name": self.employee.full_name,
                "post": self.employee.post,
                "task_count": self.employee.task_count
            }
        ]
        data = response.json()
        self.assertEqual(
            data, result
        )


class TaskTestCase(APITestCase):
    """Тесты для CRUD задач."""
    def setUp(self):
        """Создаю пользователя и задачу для тестов."""
        self.employee = Employee.objects.create(full_name='test_1', post='test_1', task_count=1)
        self.task = Task.objects.create(title='test_1', employee=self.employee, date='2024-02-02')

    def test_employee_create(self):
        """Тест на создание задачи и добавление +1 к списку задач сотрудника, к которому относится эта задача."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:task-create')

        # Act(совершаю действие которое тестирую)
        data = {'title': 'test_2', 'parent_task': self.task.pk, 'employee': self.employee.pk, 'date': '2024-02-02'}
        response = self.client.post(url, data)

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Task.objects.all().count(), 2
        )
        self.assertEqual(
            Employee.objects.get(pk=self.employee.pk, task_count=2), self.employee
        )

    def test_task_update(self):
        """Тест на обновление задачи."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:task-update', args=(self.task.pk,))

        # Act(совершаю действие которое тестирую)
        data = {'title': 'test_new'}
        response = self.client.patch(url, data)
        data = response.json()

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'test_new'
        )

    def test_task_delete(self):
        """Тест на удаление задачи с проверкой, что и у пользователя назначенного на эту задачу она удаляется."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:task-destroy', args=(self.task.pk,))

        # Act(совершаю действие которое тестирую)
        response = self.client.delete(url)

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Task.objects.all().count(), 0
        )
        self.assertEqual(
            Employee.objects.get(pk=self.employee.pk, task_count=0), self.employee
        )

    def test_task_retrieve(self):
        """Тест на детальный просмотр задачи."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:task-retrieve', args=(self.task.pk,))

        # Act(совершаю действие которое тестирую)
        response = self.client.get(url)
        data = response.json()

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.task.title
        )

    def test_task_list(self):
        """Тест на просмотр всех задач."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:task-list')

        # Act(совершаю действие которое тестирую)
        response = self.client.get(url)

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = [
            {
                "id": self.task.pk,
                "title": self.task.title,
                "date": self.task.date,
                "status": self.task.status,
                "parent_task": self.task.parent_task,
                "employee": self.task.employee.pk
            }
        ]
        data = response.json()
        self.assertEqual(
            data, result
        )


class EmployeeWithTaskTestCase(APITestCase):
    """Тесты для контроллера, который выводит список сотрудников с их задачами и общим количеством задач с возможностью
    сортировки."""
    def setUp(self):
        """Создаю пользователя и задачу для тестов."""
        self.employee = Employee.objects.create(full_name='test_1', post='test_1')
        self.task = Task.objects.create(title='test_1', employee=self.employee, date='2024-02-02')

    def test_employee_with_task_list(self):
        """Тест на просмотр списка сотрудников с их задачами и общим количеством задач."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:employee_with_task-list')

        # Act(совершаю действие которое тестирую)
        response = self.client.get(url)

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = [
            {
                "id": self.employee.pk,
                "task": [
                    self.task.pk
                ],
                "full_name": self.employee.full_name,
                "post": self.employee.post,
                "task_count": self.employee.task_count
            }
        ]
        data = response.json()
        self.assertEqual(
            data, result
        )


class ImportantTasksTestCase(APITestCase):
    """Тесты для контроллера, который получает список задач не взятых в работу, но от которых зависят другие задачи и
    выводит {важная задача, срок, фио сотрудника}."""
    def setUp(self):
        """Создаю 2 пользователя и 2 группы из задач:
        1. Задача с сотрудником -> задача без сотрудника -> задача с сотрудником;
        2. Задача без сотрудника -> задача с сотрудником."""
        self.employee_1 = Employee.objects.create(full_name='test_1', post='test_1', task_count=2)
        self.employee_2 = Employee.objects.create(full_name='test_2', post='test_2', task_count=1)
        self.task_1 = Task.objects.create(title='test_1', employee=self.employee_1, date='2024-02-02')
        self.task_2 = Task.objects.create(title='test_2', parent_task=self.task_1, date='2024-02-02')
        self.task_3 = Task.objects.create(title='test_3', parent_task=self.task_2, employee=self.employee_1,
                                          date='2024-02-02')
        self.task_4 = Task.objects.create(title='test_4', date='2024-02-02')
        self.task_5 = Task.objects.create(title='test_5', employee=self.employee_2, parent_task=self.task_4,
                                          date='2024-02-02')

    def test_employee_with_task_list(self):
        """Тест на просмотр списка в формате {важная задача, срок, фио сотрудника}."""
        # Arrange(подготавливаю данные для теста)
        url = reverse('employees:important_tasks-list')

        # Act(совершаю действие которое тестирую)
        response = self.client.get(url)

        # Assert(делаю проверки)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = [
            {
                "title": self.task_2.title,
                "date": self.task_2.date,
                "employee": self.employee_1.full_name
            },
            {
                "title": self.task_4.title,
                "date": self.task_4.date,
                "employee": self.employee_2.full_name
            }
        ]
        data = response.json()
        self.assertEqual(
            data, result
        )
