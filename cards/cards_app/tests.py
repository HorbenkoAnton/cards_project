from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Card
import datetime

class CardModelTest(TestCase):

    def setUp(self):
        self.card = Card.objects.create(
            eng_word="hello",
            ukr_word="привіт",
            last_time_drafted=timezone.now(),
            last_result=True
        )

    def test_card_str(self):
        self.assertEqual(str(self.card), "hello")

    def test_update_is_draftable_true(self):
        self.card.last_result = False
        self.card.last_time_drafted = timezone.now() - datetime.timedelta(days=3)
        self.card.update_is_draftable()
        self.assertTrue(self.card.is_draftable)

    def test_update_is_draftable_false(self):
        self.card.last_result = True
        self.card.last_time_drafted = timezone.now() - datetime.timedelta(days=1)
        self.card.update_is_draftable()
        self.assertFalse(self.card.is_draftable)


class DraftViewTest(TestCase):

    def setUp(self):
        self.card = Card.objects.create(
            eng_word="hello",
            ukr_word="привіт",
            last_time_drafted=timezone.now(),
            last_result=True
        )

    def test_draft_view_with_draftable_cards(self):
        response = self.client.get(reverse('draft_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hello")

    def test_draft_view_with_no_draftable_cards(self):
        self.card.is_draftable = False
        self.card.save()
        response = self.client.get(reverse('draft_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Congrats, you revised all your words!")


class DraftedRevisionActionTest(TestCase):

    def setUp(self):
        self.card = Card.objects.create(
            eng_word="hello",
            ukr_word="привіт",
            last_time_drafted=timezone.now(),
            last_result=True
        )

    def test_drafted_revision_action_correct_result(self):
        response = self.client.post(reverse('drafted_revision', args=[self.card.id, "true"]))
        self.card.refresh_from_db()
        self.assertTrue(self.card.last_result)
        self.assertEqual(self.card.last_time_drafted.date(), timezone.now().date())

    def test_drafted_revision_action_incorrect_result(self):
        response = self.client.post(reverse('drafted_revision', args=[self.card.id, "false"]))
        self.card.refresh_from_db()
        self.assertFalse(self.card.last_result)
        self.assertEqual(self.card.last_time_drafted.date(), timezone.now().date())


class AddWordActionTest(TestCase):

    def test_add_word_action(self):
        response = self.client.post(reverse('add_word'), {'eng_word': 'test', 'ukr_word': 'тест'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.first().eng_word, 'test')


class EditWordActionTest(TestCase):

    def setUp(self):
        self.card = Card.objects.create(
            eng_word="hello",
            ukr_word="привіт",
            last_time_drafted=timezone.now(),
            last_result=True
        )

    def test_edit_word_action(self):
        response = self.client.post(reverse('edit_word', args=[self.card.id]), {
            'eng_word': 'hi',
            'ukr_word': 'привітання'
        })
        self.card.refresh_from_db()
        self.assertEqual(self.card.eng_word, 'hi')
        self.assertEqual(self.card.ukr_word, 'привітання')
        self.assertEqual(response.status_code, 302)


class DeleteWordActionTest(TestCase):

    def setUp(self):
        self.card = Card.objects.create(
            eng_word="hello",
            ukr_word="привіт",
            last_time_drafted=timezone.now(),
            last_result=True
        )

    def test_delete_word_action(self):
        response = self.client.post(reverse('delete_word', args=[self.card.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 0)


class WordsViewTest(TestCase):

    def setUp(self):
        self.card1 = Card.objects.create(
            eng_word="hello",
            ukr_word="привіт",
            last_time_drafted=timezone.now(),
            last_result=True
        )
        self.card2 = Card.objects.create(
            eng_word="world",
            ukr_word="світ",
            last_time_drafted=timezone.now(),
            last_result=False
        )

    def test_words_view(self):
        response = self.client.get(reverse('words_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hello")
        self.assertContains(response, "world")


class IndexViewTest(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('index_page'))
        self.assertEqual(response.status_code, 200)

class UnreviseViewTest(TestCase):
    def setUp(self):
        self.card1 = Card.objects.create(
            eng_word="hello",
            ukr_word="привіт",
            last_time_drafted=timezone.now(),
            last_result=True,
            is_draftable=False
        )
        self.card2 = Card.objects.create(
            eng_word="world",
            ukr_word="світ",
            last_time_drafted=timezone.now(),
            last_result=False,
            is_draftable=False
        )

    def test_unrevise_action_single_card(self):
        url = reverse("unrevise", args=[self.card1.id])
        response = self.client.post(url)

        self.card1.refresh_from_db()
        self.assertTrue(self.card1.is_draftable)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("words_page"))

    def test_unrevise_action_get_method_does_nothing(self):
        url = reverse("unrevise", args=[self.card1.id])
        response = self.client.get(url)

        self.card1.refresh_from_db()
        self.assertFalse(self.card1.is_draftable)  # Should remain unchanged
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("words_page"))

    def test_unrevise_all_action(self):
        url = reverse("unrevise_all")
        response = self.client.post(url)

        self.card1.refresh_from_db()
        self.card2.refresh_from_db()
        self.assertTrue(self.card1.is_draftable)
        self.assertTrue(self.card2.is_draftable)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("words_page"))

    def test_unrevise_all_get_method_does_nothing(self):
        url = reverse("unrevise_all")
        response = self.client.get(url)

        self.card1.refresh_from_db()
        self.card2.refresh_from_db()
        self.assertFalse(self.card1.is_draftable)
        self.assertFalse(self.card2.is_draftable)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("words_page"))
