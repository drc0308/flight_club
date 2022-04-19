import type { Member, Club } from "$lib/models";
import type { Unsubscribe } from "@firebase/util";
import type { Writable, Readable } from "svelte/store";
import { watchMember, watchClubs } from "$lib/firebase";
import { userDefaults } from "$lib/models";

function userStore(): Writable<Member> {
    let value: Member = null;
    let subs = [];
    let subscribedToUser = false;
    let unsubscribe: Unsubscribe;

    const subscribe = (handler: (value: Member) => void) => {
        subs = [...subs, handler];
        handler(value);
        return () => {
            subs = subs.filter(sub => sub != handler);
            if (!subs) { unsubscribe(); };
        };
    }

    const set = (userUpdate: Member) => {
        if (value == userUpdate) return;
        if (!userUpdate) {
            // Logout
            value = null;
        } else {
            value = { ...userDefaults, ...userUpdate };
        }

        if (!subscribedToUser && value.id) {
            subscribedToUser = true;
            // On first login, subscribe to changes on the firebase user document
            unsubscribe = watchMember(value.id, (update) => {
                set(update)
            });
        } else if (!value && subscribedToUser) {
            // Unsubscribe on logout
            unsubscribe();
            subscribedToUser = false;
        }

        subs.forEach(sub => sub(value))
    }

    const update = (updateFunction: (value: Member) => Member) => set(updateFunction(value));

    return {
        subscribe,
        set,
        update,
    }
}

function clubsStore(user: Writable<Member>): Readable<Club[]> {
    let value: Club[] = [];
    let subs = [];
    let clubList: string[] = [];
    let subscribedToUser: boolean = false;

    let unsubscribeClubs: Unsubscribe = () => undefined;
    let unsubscribeUser = () => undefined;

    const subscribe = (handler: (value: Club[]) => void) => {
        subs = [...subs, handler];
        if (!subscribedToUser) {
            unsubscribeUser = user.subscribe((userUpdate) => {
                if (userUpdate && userUpdate.clubs.length > 0 && userUpdate.clubs != clubList) {
                    // When a user is logged in with a valid club list, get or update that list 
                    unsubscribeClubs();
                    unsubscribeClubs = watchClubs(userUpdate.clubs, (update) => {
                        value = update;
                        subs.forEach(sub => sub(value));
                    })
                }
            })

        }
        handler(value);
        return () => {
            subs = subs.filter(sub => sub != handler);
            if (!subs) {
                unsubscribeClubs();
                unsubscribeUser();
                subscribedToUser = false;
                clubList = [];
            }
        }
    }

    return {
        subscribe
    }
}

function activeClubStore(clubs: Readable<Club[]>) {
    console.log('here')
    let id: string = null;
    let value: Club;
    let subs = [];
    let clubList: Club[] = [];
    let subscribedToClub: boolean = false;

    let unsubscribe = () => undefined;

    const subscribe = (handler: (value: Club) => void) => {
        subs = [...subs, handler];
        if (!subscribedToClub) {
            unsubscribe = clubs.subscribe((clubsUpdate) => {
                if (clubsUpdate.length > 0) {
                    clubList = clubsUpdate;
                    if (!id) { 
                        id = clubList[0].id;
                    }
                    value = clubList.find(club => club.id == id);
                    subs.forEach(sub => sub(value));
                }
            })
        }
        handler(value);
        return () => {
            subs = subs.filter(sub => sub != handler);
            if (!subs) { 
                unsubscribe();
                subscribedToClub = false;
            };
        }
    }

    const set = (update: string) => {
        if (!value || update != id) {
            id = update;
            if (clubList.length > 0) {
                value = clubList.find(club => club.id == id);
                subs.forEach(sub => sub(value));
            }
        }
    }

    const update = (updateFunction: (value: Club) => string) => set(updateFunction(value));

    return {
        subscribe,
        set,
        update,
        value: () => value,
    }
}

export const user = userStore();
export const clubs = clubsStore(user);
export const activeClub = activeClubStore(clubs);
