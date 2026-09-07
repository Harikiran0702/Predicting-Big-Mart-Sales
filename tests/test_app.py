import io
import unittest

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.values = dict(Item_Type='0', Item_Weight='9.3', Item_MRP='249.8092',
                           Item_Visibility='0.016047301', Item_Fat_Content='1',
                           Outlet_Establishment_Year='1999', Outlet_Size='1',
                           Outlet_Location_Type='0', Outlet_Type='0')

    def test_pages(self):
        for path in ['/', '/index', '/upload', '/result', '/chart', '/performance']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(self.client.get('/preview').status_code, 302)
        self.assertEqual(self.client.get('/login').status_code, 302)

    def test_prediction_ignores_form_order(self):
        first = self.client.post('/predict', data=self.values)
        second = self.client.post('/predict', data=dict(reversed(list(self.values.items()))))
        self.assertEqual(first.status_code, 200)
        self.assertIn(b'Estimated sales:', first.data)
        self.assertEqual(first.data, second.data)

    def test_invalid_predictions(self):
        self.assertEqual(self.client.post('/predict', data={}).status_code, 400)
        for key, value in [('Item_Weight', 'nan'), ('Item_MRP', 'inf'),
                           ('Item_Type', '16'), ('Item_Fat_Content', '2'),
                           ('Item_Weight', '-1'), ('Item_Visibility', '2'),
                           ('Outlet_Establishment_Year', '1999.5')]:
            with self.subTest(key=key, value=value):
                data = self.values | {key: value}
                self.assertEqual(self.client.post('/predict', data=data).status_code, 400)

    def test_csv_without_id_and_escaping(self):
        response = self.client.post('/preview', data={
            'datasetfile': (io.BytesIO(b'name\n<script>alert(1)</script>\n'), 'sample.csv')})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'&lt;script&gt;', response.data)
        self.assertNotIn(b'<script>alert(1)</script>', response.data)

    def test_invalid_uploads(self):
        self.assertEqual(self.client.post('/preview').status_code, 400)
        for content, filename, status in [(b'', 'empty.csv', 400),
                                          (b'hello', 'sample.txt', 400)]:
            response = self.client.post('/preview', data={
                'datasetfile': (io.BytesIO(content), filename)})
            self.assertEqual(response.status_code, status)

    def test_upload_limit(self):
        self.assertEqual(app.config['MAX_CONTENT_LENGTH'], 2 * 1024 * 1024)
        # Exercise the rejection without creating a disk-spooled test upload.
        with self.client.post('/preview', data=b'a' * (2 * 1024 * 1024 + 1),
                              content_type='application/octet-stream') as response:
            self.assertEqual(response.status_code, 413)


if __name__ == '__main__':
    unittest.main()
