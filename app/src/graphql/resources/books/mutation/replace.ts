import { getCollection, handleCouchbaseError } from "apollo-couchbase";
import { Book, BookReplaceInput, BooksResponse } from "../../../generated-types";

const COLLECTION_NAME = "books";

async function replaceBook(record: BookReplaceInput): Promise<Book> {
  const collection = await getCollection(COLLECTION_NAME);
  await collection.replace(record.id, record.content);
  return record;
}

export async function resolver(_: any, { records }: { records: BookReplaceInput[] }): Promise<BooksResponse> {
  const results = await Promise.allSettled(records.map(replaceBook));
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
