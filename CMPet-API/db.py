import sqlalchemy
from databases import Database
from sqlalchemy import exc


from config import data_settings

while True:
    try:
        DATABASE_URL = f"{data_settings.DB_MODE}://{data_settings.DB_USER}:{data_settings.DB_PSWD}@{data_settings.DB_HOST}:{data_settings.DB_PORT}/{data_settings.DB_NAME}?charset=utf8"

        database = Database(DATABASE_URL)

        metadata = sqlalchemy.MetaData()

        engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=3, max_overflow=0, connect_args={'connect_timeout': 120},
                                          pool_pre_ping=True, echo=True)

        break  # Break the loop if the connection is successful
    except exc.OperationalError:
        # Handle IncompleteRead error here
        continue  # Continue the loop if an IncompleteRead error occur
