import unittest
import Metro
import Exceptions
import datetime
import Main


class TestTicket(unittest.TestCase):

    def setUp(self):
        self.ticket = Metro.Ticket("Main")
        self.id = self.ticket.cid

    def test_Working(self):
        self.assertEqual(self.ticket.__repr__(), f'{self.id}-Main')


class TestStation(unittest.TestCase):
    """
    test class Station
    """

    def setUp(self) -> None:
        self.station = Metro.Station()
        self.ot_ticket1 = Metro.MOtcCredit(card_type = "OT")
        self.ot_ticket1_2 = Metro.MOtcCredit(card_type = "OT")
        self.ot_ticket1_2.status = False
        self.ot_ticket2 = Metro.MCredit(card_type = "C", balance = 5000)
        self.ot_ticket2_2 = Metro.MCredit(card_type = "C", balance = 1500)
        self.ot_ticket3 = Metro.MTimeCredit.create(card_type = "CT", balance = 5000, time = 5)
        self.ot_ticket3_2 = Metro.MTimeCredit.create(card_type = "CT", balance = 1200, time = 5)
        self.ot_ticket3_3 = Metro.MTimeCredit.create(card_type = "CT", balance = 5000, time = 0)
        self.person1 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket1)
        self.person1_2 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket1)
        self.person2 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket2)
        self.person2_2 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket2_2)
        self.person3 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket3)
        self.person3_2 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket3_2)
        self.person3_3 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket3_3)

    def test_checkout(self):
        """ testing checkout methode form Station class
        """
        self.assertEqual(self.station.checkout(self.person1, 0), False)
        self.assertEqual(self.station.checkout(self.person3, 0), 2500)
        self.assertEqual(self.station.checkout(self.person2, 0), 2500)
        with self.assertRaises(Exceptions.NotValidCredit):
            self.station.checkout(self.person1_2, 0)

        with self.assertRaises(Exceptions.BalanceNotEnough):
            self.station.checkout(self.person2_2, 0)
            self.station.checkout(self.person3_2, 0)

        # with self.assertRaises(Exceptions.TimeExpiredCredit):
        #     self.station.checkout(self.person3_3, 0)

    def test_charge(self):
        """test for methode increase balance in station class"""
        self.test_time = self.ot_ticket3_2.expire_time + datetime.timedelta(days = 2)
        self.assertEqual(self.station.increase_balance(person = self.person2, card_number = 0, amount = 2000), 7000)
        self.assertEqual(self.station.increase_balance(self.person3_2, 0, 2000, 2), (3200, self.test_time.day))
        with self.assertRaises(Exceptions.NotChargeable):
            self.station.increase_balance(person = self.person1, card_number = 0, amount = 2000)


class TestFunctions(unittest.TestCase):
    """
    testing other side function
    """

    def setUp(self):
        self.ticket = Metro.Ticket("Main")
        self.ot_ticket1 = Metro.MOtcCredit(card_type = "OT")
        self.ot_ticket2 = Metro.MCredit(card_type = "C", balance = 5000)
        self.person1 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket1)
        self.person2 = Metro.Person(first_name = 'demo', last_name = 'demo', card = self.ot_ticket2)

    def test_get_person(self):
        self.assertEqual(Main.get_person(), ("demo", "demo"))

    def test_select_ticket(self):
        self.assertIsInstance(Main.select_ticket(), Metro.MOtcCredit)
        self.assertIsInstance(Main.select_ticket(), Metro.MTimeCredit)
        self.assertIsInstance(Main.select_t1icket(), Metro.MCredit)

    # def test_pick_person(self):
    #     self.data = [self.person1, self.person2]
    #     self.assertEqual(Main.picked_person(self.data), 0, 1)

    def test_pick_ticket(self):
        self.assertEqual(Main.pick_ticket(self.person2), 0)

    def test_charge_balance(self):
        self.assertEqual(Main.charge_balance(), 1200)

    def test_extend_time(self):
        self.assertEqual(Main.extend_time(), 14)
