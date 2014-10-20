//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#include <cstring>
#include "ActiveTypeQueue.hpp"
#ifdef HAVE_OPA
#include "sched.h"
#endif /* HAVE_OPA */

/* struct for passing data to threads */
struct thread_data {
  ActiveTypeQueue * queue;
  unsigned int slice;
};

/*
 * Initialize the queue and launch the threads which access the queue.
 * numSlices is the number of slices in the queue, and thus the number
 * of threads which will work on the queue
 */
ActiveTypeQueue::ActiveTypeQueue(const int& numSlices)
{
  int err, i;

  slices = numSlices;

  sleep_amt.tv_sec = 0;
  sleep_amt.tv_nsec = 200000;

#ifdef HAVE_OPA
  queue = (entryWrapper *) malloc(sizeof(entryWrapper) * MAX_QUEUE_SIZE);
#else
  queue = (ActiveTypeQueueEntry **) 
                    malloc(sizeof(ActiveTypeQueueEntry *) * MAX_QUEUE_SIZE);
  rw_locks = (pthread_rwlock_t *)
                    malloc(sizeof(pthread_rwlock_t) * MAX_QUEUE_SIZE);
  for (i = 0; i < slices; ++i)
    full ^= 1 << i;
#endif /* HAVE_OPA */
  queueWrite = 0;
  tail = MAX_QUEUE_SIZE - 1;

  for (i = 0; i < MAX_QUEUE_SIZE; ++i) {
#ifdef HAVE_OPA
    queue[i].data = new ActiveTypeQueueEntry();
    OPA_store_int(&queue[i].cnt, 0);
#else
    queue[i] = new ActiveTypeQueueEntry();
    pthread_rwlock_init(&rw_locks[i], NULL);
#endif /* HAVE_OPA */
  }

  thread_ids = (pthread_t *) malloc(sizeof(pthread_t) * slices);

  for (i = 0; i < slices; ++i) {
    struct thread_data * td = 
          (struct thread_data *) malloc(sizeof(struct thread_data *));
    td->queue = this;
    td->slice = i;
    if (err = pthread_create(&thread_ids[i], NULL, launch, (void *) td)) {
      fprintf(stderr, "pthread_create() failed: %s\n", strerror(err));
      exit(EXIT_FAILURE);
    }
  }
}

ActiveTypeQueue::~ActiveTypeQueue() 
{
  int err, i;

  for (i = 0; i < slices; ++i) {
#ifndef HAVE_OPA
    if (err = pthread_kill(thread_ids[i], SIGUSR1)) {
      fprintf(stderr, "pthread_kill() failed: %d\n", err);
      exit(EXIT_FAILURE);
    }
#endif /* !(HAVE_OPA) */
    if (err = pthread_join(thread_ids[i], NULL)) {
      fprintf(stderr, "pthread_join() failed: %d\n", err);
      exit(EXIT_FAILURE);
    }
  }
#ifndef HAVE_OPA
  for (i = 0; i < MAX_QUEUE_SIZE; ++i) {
    pthread_rwlock_destroy(&rw_locks[i]);
  }
#endif /* !(HAVE_OPA) */

  free(thread_ids);
  free(queue);
}

void ActiveTypeQueue::blockUntilEmpty(void)
{
#ifdef HAVE_OPA
  entryWrapper * entry = &queue[queueWrite - 1];
  while (OPA_load_int(&entry->cnt) > 0)
        ;
#else
  ActiveTypeQueueEntry * entry = queue[queueWrite - 1];
  while (!entry->checkForRead(full))
    ;
#endif
}

/** Outside methods **/

/* Called when creating the new thread to control the queue */
void * launch(void * arg)
{
  struct thread_data * td = static_cast<struct thread_data *>(arg);
  ActiveTypeQueue * atq = td->queue;
  unsigned int slice    = td->slice;
  queue_int read_loc;
#ifdef HAVE_OPA
  entryWrapper * entry;
  
  for (read_loc = 0; ; ++read_loc) {
    entry = &atq->queue[read_loc];
    while (entry == &atq->queue[atq->tail])
      nanosleep(&atq->sleep_amt, NULL);
    while (OPA_load_int(&entry->cnt) == 0)
      nanosleep(&atq->sleep_amt, NULL);

//    OPA_read_barrier();
    entry->data->func(*(entry->data), slice);

    if (OPA_fetch_and_decr_int(&entry->cnt) == 1) {
      ++atq->tail;
    }
  }
#else
  slice_bits slice_toggle = 1 << slice;
  ActiveTypeQueueEntry * entry;

  signal(SIGUSR1, leave);

  for (read_loc = 0; ; ++read_loc) {
    entry = atq->queue[read_loc];
    while (entry == atq->queue[atq->tail])
      nanosleep(&atq->sleep_amt, NULL);
    while (entry->checkForRead(slice_toggle))
      nanosleep(&atq->sleep_amt, NULL);
    
    pthread_rwlock_rdlock(&atq->rw_locks[read_loc]);
    entry->func(*entry, slice);
    pthread_rwlock_unlock(&atq->rw_locks[read_loc]);

    if (entry->toggleAndCheck(slice_toggle, atq->full)) {
      ++atq->tail;
    }
  }
#endif
  return NULL;
}

void leave(int sig)
{
#ifndef HAVE_OPA
  ActiveTypeQueue * atq = ActiveTypeQueue::atQueue;
  ActiveTypeQueueEntry * entry;
  for (int i = 0; i < MAX_QUEUE_SIZE; ++i) {
    entry = *(atq->queue + i);
    if (entry != NULL)
      delete entry;
  }
  pthread_exit(NULL);
#endif /* !(HAVE_OPA) */
}
