import { render } from '@testing-library/svelte';
import SessionInfo from '$lib/SessionInfo.svelte';

import type { Session } from '$lib/models';

const testInputs = [
    {
        club: undefined,
        number: undefined,
        date: undefined,
        location: undefined
    },
    {
    }
]

describe('SessionInfo', () => {
    test.each(testInputs)('renders with input data', (data: Session) => {
        const result = render(SessionInfo, { props: { session: data } });
        expect(() => result).not.toThrow()
    })
})