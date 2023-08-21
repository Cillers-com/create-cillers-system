import { getCouchbaseClient } from "apollo-couchbase";
import { BooksListInput, BooksListResponse } from "../../../generated-types";

export async function resolver(_: any, { query }: { query: BooksListInput }) : Promise<BooksListResponse> {
    const { cluster } = await getCouchbaseClient();
    let queryString = `SELECT META().id, * FROM ${process.env.COUCHBASE_DEFAULT_BUCKET}.${process.env.COUCHBASE_DEFAULT_SCOPE}.books`;
    const response = await cluster.query(queryString);
    const records = response.rows.map((row: any) => { return { id: row.id, content: row.books } });

    return {
        code: 200,
        message: "Success", 
        records: records
    }
}
