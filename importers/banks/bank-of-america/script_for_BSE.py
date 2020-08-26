from Bank_Statement_Extractor import BankStatementExtractor
import asyncio
online_id = input('Enter your online ID: ')
password = input('Enter your password: ')
BOFA = BankStatementExtractor('https://www.bankofamerica.com/',online_id,password)
asyncio.get_event_loop().run_until_complete(BOFA.put_together())