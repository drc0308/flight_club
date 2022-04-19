import type { Beer, Session, Member, Club } from '$lib/models';
import type { Unsubscribe } from '@firebase/util';
import { userDefaults } from '$lib/models';
import { initializeApp } from '@firebase/app';
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut } from '@firebase/auth';
import {
  enableIndexedDbPersistence,
  getFirestore,
  collection,
  doc,
  setDoc,
  query,
  where,
  getDoc,
  getDocs,
  deleteDoc,
  updateDoc,
  arrayUnion,
  arrayRemove,
  onSnapshot,
  documentId
} from '@firebase/firestore';
import { getStorage, ref, uploadBytes, getDownloadURL, list, deleteObject } from '@firebase/storage';

export let login: () => void;
export let logout: () => void;
export let watchAuthState: (setUser: (member: Member) => void) => Unsubscribe;

export let newSessionId: () => string;
export let getSessionId: (club: string, id: number) => Promise<string>;
export let updateSession: (session: Session) => Promise<void>;
export let deleteSession: (id: string) => Promise<void>;
export let watchSession: (id: string, onChange: (session: any) => void) => Unsubscribe;
export let watchSessions: (club: string, onChange: (sessions: any[]) => void) => Unsubscribe;
export let findSession: (club: string, number: number) => Promise<string | false>;

export let newBeerId: () => string;
export let updateBeer: (beer: Beer) => Promise<void>;
export let deleteBeer: (id: string) => Promise<void>;
export let watchBeers: (club: string, onChange: (beers: any[]) => void) => Unsubscribe;

export let getMemberId: (member: string) => Promise<string>;
export let updateMember: (member: Member) => Promise<void>;
let updateMemberDefaults: (memberId: string) => Promise<void>;
export let watchMember: (id: string, onChange: (member: any) => void) => Unsubscribe;
export let watchMembers: (club: Club, onChange: (members: any[]) => void) => Unsubscribe;

export let joinClub: (user: string, club: Club) => Promise<void>;
export let leaveClub: (user: string, club: Club) => Promise<void>;
export let updateClub: (club: Club) => Promise<void>;
export let watchClub: (id: string, onChange: (club: any) => void) => Unsubscribe;
export let watchClubs: (ids: string[], onChange: (clubs: any[]) => void) => Unsubscribe;
export let watchAllClubs: (onChange: (clubs: any[]) => void) => Unsubscribe;

export let uploadPhotos: (sessionId: string, files: FileList) => Promise<void>;
export let deletePhotos: (sessionId: string) => Promise<void>;

const firebaseConfig = {
  apiKey: 'AIzaSyAOzCtQq2cKSTi7RXgy1tuSJgPxY2jKs8Q',
  authDomain: 'dgang-flight-club.firebaseapp.com',
  projectId: 'dgang-flight-club',
  storageBucket: 'dgang-flight-club.appspot.com',
  messagingSenderId: '34180351223',
  appId: '1:34180351223:web:df3852031092f57f333ff2'
};



// Firebase initialization
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);
const storage = getStorage(app);
const provider = new GoogleAuthProvider();

// Database setup - enable local caching

enableIndexedDbPersistence(db)
  .catch((err) => {
    if (err.code == 'failed-precondition') {
      console.log(err.code);
    } else if (err.code == 'unimplemented') {
      console.log(err.code);
    }
  });

// Auth functions

login = () => { signInWithPopup(auth, provider); }
logout = () => { signOut(auth); }

// Convert the Google user format to our database format
const userFromGoogleUser = (googleUser: any): any => {
  return {
    id: googleUser.uid,
    full_name: googleUser.displayName,
    email: googleUser.email,
    photoURL: googleUser.photoURL
  };
}

watchAuthState = (setUser) => {
  return auth.onAuthStateChanged(async (googleUser) => {
    if (googleUser) {
      // Add or update the user to our database on login
      const user = userFromGoogleUser(googleUser);
      setUser(user); // Populates the ID in the user store, allowing it to subscribe to the firestore user
      await updateMember(user); // Updates the firestore user with any changes from the google user, creating a new user if necessary
      updateMemberDefaults(user.id); // Populate any defaults for new users or model updates to firebase
    } else {
      setUser(null);
    }
  });
}

// Session functions

newSessionId = () => {
  const sessionRef = doc(collection(db, 'sessions'));
  return sessionRef.id;
}

getSessionId = async (club, number) => {
  const sessionQuery = query(collection(db, 'sessions'), where('number', '==', number), where('club', '==', club));
  const queryResults = await getDocs(sessionQuery);
  if (queryResults.empty) {
    throw new Error(`Session ${number} does not exist!`);
  }
  return queryResults.docs[0].ref.id;
}

updateSession = async (session) => {
  const sessionRef = doc(db, 'sessions', session.id);
  await setDoc(sessionRef, session, { merge: true });
}

deleteSession = async (id) => {
  const sessionRef = doc(db, 'sessions', id);
  await deletePhotos(id);
  await deleteDoc(sessionRef);
}

watchSession = (id, onChange) => {
  return onSnapshot(doc(db, 'sessions', id), (snapshot) => {
    const session = snapshot.data();
    session.id = snapshot.id;
    onChange(session);
  });
}

watchSessions = (club, onChange) => {
  const sessionsQuery = query(collection(db, 'sessions'), where('club', '==', club));
  return onSnapshot(sessionsQuery, (snapshot) => {
    const sessions = snapshot.docs.map((doc) => {
      return { ...doc.data(), id: doc.id };
    });
    onChange(sessions);
  });
}

findSession = async (club, number) => {
  const sessionQuery = query(collection(db, 'sessions'),
    where('club', '==', club),
    where('number', '==', number));
  const result = await getDocs(sessionQuery);
  if (!result.empty) {
    return result.docs[0].id;
  } else {
    return false;
  }
}

// Beer functions

newBeerId = () => {
  const newBeerRef = doc(collection(db, 'beers'));
  return newBeerRef.id;
}

updateBeer = async (beer) => {
  const beerRef = doc(db, 'beers', beer.id);
  await setDoc(beerRef, beer, { merge: true });
}

deleteBeer = async (id) => {
  const beerRef = doc(db, 'beers', id);
  deleteDoc(beerRef);
}

watchBeers = (club, onChange) => {
  const beersQuery = query(collection(db, 'beers'), where('club', '==', club));
  return onSnapshot(beersQuery, (snapshot) => {
    const beers = snapshot.docs.map((doc) => {
      return { ...doc.data(), id: doc.id };
    });
    onChange(beers);
  });
}

// Member functions

getMemberId = async (name) => {
  const memberQuery = query(collection(db, 'users'), where('name', '==', name));
  const queryResults = await getDocs(memberQuery);
  if (queryResults.empty) {
    throw new Error(`Member ${name} does not exist!`);
  }
  return queryResults.docs[0].ref.id;
}

updateMember = async (member) => {
  const memberRef = doc(db, 'users', member.id);
  await setDoc(memberRef, member, { merge: true });
}

updateMemberDefaults = async (memberId) => {
  // Update the firestore document with all defaults without overwiting existing data
  // Would be nice if there was a firebase function to do this directly 
  const memberRef = doc(db, 'users', memberId);
  const memberDoc = await getDoc(memberRef);
  const memberData = memberDoc.data();
  const update = { ...userDefaults, ...memberData };
  if (!update.name) {
    // If empty, set the name to the Google user's first name
    update.name = memberData.full_name.split(' ')[0];
  }
  await setDoc(memberRef, update, { merge: true });
}

watchMember = (id, onChange) => {
  return onSnapshot(doc(db, 'users', id), (snapshot) => {
    const member = snapshot.data();
    member.id = snapshot.id;
    onChange(member);
  });
}

watchMembers = (club, onChange) => {
  const membersQuery = query(collection(db, 'users'), where('clubs', 'array-contains', club.id));
  return onSnapshot(membersQuery, (snapshot) => {
    const members = snapshot.docs.map((doc) => {
      return { ...doc.data(), id: doc.id };
    });
    onChange(members);
  });
}

// Club functions

joinClub = async (user, club) => {
  const userRef = doc(db, 'users', user);
  await updateDoc(userRef, { clubs: arrayUnion(club.id) });
}

leaveClub = async (user, club) => {
  const userRef = doc(db, 'users', user);
  await updateDoc(userRef, { clubs: arrayRemove(club.id) });
}

updateClub = async (club) => {
  const clubRef = doc(db, 'clubs', club.id);
  await setDoc(clubRef, club, { merge: true });
}

watchClub = (id, onChange) => {
  return onSnapshot(doc(db, 'clubs', id), (snapshot) => {
    const club = snapshot.data();
    club.id = snapshot.id;
    onChange(club);
  })
}

watchClubs = (ids, onChange) => {
  const clubsQuery = query(collection(db, 'clubs'), where(documentId(), 'in', ids));
  return onSnapshot(clubsQuery, (snapshot) => {
    const clubs = snapshot.docs.map((doc) => {
      return { ...doc.data(), id: doc.id };
    });
    onChange(clubs);
  })
}

watchAllClubs = (onChange) => {
  return onSnapshot(collection(db, 'clubs'), (snapshot) => {
    const clubs = snapshot.docs.map((doc) => {
      return { ...doc.data(), id: doc.id };
    });
    onChange(clubs);
  })

}

// Photo functions

uploadPhotos = async (sessionId, files) => {
  const sessionRef = doc(db, 'sessions', sessionId);
  for (const file of files) {
    const storageRef = ref(storage, sessionId + '/' + file.name);
    await uploadBytes(storageRef, file);
    const storageURL = await getDownloadURL(storageRef);
    updateDoc(sessionRef, { photos: arrayUnion(storageURL) });
  }
}

deletePhotos = async (sessionId) => {
  const storageRef = ref(storage, sessionId);
  const allPhotos = await list(storageRef);
  for (const photoRef of allPhotos.items) {
    await deleteObject(photoRef);
  }
  const sessionRef = doc(db, 'sessions', sessionId);
  await setDoc(sessionRef, { photos: [] }, { merge: true });
}

