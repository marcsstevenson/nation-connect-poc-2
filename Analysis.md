# Analysis

This document provides analysis of testing an development options for the project.

## File Search Tool in Gemini API

[Docs](https://ai.google.dev/gemini-api/docs/file-search)

This a relatively new feature in the Gemini API that allows for RAG searching through files. It can be useful for projects that require efficient retrieval of information from large datasets or documents. Performance, ease of use, and pricing all seem extremely favorable when compared to other similar tools.

### Testing Methodology

The following steps were taken to test the Gemini API File Search Tool:

- Upload 90 files from the [Waitangi Tribunal Documents](https://www.waitangitribunal.govt.nz/en/reports-and-documents). The chosen PDF files combined with older large documents and newer smaller documents.
- Ingest the files into the Gemini API File Search Tool.
- Run a series of queries to evaluate the performance and accuracy of the search results.
- Use LLM as a judge to assess the relevance of the retrieved documents.
- Record the response times and costs associated with the queries.

Note that the combined size of the files is 1GB, which is still within the limits of the Free tier of the Gemini API File Search Tool.

### Testing Results

[eval-results.csv](src\gemini-file-search\eval-results.csv)
The testing results indicate that the Gemini API File Search Tool performs exceptionally well in terms of both speed and accuracy. The average response time for queries averaged ~8 seconds, and the average rated score of the results was 6.3/10 by the LLM judge (although evaluations by a subject mater expert would provide more definitive scoring).

[evals-summary.md](src\gemini-file-search\evals-summary.md)
A summary of the above.

> **Note:** Images within the PDF files were automatically extracted and indexed, which enhanced the search capabilities.

### Cost Analysis

All testing was conducted within the Free tier limits of the Gemini API File Search Tool. The Free tier allows for up to 5,000 queries per month and 10GB of storage, which was sufficient for our testing needs. Therefore, no additional costs were incurred during the testing phase but it does provide limited indication of potential costs for larger scale usage.

### Scaling Considerations

The documentation of the Gemini API File Search Tool indicates that it can handle larger datasets, but performance may vary based on the size of the data and the complexity of the queries. For larger datasets, it is recommended to monitor response times and costs closely.

> Recommendation: Limit the size of each File Search store to under 20 GB to ensure optimal retrieval latencies.

It is typical for RAG database size to be approximately 2-3x the size of the original data due to indexing and metadata storage. Extrapolating from the testing results to a total of ~7200 documents contained within the Waitangi Tribunal reports, this would result in a total database size of approximately 100 GB. This is still well within the maximum capacity of the Gemini API File Search Tool, which supports up to 1 TB of storage but it would increase query times and service costs. The _amount_ of extra query times and service costs are yet unknown without expanded testing and determination of non-functional requirements. It is worth noting that response times of RAGs scale sub-linearly with size, so doubling the size of the database does not double the response times. A rough estimate based on similar tools is a 10x increase in response times when scaling from 1 GB to 100 GB.

Alternatively, large RAG systems can be sharded into multiple smaller RAGs based on topic, date range, or other criteria to help maintain optimal performance but at time of writing there is no obvious way to shard on a given criteria which would aid routing queries to specific shared RAGs.
