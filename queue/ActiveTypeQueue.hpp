//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#ifndef _ActiveTypeQueue_INCLUDE_
#define _ActiveTypeQueue_INCLUDE_

#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <iostream>
#include "ActiveTypeQueueEntry.hpp"

/**
 * Class for the active type queue.
 * Overloaded operator functions are placed in the queue to be 
 * executed later.
 */
class ActiveTypeQueue
{
  friend void * launch(void *);
  friend void leave(int);

  public:
    static ActiveTypeQueue * atQueue;

    template <typename P>
    void push(locint, P, locint, P, locint, P, locint, P, 
              void (*) (const ActiveTypeQueueEntry&, const int&));
    template <typename P>
    void copyTo(ActiveTypeQueueEntry *,
              locint, P, locint, P, locint, P, locint, P, 
              void (*) (const ActiveTypeQueueEntry&, const int&));
    void blockUntilEmpty(void);

  private:

    ActiveTypeQueue(const int& slices);
    ~ActiveTypeQueue();

    pthread_t * thread_ids;

    struct timespec sleep_amt;
     
    unsigned int slices; 
    queue_int tail;
    queue_int queueWrite;
#ifdef HAVE_OPA
    entryWrapper * queue;
#else
    slice_bits full;
    /* Pointer to the internal queue, which is a pointer to a list of
     * pointers of type ActiveTypeQueueEntry. */
    ActiveTypeQueueEntry ** queue;
    pthread_rwlock_t * rw_locks;
#endif
};

template <typename P>
inline void
ActiveTypeQueue::copyTo(ActiveTypeQueueEntry * to,
    locint xLoc, P xVal, locint yLoc, P yVal,
    locint zLoc, P zVal, locint rLoc, P rVal,
    void (*func) (const ActiveTypeQueueEntry&, 
                  const int&))
{
  to->x_loc = xLoc;
  to->y_loc = yLoc;
  to->z_loc = zLoc;
  to->r_loc = rLoc;
  memcpy(&(to->x_val), &xVal, sizeof(double));
  memcpy(&(to->y_val), &yVal, sizeof(double));
  memcpy(&(to->z_val), &zVal, sizeof(double));
  memcpy(&(to->r_val), &rVal, sizeof(double));
  to->func = func;
#ifndef HAVE_OPA
  to->reads_bitmap = 0;
#endif
}

template <typename P>
void 
ActiveTypeQueue::push(locint xLoc, P xVal, locint yLoc, P yVal,
                      locint zLoc, P zVal, locint rLoc, P rVal,
                      void (*func) (const ActiveTypeQueueEntry&, 
                                    const int&))
{
#ifdef HAVE_OPA
  entryWrapper * nextEntry = &queue[queueWrite];
  while (OPA_load_int(&nextEntry->cnt) > 0)
    nanosleep(&sleep_amt, NULL);

//  OPA_write_barrier();
  copyTo(nextEntry->data, 
         xLoc, xVal, yLoc, yVal, zLoc, zVal, rLoc, rVal, func);
  OPA_store_int(&nextEntry->cnt, slices);

  ++queueWrite;
#else
  ActiveTypeQueueEntry * nextEntry = queue[queueWrite];
  while (!nextEntry->checkForRead(full))
    nanosleep(&sleep_amt, NULL);
  pthread_rwlock_wrlock(&rw_locks[queueWrite]);
  copyTo(nextEntry, 
         xLoc, xVal, yLoc, yVal, zLoc, zVal, rLoc, rVal, func);
  pthread_rwlock_unlock(&rw_locks[queueWrite]);
  ++queueWrite;
#endif
}

void * launch(void *);
void leave(int);

#endif /* _ActiveTypeQueue_INCLUDE_ */
