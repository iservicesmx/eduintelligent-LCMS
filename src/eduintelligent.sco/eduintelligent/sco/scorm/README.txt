===================
A generic SCORM API
===================

  ($Id: README.txt 1952 2007-08-23 12:40:09Z helmutm $)

In order to work with the SCORM API we first need a tracking storage.

  >>> from cybertools.tracking.btree import TrackingStorage
  >>> tracks = TrackingStorage()

We can now create a ScormAPI adapter. Note that this adapter is stateless
as usually a new instance is created upon each request. In order to comply
with Zope's adapter protocol the constructor can only have one argument,
the context, i.e. the tracking storage. Therefore we have to set the
basic attributes of the adapter with a separate ``init()`` call.

  >>> from cybertools.scorm.base import ScormAPI
  >>> api = ScormAPI(tracks)
  >>> api.init('a001', 0, 'user1')

The first step is always the initialize() call - though in our case it
does not do anything.

  >>> api.initialize()
  '0'

Then we can set some values.

  >>> rc = api.setValue('cmi.interactions.0.id', 'q007')
  >>> rc = api.setValue('cmi.interactions.0.result', 'correct')
  >>> rc = api.setValue('cmi.comments_from_learner.comment', 'Hello SCORM')
  >>> rc = api.setValue('cmi.interactions.1.id', 'q009')
  >>> rc = api.setValue('cmi.interactions.1.result', 'incorrect')

Depending on the data elements the values entered are kept together in
one track or stored in separate track objects. So there is a separate
track for each interaction and one additional track for all the other elements.

  >>> for t in sorted(tracks.values(), key=lambda x: x.data['recnum']):
  ...     print t.data
  {'recnum': -1, 'cmi.comments_from_learner.comment': 'Hello SCORM'}
  {'cmi.interactions.0.id': 'q007', 'cmi.interactions.0.result': 'correct', 'recnum': 0}
  {'cmi.interactions.1.result': 'incorrect', 'cmi.interactions.1.id': 'q009', 'recnum': 1}

Using the getValue() method we can retrieve certain values without having
to care about the storage in different track objects.

  >>> api.getValue('cmi.comments_from_learner.comment')
  ('Hello SCORM', '0')
  >>> api.getValue('cmi.interactions.0.id')
  ('q007', '0')
  >>> api.getValue('cmi.interactions.1.result')
  ('incorrect', '0')

We can also query special elements like _count and _children.

  >>> api.getValue('cmi.objectives._count')
  (0, '0')
  >>> api.getValue('cmi.interactions._count')
  (2, '0')

  >>> api.getValue('cmi.interactions._children')
  (('id', 'type', 'objectives', 'timestamp', 'correct_responses',
    'weighting', 'learner_response', 'result', 'latency', 'description'), '0')
  >>> api.getValue('cmi.objectives.5.score._children')
  (('scaled', 'raw', 'min', 'max'), '0')

We may also update existing tracks using the ``setValue()`` method.

  >>> rc = api.setValue('cmi.comments_from_learner.location', 'q007')
  >>> for t in sorted(tracks.values(), key=lambda x: x.data['recnum']):
  ...     print t.data
  {'recnum': -1, 'cmi.comments_from_learner.comment': 'Hello SCORM',
   'cmi.comments_from_learner.location': 'q007'}
  {'cmi.interactions.0.id': 'q007', 'cmi.interactions.0.result': 'correct', 'recnum': 0}
  {'cmi.interactions.1.result': 'incorrect', 'cmi.interactions.1.id': 'q009', 'recnum': 1}

With the ``setValues()`` method we may set more than one element with
one call. (This is not a SCORM-compliant call but is provided for efficiency
reasons as it allows us to update a bunch of elements with just one
XML-RPC call.)

  >>> data = {'cmi.interactions.2.result': 'correct',
  ...         'cmi.interactions.2.learner_response': 'my answer',
  ... }
  >>> rc = api.setValues(data)

  >>> for t in sorted(tracks.values(), key=lambda x: x.data['recnum']):
  ...     print t.data
  {'recnum': -1, 'cmi.comments_from_learner.comment': 'Hello SCORM',
   'cmi.comments_from_learner.location': 'q007'}
  {'cmi.interactions.0.id': 'q007', 'cmi.interactions.0.result': 'correct', 'recnum': 0}
  {'cmi.interactions.1.result': 'incorrect', 'cmi.interactions.1.id': 'q009', 'recnum': 1}
  {'cmi.interactions.2.learner_response': 'my answer',
   'cmi.interactions.2.result': 'correct', 'recnum': 2}

  >>> api.getValue('cmi.interactions.2.result')
  ('correct', '0')
  >>> api.getValue('cmi.interactions.2.learner_response')
  ('my answer', '0')
  >>> api.getValue('cmi.comments_from_learner.comment')
  ('Hello SCORM', '0')
  >>> api.getValue('cmi.comments_from_learner.location')
  ('q007', '0')
