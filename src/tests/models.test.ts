import * as m from '../lib/models';

const requiredProperties = [
    'id',
    'name'
]

describe('userDefaults', () => {
    test.each(requiredProperties)(`should have property: $key`, (key) => {
            expect(m.userDefaults).toHaveProperty(key)
        }
    )
})