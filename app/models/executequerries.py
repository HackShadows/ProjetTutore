from .connexion import *

def SelectAll(query, params=None):
	try:
		cursor.execute(query, params or ())
		return cursor.fetchall()
	except Exception as e:
		print("Database error:", e)
		return []


def SelectOne(query, params=None):
	try:
		cursor.execute(query, params or ())
		return cursor.fetchone()
	except Exception as e:
		print("Database error:", e)
		return None


conn, cursor = get_cursor()
# print(SelectAll("SELECT * FROM Lieu"))


def execute_select_query(query, params=[]):
	"""
	Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
	"""
	connexion, cursor = get_cursor()
	try:
		cursor.execute(query, params)
		result = cursor.fetchall()
		return result
	except psycopg2.Error as e:
		# logger.error(e)
		return None


def execute_other_query(query, params=[]):
	"""
	Méthode générique pour exécuter une requête INSERT, UPDATE, DELETE.
	Utilisée par des fonctions plus spécifiques.
	"""
	connexion, cursor = get_cursor()
	try:
		cursor.execute(query, params)
		connexion.commit()
		result = cursor.rowcount
		return result
	except psycopg2.Error as e:
		print(f"Erreur dans executeotherquery, pour {query} : {e}")
		# logger.error(e)
		return None


def select(nomTable, attributs="*", limit=None, where="", orderby=None, desc=False, distinct=False,
		   join=None, using=None, groupby="", count=""):
	"""
	Retourne les colonnes attributs de la table nomTable
	String nomTable : nom de la table
	String ou List attributs : liste des attributs
	Int limit : taille de la limite
	String where : fstring précisant les conditions du where
	String ou List orderby : Les éléments selon lesquels faire le ORDER BY
	Bool ou List desc : Booléens pour savoir si l'ordre est ASC ou DESC
	Bool distinct : Indique si les éléments sont DISTINCT ou non
	String ou List join : Noms des tables à join
	String ou List using : Noms des attributs à utiliser dans le using
	String ou List group by : Noms des attributs dans le GROUP BY
	String ou List count : Nom de l'attribut à compter
	"""
	if type(attributs) == str:
		attributs = [attributs]
	if type(orderby) == str:
		orderby = [orderby]
	if type(join) == str:
		join = [join]
	if type(using) == str:
		using = [using]
	if type(groupby) == str:
		groupby = [groupby]
	if type(desc) == bool and orderby:
		desc = [desc for _ in range(len(orderby))]
	if orderby:
		orderby = sql.SQL(', ').join([
			sql.SQL('{} {}'.format(
				sql.Identifier(attr).as_string(connexion),
				'DESC' if desc[i] else ''
			)) for i, attr in enumerate(orderby)
		])
		orderby = sql.SQL('ORDER BY {}').format(orderby)
	else:
		orderby = sql.SQL('')
	if attributs == ["*"]:
		attributs = sql.SQL('*')
	else:
		attributs = sql.SQL(', ').join(
			[sql.Identifier(attr) for attr in attributs])
	if limit:
		limit = sql.SQL('LIMIT {limit}').format(limit=limit)
	else:
		limit = sql.SQL('')
	if where != "":
		where = sql.SQL('WHERE {where}').format(where=sql.SQL(where))
	else:
		where = sql.SQL('')
	if distinct:
		distinct = sql.SQL('DISTINCT')
	else:
		distinct = sql.SQL('')
	if join and using:
		join = sql.SQL(' ').join([sql.SQL('JOIN {join} USING ({using})').format(
			join=sql.Identifier(join[i]), using=sql.Identifier(using[i])) for i in range(len(join))])
	elif join:
		join = sql.SQL(' ').join([sql.SQL('JOIN {join}').format(
			join=sql.Identifier(join)) for join in join])
	else:
		join = sql.SQL('')
	if groupby != [""]:
		grp = sql.SQL(', ').join([sql.Identifier(attr) for attr in groupby])
		groupby = sql.SQL('GROUP BY {groupby}').format(groupby=grp)
	else:
		groupby = sql.SQL('')
	if count != "":
		count = sql.SQL(', COUNT({count}) as c').format(count=count)
	else:
		count = sql.SQL('')
	query = sql.SQL(
		'SELECT {fields} {count} {distinct} FROM {table} {join} {where} {groupby} {orderby} {limit}').format(
		table=sql.Identifier(nomTable), fields=attributs, count=count, limit=limit, where=where, groupby=groupby,
		orderby=orderby, distinct=distinct, join=join)
	print(f"query : {query.as_string(conn)}")
	return execute_select_query(query)
