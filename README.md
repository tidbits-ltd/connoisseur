# Connoisseur

Connoisseur is an open source financial data aggregator for people and businesses. Connoisseur will be deployed as a cloud service, and will integrate with existing financial data APIs such as Plaid. THe financial data will be stored in a secure database, and a well defined API will be presented for use by cloud applications authorized by the user.

## Development Roadmap

1. Develop importers of financial statements to serve as raw seed data
2. Develop folder/storage scheme for raw seed data
3. Design database + API
4. Process raw seed data and store in database
5. Integrate with Plaid and other financial data APIs
6. Deploy on cloud service provider. Connoisseur itself will be provider agnostic, but we can figure out which one to start with.
