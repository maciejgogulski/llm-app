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
     


    def test_get_documents_route_success(self):
        """
        Should return 200 with a list of documents.
        """

        mock_docs = [
                {"id": 1, "filename": "test1.pdf", "filepath": "/uploads/test1.pdf", "added_at": "2025-06-25 12:00:00", "updated_at": "2025-06-25 12:00:00"},
            {"id": 2, "filename": "test2.pdf", "filepath": "/uploads/test2.pdf", "added_at": "2025-06-25 12:00:00", "updated_at": "2025-06-25 12:00:00"}
        ]

        with mock.patch('db.repo.fetch_documents') as mock_fetch_documents:

            # given
            mock_fetch_documents.return_value = mock_docs

            # when
            response = self.client.get('/documents/')

            # then
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), mock_docs)
            mock_fetch_documents.assert_called_once()


    def test_get_documents_route_db_error(self):
        """
        Should return 500 when DB call fails.
        """

        with mock.patch('db.repo.fetch_documents') as mock_fetch_documents:

            # given
            mock_fetch_documents.side_effect = Exception("DB is down")

            # when
            response = self.client.get('/documents/')
            
            # then
            self.assertEqual(response.status_code, 500)
            self.assertIn(b'DB error', response.data)
     

    def test_delete_document_route_success(self):
        """
        Should return 200 when a document is deleted successfully.
        """

        with mock.patch('db.repo.delete_document') as mock_delete_document:

            # given
            mock_delete_document.return_value = None
            
            # when
            response = self.client.delete('/documents/test.pdf')
            
            # then
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Deleted document test.pdf', response.data)
            mock_delete_document.assert_called_once_with('test.pdf')


    def test_delete_document_route_not_found(self):
        """
        Should return 404 if no document was deleted.
        """

        with mock.patch('db.repo.delete_document') as mock_delete_document:

            # given
            mock_delete_document.return_value = 0
            
            # when
            response = self.client.delete('/documents/missing.pdf')
            
            # then
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Document not found', response.data)


    def test_delete_document_route_db_error(self):
        """
        Should return 500 when the DB raises an exception during delete.
        """

        with mock.patch('db.repo.delete_document') as mock_delete_document:
            # given
            mock_delete_document.side_effect = Exception("DB error")
            
            # when
            response = self.client.delete('/documents/test.pdf')
            
            # then
            self.assertEqual(response.status_code, 500)
            self.assertIn(b'DB error', response.data)


