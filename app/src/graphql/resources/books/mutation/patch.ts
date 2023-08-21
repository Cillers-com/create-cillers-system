import { getCollection, handleCouchbaseError } from "apollo-couchbase";
import { MutateInSpec } from "couchbase";
import { Book, BookPatchInput, BooksResponse } from "../../../generated-types";

const COLLECTION_NAME = "books";

async function patchBook(record: BookPatchInput): Promise<Book> {
  const collection = await getCollection(COLLECTION_NAME);
  const specs = Object.entries(record.content).map(([field, value]) => {
    return MutateInSpec.replace(field, value);
  });
  await collection.mutateIn(record.id, specs);
  const book = await collection.get(record.id);
  return { id: record.id, content: book.content };
}

export async function resolver(_: any, { records }: { records: BookPatchInput[] }): Promise<BooksResponse> {
  const results = await Promise.allSettled(records.map(patchBook));
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
