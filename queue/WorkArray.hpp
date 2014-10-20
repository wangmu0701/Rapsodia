//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#ifndef _WorkArray_INCLUDE_
#define _WorkArray_INCLUDE_

#ifndef RA_WORKARRAY_LENGTH
#define RA_WORKARRAY_LENGTH 1024
#endif

#ifdef RA_DEBUG
#include <iostream>
#endif 

#include <cassert>
#include <pthread.h>
#include <limits.h>
#include <stdlib.h>

#include "defines.hpp"
#include "RAtypes.hpp"

/**
 * Class for the work array to manage the memory used by the queue
 * The datastructure and much of the code taken from ADOL-C
 */
template <typename STRUCT, typename SLICE>
class WorkArray 
{
  public:
    static WorkArray* workArrayS;
    static WorkArray* workArrayD;

    void lock();
    void unlock();
    locint nextLocation();
    STRUCT& getLocation(const locint index); 
    SLICE& getLocation(const locint index, const int slice); 
    void freeLocation(const locint index);
    void dumpStats();

  private:

    WorkArray();
    ~WorkArray();

    locint locMinUnused;
    locint numMaxAlive;
    locint storeSize;
    locint numToFree;
    locint minLocToFree;
    locint maxLoc;

    STRUCT * store;

    /* lock for access to the store pointer */
    pthread_rwlock_t store_lock;
};

/* Template public methods */

/* Retrieve a pointer to the slice structure at the given index */
template <typename STRUCT, typename SLICE>
inline STRUCT& WorkArray<STRUCT, SLICE>::getLocation(const locint index)
{
  return store[index];
}

/* Retrieve a pointer to the given slice of the structure at the given 
 * index */
template <typename STRUCT, typename SLICE>
inline SLICE& WorkArray<STRUCT, SLICE>::getLocation(const locint index, 
                                                    const int slice)
{
  return store[index].s[slice];
}

template <typename STRUCT, typename SLICE>
inline void WorkArray<STRUCT, SLICE>::lock(void)
{
//  pthread_rwlock_rdlock(&store_lock);
}

template <typename STRUCT, typename SLICE>
inline void WorkArray<STRUCT, SLICE>::unlock(void)
{
//  pthread_rwlock_unlock(&store_lock);
}

template <typename STRUCT, typename SLICE>
inline void WorkArray<STRUCT, SLICE>::freeLocation(const locint index)
{
  ++numToFree;
  if (index < minLocToFree)
    minLocToFree = index;
}

template <typename STRUCT, typename SLICE>
locint WorkArray<STRUCT, SLICE>::nextLocation()
{
  /* update locations */
  if (numToFree && minLocToFree + numToFree == locMinUnused) {
    locMinUnused = minLocToFree;
    numToFree = 0;
    minLocToFree = maxLoc;
  }
  /* get the next available location and expand store if necessary */
  if (locMinUnused == numMaxAlive)
    ++numMaxAlive;
  if (numMaxAlive > storeSize) {
    storeSize *= 2;
    if (store == NULL) {
//      pthread_rwlock_wrlock(&store_lock);
      storeSize=RA_WORKARRAY_LENGTH;
      store = (STRUCT *) malloc(sizeof(STRUCT) * storeSize);
#ifdef RA_DEBUG
      std::cout << "RA_DEBUG: " << __FILE__ << ":" << __LINE__ << "allocate: store=" << store << " (storeSize=" << storeSize <<")" << std::endl; 
#endif
//      pthread_rwlock_unlock(&store_lock);
      minLocToFree = maxLoc;
    } else {
//      pthread_rwlock_wrlock(&store_lock);
      STRUCT * oldStore = store;
      store = (STRUCT *) realloc((void *) store, sizeof(STRUCT) * storeSize);
#ifdef RA_DEBUG
      std::cout << "RA_DEBUG: " << __FILE__ << ":" << __LINE__ << "reallocate: store=" << store << " (storeSize=" << storeSize <<") oldStore=" << oldStore << std::endl; 
#endif
      assert(store == oldStore);
//      pthread_rwlock_unlock(&store_lock);
    }
  }
  return locMinUnused++;
}

template <typename STRUCT, typename SLICE>
WorkArray<STRUCT, SLICE>::WorkArray()
{
  locMinUnused = 0;
  numMaxAlive = 0;
  numToFree = 0;
  minLocToFree = 0;
  maxLoc = UINT_MAX;
  storeSize = 0;
  store = NULL;

  pthread_rwlock_init(&store_lock, NULL);
}

template <typename STRUCT, typename SLICE>
WorkArray<STRUCT, SLICE>::~WorkArray() 
{
  pthread_rwlock_destroy(&store_lock);
  if (store != NULL)
    free(store);
}

template <typename STRUCT, typename SLICE>
void WorkArray<STRUCT, SLICE>::dumpStats() {
  std::cout << "RA_DEBUG: " << __FILE__ << ":" << __LINE__ << " final storeSize=" << storeSize << " numMaxAlive=" << numMaxAlive << std::endl;
}

#endif /* _WorkArray_INCLUDE_ */
