#Flask dependencies
from flask import current_app

#App dependencies
from app import db


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index,
                                    id=model.id, body=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


class SearchableMixin(object):
    """
    Class to manage Full text search for app.
    """
    @classmethod
    def search(cls, expression, page, per_page):
        """
        Actual search method for every class that class the search engine method
        """
        if current_app.config['ELASTICSEARCH_URL']:
            ids, total = query_index(cls.__tablename__, expression, page, per_page)
        else:
            idss = db.session.\
                execute(
                    "SELECT id FROM "+cls.__tablename__+" "
                    "WHERE "+cls.__searchable__[0]+" "
                    "LIKE '%"+expression+"%'; "
                )
            ids = list([i[0] for i in idss])
            del idss
            total = db.session.\
                execute(
                    "SELECT COUNT(*) FROM "+cls.__tablename__+" "
                    "WHERE "+cls.__searchable__[0]+" "
                    "LIKE '%"+expression+"%'; "
                ).first()[0]
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
