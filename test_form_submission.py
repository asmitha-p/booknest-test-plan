"""Workflow 2 - Form submission: contact form success and validation errors."""
import pytest

from pages.contact_page import ContactPage


@pytest.mark.smoke
def test_contact_form_valid_submission_shows_success(logged_in_driver):
    page = ContactPage(logged_in_driver).open()
    page.fill_and_submit("Jane Tester", "jane@example.com", "Hello, this is a test message.")

    assert page.is_visible(page.SUCCESS), "Success banner should appear"
    assert "Thank you" in page.text_of(page.SUCCESS)


@pytest.mark.negative
def test_contact_form_empty_submission_shows_all_field_errors(logged_in_driver):
    page = ContactPage(logged_in_driver).open()
    page.click(page.SUBMIT)

    assert page.error_text(page.NAME_ERROR) == "Name is required"
    assert page.error_text(page.EMAIL_ERROR) == "Enter a valid email address"
    assert page.error_text(page.MESSAGE_ERROR) == "Message must be at least 10 characters"
    assert not page.is_visible(page.SUCCESS, timeout=1)


@pytest.mark.negative
@pytest.mark.parametrize("bad_email", ["plainaddress", "missing@tld", "@no-user.com", "a b@c.com"])
def test_contact_form_rejects_invalid_email(logged_in_driver, bad_email):
    page = ContactPage(logged_in_driver).open()
    page.fill_and_submit("Jane Tester", bad_email, "A long enough message body.")

    assert page.error_text(page.EMAIL_ERROR) == "Enter a valid email address"
    assert not page.is_visible(page.SUCCESS, timeout=1)
