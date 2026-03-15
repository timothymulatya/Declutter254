import { useState, useEffect } from "react"

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("")
  const [debouncedQuery, setDebouncedQuery] = useState("")

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query)
    }, 500)
    return () => clearTimeout(timer)
  }, [query])

  useEffect(() => {
    onSearch(debouncedQuery)
  }, [debouncedQuery, onSearch])

  return (
    <div style={{ width: "100%" }}>
      <input
        type="text"
        placeholder="Search for items..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{
          width: "100%",
          padding: "12px 16px",
          borderRadius: "12px",
          border: "2px solid #eee",
          background: "white",
          fontSize: "1rem",
          marginBottom: "0" // Overriding global margin for better stacking
        }}
      />
    </div>
  )
}

export default SearchBar