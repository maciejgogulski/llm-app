import os
from unittest import TestCase, mock
from llm.rag import perform_rag, load_all_documents, load_pdf, chunk_data, vectorize_documents, build_qa_chain, run_chain
from langchain_core.documents import Document

class TestRag(TestCase):

    
    @mock.patch.dict(os.environ, {"MODEL": "ollama3"}, clear=True)
    def test_perform_rag_integrates_components(self):
        """
        Verifies if method perform rag integrates process correctly.
        """

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


    @mock.patch.dict(os.environ, {}, clear=True)
    def test_perform_rag_raises_error_when_model_env_missing(self):
        """
        If there is no language model specified, performing rag should fail.
        """

        with mock.patch('llm.rag.fetch_documents') as mock_fetch_documents, \
             mock.patch('llm.rag.load_all_documents') as mock_load_all_documents, \
             mock.patch('llm.rag.chunk_data') as mock_chunk_data, \
             mock.patch('llm.rag.vectorize_documents') as mock_vectorize_documents, \
             mock.patch('llm.rag.build_qa_chain') as mock_build_qa_chain:

            mock_fetch_documents.return_value = mock.Mock()
            mock_load_all_documents.return_value = mock.Mock()
            mock_chunk_data.return_value = mock.Mock()
            mock_vectorize_documents.return_value = mock.Mock()
            mock_build_qa_chain.return_value = mock.Mock()

            # given
            prompt = "What is AI?"

            # when / then
            with self.assertRaises(ValueError) as context:
                perform_rag(prompt)

            self.assertIn("MODEL environment variable is not set", str(context.exception))


    @mock.patch('llm.rag.load_pdf')
    def test_load_all_documents_returns_flattened_list(self, mock_load_pdf):
        """
        Verifies reading and parsing document objects into flattened list. 
        """

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

    
    @mock.patch.dict(os.environ, {"DOCUMENT_STORAGE_PATH": "tests/resources/pdf"}, clear=True)
    def test_load_pdf_reads_file(self):
        """
        Testing if library actually loads file.
        """

        # given 
        filename = "Profile.pdf"  

        # when
        documents = load_pdf(filename)

        # then 
        self.assertIsInstance(documents, list)
        self.assertTrue(all(isinstance(doc, Document) for doc in documents))
        self.assertGreater(len(documents), 0)


    @mock.patch.dict(os.environ, {}, clear=True)
    def test_load_pdf_fails_when_path_env_missing(self):
        """
        If there is no path specified specified, loading document should fail.
        """

        # given
        filename = "Profile.pdf"  

        # when / then
        with self.assertRaises(ValueError) as context:
            load_pdf(filename)

        self.assertIn("DOCUMENT_STORAGE_PATH environment variable is not set", str(context.exception))


    def test_chunk_data_splits_documents_correctly(self):
        """
        Verification of splitting documents into chunks.
        """

        # given
        long_text = "This is a test sentence. " * 100
        doc = Document(page_content=long_text)

        # when
        chunks = chunk_data([doc])

        # then
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(isinstance(chunk, Document) for chunk in chunks))
        self.assertTrue(all(len(chunk.page_content) <= 500 for chunk in chunks))


    def test_chunk_data_maintains_overlap(self):
        """
        Verification of chunk overlapping.
        """

        # given
        text = "a" * 450 + "bc" * 50 + "d" * 100
        doc = Document(page_content=text)
        
        # when
        chunks = chunk_data([doc])
        
        # then
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].page_content[-50:], chunks[1].page_content[:50])  # overlap
    

    @mock.patch.dict(os.environ, {"EMBEDDING_MODEL": "mock-embed-model"}, clear=True)
    @mock.patch("llm.rag.OllamaEmbeddings")
    @mock.patch("llm.rag.FAISS")
    def test_vectorize_documents_calls_faiss_with_correct_arguments(self, mock_faiss, mock_embeddings):
        """
        Verify if vectorization library is called, when passing chunks. 
        """

        # given
        mock_embed_instance = mock.Mock()
        mock_embeddings.return_value = mock_embed_instance

        mock_vectorstore = mock.Mock()
        mock_faiss.from_documents.return_value = mock_vectorstore

        chunks = [
            Document(page_content="Chunk 1"),
            Document(page_content="Chunk 2")
        ]

        # when
        result = vectorize_documents(chunks)

        # then
        mock_embeddings.assert_called_once_with(model="mock-embed-model")
        mock_faiss.from_documents.assert_called_once_with(chunks, mock_embed_instance)
        self.assertEqual(result, mock_vectorstore)


    @mock.patch.dict(os.environ, {}, clear=True)
    def test_vectorize_documents_raises_error_when_env_missing(self):
        """
        If there is no embedding model specified, vectorization should fail.
        """

        # given
        chunks = [Document(page_content="Chunk 1")]

        # when / then
        with self.assertRaises(ValueError) as context:
            vectorize_documents(chunks)

        self.assertIn("EMBEDDING_MODEL environment variable is not set", str(context.exception))

    
    @mock.patch("llm.rag.RetrievalQA")
    def test_build_qa_chain_builds_with_llm_and_retriever(self, mock_retrieval_qa):
        """
        
        """

        # given
        mock_model = mock.Mock()
        mock_vectorstore = mock.Mock()
        mock_retriever = mock.Mock()

        mock_vectorstore.as_retriever.return_value = mock_retriever

        mock_chain = mock.Mock()
        mock_retrieval_qa.from_chain_type.return_value = mock_chain

        # when
        result = build_qa_chain(mock_model, mock_vectorstore)

        # then
        mock_vectorstore.as_retriever.assert_called_once()
        mock_retrieval_qa.from_chain_type.assert_called_once_with(
            llm=mock_model,
            retriever=mock_retriever,
            return_source_documents=False
        )
        self.assertEqual(result, mock_chain)


    def test_run_chain_calls_chain_and_returns_result(self):
        """

        """
        # given
        mock_chain = mock.Mock()
        mock_chain.return_value = "Final answer"
        prompt = "What is AGI?"

        # when
        result = run_chain(mock_chain, prompt)

        # then
        mock_chain.assert_called_once_with(prompt)
        self.assertEqual(result, "Final answer")


