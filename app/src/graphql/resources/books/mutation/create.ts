import { generateId, getCollection, handleCouchbaseError } from "apollo-couchbase";
import { Book, BookContentInput, BooksResponse } from "../../../generated-types";

const COLLECTION_NAME = "books";

async function createBook(content: BookContentInput): Promise<Book> {
  const collection = await getCollection(COLLECTION_NAME); 
  const id = generateId(COLLECTION_NAME);
  await collection.insert(id, content);
  return { id, content }
}

export async function resolver(_: any, { contents }: { contents: BookContentInput[] }, context: any): Promise<BooksResponse> {
  const results = await Promise.allSettled(contents.map(createBook));
  const response = results.reduce<BooksResponse>((acc, result) => {
      if (result.status === "fulfilled") {
        acc.records.push(result.value);
      } else {
        acc.errors.push(handleCouchbaseError(result.reason));
      }
      return acc;
    }, {
      records: [],
      errors: []
    }
  );
  return response;
}
