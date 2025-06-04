import os
from unittest import TestCase, mock
from llm.rag import perform_rag, load_all_documents, load_pdf
from langchain_core.documents import Document

@mock.patch.dict(os.environ, {"DOCUMENT_STORAGE_PATH": "tests/resources/pdf"}, clear=True)
class TestRag(TestCase):

    def test_perform_rag_integrates_components(self):
        with mock.patch('llm.rag.fetch_documents') as mock_fetch_documents, \
             mock.patch('llm.rag.load_all_documents') as mock_load_all_documents, \
             mock.patch('llm.rag.chunk_data') as mock_chunk_data, \
             mock.patch('llm.rag.vectorize_documents') as mock_vectorize_documents, \
             mock.patch('llm.rag.build_qa_chain') as mock_build_qa_chain, \
             mock.patch('llm.rag.run_chain') as mock_run_chain:

            # given
            mock_fetch_documents.return_value = [{'filename': 'doc1.pdf'}]
            mock_load_all_documents.return_value = ['doc content']
            mock_chunk_data.return_value = ['chunk1', 'chunk2']
            mock_vectorize_documents.return_value = 'vectorstore'
            mock_build_qa_chain.return_value = 'qa_chain'
            mock_run_chain.return_value = "final answer"

            # when 
            result = perform_rag("What is AI?")

            # then
            assert result == "final answer"

    @mock.patch('llm.rag.load_pdf')
    def test_load_all_documents_returns_flattened_list(self, mock_load_pdf):
        # given
        input_rows = [
            {"filename": "doc1.pdf"},
            {"filename": "doc2.pdf"}
        ]

        mock_load_pdf.side_effect = [
            [Document(page_content="Content from doc1 page 1")],
            [Document(page_content="Content from doc2 page 1"), Document(page_content="Content from doc2 page 2")]
        ]

        # when
        result = load_all_documents(input_rows)

        # then
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].page_content, "Content from doc1 page 1")
        self.assertEqual(result[1].page_content, "Content from doc2 page 1")
        self.assertEqual(result[2].page_content, "Content from doc2 page 2")


    def test_load_pdf_reads_file(self):
        # given 
        filename = "Profile.pdf"  

        # when
        documents = load_pdf(filename)

        # then 
        self.assertIsInstance(documents, list)
        self.assertTrue(all(isinstance(doc, Document) for doc in documents))
        self.assertGreater(len(documents), 0)

