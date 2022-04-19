import functions = require("firebase-functions");
import admin = require("firebase-admin");

admin.initializeApp();
const db = admin.firestore();

export const onBeerUpdate = functions.firestore.document("beers/{beerId}").onWrite(async (change) => {
    const club = change.after.exists ? change.after.get("club") : change.before.get("club");
    const session = change.after.exists ? change.after.get("session") : change.before.get("session");
    const user = change.after.exists ? change.after.get("user") : change.before.get("user");
    functions.logger.log("Recalculating session", session, "and user", user)
    await updateSession(club, session);
    return updateUser(user, [club]);
});

export const onUserUpdate = functions.firestore.document("users/{userId}").onWrite(async (change, context) => {
    if (change.after.exists && change.after.get("name")) {
        const user = change.after.get("name");
        const clubs = change.after.get("clubs");
        functions.logger.log("Recalculating user", user, context.params.userId);
        return updateUser(user, clubs);
    } else {
        return null;
    }
});

export const updateAll = functions.firestore.document("testing/{id}").onWrite(async () => {
    const sessionsRefs = await db.collection("sessions").listDocuments();
    for (const sessionRef of sessionsRefs) {
        const session = await sessionRef.get();
        await updateSession(session.get("club"), session.get("number"))
    }
    const usersRefs = await db.collection("users").listDocuments();
    for (const userRef of usersRefs) {
        const user = await userRef.get();
        if (user.get("name")) {
            await updateUser(user.get("name"), user.get("clubs"));
        }
    }
});

async function updateSession(club: string, session: number) {
    const beersQuery = await db.collection("beers").where("club", "==", club).where("session", "==", session).get();
    const beers = beersQuery.docs.map(beer => beer.data());
    const winningBeer = beers.find(beer => beer.win == true);
    const sessionData = {
        winner: winningBeer != undefined ? winningBeer.user : null,
        beer: winningBeer != undefined ? winningBeer.name : null,
        brewery: winningBeer != undefined ? winningBeer.brewery : null,
        avg_abv: beers.map(beer => beer.abv).reduce((curr, next) => curr + next, 0) / beers.length,
        count: beers.length
    };
    functions.logger.log("Updating session", session, sessionData);
    const sessionQuery = await db.collection("sessions").where("number", "==", session).get();
    return sessionQuery.docs[0].ref.set(sessionData, { merge: true });
}

interface MemberData {
    wins: number,
    avg_score: number,
    avg_abv: number,
    count: number,
    win_rate: number
}

async function updateUser(user: string, clubs: string[]) {
    const data: { [id: string]: MemberData; } = {};
    for (const club of clubs) {
        const beerQuery = await db.collection("beers").where("club", "==", club).where("user", "==", user).get();
        const beers = beerQuery.docs.map(beer => beer.data());
        data[club] = {
            wins: beers.filter(beer => beer.win == true).length,
            avg_score: beers.map(beer => beer.score).reduce((curr, next) => curr + next, 0) / beers.length,
            avg_abv: beers.map(beer => beer.abv).reduce((curr, next) => curr + next, 0) / beers.length,
            count: beers.length,
            win_rate: beers.filter(beer => beer.win == true).length / beers.length
        };
    }
    functions.logger.log("Updating user", user, data);
    const userData = { data: data };
    const memberQuery = await db.collection("users").where("name", "==", user).get();
    if (memberQuery.empty) { return null; }
    return memberQuery.docs[0].ref.set(userData, { merge: true });
}
