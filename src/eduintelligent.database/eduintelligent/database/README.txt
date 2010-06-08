=========================
User/Interaction tracking
=========================

  ($Id: README.txt 2098 2007-10-08 11:21:50Z helmutm $)

  >>> from cybertools.tracking.btree import TrackingStorage

Let's create a tracking storage and store a few tracks in it. A track
is basically an arbitrary mapping. (In the following examples we
ignore the ``run`` argument and use a 0 value for it; thus we are just
working with the current run of a task.)

  >>> tracks = TrackingStorage()
  >>> tracks.saveUserTrack('a001', 0, 'u1', {'somekey': 'somevalue'})
  '0000001'
  >>> t1 = tracks.getUserTracks('a001', 0, 'u1')
  >>> len(t1)
  1
  >>> t1[0].data
  {'somekey': 'somevalue'}
  >>> tracks.getUserNames('a001')
  ['u1']
  >>> tracks.getUserNames('a002')
  []
  >>> [str(id) for id in tracks.getTaskIds()]
  ['a001']

We can query the tracking storage using the tracks' metadata. These
are mapped to btree indexes, so we get fast access to the resulting
track data.

  >>> tracks.query(taskId='a001')
  [<Track ['a001', 1, 'u1', '...-...-... ...:...']: {'somekey': 'somevalue'}>]

  >>> tracks.saveUserTrack('a002', 0, 'u1', {'somekey': 'anothervalue'})
  '0000002'
  >>> result = tracks.query(userName='u1')
  >>> len(result)
  2

By supplying a list we can also search for more than one value in one query.

  >>> result = tracks.query(taskId=('a001', 'a002'))
  >>> len(result)
  2

What happens if we store more than on record for one set of keys?

  >>> tracks.saveUserTrack('a001', 0, 'u1', {'somekey': 'newvalue'})
  '0000003'
  >>> t2 = tracks.getUserTracks('a001', 0, 'u1')
  >>> [t.data for t in t2]
  [{'somekey': 'somevalue'}, {'somekey': 'newvalue'}]

It is also possible to retrieve the last entry for a set of keys directly.

  >>> tracks.getLastUserTrack('a001', 0, 'u1')
  <Track ['a001', 1, 'u1', ...]: {'somekey': 'newvalue'}>

Instead of creating a new track object for each call one can also replace
an existing one (if present). The replaced entry is always the last one
for a given set of keys.

  >>> tracks.saveUserTrack('a001', 0, 'u1', {'somekey': 'newvalue2'}, update=True)
  '0000003'
  >>> t3 = tracks.getUserTracks('a001', 0, 'u1')
  >>> [t.data for t in t3]
  [{'somekey': 'somevalue'}, {'somekey': 'newvalue2'}]

  >>> tracks.saveUserTrack('a001', 0, 'u2', {'somekey': 'user2'}, update=True)
  '0000004'
  >>> t4 = tracks.getUserTracks('a001', 0, 'u2')
  >>> [t.data for t in t4]
  [{'somekey': 'user2'}]

The tracks of a tracking store may be reindexed:

  >>> tracks.reindexTracks()

Runs
----

We may explicitly start a new run for a given task. This will also replace
the task's current run.

  >>> tracks.startRun('a001')
  3
  >>> tracks.saveUserTrack('a001', 0, 'u1', {'k1': 'value1'})
  '0000005'
  >>> tracks.getLastUserTrack('a001', 0, 'u1')
  <Track ['a001', 3, 'u1', ...]: {'k1': 'value1'}>

We still have access to older runs.

  >>> tracks.getLastUserTrack('a001', 1, 'u1')
  <Track ['a001', 1, 'u1', ...]: {'somekey': 'newvalue2'}>

We can also retrieve a run object with the run's data.

  >>> tracks.getRun(runId=3)
  <Run 3, ..., ..., False>

We can also use the taskId for retrieving a task's current run.

  >>> tracks.getRun(taskId='a001')
  <Run 3, ..., ..., False>

When we stop a run explicitly it is marked as ``finished``.

  >>> tracks.stopRun('a001')
  3
  >>> tracks.getRun(runId=3)
  <Run 3, ..., ..., True>
  >>> tracks.getRun(runId=3).finished
  True

Stopping a run removes it from the set of current runs, so the associated
task hasn't got a current run any longer:

  >>> tracks.getRun('a001') is None
  True

We can also mark earlier runs by stopping them.

  >>> tracks.getRun(runId=2)
  <Run 2, ..., ..., False>
  >>> tracks.stopRun('a001', 2)
  2
  >>> tracks.getRun(runId=2)
  <Run 2, ..., ..., True>

