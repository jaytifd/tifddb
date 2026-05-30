"""
tests.py — Unit tests for tifddb camp and membership registration.

Run with:
    python manage.py test camp --settings=tifddb.test_settings

Key areas covered:
  - calculate_paypal_fee()             (pure function, no DB)
  - get_discount()                     (mocked ORM)
  - generate_cart_from_registration()  (mocked ORM, full cart-building pipeline)
  - renew_tifd_membership()            (pure + mock camper path)
  - show_me_the_money() / IPN handler  (mocked IPN object)
  - itemize_payment()                  (mocked ORM)
  - Import sanity tests                (catch circular import regressions)

Design decisions:
  - All DB calls are mocked via unittest.mock.patch — no MySQL required.
  - Import sanity tests verify each module loads cleanly after refactoring.
  - IPN handler tests use mock ipn_obj — no real PayPal connection.
"""

import datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.test import TestCase, RequestFactory


# ---------------------------------------------------------------------------
# 1. calculate_paypal_fee  (pure function)
# ---------------------------------------------------------------------------

class CalculatePaypalFeeTests(TestCase):

    def _fee(self, amount):
        from camp.views import calculate_paypal_fee
        return calculate_paypal_fee(amount)

    def test_zero_subtotal(self):
        fee = self._fee(Decimal("0.00"))
        self.assertGreater(fee, Decimal("0.00"))
        self.assertLess(fee, Decimal("1.00"))

    def test_known_amount_100(self):
        # Actual rate in code: 3.49% + $0.49
        # (100 + 0.49) / (1 - 0.0349) - 100 = (100.49 / 0.9651) - 100 ≈ 2.53
        fee = self._fee(Decimal("100.00"))
        self.assertEqual(fee, Decimal("2.53"))

    def test_returns_quantized_decimal(self):
        fee = self._fee(Decimal("366.00"))
        self.assertEqual(fee, fee.quantize(Decimal("0.01")))

    def test_fee_is_positive_for_various_amounts(self):
        for amount in ["15.00", "100.00", "366.00", "500.00", "1000.00"]:
            with self.subTest(amount=amount):
                self.assertGreater(self._fee(Decimal(amount)), Decimal("0"))

    def test_gross_up_formula_is_correct(self):
        """Fee should be in the right ballpark: more than the base charge
        and less than 10% of the subtotal."""
        subtotal = Decimal("200.00")
        fee = self._fee(subtotal)
        self.assertGreater(fee, Decimal("0.49"))
        self.assertLess(fee, subtotal * Decimal("0.10"))

    def test_accepts_string_input(self):
        fee = self._fee("100.00")
        self.assertIsInstance(fee, Decimal)


# ---------------------------------------------------------------------------
# 2. renew_tifd_membership — no camper (pure return path)
# ---------------------------------------------------------------------------

class RenewMembershipNoCamperTests(TestCase):

    def test_returns_two_dates(self):
        from registrar.views import renew_tifd_membership
        result = renew_tifd_membership(None, save=False)
        self.assertEqual(len(result), 2)

    def test_valid_from_is_today(self):
        from registrar.views import renew_tifd_membership
        valid_from, _ = renew_tifd_membership(None, save=False)
        self.assertEqual(valid_from.date(), datetime.datetime.now().date())

    def test_valid_to_is_366_days_out(self):
        from registrar.views import renew_tifd_membership
        valid_from, valid_to = renew_tifd_membership(None, save=False)
        self.assertEqual((valid_to - valid_from).days, 366)

    def test_valid_to_after_valid_from(self):
        from registrar.views import renew_tifd_membership
        valid_from, valid_to = renew_tifd_membership(None, save=False)
        self.assertGreater(valid_to, valid_from)


# ---------------------------------------------------------------------------
# 3. renew_tifd_membership — with mock camper
# ---------------------------------------------------------------------------

class RenewMembershipWithCamperTests(TestCase):

    def _mock_camper(self, join_tifd=1, membership_years=1,
                     reg_type_desc="Full-time Camper", current_valid_to=None):
        from types import SimpleNamespace
        # Use SimpleNamespace instead of MagicMock — renew_tifd_membership reads
        # and writes camper attributes directly, and MagicMock's attribute
        # interception can cause comparison operators to behave unexpectedly.
        reg_type = SimpleNamespace(description=reg_type_desc)
        camper = SimpleNamespace(
            join_tifd=join_tifd,
            membership_years=membership_years,
            registration_type=reg_type,
            registration_id=999,
            membership_valid_from=None,
            membership_valid_to=current_valid_to,
        )
        camper.save = lambda: None  # renew_tifd_membership calls save() when save=True
        return camper

    def test_lifetime_gets_100_year_validity(self):
        from registrar.views import renew_tifd_membership
        camper = self._mock_camper(join_tifd=1, reg_type_desc="Lifetime Membership")
        renew_tifd_membership(camper, save=False)
        self.assertIsNotNone(camper.membership_valid_to)
        self.assertIsNotNone(camper.membership_valid_from)
        delta = camper.membership_valid_to - camper.membership_valid_from
        self.assertGreater(delta.days, 36000)

    def test_standard_camper_gets_366_days(self):
        from registrar.views import renew_tifd_membership
        camper = self._mock_camper(join_tifd=1)
        renew_tifd_membership(camper, save=False)
        self.assertIsNotNone(camper.membership_valid_to)
        delta = camper.membership_valid_to - camper.membership_valid_from
        self.assertEqual(delta.days, 366)

    def test_join_tifd_false_leaves_dates_unchanged(self):
        from registrar.views import renew_tifd_membership
        camper = self._mock_camper(join_tifd=0)
        renew_tifd_membership(camper, save=False)
        self.assertIsNone(camper.membership_valid_to)


# ---------------------------------------------------------------------------
# 4. get_discount — mocked ORM
# ---------------------------------------------------------------------------

class GetDiscountTests(TestCase):

    def test_no_rebate_no_adjustment_is_zero(self):
        from camp.views import get_discount
        mock_reg = MagicMock()
        mock_reg.rebate_id = None
        mock_reg.adjustment = None

        with patch('camp.views.CampRegistration.objects.get', return_value=mock_reg), \
             patch('camp.views.CampCamper.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value = []
            discount_list, total = get_discount(999)

        self.assertEqual(discount_list, [])
        self.assertEqual(total, 0)

    def test_rebate_applied(self):
        from camp.views import get_discount
        mock_rebate = MagicMock()
        mock_rebate.price = Decimal("-15.00")
        mock_rebate.cart_description = "Rebate"
        mock_rebate.description = "Life membership rebate"

        mock_reg = MagicMock()
        mock_reg.rebate_id = 23
        mock_reg.rebate = mock_rebate
        mock_reg.adjustment = None

        with patch('camp.views.CampRegistration.objects.get', return_value=mock_reg), \
             patch('camp.views.CampCamper.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value = []
            discount_list, total = get_discount(999)

        self.assertEqual(len(discount_list), 1)
        self.assertEqual(total, Decimal("-15.00"))

    def test_registrar_adjustment(self):
        from camp.views import get_discount
        mock_reg = MagicMock()
        mock_reg.rebate_id = None
        mock_reg.adjustment = Decimal("-50.00")

        with patch('camp.views.CampRegistration.objects.get', return_value=mock_reg), \
             patch('camp.views.CampCamper.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value = []
            discount_list, total = get_discount(999)

        self.assertEqual(total, Decimal("-50.00"))
        self.assertEqual(discount_list[0]['cart_description'], 'Registrar adjustment')

    def test_free_staff_shirt(self):
        from camp.views import get_discount
        mock_shirt = MagicMock()
        mock_shirt.price = Decimal("22.00")
        mock_camper = MagicMock()
        mock_camper.free_t_shirt = True
        mock_camper.t_shirt_type = mock_shirt
        mock_camper.custom_registration_discount = None

        mock_reg = MagicMock()
        mock_reg.rebate_id = None
        mock_reg.adjustment = None

        with patch('camp.views.CampRegistration.objects.get', return_value=mock_reg), \
             patch('camp.views.CampCamper.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value = [mock_camper]
            _, total = get_discount(999)

        self.assertEqual(total, Decimal("-22.00"))

    def test_combined_rebate_and_adjustment(self):
        from camp.views import get_discount
        mock_rebate = MagicMock()
        mock_rebate.price = Decimal("-15.00")
        mock_rebate.cart_description = "rebate"
        mock_rebate.description = "rebate"

        mock_reg = MagicMock()
        mock_reg.rebate_id = 23
        mock_reg.rebate = mock_rebate
        mock_reg.adjustment = Decimal("-25.00")

        with patch('camp.views.CampRegistration.objects.get', return_value=mock_reg), \
             patch('camp.views.CampCamper.objects.filter') as mock_filter:
            mock_filter.return_value.order_by.return_value = []
            discount_list, total = get_discount(999)

        self.assertEqual(len(discount_list), 2)
        self.assertEqual(total, Decimal("-40.00"))


# ---------------------------------------------------------------------------
# 5. generate_cart_from_registration — mocked ORM
# ---------------------------------------------------------------------------

def _build_cart_mocks(registration_source=0, adult_or_child="adult",
                      reg_type_price=Decimal("366.00"),
                      reg_type_desc="Full-time Camper",
                      reg_type_slug="registration",
                      housing_type_id=None,
                      t_shirt_type_id=None,
                      dvd=False, need_linen=False,
                      join_tifd=True, late=False):
    """Construct mock objects for generate_cart_from_registration tests."""
    mock_reg_type = MagicMock()
    mock_reg_type.price = reg_type_price
    mock_reg_type.cart_description = reg_type_desc
    mock_reg_type.description = reg_type_desc
    mock_reg_type.slug = reg_type_slug

    mock_reg = MagicMock()
    mock_reg.id = 42
    mock_reg.pk = 42
    mock_reg.registration_source = registration_source
    mock_reg.year = datetime.datetime.now().year
    mock_reg.created_at = datetime.datetime.now()
    mock_reg.rebate_id = None
    mock_reg.adjustment = None
    mock_reg.late_fee = Decimal("0.00")
    mock_reg.paypal_fee_reimburse_flag = False

    mock_camper = MagicMock()
    mock_camper.first_name = "Jane"
    mock_camper.last_name = "Doe"
    mock_camper.adult_or_child = adult_or_child
    mock_camper.registration_type = mock_reg_type
    mock_camper.registration_id = 42
    mock_camper.registration = mock_reg
    mock_camper.housing_type_id = housing_type_id
    mock_camper.t_shirt_type_id = t_shirt_type_id
    mock_camper.dvd = dvd
    mock_camper.need_linen = need_linen
    mock_camper.join_tifd = join_tifd
    mock_camper.membership_years = 1
    mock_camper.custom_registration_price = None
    mock_camper.free_t_shirt = False
    mock_camper.membership_valid_from = None
    mock_camper.membership_valid_to = None

    if housing_type_id:
        mock_camper.housing_type.price = Decimal("100.00")
        mock_camper.housing_type.cart_description = "Private room (single)"

    if t_shirt_type_id and t_shirt_type_id != 1:
        mock_camper.t_shirt_type.price = Decimal("22.00")
        mock_camper.t_shirt_type.cart_description = "T-Shirt"

    if late:
        mock_camper.registration.created_at = datetime.datetime.now()
        late_date_val = (datetime.datetime.now() - datetime.timedelta(days=30)).date()
    else:
        late_date_val = (datetime.datetime.now() + datetime.timedelta(days=365)).date()

    mock_late_date = MagicMock()
    mock_late_date.date = late_date_val

    mock_late_fee_price = MagicMock()
    mock_late_fee_price.price = Decimal("25.00")
    mock_late_fee_price.cart_description = "Late fee"

    return mock_reg, mock_camper, mock_late_date, mock_late_fee_price


def _run_cart(mock_reg, mock_camper, mock_late_date, mock_late_fee_price, save=False):
    from camp.views import generate_cart_from_registration

    # Build CampPrices mock objects for each slug the function fetches
    def make_price(slug, desc, price):
        m = MagicMock()
        m.slug = slug
        m.cart_description = desc
        m.price = price
        return m

    mock_dvd     = make_price('dvd',        'Dance review video',       Decimal("21.00"))
    mock_linen   = make_price('linen',      'Linens from GFC',          Decimal("15.00"))
    mock_mem     = make_price('membership', 'TIFD membership - 1 year', Decimal("15.00"))
    mock_late_fee_price.cart_description = 'Late fee'
    mock_late_fee_price.price            = Decimal("25.00")

    price_by_slug = {
        'dvd':        mock_dvd,
        'linen':      mock_linen,
        'membership': mock_mem,
        'late_fee':   mock_late_fee_price,
    }

    def prices_get_side_effect(slug):
        if slug in price_by_slug:
            return price_by_slug[slug]
        raise KeyError(f"Unexpected CampPrices slug in test: {slug!r}")

    donations_row = {
        'donation_tifd': Decimal("0.00"),
        'donation_floor_fund': Decimal("0.00"),
        'donation_bobbi_gillotti': Decimal("0.00"),
        'donation_live_music': Decimal("0.00"),
        'donation_chuck': Decimal("0.00"),
    }

    with patch('camp.views.CampCamper.objects.filter') as mock_filter, \
         patch('camp.views.CampRegistration.objects.get', return_value=mock_reg), \
         patch('camp.views.CampRegistration.objects.filter') as mock_reg_filter, \
         patch('camp.views.CampDates.objects.get', return_value=mock_late_date), \
         patch('camp.views.CampPrices.objects.get',
               side_effect=lambda **kw: prices_get_side_effect(kw.get('slug'))), \
         patch('camp.views.CampPrices.get_price',
               side_effect=lambda slug: price_by_slug[slug].price if slug in price_by_slug else None), \
         patch('camp.views.CampPrices.get_description',
               side_effect=lambda slug: price_by_slug[slug].cart_description if slug in price_by_slug else ''), \
         patch('camp.views.get_discount', return_value=([], Decimal("0.00"))), \
         patch('registrar.views.renew_tifd_membership',
               return_value=(datetime.datetime.now(),
                              datetime.datetime.now() + datetime.timedelta(days=366))):

        mock_filter.return_value.order_by.return_value = [mock_camper]
        mock_reg_filter.return_value.values.return_value = [donations_row]
        return generate_cart_from_registration(42, save=save)


class GenerateCartTests(TestCase):

    def test_returns_cart_dict_and_numeric_total(self):
        cart, total = _run_cart(*_build_cart_mocks())
        self.assertIsInstance(cart, dict)
        self.assertIsInstance(total, (int, float, Decimal))

    def test_camper_name_key_in_cart(self):
        cart, _ = _run_cart(*_build_cart_mocks())
        self.assertIn("Jane Doe", cart)

    def test_camp_registration_fee_in_cart(self):
        cart, _ = _run_cart(*_build_cart_mocks(reg_type_price=Decimal("366.00")))
        values = list(cart.get("Jane Doe", {}).values())
        self.assertIn(Decimal("366.00"), values)

    def test_membership_fee_added_for_adult_join_tifd(self):
        cart, _ = _run_cart(*_build_cart_mocks(join_tifd=True))
        values = list(cart.get("Jane Doe", {}).values())
        self.assertIn(Decimal("15.00"), values)

    def test_housing_fee_in_cart(self):
        cart, _ = _run_cart(*_build_cart_mocks(housing_type_id=21))
        values = list(cart.get("Jane Doe", {}).values())
        self.assertIn(Decimal("100.00"), values)

    def test_shirt_in_cart_when_not_option_1(self):
        cart, _ = _run_cart(*_build_cart_mocks(t_shirt_type_id=5))
        values = list(cart.get("Jane Doe", {}).values())
        self.assertIn(Decimal("22.00"), values)

    def test_dvd_in_cart(self):
        cart, _ = _run_cart(*_build_cart_mocks(dvd=True))
        values = list(cart.get("Jane Doe", {}).values())
        self.assertIn(Decimal("21.00"), values)

    def test_linen_in_cart(self):
        cart, _ = _run_cart(*_build_cart_mocks(need_linen=True))
        values = list(cart.get("Jane Doe", {}).values())
        self.assertIn(Decimal("15.00"), values)

    def test_total_equals_sum_of_cart_items(self):
        cart, total = _run_cart(*_build_cart_mocks(housing_type_id=21))
        computed = sum(v for items in cart.values() for v in items.values() if v)
        self.assertEqual(total, computed)

    def test_donations_section_present_when_nonzero(self):
        mocks = _build_cart_mocks()
        mock_reg, mock_camper, mock_late_date, mock_late_fee_price = mocks

        price_by_slug = {
            'dvd':        MagicMock(cart_description='Dance review video',       price=Decimal("21.00")),
            'linen':      MagicMock(cart_description='Linens from GFC',          price=Decimal("15.00")),
            'membership': MagicMock(cart_description='TIFD membership - 1 year', price=Decimal("15.00")),
            'late_fee':   mock_late_fee_price,
        }
        mock_late_fee_price.cart_description = 'Late fee'
        mock_late_fee_price.price = Decimal("25.00")

        from camp.views import generate_cart_from_registration
        with patch('camp.views.CampCamper.objects.filter') as mock_filter, \
             patch('camp.views.CampRegistration.objects.get', return_value=mock_reg), \
             patch('camp.views.CampRegistration.objects.filter') as mock_reg_filter, \
             patch('camp.views.CampDates.objects.get', return_value=mock_late_date), \
             patch('camp.views.CampPrices.objects.get',
                   side_effect=lambda **kw: price_by_slug[kw.get('slug')]), \
             patch('camp.views.CampPrices.get_price',
                   side_effect=lambda slug: price_by_slug[slug].price), \
             patch('camp.views.CampPrices.get_description',
                   side_effect=lambda slug: price_by_slug[slug].cart_description), \
             patch('camp.views.get_discount', return_value=([], Decimal("0.00"))), \
             patch('registrar.views.renew_tifd_membership',
                   return_value=(datetime.datetime.now(),
                                  datetime.datetime.now() + datetime.timedelta(days=366))):
            mock_filter.return_value.order_by.return_value = [mock_camper]
            mock_reg_filter.return_value.values.return_value = [{
                'donation_tifd': Decimal("25.00"),
                'donation_floor_fund': Decimal("0.00"),
                'donation_bobbi_gillotti': Decimal("0.00"),
                'donation_live_music': Decimal("0.00"),
                'donation_chuck': Decimal("0.00"),
            }]
            cart, _ = generate_cart_from_registration(42, save=False)

        self.assertIn("Donations", cart)

    def test_membership_source_uses_reg_type_price(self):
        cart, _ = _run_cart(*_build_cart_mocks(
            registration_source=1,
            reg_type_slug="membership",
            reg_type_desc="Individual Membership",
            reg_type_price=Decimal("15.00"),
        ))
        values = list(cart.get("Jane Doe", {}).values())
        self.assertTrue(any(v == Decimal("15.00") for v in values))


# ---------------------------------------------------------------------------
# 6. PayPal IPN handler (show_me_the_money)
# ---------------------------------------------------------------------------

class PaypalIPNTests(TestCase):

    def _mock_ipn(self, status_key="completed", mc_gross=Decimal("366.00"),
                  mc_fee=Decimal("11.00"), invoice="TXN-ABC",
                  receiver_email="payments@tifd.org"):
        from paypal.standard.models import ST_PP_COMPLETED, ST_PP_REFUNDED, ST_PP_REVERSED
        ipn = MagicMock()
        ipn.payment_status = {
            "completed": ST_PP_COMPLETED,
            "refunded": ST_PP_REFUNDED,
            "reversed": ST_PP_REVERSED,
            "pending": "Pending",
        }[status_key]
        ipn.mc_gross = mc_gross
        ipn.mc_fee = mc_fee
        ipn.invoice = invoice
        ipn.receiver_email = receiver_email
        ipn.first_name = "Jane"
        ipn.last_name = "Doe"
        ipn.payer_email = "jane@example.com"
        ipn.contact_phone = "5125551234"
        ipn.txn_id = "PP-TXN-001"
        ipn.id = 999
        ipn.item_name = ""
        ipn.reason_code = ""
        return ipn

    def test_wrong_receiver_email_returns_false(self):
        from camp.signals import show_me_the_money
        ipn = self._mock_ipn(receiver_email="hacker@evil.com")
        self.assertFalse(show_me_the_money(ipn))

    def test_cart_total_match_saves_payment(self):
        from camp.signals import show_me_the_money
        mock_reg = MagicMock()
        mock_reg.pk = 42
        mock_reg.id = 42
        mock_reg.cart_total = Decimal("366.00")
        mock_reg.registration_source = 0
        mock_payment = MagicMock()
        ipn = self._mock_ipn(mc_gross=Decimal("366.00"))
        with patch('camp.signals.CampRegistration.objects.filter') as mock_reg_filter, \
             patch('camp.signals.MembershipPayments') as MockPayment, \
             patch('camp.signals.itemize_payment', return_value={}), \
             patch('camp.signals.CampCamper.objects.filter') as mock_camper_filter, \
             patch('camp.signals.renew_tifd_membership', return_value=True), \
             patch('camp.signals.emailconfirmation', return_value=True):
            mock_reg_filter.return_value.first.return_value = mock_reg
            MockPayment.return_value = mock_payment
            mock_camper_filter.return_value.filter.return_value = []
            result = show_me_the_money(ipn)
        mock_payment.save.assert_called()
        self.assertTrue(result)

    def test_refund_updates_refund_amt_and_status_11(self):
        from camp.signals import show_me_the_money
        mock_reg = MagicMock()
        mock_payment = MagicMock()
        mock_payment.refund_amt = None
        mock_payment.paypal_fee = Decimal("11.00")
        mock_payment.gross_amt = Decimal("366.00")
        mock_payment.notes = None

        ipn = self._mock_ipn(status_key="refunded",
                              mc_gross=Decimal("-366.00"), mc_fee=Decimal("-11.00"))

        with patch('camp.signals.CampRegistration.objects.get', return_value=mock_reg), \
             patch('camp.signals.get_object_or_404', return_value=mock_reg), \
             patch('camp.signals.MembershipPayments.objects.get', return_value=mock_payment):
            show_me_the_money(ipn)

        mock_payment.save.assert_called()
        self.assertEqual(mock_reg.registration_status_id, 11)

    def test_unknown_payment_status_returns_false(self):
        from camp.signals import show_me_the_money
        ipn = self._mock_ipn(status_key="pending")
        self.assertFalse(show_me_the_money(ipn))



    def test_cart_total_mismatch_sets_status_7(self):
        from camp.signals import show_me_the_money
        mock_reg = MagicMock()
        mock_reg.pk = 42
        mock_reg.id = 42
        mock_reg.cart_total = Decimal("500.00")
        mock_payment = MagicMock()
        ipn = self._mock_ipn(mc_gross=Decimal("366.00"))
        with patch('camp.signals.CampRegistration.objects.filter') as mock_reg_filter, \
             patch('camp.signals.MembershipPayments') as MockPayment:
            mock_reg_filter.return_value.first.return_value = mock_reg
            MockPayment.return_value = mock_payment
            result = show_me_the_money(ipn)
        self.assertFalse(result)
        self.assertEqual(mock_reg.registration_status_id, 7)

    def test_completed_sets_status_6_on_match(self):
        from camp.signals import show_me_the_money
        mock_reg = MagicMock()
        mock_reg.pk = 42
        mock_reg.id = 42
        mock_reg.cart_total = Decimal("366.00")
        mock_reg.registration_source = 0
        ipn = self._mock_ipn(mc_gross=Decimal("366.00"))
        mock_payment = MagicMock()
        with patch('camp.signals.CampRegistration.objects.filter') as mock_reg_filter, \
             patch('camp.signals.MembershipPayments') as MockPayment, \
             patch('camp.signals.itemize_payment', return_value={}), \
             patch('camp.signals.CampCamper.objects.filter') as mock_camper_filter, \
             patch('camp.signals.renew_tifd_membership', return_value=True), \
             patch('camp.signals.emailconfirmation', return_value=True):
            mock_reg_filter.return_value.first.return_value = mock_reg
            MockPayment.return_value = mock_payment
            mock_camper_filter.return_value.filter.return_value = []
            show_me_the_money(ipn)
        self.assertEqual(mock_reg.registration_status_id, 6)


    def test_invalid_ipn_logs_and_raises(self):
        """
        () should log all IPN fields and raise an Exception.
        covers the case where PayPal itself says the IPN was forged/tampered.
        """
        from camp.signals import invalid_ipn

        mock_ipn = MagicMock()
        mock_ipn.payment_status = "INVALID"
        mock_ipn.invoice = "FORGED-123"
        mock_ipn.mc_gross = Decimal("999.00")
        mock_ipn.receiver_email = "attacker@evil.com"
        mock_ipn.payer_email = "victim@example.com"
        mock_ipn.txn_id = "FAKE-TXN-001"
        mock_ipn.id = 1234
        
        with self.assertRaises(Exception) as ctx:
            invalid_ipn(mock_ipn)

        self.assertIn("FORGED-123", str(ctx.exception))

    def test_invalid_ipn_signal_connected_to_correct_handler(self):
        """
        invalid_ipn_received should be wired to invalid_ipn, NOT show_me_the_money.
        If this fails it means a forged IPN would go through full payment processing.
        """
        from paypal.standard.ipn.signals import invalid_ipn_received
        from camp.signals import invalid_ipn, show_me_the_money
        
        receivers = [r[1]() for r in invalid_ipn_received.receivers]
        self.assertIn(invalid_ipn, receivers,
            "invalid_ipn_received must be connected to invalid_ipn")
        self.assertNotIn(show_me_the_money, receivers,
						 "invalid_ipn_received must NOT be connected to show_me_the_money")


# ---------------------------------------------------------------------------
# 7. itemize_payment
# ---------------------------------------------------------------------------

class ItemizePaymentTests(TestCase):

    def test_both_none_returns_zeroed_dict(self):
        from registrar.views import itemize_payment
        result = itemize_payment(None, None)
        for val in result.values():
            self.assertEqual(val, 0)

    def test_required_keys_present(self):
        from registrar.views import itemize_payment
        result = itemize_payment(None, None)
        for key in ('camp_fee', 'membership_fee', 't_shirt_fee', 'dvd_fee',
                    'housing_fee', 'late_fee', 'bobbi_fund', 'camp_fund'):
            self.assertIn(key, result)

    def test_payment_only_returns_payment_fields(self):
        from registrar.views import itemize_payment
        mock_payment = MagicMock()
        mock_payment.camp_fee = Decimal("366.00")
        mock_payment.membership_fee = Decimal("15.00")
        mock_payment.t_shirt_fee = Decimal("0.00")
        mock_payment.dvd_fee = Decimal("0.00")
        mock_payment.housing_fee = Decimal("100.00")
        mock_payment.other_fee = Decimal("0.00")
        mock_payment.late_fee = Decimal("0.00")
        mock_payment.general_fund = Decimal("0.00")
        mock_payment.gfc_linens = Decimal("0.00")
        mock_payment.camp_fund = Decimal("0.00")
        mock_payment.bobbi_fund = Decimal("0.00")
        mock_payment.chuck_fund = Decimal("0.00")
        mock_payment.texakolo_fund = Decimal("0.00")
        mock_payment.floor_fund = Decimal("0.00")
        mock_payment.music_fund = Decimal("0.00")
        mock_payment.paypal_fee_reimburse_fee = Decimal("0.00")

        result = itemize_payment(None, mock_payment)
        self.assertEqual(result['camp_fee'], Decimal("366.00"))
        self.assertEqual(result['membership_fee'], Decimal("15.00"))
        self.assertEqual(result['housing_fee'], Decimal("100.00"))

    def test_registration_path_sums_camp_fee(self):
        """
        itemize_payment should read camp_fee from the camper's registration_type.price
        and membership_fee from CampPrices.get_price('membership').
        We use arbitrary sentinel values so the test is not coupled to real DB prices.
        """
        from registrar.views import itemize_payment

        CAMP_FEE    = Decimal("111.11")   # arbitrary sentinel — not a real price
        MEM_FEE     = Decimal("22.22")
        DVD_FEE     = Decimal("33.33")
        LINEN_FEE   = Decimal("44.44")

        mock_reg_type = MagicMock()
        mock_reg_type.price = CAMP_FEE
        mock_reg_type.slug = "registration"
        mock_reg_type.description = "Full-time Camper"

        mock_camper = MagicMock()
        mock_camper.need_linen = False
        mock_camper.t_shirt_type_id = None
        mock_camper.dvd = False
        mock_camper.housing_type_id = None
        mock_camper.registration_type_id = 1
        mock_camper.registration_type = mock_reg_type
        mock_camper.custom_registration_price = None
        mock_camper.adult_or_child = "adult"
        mock_camper.join_tifd = 1
        mock_camper.membership_years = 1

        mock_reg = MagicMock()
        mock_reg.id = 42
        mock_reg.registration_source = 0
        mock_reg.shipping_fee = None
        mock_reg.donation_camp_fund = None
        mock_reg.donation_chuck = None
        mock_reg.donation_bobbi_gillotti = None
        mock_reg.donation_floor_fund = None
        mock_reg.donation_live_music = None
        mock_reg.donation_tifd = None
        mock_reg.rebate = None                  # prevent MagicMock auto-attr triggering rebate branch
        mock_reg.paypal_fee_reimburse_flag = False
        mock_camper.registration = mock_reg

        price_map = {'dvd': DVD_FEE, 'membership': MEM_FEE, 'linen': LINEN_FEE}

        with patch('registrar.views.CampCamper.objects.filter') as mock_filter, \
             patch('registrar.views.CampPrices.get_price', side_effect=lambda slug: price_map.get(slug)):
            mock_filter.return_value.select_related.return_value = [mock_camper]
            result = itemize_payment(mock_reg, None)

        # camp_fee comes from registration_type.price — whatever that is
        self.assertEqual(result['camp_fee'], CAMP_FEE)
        # membership_fee comes from CampPrices.get_price('membership')
        self.assertEqual(result['membership_fee'], MEM_FEE)


# ---------------------------------------------------------------------------
# 8. Import sanity — catch circular import regressions immediately
# ---------------------------------------------------------------------------

class ImportSanityTests(TestCase):
    """
    Each test imports one module. If a circular import is re-introduced
    during your refactor, the relevant test will fail with an ImportError
    and point you directly at the broken module.
    """

    def test_camp_models_importable(self):
        import importlib
        self.assertIsNotNone(importlib.import_module('camp.models'))

    def test_camp_views_importable(self):
        import importlib
        self.assertIsNotNone(importlib.import_module('camp.views'))

    def test_camp_signals_importable(self):
        import importlib
        self.assertIsNotNone(importlib.import_module('camp.signals'))

    def test_membership_models_importable(self):
        import importlib
        self.assertIsNotNone(importlib.import_module('membership.models'))

    def test_membership_views_importable(self):
        import importlib
        self.assertIsNotNone(importlib.import_module('membership.views'))

    def test_registrar_views_importable(self):
        import importlib
        self.assertIsNotNone(importlib.import_module('registrar.views'))

    def test_generate_cart_is_callable(self):
        from camp.views import generate_cart_from_registration
        self.assertTrue(callable(generate_cart_from_registration))

    def test_calculate_paypal_fee_is_callable(self):
        from camp.views import calculate_paypal_fee
        self.assertTrue(callable(calculate_paypal_fee))

    def test_renew_tifd_membership_is_callable(self):
        from registrar.views import renew_tifd_membership
        self.assertTrue(callable(renew_tifd_membership))

    def test_itemize_payment_is_callable(self):
        from registrar.views import itemize_payment
        self.assertTrue(callable(itemize_payment))

    def test_show_me_the_money_is_callable(self):
        from camp.signals import show_me_the_money
        self.assertTrue(callable(show_me_the_money))

    def test_get_discount_is_callable(self):
        from camp.views import get_discount
        self.assertTrue(callable(get_discount))
