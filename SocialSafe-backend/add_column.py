from playhouse.migrate import *

DATABASE = SqliteDatabase('restaurants.sqlite')
migrator = SqliteMigrator(DATABASE)

social_distancing_rating = DecimalField(2,1)

migrate(
migrator.add_column('review', 'social_distancing_rating', social_distancing_rating),
)
