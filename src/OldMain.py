# import asyncio
# import os
# import traceback
# from typing import List, Optional

# from dotenv import load_dotenv

# load_dotenv()

# from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
# from llama_index.core.base.llms.types import ChatMessage, MessageRole
# from llama_index.core.schema import NodeWithScore
# from llama_index.core.workflow import Context, Event, StartEvent, StopEvent, Workflow, step
# from llama_index.embeddings.cohere import CohereEmbedding
# from llama_index.llms.cohere import Cohere
# import gradio as gr

# from src.structured_data import build_structured_response, is_structured_query

# # ===============================
# # Events
# # ===============================

# class InputValidatedEvent(Event):
#     query: str
#     retry_count: int = 0


# class RetrievalDoneEvent(Event):
#     query: str
#     nodes: List[NodeWithScore]


# class RetrySearchEvent(Event):
#     query: str
#     reason: str


# class SynthesisReadyEvent(Event):
#     query: str
#     nodes: List[NodeWithScore]


# class AnswerReadyEvent(Event):
#     answer: str


# # ===============================
# # Helpers
# # ===============================

# def normalize_query(query: Optional[str]) -> str:
#     if query is None:
#         raise ValueError("query_missing")

#     normalized = query.strip()
#     if not normalized:
#         raise ValueError("query_empty")

#     if len(normalized) < 3:
#         raise ValueError("query_too_short")

#     return normalized


# def expand_query_for_retry(query: str, reason: str) -> str:
#     if reason == "no_results":
#         return f"ניסיון נוסף: {query}"

#     if reason == "low_confidence":
#         return f"תמצית והקשר: {query}"

#     return query


# def compute_best_score(nodes: List[NodeWithScore]) -> float:
#     if not nodes:
#         return 0.0

#     return max(float(node.score or 0.0) for node in nodes)


# def should_retry(nodes: List[NodeWithScore], min_score: float = 0.35) -> tuple[bool, str]:
#     if not nodes:
#         return True, "no_results"

#     score = compute_best_score(nodes)
#     if score < min_score:
#         return True, "low_confidence"

#     return False, ""


# def build_context_block(nodes: List[NodeWithScore]) -> str:
#     if not nodes:
#         return "אין קטעי הקשר זמינים."

#     parts = []
#     for index, node in enumerate(nodes, start=1):
#         metadata = node.node.metadata or {}
#         file_name = metadata.get("file_name") or metadata.get("source_file") or "unknown_source"
#         title = metadata.get("title") or file_name
#         score = float(node.score or 0.0)
#         parts.append(
#             f"[{index}] source={file_name} | title={title} | score={score:.3f}\n{node.node.get_content()}"
#         )

#     return "\n\n".join(parts)


# def build_prompt(query: str, context_block: str) -> str:
#     return (
#         "הסתמך על ההקשר הבא בלבד כדי לענות על השאלה.\n"
#         "אם אין בהקשר תשובה, אמור שאינך יודע.\n\n"
#         f"הקשר:\n{context_block}\n\n"
#         f"שאלה: {query}\n"
#         "תשובה:"
#     )


# # ===============================
# # Runtime loading
# # ===============================

# def prepare_documents() -> List:
#     loader = SimpleDirectoryReader("data/md_files", recursive=True)
#     documents = loader.load_data()

#     for document in documents:
#         metadata = dict(document.metadata or {})
#         metadata.setdefault("source_file", metadata.get("file_name") or "unknown_source")
#         metadata.setdefault(
#             "title",
#             document.text.splitlines()[0].replace("#", "").strip() if document.text else "unknown_title",
#         )
#         document.metadata = metadata

#     return documents


# def build_runtime() -> tuple[VectorStoreIndex, Cohere]:
#     cohere_key = os.environ.get("COHERE_API_KEY")
#     if not cohere_key:
#         raise ValueError("COHERE_API_KEY Missing")

#     embed_model = CohereEmbedding(model_name="embed-multilingual-v3.0", api_key=cohere_key)
#     llm = Cohere(model="command-r-08-2024", api_key=cohere_key)

#     Settings.embed_model = embed_model
#     Settings.llm = llm

#     documents = prepare_documents()
#     index = VectorStoreIndex.from_documents(documents, show_progress=True)
#     return index, llm


# # ===============================
# # Workflow
# # ===============================

# class RAGWorkflow(Workflow):
#     @step
#     async def validate_input(self, ctx: Context, ev: StartEvent) -> InputValidatedEvent | StopEvent:
#         try:
#             # שליפת השאילתה מתוך ה-StartEvent הכללי בצורה בטוחה
#             query_text = ev.get("query", "")
#             query = normalize_query(query_text)
#         except ValueError as error:
#             reason = str(error)
#             if reason == "query_empty":
#                 return StopEvent(result="שגיאה: השאילתה ריקה. אנא נסה שנית.")
#             if reason == "query_too_short":
#                 return StopEvent(result="שגיאה: השאילתה קצרה מדי. נסה לתאר את הבעיה בפירוט.")
#             return StopEvent(result="שגיאה: לא ניתן לעבד את השאילתה.")

#         await ctx.store.set("original_query", query)
#         await ctx.store.set("retry_count", 0)
#         return InputValidatedEvent(query=query)

#     @step
#     async def retrieve_context(self, ctx: Context, ev: InputValidatedEvent | RetrySearchEvent) -> RetrievalDoneEvent:
#         runtime = get_runtime_cache()
#         index = runtime["index"]
#         query = ev.query
#         retriever = index.as_retriever(similarity_top_k=5)
#         nodes = retriever.retrieve(query)
#         await ctx.store.set("last_query", query)
#         return RetrievalDoneEvent(query=query, nodes=nodes)

#     @step
#     async def validate_results(self, ctx: Context, ev: RetrievalDoneEvent) -> SynthesisReadyEvent | RetrySearchEvent | StopEvent:
#         should_retry_now, reason = should_retry(ev.nodes)
#         if should_retry_now:
#             retry_count = await ctx.store.get("retry_count")
#             if retry_count >= 1:
#                 return StopEvent(
#                     result="לא מצאתי תוצאות מספיק רלוונטיות במאגר. נסה לנסח את השאלה אחרת או הוסף מידע נוסף."
#                 )

#             await ctx.store.set("retry_count", retry_count + 1)
#             expanded_query = expand_query_for_retry(ev.query, reason)
#             return RetrySearchEvent(query=expanded_query, reason=reason)

#         await ctx.store.set("retrieved_nodes", ev.nodes)
#         return SynthesisReadyEvent(query=ev.query, nodes=ev.nodes)

#     @step
#     async def generate_answer(self, ctx: Context, ev: SynthesisReadyEvent) -> AnswerReadyEvent:
#         runtime = get_runtime_cache()
#         llm = runtime["llm"]
#         context_block = build_context_block(ev.nodes)
#         prompt = build_prompt(ev.query, context_block)
#         response = await llm.achat([ChatMessage(role=MessageRole.USER, content=prompt)])
#         answer = response.message.content or ""
#         return AnswerReadyEvent(answer=str(answer))

#     @step
#     async def finish(self, ctx: Context, ev: AnswerReadyEvent) -> StopEvent:
#         await ctx.store.set("final_answer", ev.answer)
#         return StopEvent(result=ev.answer)


# # ===============================
# # App runtime
# # ===============================

# runtime_cache = None


# def get_runtime_cache() -> dict:
#     global runtime_cache

#     if runtime_cache is None:
#         runtime_cache = {"index": None, "llm": None}

#     if runtime_cache["index"] is None or runtime_cache["llm"] is None:
#         index, llm = build_runtime()
#         runtime_cache["index"] = index
#         runtime_cache["llm"] = llm

#     return runtime_cache


# async def run_rag_workflow(query: str) -> str:
#     if is_structured_query(query):
#         return build_structured_response(query)

#     get_runtime_cache()
#     workflow = RAGWorkflow(timeout=30)

#     # הפעלה נקייה: העברת הפרמטר ישירות לתוך ה-Workflow
#     result = await workflow.run(query=query)
#     return str(result)


# # ===============================
# # Gradio UI
# # ===============================

# def gradio_interface(query: str) -> str:
#     try:
#         return asyncio.run(run_rag_workflow(query))
#     except Exception as exc:
#         traceback.print_exc()
#         return f"שגיאה: {exc}"


# interface = gr.Interface(
#     fn=gradio_interface,
#     inputs=gr.Textbox(label="שאל שאלה", placeholder="למשל: מה הוא RAG?"),
#     outputs=gr.Textbox(label="תשובה", lines=5),
#     title="Event-Driven RAG System",
#     description="Workflow מבוסס אירועים ל-RAG על קבצי Markdown",
# )


# def main() -> None:
#     print("בנה ממשק Gradio לשאילתות על קבצי MD")
#     get_runtime_cache()
#     interface.launch()


# if __name__ == "__main__":
#     main()