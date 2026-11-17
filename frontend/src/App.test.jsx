import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import App from './App'

describe('App', () => {
  it('increments the counter', () => {
    render(<App />)

    const counter = screen.getByRole('button', { name: /count is 0/i })
    fireEvent.click(counter)

    expect(counter).toHaveTextContent('Count is 1')
  })
})
