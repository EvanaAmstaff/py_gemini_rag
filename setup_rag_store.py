import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

FILE_SEARCH_STORE_NAME = "fileSearchStores/gas-documentation-rag-store-ftwf69nijziu"

doc_dirs = ["gas_docs_txt", "gemini_api_docs_txt"]

for doc_directory in doc_dirs:
    print(f"\n📂 ディレクトリ '{doc_directory}' の処理開始...")

    for filename in os.listdir(doc_directory):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(doc_directory, filename)
        print(f"  - アップロード中: {filename}")

        # ✅ file は「文字列パス」で渡すのが正解
        op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=FILE_SEARCH_STORE_NAME,
            file=file_path,
        )

        while True:
            try:
                current = client.operations.get(op)
                if current.done:
                    break
            except Exception as e:
                print("    ⚠️ 一時エラー再試行:", e)

            time.sleep(2)

print("\n✅ すべてのファイルをアップロードしました")








