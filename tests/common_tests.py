class ConnectorCommonTests(object):
    "Mixin for common tests in shelf connector implementations."

    def smoke_test(self, reason='smoke'):
        # Use reason argument to produce a unique unittest failure message.
        self.assertEquals(self.connector.get('', ''), {})

    def test_get_keymiss(self):
        self.assertEquals(self.connector.get('site', 'rule'), {})

    def test_new_item(self):
        self.assertEquals(self.connector.get('site', 'rule'), {})
        item = {'spam': 'eggs'}
        self.connector.put('site', 'rule', item)
        self.assertEquals(self.connector.get('site', 'rule'), item)

    def test_update_item(self):
        self.test_new_item()
        item = {'spam': 'eggs'}
        update = {'spam': 'eggs', 'foo': 'bar'}
        self.connector.put('site', 'rule', update)
        self.assertEqual(self.connector.get('site', 'rule'), update)
        self.assertNotEqual(self.connector.get('site', 'rule'), item)

    def test_item_separation(self):
        another = {1: 'one', 2: 'two', 3: 'three'}
        yetanother = {4: 'four', 5: 'five', 6: 'six'}
        self.connector.put('site', 'another', another)
        self.test_get_keymiss()
        self.test_new_item()
        self.assertEqual(self.connector.get('site', 'another'), another)
        self.connector.put('yet', 'another', yetanother)
        self.assertEqual(self.connector.get('site', 'another'), another)
        self.assertEqual(self.connector.get('yet', 'another'), yetanother)
        yetanother.update({7: 'seven'})
        self.connector.put('yet', 'another', yetanother)
        self.assertEqual(self.connector.get('site', 'another'), another)
