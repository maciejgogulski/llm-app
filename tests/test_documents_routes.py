import io
from unittest import TestCase, mock
from main import create_app

class TestDocumentsRoutes(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def test_upload_documents_route_success(self):
        """
        Should return 200 when a new PDF is uploaded and saved successfully.
        """

        with mock.patch('routes.documents.compute_checksum') as mock_compute_checksum, \
             mock.patch('db.repo.document_exists_by_checksum') as mock_document_exists_by_checksum, \
             mock.patch('db.repo.insert_document') as mock_insert_document, \
             mock.patch('werkzeug.datastructures.FileStorage.save') as mock_file_save:

            # given 
            fake_checksum = "6c99f39e9003a9f6ee089c472790def8f87e5f05fbd0c248e5a7b4aca5aecbb3"
            mock_compute_checksum.return_value = fake_checksum
            mock_document_exists_by_checksum.return_value = False
            mock_insert_document.return_value = None  # No-op
            mock_file_save.return_value = None  # Avoid actual disk write

            data = {
                'file': (io.BytesIO(b"%PDF-1.4 some pdf content"), 'test.pdf')
            }

            # when 
            response = self.client.post('/documents/', data=data, content_type='multipart/form-data')
            
            # then
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Saved to', response.data)


    def test_upload_documents_route_file_not_uploaded(self):
        """
        Should return 400 when no file is uploaded
        """

        # given
        # --

        # when
        response = self.client.post('/documents/')

        #then
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid file', response.data)


    def test_upload_documents_route_duplicate_checksum(self):
        """
        Should return 409 when there is a checksum conflict.
        """

        with mock.patch('routes.documents.compute_checksum') as mock_compute_checksum, \
                mock.patch('db.repo.document_exists_by_checksum') as mock_document_exists_by_checksum:

            # given
            mock_compute_checksum.return_value = "6c99f39e9003a9f6ee089c472790def8f87e5f05fbd0c248e5a7b4aca5aecbb3"
            mock_document_exists_by_checksum.return_value = True

            data = {
                'file': (io.BytesIO(b"fake pdf content"), 'test.pdf')
            }
            
            # when
            response = self.client.post('/documents/', data=data, content_type='multipart/form-data')

            # then
            self.assertEqual(response.status_code, 409)
            self.assertIn(b'Duplicate document', response.data)


    def test_upload_documents_route_db_error(self):
        """
        Should return 500 when DB insert fails.
        """

        with mock.patch('routes.documents.compute_checksum') as mock_compute_checksum, \
             mock.patch('db.repo.document_exists_by_checksum') as mock_document_exists_by_checksum, \
             mock.patch('db.repo.insert_document') as mock_insert_document:

            # given
            mock_compute_checksum.return_value = "6c99f39e9003a9f6ee089c472790def8f87e5f05fbd0c248e5a7b4aca5aecbb3" 
            mock_document_exists_by_checksum.return_value = False
            mock_insert_document.side_effect = Exception("DB is down")

            data = {
                'file': (io.BytesIO(b"valid pdf content"), 'test.pdf')
            }
            
            # when
            response = self.client.post('/documents/', data=data, content_type='multipart/form-data')
            
            # then
            self.assertEqual(response.status_code, 500)
            self.assertIn(b'DB error', response.data)
        
