from django.test import TestCase
from django.urls import reverse
from app.models import Task

class TaskWorkflowTests(TestCase):
    def test_home_shows_pending_and_completed_tasks(self):
        Task.objects.create(task='Pending task', is_completed=False)
        Task.objects.create(task='Completed task', is_completed=True)

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pending task')
        self.assertContains(response, 'Completed task')
        self.assertContains(response, 'Completed tasks')
        self.assertEqual(response.context['pending_tasks'].count(), 1)
        self.assertEqual(response.context['completed_tasks'].count(), 1)
        self.assertEqual(response.context['pending_task_count'], 1)
        self.assertContains(response, '1 task')
        self.assertNotContains(response, '2 tasks')

    def test_add_task(self):
        response = self.client.post(reverse('task_add'), {'task': 'New task'})

        self.assertRedirects(response, reverse('home'))
        task = Task.objects.get(task='New task')
        self.assertFalse(task.is_completed)

    def test_mark_task_done(self):
        task = Task.objects.create(task='Do this', is_completed=False)

        response = self.client.post(
            reverse('task_done', args=[task.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse('home'))
        task.refresh_from_db()
        self.assertTrue(task.is_completed)
        self.assertEqual(response.context['pending_tasks'].count(), 0)
        self.assertEqual(response.context['completed_tasks'].get(), task)
        self.assertContains(response, '0 tasks')

    def test_mark_task_undone(self):
        task = Task.objects.create(task='Do this again', is_completed=True)

        response = self.client.post(
            reverse('task_undone', args=[task.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse('home'))
        task.refresh_from_db()
        self.assertFalse(task.is_completed)
        self.assertEqual(response.context['completed_tasks'].count(), 0)
        self.assertEqual(response.context['pending_tasks'].get(), task)

    def test_delete_task(self):
        task = Task.objects.create(task='Remove this')

        response = self.client.post(reverse('task_delete', args=[task.pk]))

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_edit_task(self):
        task = Task.objects.create(task='Old title')

        response = self.client.post(
            reverse('task_edit', args=[task.pk]),
            {'task': 'Updated title'},
        )

        self.assertRedirects(response, reverse('home'))
        task.refresh_from_db()
        self.assertEqual(task.task, 'Updated title')

    def test_task_actions_require_post(self):
        task = Task.objects.create(task='Keep this')

        self.assertEqual(
            self.client.get(reverse('task_done', args=[task.pk])).status_code,
            405,
        )
        self.assertEqual(
            self.client.get(reverse('task_undone', args=[task.pk])).status_code,
            405,
        )
        self.assertEqual(
            self.client.get(reverse('task_delete', args=[task.pk])).status_code,
            405,
        )