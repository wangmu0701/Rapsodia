//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#ifndef _ActiveTypeQueueEntry_INCLUDE_
#define _ActiveTypeQueueEntry_INCLUDE_

#include <pthread.h>
#include <stdio.h>
#include "defines.hpp"
#ifdef HAVE_OPA
#include "opa_primitives.h"
#endif

/* An active type's value can be either a float or double, depending
 * on the precision of the active type */
union ActiveTypePrec {
  float S;
  double D;
};

/**
 * Class for an entry in the active type queue.
 * Contains the memory location and value of the possible active types
 * (max of four), as well as a function pointer to the necessary code
 */
class ActiveTypeQueueEntry
{
  friend class ActiveTypeQueue;
  friend void * launch(void *);
  friend void leave(int);

  public:

    locint x_loc;
    ActiveTypePrec x_val;
    locint y_loc;
    ActiveTypePrec y_val;
    locint z_loc;
    ActiveTypePrec z_val;
    locint r_loc;
    ActiveTypePrec r_val;

  private:
    /* Single precision */
//    ActiveTypeQueueEntry(locint xl, float xv, locint yl, float yv, 
//                         locint zl, float zv, locint rl, float rv, 
//                         void (*f) (const ActiveTypeQueueEntry&, 
//                                    const int&));
//    /* Double precision */
//    ActiveTypeQueueEntry(locint xl, double xv, locint yl, double yv, 
//                         locint zl, double zv, locint rl, double rv, 
//                         void (*) (const ActiveTypeQueueEntry&,
//                                   const int&));
    ActiveTypeQueueEntry()
    {
#ifndef HAVE_OPA
      reads_bitmap = ~0;
      pthread_rwlock_init(&reads_lock, NULL);
#endif
    }
    ~ActiveTypeQueueEntry()
    {
#ifndef HAVE_OPA
      pthread_rwlock_destroy(&reads_lock);
#endif
    };

#ifndef HAVE_OPA
//    int read();
//    int readsLeft();
    bool checkForRead(const slice_bits&);
    void toggleRead(const slice_bits&);
    bool toggleAndCheck(const slice_bits&, const slice_bits&);

//    int reads;
    slice_bits reads_bitmap;
    pthread_rwlock_t reads_lock;
#endif /* !HAVE_OPA */

    void (*func) (const ActiveTypeQueueEntry&, const int&);
};

#ifdef HAVE_OPA
struct entryWrapper
{
  OPA_int_t cnt;
  ActiveTypeQueueEntry * data;
};
#else
// inline int
// ActiveTypeQueueEntry::read()
// {
//   int prev;
//   pthread_rwlock_wrlock(&reads_lock);
//   prev = reads;
//   --reads;
//   pthread_rwlock_unlock(&reads_lock);
//   return prev;
// }
// 
// inline int
// ActiveTypeQueueEntry::readsLeft()
// {
//   int ret;
//   pthread_rwlock_rdlock(&reads_lock);
//   ret = reads;
//   pthread_rwlock_unlock(&reads_lock);
//   return reads;
// }

inline bool 
ActiveTypeQueueEntry::checkForRead(const slice_bits& r)
{
  slice_bits result;
  pthread_rwlock_rdlock(&reads_lock);
  result = reads_bitmap & r;
  pthread_rwlock_unlock(&reads_lock);
  return result == r ? true : false;
}

inline void 
ActiveTypeQueueEntry::toggleRead(const slice_bits& r)
{
  pthread_rwlock_wrlock(&reads_lock);
  reads_bitmap ^= r;
  pthread_rwlock_unlock(&reads_lock);
}

inline bool
ActiveTypeQueueEntry::toggleAndCheck(const slice_bits& r, 
                                     const slice_bits& full)
{
  slice_bits result;
  pthread_rwlock_wrlock(&reads_lock);
  reads_bitmap ^= r;
  result = reads_bitmap & full;
  pthread_rwlock_unlock(&reads_lock);
  return result == full ? true : false;
}
#endif /* HAVE_OPA */

#endif /* _ActiveTypeQueueEntry_INCLUDE_ */
