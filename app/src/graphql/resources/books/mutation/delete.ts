import { getCollection, handleCouchbaseError } from "apollo-couchbase";
import { BooksDeleteResponse } from "../../../generated-types";

const COLLECTION_NAME = "books";

async function deleteBook(id: string): Promise<string> {
  const collection = await getCollection(COLLECTION_NAME);
  await collection.remove(id);
  return id;
}

export async function resolver(_: any, { ids }: { ids: string[] }): Promise<BooksDeleteResponse> {
  const results = await Promise.allSettled(ids.map(deleteBook));
  const response = results.reduce<BooksDeleteResponse>((acc, result) => {
      if (result.status === "fulfilled") {
        acc.deletedIds.push(result.value);
      } else {
        acc.errors.push(handleCouchbaseError(result.reason));
      }
      return acc;
    }, {
      deletedIds: [],
      errors: []
    }
  );

  return response;
}
