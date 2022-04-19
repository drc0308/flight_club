import { render } from '@testing-library/svelte';
import Footer from '$lib/Footer.svelte';


describe('Footer', () => {
    it('renders', () => {
        const result = render(Footer);
        expect(() => result.getByText(`MAMA'S`)).not.toThrow();
        expect(() => result.getByText(`THIRSTY`)).not.toThrow();
    })
})
