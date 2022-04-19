# Flight Club

This is a client-side implementation of the Flight Club app, the original version is here: https://github.com/drc56/flight_club

The site is built using [Svelte](https://svelte.dev) and [SvelteKit](https://kit.svelte.dev)

[Firebase](https://firebase.google.com) provides auth, hosting, database, storage, and cloud functions. 

# Setup

1. Requires [Node.js](https://nodejs.dev/download/)
2. `npm install` to install required dependencies
3. `npm run dev` to launch the site locally

Ready for local development from here. Saving files will cause a hot-reload, though a full browser refresh or re-starting step 3 sometimes fixes insidious bugs. 

# Build and deploy
- `npm run build` to compile the Svelte files to plain javascript
- `npm run preview` to quickly see the built site
- `npm run start` to serve the site locally as it will be deployed using firebase emulators
- `npm run test` run tests
- `npm run deploy-site` to deploy changes to the static site. This requires user credentials with the correct permissions
- `npm run deploy-functions` to deploy changes to the firebase functions. Requires credentials

# Implementation details
Firebase hosting only serves static content, so the SvelteKit server-side (SSR) features are disabled by using the `adapter-static` in [SPA mode](https://github.com/sveltejs/kit/tree/master/packages/adapter-static#spa-mode). 

The `firebaseConfig` object in [firebase.ts](/src/lib/firebase.ts) is served to every user and considered public, data protection is maintained through Firebase Security Rules.

Most of the site is unavailable without logging in - see the `if` block in the [template](src/routes/__layout.svelte) file. This is not true data protection, which is again maintained through Firebase Security Rules.

Users authenticated via Google with firebase auth, which is made available site-wide by a [store](https://svelte.dev/docs#run-time-svelte-store) in [this](src/lib/stores.ts) file.

The Firestore data structure prioritizes read efficiency, so there is some redundancy. Secondary data updates are handled by cloud functions defined [here](functions/src/index.ts). These are called when primary data changes (ie. a beer is added). This secondary data includes:
- User aggregate data (ie. total wins)
- Session aggregate data (ie. average ABV)

# What's here
`/src` most of the site lives here\
`/src/routes` files and folders names here translate to URLs on the site\
`/src/lib` components and modules that aren't full pages\
`/src/lib/firebase.ts` all firestore interfaces are maintained here\
`/src/lib/models.ts` the data model is maintained here\
`/src/lib/stores.ts` data available site-wide are defined in [stores](https://svelte.dev/docs#run-time-svelte-store) here\
`/src/tests` jest test files\
`/static` static assets like fonts and images\
`/functions` cloud functions

`svelte.config.js` Svelte settings and options\
`firebase.json` Firebase settings and options\
`package.json` Node.js settings and options\
`firestore.rules` security rules to protect the database\
`storage.rules` security rules to protect the file storage (mostly pictures)\
`firestore.indexes.json` unlike SQL, compound queries are only possible if there is an index\
`jest.config.mjs` Jest settings and options

# Data Model
The data is maintained in firestore which is a document/collection system. There are three main collections:
- **Users**
- **Clubs**
- **Sessions**
- **Beers** 