import { getCollection, handleCouchbaseError } from "apollo-couchbase";
import { Book, ErrorResponse } from "src/graphql/generated-types";

const COLLECTION_NAME = "books";

export async function resolver(_: any, { ids }: { ids: string[] }) {
    const records: Book[] = [];
    const errors: ErrorResponse[] = [];

    const collection = await getCollection(COLLECTION_NAME);
    const results = await Promise.allSettled(ids.map(id => collection.get(id)));
    results.forEach((result, index) => {
        if (result.status === "fulfilled") {
            records.push({ id: ids[index], content: result.value.content });
        } else {
            errors.push(handleCouchbaseError(result.reason, ids[index]));
        }
    });

    return {
        records,
        errors
    };
}
